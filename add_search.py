#!/usr/bin/env python3
"""
Add search overlay HTML and ds-shared.js script include to pages that are missing them.
Also ensure pages that have inline search JS (ds-01 through ds-13) use ds-shared.js instead.
"""
import os, re

BASE = "/Users/lucasye/Documents/Norbielink Design system"
files = sorted(f for f in os.listdir(BASE) if f.startswith('ds-') and f.endswith('.html'))

# The minimal search overlay HTML block
SEARCH_OVERLAY = '''<!-- SEARCH OVERLAY -->
<div id="search-overlay" onclick="if(event.target===this)closeSearch()">
  <div class="search-modal">
    <div class="search-input-wrap">
      <span class="material-icons-round">search</span>
      <input id="search-input" type="text" placeholder="Search components, foundations…"
        oninput="renderResults(this.value)" onkeydown="searchKeydown(event)">
      <span class="material-icons-round search-close" onclick="closeSearch()">close</span>
    </div>
    <div class="search-results" id="search-results"></div>
    <div class="search-hint">
      <span>Press</span><kbd>↑</kbd><kbd>↓</kbd><span>to navigate</span>
      <kbd>↵</kbd><span>to open</span><kbd>Esc</kbd><span>to close</span>
    </div>
  </div>
</div>
<!-- END SEARCH -->
'''

modified = 0
for fn in files:
    if fn == 'ds-00-home.html':
        continue

    fpath = os.path.join(BASE, fn)
    with open(fpath, encoding='utf-8') as f:
        html = f.read()

    changed = False

    # 1. Add search overlay HTML after </header> if missing
    if 'id="search-overlay"' not in html:
        html = html.replace('</header>\n', '</header>\n' + SEARCH_OVERLAY, 1)
        changed = True

    # 2. Ensure ds-shared.js is included before </body>
    if 'ds-shared.js' not in html:
        html = html.replace('</body>', '<script src="ds-shared.js"></script>\n</body>', 1)
        changed = True

    if changed:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  ✓  {fn}')
        modified += 1
    else:
        print(f'  –  {fn}')

print(f'\nDone. {modified} files updated.')
