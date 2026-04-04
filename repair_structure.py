#!/usr/bin/env python3
"""
Fix the structural corruption introduced by remove_darkmode_sections.py
and the earlier (incorrect) fix_div_balance.py run.

Strategy per file:
  1. Find <div class="ds-content"> and note depth D at that point.
  2. Scan from ds-content; detect any </div> that would prematurely
     close ds-content (depth == content_depth when a close is seen,
     but more ds-section/ds-page-nav content follows).  Skip that orphan
     and skip subsequent garbage until the next clean ds-section/ds-divider.
  3. After rebuilding, insert before </main>:
       (cur_depth - D) × </div>        ← closes ds-content + anything inside
  4. After </main>, insert:
       D × </div>                       ← closes wrappers (e.g. ds-shell)
"""
import os, re

BASE = "/Users/lucasye/Documents/Norbielink Design system"
files = sorted(f for f in os.listdir(BASE) if f.startswith('ds-') and f.endswith('.html'))

TOKEN_RE = re.compile(r'(<div(?:\s[^>]*)?>|</div\s*>)', re.IGNORECASE)

def count_balance(html):
    o = len(re.findall(r'<div(?:\s[^>]*)?>',  html, re.IGNORECASE))
    c = len(re.findall(r'</div\s*>',           html, re.IGNORECASE))
    return o - c

def get_depth_at(html, pos):
    """Global div depth just before character position pos."""
    depth = 0
    for m in TOKEN_RE.finditer(html[:pos]):
        tok = m.group(0)
        depth += 1 if re.match(r'<div', tok, re.IGNORECASE) else -1
    return depth

def repair_file(html):
    cm = re.search(r'<div[^>]+class="[^"]*ds-content[^"]*"[^>]*>', html)
    if not cm:
        return html, 'no ds-content found'

    content_start  = cm.start()
    D              = get_depth_at(html, content_start)   # depth before ds-content (e.g. 1)
    content_depth  = D + 1                               # ds-content lives here (e.g. 2)

    prefix = html[:content_start]
    body   = html[content_start:]

    result      = []
    depth       = D          # current global depth (starts at D, becomes D+1 after ds-content open)
    in_garbage  = False
    orphans_rm  = 0
    garbage_chars = 0
    pos         = 0

    for m in TOKEN_RE.finditer(body):
        ms, me, tok = m.start(), m.end(), m.group(0)
        segment  = body[pos:ms]
        is_open  = bool(re.match(r'<div', tok, re.IGNORECASE)) and not tok.endswith('/>')
        new_depth = depth + 1 if is_open else depth - 1

        # ── Detect premature ds-content close ──────────────────────────────
        if not in_garbage and not is_open and depth == content_depth:
            # This </div> would close ds-content.  Only legitimate if nothing
            # more follows (no ds-section or ds-page-nav after this point).
            rest = body[me:]
            has_more = bool(
                re.search(r'<div[^>]+class="[^"]*ds-section[^"]*"',  rest) or
                re.search(r'<div[^>]+class="[^"]*ds-page-nav[^"]*"', rest)
            )
            if has_more:
                in_garbage = True
                orphans_rm += 1
                pos = me
                continue   # skip orphan; depth stays at content_depth

        # ── While in garbage: skip until next clean restart token ──────────
        if in_garbage:
            # A clean restart is a ds-section/ds-divider open that would put
            # us back at content_depth (i.e. new_depth_from_reset == content_depth+1
            # so the open takes depth from content_depth to content_depth+1).
            is_clean = bool(re.match(
                r'<div[^>]+class="[^"]*(?:ds-section|ds-divider|ds-page-nav)[^"]*"',
                tok, re.IGNORECASE
            ))
            # To check "would take us to content_depth+1 from content_depth":
            # we don't care about garbage-tracked depth; just check that this is
            # a recognised clean open and we can restart.
            if is_clean:
                in_garbage = False
                # Reset depth to content_depth (where we should be) and open new section
                depth     = content_depth
                new_depth = depth + 1   # recompute with reset depth
                # fall through to normal emit below
            else:
                garbage_chars += len(segment) + len(tok)
                depth = new_depth
                pos   = me
                continue

        # ── Normal emit ────────────────────────────────────────────────────
        result.append(segment)
        result.append(tok)
        depth = new_depth
        pos   = me

    result.append(body[pos:])
    rebuilt = ''.join(result)

    # ── Add closing tags ───────────────────────────────────────────────────
    # Before </main>: close ds-content (and anything else still open inside)
    main_m = re.search(r'</main\s*>', rebuilt, re.IGNORECASE)
    added_before = 0
    added_after  = 0

    if main_m:
        ins = main_m.start()
        cur = get_depth_at(prefix + rebuilt, len(prefix) + ins)
        need_before = cur - D          # how many closes to reach D (pre-ds-content depth)
        if need_before > 0:
            rebuilt = rebuilt[:ins] + ('  </div>\n' * need_before) + rebuilt[ins:]
            added_before = need_before

        # After </main>: close outer wrappers (e.g. ds-shell) — D closes needed
        main_m2 = re.search(r'</main\s*>', rebuilt, re.IGNORECASE)   # re-find after edit
        ins2 = main_m2.end()
        if D > 0:
            rebuilt = rebuilt[:ins2] + ('\n</div>' * D) + rebuilt[ins2:]
            added_after = D
    else:
        # No </main> — add at very end
        cur = get_depth_at(prefix + rebuilt, len(prefix + rebuilt))
        if cur > 0:
            rebuilt = rebuilt + ('</div>\n' * cur)
            added_before = cur

    full = prefix + rebuilt
    bal  = count_balance(full)
    desc = (f'removed {orphans_rm} orphan(s) + ~{garbage_chars}ch garbage; '
            f'added {added_before} before </main> + {added_after} after; '
            f'final balance={bal:+d}')
    return full, desc


modified = 0
for fn in files:
    fpath = os.path.join(BASE, fn)
    with open(fpath, encoding='utf-8') as f:
        original = f.read()

    fixed, desc = repair_file(original)
    new_bal = count_balance(fixed)

    if fixed != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(fixed)
        status = '✓ ' if new_bal == 0 else '⚠ '
        print(f'  {status} {fn}  ({desc})')
        modified += 1
    else:
        bal = count_balance(original)
        print(f'  –  {fn}  (no change, balance={bal:+d})')

print(f'\nDone. {modified} files modified.')
