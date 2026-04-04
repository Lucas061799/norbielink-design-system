#!/usr/bin/env python3
"""
1. Remove all "Dark mode" ds-section blocks from every page
2. Remove "Dark mode" TOC items
3. Remove dark-bg-pane preview divs
4. Remove in-page <style> dark mode overrides (the ones duplicating shared CSS)
"""
import os, re

BASE = "/Users/lucasye/Documents/Norbielink Design system"
files = sorted(f for f in os.listdir(BASE) if f.startswith('ds-') and f.endswith('.html'))

def remove_dark_sections(html):
    # ── A. Remove dark mode TOC item ──────────────────────────────────────
    html = re.sub(
        r'\s*<a[^>]+href=["\']#dark-?mode["\'][^>]*>.*?</a>',
        '', html, flags=re.DOTALL
    )

    # ── B. Remove ds-section with id="dark-mode" ──────────────────────────
    # Also removes any divider immediately before it
    html = re.sub(
        r'(\s*<div class="ds-divider"[^/]*/?>)?\s*(?:<!--[^>]*[Dd]ark[^>]*-->)?\s*'
        r'<div[^>]+id=["\']dark-?mode["\'][^>]*>.*?</div>(?=\s*(?:<div|</div>|</main>|\s*$))',
        '',
        html, flags=re.DOTALL
    )

    # ── C. Remove any remaining dark-bg-pane divs ─────────────────────────
    html = re.sub(
        r'\s*<div[^>]+dark-bg-pane[^>]*>.*?</div>',
        '', html, flags=re.DOTALL
    )

    # ── D. Remove dark-bg example containers ──────────────────────────────
    html = re.sub(
        r'\s*<div[^>]+class="[^"]*ds-example[^"]*dark-bg[^"]*"[^>]*>.*?</div>',
        '', html, flags=re.DOTALL
    )

    # ── E. Remove in-page <style> dark mode overrides that duplicate shared CSS ──
    # Pattern: body.dark-mode lines inside a <style> block in the page <head>
    def strip_darkmode_from_style(m):
        style_content = m.group(1)
        # Remove all body.dark-mode {...} rules
        cleaned = re.sub(
            r'\n?body\.dark-mode[^{]*\{[^}]*\}',
            '', style_content
        )
        # Remove all lines starting with body.dark-mode
        cleaned = re.sub(r'\nbody\.dark-mode[^\n]*', '', cleaned)
        return f'<style>{cleaned}</style>'

    html = re.sub(
        r'<style>(.*?)</style>',
        strip_darkmode_from_style,
        html, flags=re.DOTALL
    )

    # ── F. Remove standalone dark mode h2 headings ────────────────────────
    html = re.sub(
        r'\s*<h2[^>]*>[Dd]ark\s*[Mm]ode</h2>',
        '', html
    )

    return html

modified = 0
for fn in files:
    if fn == 'ds-00-home.html':
        continue
    fpath = os.path.join(BASE, fn)
    with open(fpath, encoding='utf-8') as f:
        original = f.read()

    cleaned = remove_dark_sections(original)

    if cleaned != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        print(f'  ✓  {fn}')
        modified += 1
    else:
        print(f'  –  {fn}')

print(f'\nDone. {modified} files modified.')
