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

# Visual Elements is one page with five sections, so it expands in place.
VE = "ds-brand-visual-elements.html"
# Plain labels — the emoji belong on the page's own tabs, where the brand
# guide puts them, not in the rail.
VE_SECTIONS = [
    ("Tiles / Product icon", "tab-tiles"),
    ("Monstera Leaves", "tab-monstera"),
    ("Banana", "tab-banana"),
    ("Marketplace awning", "tab-awning"),
    ("Jungle Background", "tab-jungle"),
]

GROUPS = [
    ("Getting Started", [
        ("Introduction", "ds-00-home.html"),
        ("Colors",       "ds-01-color.html"),
        ("Typography",   "ds-02-typography.html"),
        ("Elevation",    "ds-03-elevation.html"),
        ("Shape",        "ds-04-shape.html"),
        ("Spacing",      "ds-05-spacing.html"),
    ]),
    ("Brand assets", [
        ("Norbielink Logo",  "ds-brand-norbielink-logo.html"),
        ("BTIS Logo",        "ds-brand-logo.html"),
        ("Brand Characters", "ds-brand-characters.html"),
        ("Visual Elements",  VE),
    ]),
    ("Components", COMPONENTS),
]


def nav_for(current):
    out = ['<!-- SUB-NAV -->', '<nav class="ds-sidenav">']
    for title, items in GROUPS:
        out.append('  <div class="ds-sidenav-group">')
        out.append('    <div class="ds-sidenav-group-title">%s</div>' % title)
        for label, href in items:
            a = " active" if href == current else ""
            if href != VE:
                out.append('    <a class="ds-sidenav-item%s" href="%s">%s</a>' % (a, href, label))
                continue
            here = href == current
            out.append('    <div class="ds-sidenav-nest%s">' % (" open" if here else ""))
            out.append('      <div class="ds-sidenav-nest-row%s">' % a)
            out.append('        <a class="ds-sidenav-item%s" href="%s">%s</a>' % (a, href, label))
            out.append('        <button class="ds-sidenav-nest-btn" type="button" '
                       'aria-label="Toggle %s sections" aria-expanded="%s" '
                       'onclick="toggleSidenavNest(this)">'
                       '<span class="material-icons-round">expand_more</span></button>'
                       % (label, "true" if here else "false"))
            out.append('      </div>')
            out.append('      <div class="ds-sidenav-nest-sub">')
            for sub, pane in VE_SECTIONS:
                out.append('        <a class="ds-sidenav-subitem" href="%s#%s">%s</a>' % (href, pane, sub))
            out.append('      </div>')
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
