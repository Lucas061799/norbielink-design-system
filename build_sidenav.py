# -*- coding: utf-8 -*-
"""Rebuild the left sub-nav on every page from one list.

It had drifted: Cards, App Bars, Chart and Hover Card were missing, and there
was no Resources group at all, so the four brand pages had nothing on the left.
"""
import re, glob, os
ROOT = "/Users/lucasye/Documents/Norbielink Design system"
os.chdir(ROOT)

# Components come from the NAV block in ds-shared.js so there is one source.
js = open("ds-shared.js").read()
blk = js[js.index("label: 'Components'"):js.index("label: 'Resources'")]
COMPONENTS = [(l, h) for h, l in
              ((m.group(2), m.group(1)) for m in
               re.finditer(r"\{ label: '([^']+)',\s*href: '([^']+)' \}", blk))]

GROUPS = [
    ("Getting Started", "school", [
        ("Introduction", "ds-00-home.html"),
        ("Colors",       "ds-01-color.html"),
        ("Typography",   "ds-02-typography.html"),
        ("Elevation",    "ds-03-elevation.html"),
        ("Shape",        "ds-04-shape.html"),
        ("Spacing",      "ds-05-spacing.html"),
    ]),
    ("Brand assets", "palette", [
        ("Norbielink Logo",  "ds-brand-norbielink-logo.html"),
        ("BTIS Logo",        "ds-brand-logo.html"),
        ("Brand Characters", "ds-brand-characters.html"),
        ("Visual Elements",  "ds-brand-visual-elements.html"),
    ]),
    ("Components", "widgets", COMPONENTS),
]


def nav_for(current):
    """Collapsible sections, the same shape as the app's own 'Tools & Resources'
    rail: an icon, the label, a chevron, and the children indented under a
    guide line. The section holding the current page starts open."""
    out = ['<!-- SUB-NAV -->', '<nav class="ds-sidenav">']
    for title, icon, items in GROUPS:
        here = any(h == current for _, h in items)
        out.append('  <div class="ds-sidenav-group%s">' % (" open" if here else ""))
        out.append('    <button class="ds-sidenav-sec" type="button" '
                   'onclick="toggleSidenavSection(this)" aria-expanded="%s">'
                   % ("true" if here else "false"))
        out.append('      <span class="material-icons-round ds-sidenav-sec-icon">%s</span>' % icon)
        out.append('      <span class="ds-sidenav-sec-label">%s</span>' % title)
        out.append('      <span class="material-icons-round ds-sidenav-chev">expand_more</span>')
        out.append('    </button>')
        out.append('    <div class="ds-sidenav-sub">')
        for label, href in items:
            a = " active" if href == current else ""
            out.append('      <a class="ds-sidenav-item%s" href="%s">%s</a>' % (a, href, label))
        out.append('    </div>')
        out.append('  </div>')
    out.append('</nav>')
    return "\n".join(out) + "\n"


print("%d components · %d groups" % (len(COMPONENTS), len(GROUPS)))
replaced = inserted = 0
for f in sorted(glob.glob("ds-*.html")):
    s = open(f, encoding="utf-8").read()
    nav = nav_for(f)
    m = re.search(r'(?:<!-- SUB-NAV -->\s*)?<nav class="ds-sidenav">.*?</nav>\s*', s, re.S)
    if m:
        s = s[:m.start()] + nav + s[m.end():]
        replaced += 1
    else:
        anchor = '<aside class="ds-toc">'
        if anchor not in s:
            continue
        i = s.index(anchor)
        s = s[:i] + nav + "\n" + s[i:]
        inserted += 1
    open(f, "w", encoding="utf-8").write(s)
print("replaced %d · inserted %d" % (replaced, inserted))
