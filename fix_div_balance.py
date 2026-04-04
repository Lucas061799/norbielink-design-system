#!/usr/bin/env python3
"""
Fix extra </div> closing tags introduced by regex-based HTML manipulation.
Strategy: scan entire file tracking div depth; any </div> that would take
depth below 0 is orphaned — remove it.
"""
import os, re

BASE = "/Users/lucasye/Documents/Norbielink Design system"
files = sorted(f for f in os.listdir(BASE) if f.startswith('ds-') and f.endswith('.html'))

# Match open divs (non-self-closing) or close divs
TOKEN_RE = re.compile(r'(<div(?:\s[^>]*)?>|</div\s*>)', re.IGNORECASE)

def count_balance(html):
    opens  = len(re.findall(r'<div(?:\s[^>]*)?>',  html, re.IGNORECASE))
    closes = len(re.findall(r'</div\s*>',           html, re.IGNORECASE))
    return opens - closes   # 0 = balanced, negative = too many closes

def fix_balance(html):
    """Remove orphaned </div> tags (those that would take depth below 0)."""
    parts   = []
    depth   = 0
    removed = 0
    last    = 0

    for m in TOKEN_RE.finditer(html):
        tok = m.group(0)
        parts.append(html[last:m.start()])

        if re.match(r'<div(?:\s|>)', tok, re.IGNORECASE):   # opening tag
            depth += 1
            parts.append(tok)
        else:                                                 # </div>
            if depth > 0:
                depth -= 1
                parts.append(tok)
            else:
                removed += 1   # orphaned — skip it

        last = m.end()

    parts.append(html[last:])
    return ''.join(parts), removed


modified = 0
for fn in files:
    fpath = os.path.join(BASE, fn)
    with open(fpath, encoding='utf-8') as f:
        original = f.read()

    bal = count_balance(original)

    if bal >= 0:
        print(f'  OK  {fn}  (balance={bal:+d})')
        continue

    fixed, removed = fix_balance(original)
    new_bal = count_balance(fixed)

    if fixed != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(fixed)
        print(f'  ✓  {fn}  balance {bal:+d} → {new_bal:+d}  (removed {removed} orphan </div>)')
        modified += 1
    else:
        print(f'  ??  {fn}  balance={bal:+d} but nothing removed')

print(f'\nDone. {modified} files repaired.')
