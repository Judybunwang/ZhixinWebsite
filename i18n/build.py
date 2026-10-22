"""Generate the French, Spanish and Chinese versions of the site.

The English pages in the repo root are the source. Run from the repo root:

    python3 i18n/build.py

This (re)writes the language switcher in every English page, then writes
fr/, es/ and zh/ copies with the text from i18n/translations.py. After
editing an English page, add any new or changed text to translations.py
and run the script again. It warns about text it could not translate.
"""
import html
import pathlib
import re
import sys
from html.parser import HTMLParser

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from translations import T  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ["index.html", "career.html", "research.html", "cooking.html", "pets.html"]
LANGS = [("en", "English", "EN"), ("fr", "Français", "FR"), ("es", "Español", "ES"), ("zh", "中文", "中文")]
COL = {"fr": 0, "es": 1, "zh": 2}
HTML_LANG = {"en": "en", "fr": "fr", "es": "es", "zh": "zh-Hans"}
SWITCH_LABEL = {"en": "Language", "fr": "Langue", "es": "Idioma", "zh": "语言"}

# Text that is the same in every language and needs no warning.
KEEP = {"LinkedIn", "©", "·", "3", "4", "PCR", "HACCP", "Farther Farms", "Zhixin Wang ·",
        "English", "Français", "Español", "中文", "EN",
        # Paper titles stay in their published (English) form.
        "Cellulose-Binding Module-Mediated Immobilization of L-Arabinose Isomerase for Reusable D-Tagatose Production",
        "Consumers Respond Positively to the Sensory, Health, and Sustainability Benefits of the Rare Sugar Allulose in Yogurt Formulations",
        "Recombinant lactase with a cellulose binding domain permits facile immobilization onto cellulose with retained activity",
        "Concentrated sugar solutions protect lactase from thermal inactivation"}


def href(from_lang, to_lang, page):
    if from_lang == to_lang:
        return page
    if from_lang == "en":
        return f"{to_lang}/{page}"
    if to_lang == "en":
        return f"../{page}"
    return f"../{to_lang}/{page}"


def switcher(lang, page):
    current = next(l for l in LANGS if l[0] == lang)
    items = "\n".join(
        f'          <li><a href="{href(lang, code, page)}" hreflang="{HTML_LANG[code]}" lang="{HTML_LANG[code]}"'
        f'{" aria-current=\"true\"" if code == lang else ""}>{name}</a></li>'
        for code, name, _ in LANGS)
    return (f'<details class="lang-switch">\n'
            f'        <summary aria-label="{SWITCH_LABEL[lang]}"><span aria-hidden="true">🌐</span> {current[2]}</summary>\n'
            f'        <ul>\n{items}\n        </ul>\n'
            f'      </details>')


def alternates(lang, page):
    return "\n".join(
        f'  <link rel="alternate" hreflang="{HTML_LANG[code]}" href="{href(lang, code, page)}">'
        for code, _, _ in LANGS)


def with_chrome(src, lang, page):
    """Insert (or refresh) the switcher and hreflang links."""
    src = re.sub(r'\n  <link rel="alternate" hreflang=[^\n]*', "", src)
    src = src.replace('  <link rel="stylesheet"', alternates(lang, page) + '\n  <link rel="stylesheet"', 1)
    src = re.sub(r'\s*<details class="lang-switch">.*?</details>', "", src, flags=re.S)
    src = src.replace("\n    </nav>", "\n      " + switcher(lang, page) + "\n    </nav>", 1)
    return src


class Texts(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.found, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip and data.strip():
            self.found.append(data.strip())


def translate(src, lang):
    col = COL[lang]
    # Longest first so a short string never clobbers part of a longer one.
    for en in sorted(T, key=len, reverse=True):
        tr = T[en][col]
        esc_en, esc_tr = html.escape(en, quote=False), html.escape(tr, quote=False)
        src = re.sub(r"(>\s*)" + re.escape(esc_en) + r"(\s*<)", lambda m: m.group(1) + esc_tr + m.group(2), src)
        for attr in ("content", "aria-label", "alt"):
            src = src.replace(f'{attr}="{html.escape(en)}"', f'{attr}="{html.escape(tr)}"')
    src = src.replace('<html lang="en">', f'<html lang="{HTML_LANG[lang]}">', 1)
    for asset in ("styles.css", "bunny.svg", "apple-touch-icon.png"):
        src = src.replace(f'"{asset}"', f'"../{asset}"')
    src = src.replace('src="photos/', 'src="../photos/')
    return src


def main():
    missing = set()
    for page in PAGES:
        path = ROOT / page
        en = with_chrome(path.read_text(), "en", page)
        path.write_text(en)
        for lang in COL:
            out = translate(with_chrome(en, lang, page), lang)
            p = Texts()
            p.feed(out)
            english_left = {t for t in p.found if t in T and T[t][COL[lang]] != t}
            missing |= {t for t in Texts_of(en) if t not in T and t not in KEEP and not is_emoji(t) and not re.fullmatch(r"[\d –-]+", t)}
            if english_left:
                print(f"warning: {lang}/{page} still has English: {sorted(english_left)}")
            (ROOT / lang).mkdir(exist_ok=True)
            (ROOT / lang / page).write_text(out)
    for t in sorted(missing):
        print(f"no translation (kept as is): {t!r}")
    print("done")


def Texts_of(src):
    p = Texts()
    p.feed(src)
    return p.found


def is_emoji(t):
    return all(ord(c) > 0x2000 for c in t.replace(" ", ""))


if __name__ == "__main__":
    main()
