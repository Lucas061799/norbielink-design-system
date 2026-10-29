# -*- coding: utf-8 -*-
"""Generate the four brand-asset pages for the Norbielink DS.

Every value on these pages is transcribed from the BTIS brand style guide on
zeroheight; the downloadable files are the originals, mirrored into
brand-assets/ so the DS serves them itself instead of linking out.
"""
import os, html, collections
from PIL import Image

ROOT = "/Users/lucasye/Documents/Norbielink Design system"

def size_of(path):
    b = os.path.getsize(os.path.join(ROOT, path))
    if b >= 1024 * 1024:
        return "%.1f MB" % (b / 1048576)
    if b >= 1024:
        return "%.1f KB" % (b / 1024)
    return "%d B" % b

def raw_size(path):
    return os.path.getsize(os.path.join(ROOT, path))

ON_DARK = set("""
brand-assets/btis-logo/Logo_Fullwhite.svg brand-assets/btis-logo/Logo_Fullwhite.png
brand-assets/btis-logo/Logo_white.svg brand-assets/btis-logo/Logo_white.png
brand-assets/btis-logo/Logo_withname_white.svg brand-assets/btis-logo/Logo_withname_white.png
brand-assets/btis-logo/Logo_yuellow.svg brand-assets/btis-logo/Logo_yellow.png
brand-assets/btis-logo/Icon_Logo_yellow.svg brand-assets/btis-logo/Icon_Logo_yellow.png
brand-assets/norbielink-logo/Norbielink_white.svg brand-assets/norbielink-logo/Norbielink_white.png
brand-assets/norbielink-logo/Norbielink_Brandlogo-Dark.svg brand-assets/norbielink-logo/Norbielink_Brandlogo-Dark.png
brand-assets/norbielink-logo/NorbieLink-ALL_NL-btis.svg brand-assets/norbielink-logo/NorbieLink-ALL_NL-btis.png
""".split())

BADGE_ONLY = {"ai", "gif"}          # never load these into a 40px thumbnail
THUMB_MAX  = 1_600_000              # nor anything heavier than this


def file_card(path, label=None):
    """One downloadable asset. The <a download> is the whole point of the page."""
    name = label or os.path.basename(path)
    ext  = os.path.splitext(path)[1].lstrip(".").lower()
    cls  = "ba-thumb on-dark" if path in ON_DARK else "ba-thumb"
    if ext in BADGE_ONLY or raw_size(path) > THUMB_MAX:
        thumb = '<span class="ba-ext">%s</span>' % ext.upper()
    else:
        thumb = '<img src="%s" alt="">' % path
    return (
        '      <a class="ba-file" href="%s" download>\n'
        '        <span class="%s">%s</span>\n'
        '        <span class="ba-fmeta">\n'
        '          <span class="ba-fname">%s</span>\n'
        '          <span class="ba-fsub">%s · %s</span>\n'
        '        </span>\n'
        '        <span class="material-icons-round ba-dl">download</span>\n'
        '      </a>\n' % (path, cls, thumb, html.escape(name), ext.upper(), size_of(path))
    )


def files(paths):
    """paths: list of str, or (path, display-name) pairs."""
    out = ['    <div class="ba-files">\n']
    for p in paths:
        out.append(file_card(*p) if isinstance(p, tuple) else file_card(p))
    out.append("    </div>\n")
    return "".join(out)


def one_ratio(path):
    try:
        with Image.open(os.path.join(ROOT, path)) as im:
            return im.width / im.height
    except Exception:
        return None


def fill_class(path, box):
    """Fill the box when the image is no wider than it, letterbox when it is.

    Cropping top and bottom is safe — these are centred compositions with
    headroom. Cropping the sides is not: it ate the first letter of the
    wordmark."""
    r = one_ratio(path)
    return " fill" if r is not None and r <= box + 0.001 else ""


def ratio_of(paths):
    """One box ratio for the whole grid, so its cards line up.

    The median, with the images contained rather than cropped: a sideways crop
    ate the first letter of the wordmark, and cropping to the widest image left
    the whole row a 96px strip. Letterboxing against the neutral costs nothing
    these screenshots were carrying anyway."""
    import statistics
    rs = []
    for q in paths:
        try:
            with Image.open(os.path.join(ROOT, q)) as im:
                rs.append(im.width / im.height)
        except Exception:
            pass
    return round(statistics.median(rs), 3) if rs else 1.6


def canvas_colour(path):
    """The flat background an example is painted on, or white.

    Only answers when the image really is full-bleed on one colour: all four
    corners and all four edge midpoints have to agree. Guessing from the
    dominant colour put yellow bars around the banana and grey ones around a
    white jungle silhouette."""
    try:
        with Image.open(os.path.join(ROOT, path)) as im:
            im = im.convert("RGBA")
            w, h = im.size
            pts = [(1, 1), (w - 2, 1), (1, h - 2), (w - 2, h - 2),
                   (w // 2, 1), (w // 2, h - 2), (1, h // 2), (w - 2, h // 2)]
            px = [im.getpixel(p) for p in pts]
            if any(p[3] < 250 for p in px):
                return "#FFFFFF"
            r, g, b = px[0][:3]
            if any(abs(p[i] - [r, g, b][i]) > 6 for p in px for i in range(3)):
                return "#FFFFFF"
            if min(r, g, b) >= 248:
                return "#FFFFFF"
            return "#%02X%02X%02X" % (r, g, b)
    except Exception:
        return "#FFFFFF"


# A lone example never gets taller than this share of its width. Full-bleed
# artwork ran to 570px and swamped the copy around it; even half the width was
# still too much page for one picture.
ONE_MIN_RATIO = 2.8


def shots(items, cols=None):
    """A single shot runs the full content width; two or more share one box."""
    srcs = [(it[0] if isinstance(it, tuple) else it) for it in items]
    one = cols == 1 or (cols is None and len(items) == 1)
    r = max(ratio_of(srcs), ONE_MIN_RATIO) if one else ratio_of(srcs)
    style = ' style="--r:%s;"' % r
    if cols and cols > 1 and not one:
        style = ' style="--r:%s;grid-template-columns:repeat(%d,1fr);"' % (r, cols)
    out = ['    <div class="ba-shots%s"%s>\n' % (" one" if one else "", style)]
    for it in items:
        src, cap = (it if isinstance(it, tuple) else (it, None))
        out.append('      <figure class="ba-shot">'
                   '<div class="ba-shot-art%s" style="--bg:%s">'
                   '<img src="%s" alt="%s" loading="lazy"></div>%s</figure>\n'
                   % ("" if one else fill_class(src, r), canvas_colour(src), src, html.escape(cap or ""),
                      '<figcaption>%s</figcaption>' % html.escape(cap) if cap else ""))
    out.append("    </div>\n")
    return "".join(out)


def dodont(items):
    """items: (kind, src, caption) where kind is 'do' or 'dont'."""
    box = ratio_of([i[1] for i in items])
    out = ['    <div class="ba-dd" style="--r:%s;">\n' % box]
    for kind, src, cap in items:
        out.append(
            '      <figure class="ba-dd-card">\n'
            '        <div class="ba-dd-img%s"><img src="%s" alt="" loading="lazy"></div>\n'
            '        <figcaption><span class="badge-status-pill %s">%s</span>%s</figcaption>\n'
            '      </figure>\n'
            % (fill_class(src, box), src,
               "badge-sp-active" if kind == "do" else "badge-sp-declined",
               "Do" if kind == "do" else "Don’t",
               html.escape(cap)))
    out.append("    </div>\n")
    return "".join(out)


def links(items):
    out = ['    <div class="ba-links">\n']
    for label, desc, href in items:
        out.append(
            '      <a class="ba-link" href="%s" target="_blank" rel="noopener">\n'
            '        <span class="material-icons-round">open_in_new</span>\n'
            '        <span class="ba-fmeta"><span class="ba-fname">%s</span>'
            '<span class="ba-fsub">%s</span></span>\n'
            '      </a>\n' % (href, html.escape(label), html.escape(desc)))
    out.append("    </div>\n")
    return "".join(out)


def p(text):
    return '    <p class="ba-p">%s</p>\n' % text

def h3(text, anchor=None):
    a = ' id="%s"' % anchor if anchor else ""
    return '    <h3 class="ba-h3"%s>%s</h3>\n' % (a, text)


CSS = """
/* .ds-main is a flex item: without min-width:0 the widest image in these grids
   pushes it past the TOC instead of shrinking. */
.ds-main { min-width: 0; }

/* ── BRAND ASSET PAGE ──
   A mirror of the BTIS brand style guide: the same copy, the same examples, and
   the original files served from this repo so nothing has to open zeroheight. */
/* The tabbed pages list their tabs in the right-hand rail as quick jumps. */
.ds-toc-item.ds-toc-sub { padding-left: 22px; font-size: 12px; }

.ba-p { font-size: 14px; line-height: 1.7; color: var(--body-text); margin-bottom: 18px; max-width: 70ch; }
.ba-h3 { font-family: 'Montserrat', sans-serif; font-size: 15px; font-weight: 700;
  color: var(--gray-800); margin: 36px 0 10px; }
.ba-section-lead { margin-top: 0; }

.ba-note { display: flex; gap: 10px; align-items: flex-start; background: var(--gray-50);
  border: 1px solid var(--gray-200); border-radius: 10px; padding: 12px 14px;
  font-size: 13px; line-height: 1.65; color: var(--gray-600); margin: 16px 0 24px; }
.ds-section-title + .ba-note { margin-top: 18px; }
.ba-note .material-icons-round { font-size: 18px; color: #A614C3; flex-shrink: 0; }
.ba-note a { color: #A614C3; font-weight: 600; text-decoration: none; }
.ba-note a:hover { text-decoration: underline; }

/* A grid of examples shares one box (--r, the median ratio of its own images)
   so the row lines up; a lone example runs the full column at its own ratio. */
.ba-shots { display: grid; gap: 14px; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  margin-bottom: 18px; }
.ba-shots.one { grid-template-columns: 1fr; }
.ba-shot { border: 1px solid var(--gray-200); border-radius: 12px; overflow: hidden;
  background: var(--card-bg); margin: 0; }
.ba-shot-art { aspect-ratio: var(--r, 16 / 9); display: flex; align-items: center;
  justify-content: center; background: var(--bg, #FFFFFF); }
.ba-shot-art img { display: block; max-width: 100%; max-height: 100%; object-fit: contain; }
.ba-shot-art.fill img { width: 100%; height: 100%; max-width: none; max-height: none;
  object-fit: cover; }
/* A lone example is the page's hero: the artwork sits well inside its box
   rather than filling it. */
.ba-shots.one .ba-shot-art { padding: 30px 40px; }
.ba-shots.one .ba-shot-art img { max-height: 165px; }
.ba-shot figcaption { font-size: 12px; line-height: 1.5; color: var(--gray-500);
  padding: 9px 12px; border-top: 1px solid var(--gray-100); background: var(--card-bg); }

.ba-files { display: grid; gap: 10px; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); }
.ba-file, .ba-link { display: flex; align-items: center; gap: 11px; padding: 10px 12px;
  border: 1px solid var(--gray-200); border-radius: 10px; background: var(--card-bg);
  text-decoration: none; transition: border-color .15s, box-shadow .15s; }
.ba-file:hover, .ba-link:hover { background: var(--hover-bg); border-color: var(--gray-300);
  text-decoration: none; }
.ba-thumb { width: 40px; height: 40px; border-radius: 8px; background: #F3F4F6;
  border: 1px solid rgba(0,0,0,.06); display: flex; align-items: center; justify-content: center;
  flex-shrink: 0; overflow: hidden; }
.ba-thumb.on-dark { background: #2D3653; border-color: rgba(255,255,255,.10); }
.ba-thumb img { max-width: 74%; max-height: 74%; object-fit: contain; }
.ba-ext { font-family: 'Montserrat', sans-serif; font-size: 9px; font-weight: 700;
  letter-spacing: .04em; color: #6B7280; }
.ba-thumb.on-dark .ba-ext { color: #D1D5DB; }
.ba-fmeta { display: flex; flex-direction: column; gap: 2px; min-width: 0; flex: 1; }
.ba-fname { font-family: 'Montserrat', sans-serif; font-size: 12px; font-weight: 600;
  color: var(--gray-800); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.ba-fsub { font-size: 11px; color: var(--gray-400); }
.ba-dl { font-size: 18px; color: var(--gray-300); flex-shrink: 0; }
.ba-file:hover .ba-dl { color: var(--gray-500); }
.ba-link .material-icons-round:first-child { font-size: 18px; color: var(--gray-400); flex-shrink: 0; }
.ba-links { display: grid; gap: 10px; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  margin-bottom: 18px; }

/* ── Do's & Don'ts ── the brand guide's own pairing, image above its rule. */
/* Two to a row, each filling half the column: the pairs in the brand guide
   are meant to be read side by side. */
.ba-dd { display: grid; gap: 14px; grid-template-columns: repeat(2, minmax(0, 1fr)); }
@media (max-width: 720px) { .ba-dd { grid-template-columns: 1fr; } }
.ba-dd-card { margin: 0; border: 1px solid var(--gray-200); border-radius: 12px;
  overflow: hidden; background: var(--card-bg); }
.ba-dd-img { background: #FFFFFF; aspect-ratio: var(--r, 3 / 2); }
.ba-dd-img img { display: block; width: 100%; height: 100%; object-fit: contain; }
.ba-dd-img.fill img { object-fit: cover; }
.ba-dd-card figcaption { padding: 11px 13px 13px; font-size: 12px; line-height: 1.55;
  color: var(--gray-600); border-top: 1px solid var(--gray-100); background: var(--card-bg); }
/* The Do / Don't label is the product's own tonal status pill — teal for the
   positive state, red for Declined — not a new colour pair. */
.ba-dd-card figcaption .badge-status-pill { display: flex; margin-bottom: 7px; }

/* ── Tabs ── the product's own tab bar. */
.ba-tabs { display: flex; align-items: center; gap: 4px; border-bottom: 1px solid var(--gray-200);
  margin-bottom: 26px; width: 100%; overflow-x: auto; }
.ba-tab { position: relative; display: inline-flex; align-items: center; padding: 12px 16px;
  border: none; background: transparent; cursor: pointer; font-family: 'Montserrat', sans-serif;
  font-size: 13px; font-weight: 400; line-height: 1.5; letter-spacing: .01em;
  color: var(--gray-500); white-space: nowrap; transition: color .12s; }
.ba-tab:hover { color: var(--gray-800); }
.ba-tab.active { color: #A614C3; }
body.dark-mode .ba-tab.active { color: #FFFFFF; }
.ba-tab.active::after { content: ''; position: absolute; left: 0; right: 0; bottom: 0; height: 2px;
  background: linear-gradient(90deg,#5C2ED4 0%,#A614C3 65%); }
.ba-pane { display: none; }
.ba-pane.active { display: block; }

/* ── Product tiles (visual elements) ──
   A plain contact sheet: the artwork and its name, with the downloads listed
   underneath as file rows like everywhere else on these pages. */
.ba-tilegrid { display: grid; gap: 12px; grid-template-columns: repeat(auto-fill, minmax(162px, 1fr));
  margin-bottom: 8px; }
.ba-tilecell { margin: 0; border: 1px solid var(--gray-200); border-radius: 12px;
  overflow: hidden; background: var(--card-bg); }
.ba-tilecell-art { height: 104px; display: flex; align-items: center; justify-content: center;
  background: #FFFFFF; }
body.dark-mode .ba-tilecell-art { background: #0F1120; }
.ba-tilecell-art img { max-width: 64px; max-height: 64px; object-fit: contain; }
.ba-tilecell-art .dark-art { display: none; }
body.dark-mode .ba-tilecell-art.has-dark .light-art { display: none; }
body.dark-mode .ba-tilecell-art .dark-art { display: block; }
.ba-tilecell figcaption { padding: 8px 10px 10px; border-top: 1px solid var(--gray-100);
  font-family: 'Montserrat', sans-serif; font-size: 11px; font-weight: 600;
  line-height: 1.35; color: var(--gray-800); }
.ba-tilecell-dl { display: flex; gap: 5px; margin-top: 6px; }
.ba-tilecell-dl a { display: inline-flex; align-items: center; gap: 2px;
  font-size: 10px; font-weight: 600; letter-spacing: .02em; color: var(--gray-500);
  text-decoration: none; border: 1px solid var(--gray-200); border-radius: 6px;
  padding: 2px 6px 2px 4px; transition: color .12s, border-color .12s, background .12s; }
.ba-tilecell-dl a:hover { color: var(--gray-800); border-color: var(--gray-300);
  background: var(--hover-bg); text-decoration: none; }
.ba-tilecell-dl .material-icons-round { font-size: 12px; }
"""

HEAD = """<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} - Norbielink Design System</title>
<link rel="stylesheet" href="ds-shared.css">
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@800&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body class="btis-layout">
<header class="btis-header">
  <div class="btis-header-inner">
    <a class="btis-brand" href="ds-00-home.html">
      <img src="BTIS.png" class="btis-logo-img" alt="NorbieLink">
    </a>
    <nav class="btis-top-nav">
      <a class="btis-top-nav-link" href="ds-nav-foundations.html">Foundations</a>      <a class="btis-top-nav-link" href="ds-nav-components.html">Components</a>
      <a class="btis-top-nav-link active" href="ds-nav-resources.html">Resources</a>
    </nav>
    <div class="btis-header-right">
      <button class="btis-icon-btn" onclick="toggleSearch()"><span class="material-icons-round">search</span></button>
      <button class="btis-theme-pill" id="darkModeBtn" onclick="toggleDarkMode()">
        <span class="material-icons-round" id="darkModeIcon">dark_mode</span>
        <span>Theme</span>
      </button>
    </div>
  </div>
</header>

<div class="ds-shell">

<!-- SEARCH OVERLAY -->
<div id="search-overlay" onclick="if(event.target===this)closeSearch()">
  <div class="search-modal">
    <div class="search-input-wrap">
      <span class="material-icons-round">search</span>
      <input id="search-input" type="text" placeholder="Search components, foundations…" oninput="renderResults(this.value)" onkeydown="searchKeydown(event)">
      <span class="material-icons-round search-close" onclick="closeSearch()">close</span>
    </div>
    <div class="search-results" id="search-results"></div>
    <div class="search-hint">
      <kbd>↑</kbd><kbd>↓</kbd> navigate &nbsp;·&nbsp; <kbd>↵</kbd> open &nbsp;·&nbsp; <kbd>Esc</kbd> close &nbsp;·&nbsp; <kbd>⌘K</kbd> open
    </div>
  </div>
</div>

<aside class="ds-toc">
  <div class="ds-toc-title">In this article</div>
{toc}</aside>

<main class="ds-main">
  <div class="ds-content">
    <div class="ds-breadcrumb">
      <a href="ds-00-home.html">Home</a><span class="ds-breadcrumb-sep">›</span>
      <a href="ds-nav-resources.html">Resources</a><span class="ds-breadcrumb-sep">›</span><span>{title}</span>
    </div>
    <div class="ds-title-row">
      <h1 class="ds-page-title">{title}</h1>
      <div class="ds-title-actions">
        <a class="ds-nav-arrow-btn" href="{prev}" title="Previous"><span class="material-icons-round">arrow_back</span></a>
        <a class="ds-nav-arrow-btn" href="{next}" title="Next"><span class="material-icons-round">arrow_forward</span></a>
      </div>
    </div>
    <p class="ds-page-desc">{desc}</p>

{body}
  </div>
</main>
</div>
<script src="ds-search.js"></script>
<script>
function toggleDarkMode(){{
  const b=document.body,ic=document.getElementById('darkModeIcon'),bt=document.getElementById('darkModeBtn');
  b.classList.toggle('dark-mode');
  if(b.classList.contains('dark-mode')){{ic.textContent='light_mode';bt.classList.add('active');}}
  else{{ic.textContent='dark_mode';bt.classList.remove('active');}}
}}
function baTab(btn,id){{
  const wrap=btn.closest('.ba-tabwrap');
  wrap.querySelectorAll('.ba-tab').forEach(t=>t.classList.remove('active'));
  btn.classList.add('active');
  wrap.querySelectorAll('.ba-pane').forEach(p=>p.classList.toggle('active',p.id===id));
  if(history.replaceState) history.replaceState(null,'','#'+id);
  baSyncNav(id);
}}
/* The sub-nav deep-links to these tabs, so keep it in step with the page. */
function baSyncNav(id){{
  document.querySelectorAll('.ds-sidenav-subitem').forEach(a=>
    a.classList.toggle('active',(a.getAttribute('href')||'').split('#')[1]===id));
  document.querySelectorAll('.ds-toc-item.ds-toc-sub').forEach(a=>
    a.classList.toggle('active',a.getAttribute('href')==='#'+id));
}}
function baApplyHash(scroll){{
  const id=location.hash.slice(1);
  const btn=id&&document.querySelector('.ba-tab[data-pane="'+id+'"]');
  if(btn){{ baTab(btn,id); if(scroll) btn.closest('.ba-tabwrap').scrollIntoView({{block:'start'}}); }}
  else {{ const p=document.querySelector('.ba-pane.active'); if(p) baSyncNav(p.id); }}
}}
/* The shared TOC smooth-scroller swallows its own clicks, so the rail's
   tab links are handled first, in the capture phase. */
document.addEventListener('click',function(e){{
  const a=e.target.closest&&e.target.closest('a[href^="#tab-"]');
  if(!a) return;
  const id=a.getAttribute('href').slice(1);
  const btn=document.querySelector('.ba-tab[data-pane="'+id+'"]');
  if(!btn) return;
  e.preventDefault(); e.stopPropagation();
  baTab(btn,id);
  btn.closest('.ba-tabwrap').scrollIntoView({{block:'start'}});
}},true);
window.addEventListener('DOMContentLoaded',function(){{ baApplyHash(true); }});
window.addEventListener('hashchange',function(){{ baApplyHash(true); }});
</script>
<script src="ds-shared.js"></script>
</body></html>
"""


def page(filename, title, desc, toc, body, prev, nxt):
    rows = []
    for i, entry in enumerate(toc):
        a, l = entry[0], entry[1]
        cls = " ds-toc-sub" if len(entry) > 2 and entry[2] else ""
        rows.append('  <a class="ds-toc-item%s%s" href="#%s">%s</a>\n'
                    % (" active" if i == 0 else "", cls, a, l))
    toc_html = "".join(rows)
    out = HEAD.format(title=title, css=CSS, toc=toc_html, desc=desc,
                      body=body, prev=prev, next=nxt)
    with open(os.path.join(ROOT, filename), "w") as f:
        f.write(out)
    print("wrote", filename, len(out), "bytes")


def section(anchor, title, inner):
    return ('  <div class="ds-section" id="%s">\n'
            '    <h2 class="ds-section-title">%s</h2>\n%s  </div>\n\n'
            '  <div class="ds-divider"></div>\n\n' % (anchor, title, inner))


SOURCE_NOTE = (
    '    <div class="ba-note">\n'
    '      <span class="material-icons-round">info</span>\n'
    '      <span>Mirrored from the BTIS brand style guide — <a href="{url}" '
    'target="_blank" rel="noopener">{label}</a>. Every file below is the original, '
    'served from this site; nothing opens in another tab.</span>\n'
    '    </div>\n')

B = "brand-assets/btis-logo/"
N = "brand-assets/norbielink-logo/"
V = "brand-assets/visual-elements/"
C = "brand-assets/characters/"

APPEARANCE_LEAD = ("By default, the lockup and icon inherit their colors from the parent element, "
                   "however, this can lead to incorrect color combinations. Moving forward, all usages "
                   "should choose between the brand-approved appearances below.")

# ═══════════════════════════════════════════════════════════════════
# 1 — BTIS Logo
# ═══════════════════════════════════════════════════════════════════
body = ""
body += section("types", "Types",
    SOURCE_NOTE.format(url="https://zeroheight.com/741749006/p/416ed4-logo", label="Logo")
    + h3("Icon")
    + p("An icon is an image or symbol that represents a brand or app. It generally does not "
        "contain the name of the brand or app.")
    + shots([B + "img/icon.jpg"])
    + files([B + "Icon_Logo_blue.svg", B + "Icon_Logo_blue.png",
             B + "Icon_Logo_yellow.svg", B + "Icon_Logo_yellow.png"])
    + h3("Lockup")
    + p("A lockup is the combination of wordmark (the brand or app name) and its icon, generally "
        "referred altogether as a logo.")
    + shots([B + "img/lockup.jpg"])
    + files([(B + "Logo_with_name.svg", "Logo_with name.svg"), B + "Logo_withname.png",
             B + "Logo_withname_white.svg", B + "Logo_withname_white.png"]))

body += section("appearance", "Appearance",
    p(APPEARANCE_LEAD)
    + h3("Brand")
    + p("Brand app logos are used in situations that demand a bold brand presence against a "
        "neutral background.")
    + shots([B + "img/brand-1.png", B + "img/brand-2.jpg", B + "img/brand-3.jpg"])
    + files([B + "Logo_blue.svg", B + "Logo_blue.png", B + "Logo_white.svg", B + "Logo_white.png",
             B + "Logo_Darkblue.svg", B + "Logo_Darkblue.png",
             (B + "Logo_yuellow.svg", "Logo_yuellow.svg"), B + "Logo_yellow.png"])
    + h3("Neutral")
    + p("Neutral app logos can be used when the hierarchy calls for the logo to recede, but should "
        "always be evaluated for adequate contrast.")
    + shots([B + "img/neutral-1.jpg", B + "img/neutral-2.jpg"])
    + files([B + "Logo_Fullblack.svg", B + "Logo_Fullblack.png",
             B + "Logo_Fullwhite.svg", B + "Logo_Fullwhite.png"])
    + h3("Inverse")
    + p("Inverse app logos should be used to contrast against bold backgrounds.")
    + shots([B + "img/inverse-1.jpg"])
    + files([B + "InverseLogo.jpg"]))

body += section("dos", "Do's",
    p("Here are our do's, and also the BTIS logo exists mainly in the two-color version.")
    + dodont([
        ("do", B + "img/do-1.png",  "The primary color logo is preferred over all others."),
        ("do", B + "img/do-2.jpg",  "If necessary, it can be represented on our purple background with white letters"),
        ("do", B + "img/do-3.jpg",  "For strictly black and white situations, the entire logo will contrast with the black or white background."),
        ("do", B + "img/do-4.jpg",  "For strictly black and white situations, the entire logo will contrast with the black or white background."),
        ("do", B + "img/do-5.jpg",  "Additional color combination-1"),
        ("do", B + "img/do-6.jpg",  "Additional color combination-2"),
        ("do", B + "img/do-7.jpg",  "Additional color combination-3"),
        ("do", B + "img/do-8.jpg",  "Additional color combination-4"),
        ("do", B + "img/do-9.png",  "When specifically referencing the Marketplace or its features, the full BTIS Marketplace logo may be used."),
        ("do", B + "img/do-10.jpg", "When specifically referencing the Marketplace or its features, the full BTIS Marketplace logo may be used."),
        ("do", B + "img/do-11.jpg", "The “b” mark can be used situationally as a background element or in social media."),
        ("do", B + "img/do-12.jpg", "The “b” mark can be used situationally as a background element or in social media."),
    ]))

DONTS = [
    ("dont", "dont-1.jpg", "Stretching or squeezing. Never deform the logo."),
    ("dont", "dont-2.jpg", "Stretching or squeezing. Never deform the logo."),
    ("dont", "dont-3.jpg", "Moving elements. Don’t rearrange the elements of the logo."),
    ("dont", "dont-4.jpg", "Changing colors. Do not alter the colors of the logo."),
    ("dont", "dont-5.jpg", "Obscuring. Never place the logo on a background that makes the logo blend in or disappear."),
    ("dont", "dont-6.jpg", "Obscuring. Never place the logo on a background that makes the logo blend in or disappear."),
    ("dont", "dont-7.jpg", "Crowding. Always leave the prescribed space around the logo, away from other elements."),
    ("dont", "dont-8.jpg", "Visual effects. Do not add effects like drop-shadows, strokes, embossing etc. to the logo."),
]
body += section("donts", "Don'ts",
    p("Ouch.... These are some painful examples of unacceptable uses of the BTIS logo.")
    + dodont([(k, B + "img/" + f, c) for k, f, c in DONTS]))

page("ds-brand-logo.html", "BTIS Logo",
     "A logo is a visual representation of a brand or app. It can be a word, an image, or a "
     "combination of both. This is the parent BTIS mark; Norbielink has its own lockup on the "
     "<a href=\"ds-brand-norbielink-logo.html\">Norbielink Logo</a> page.",
     [("types", "Types"), ("appearance", "Appearance"), ("dos", "Do's"), ("donts", "Don'ts")],
     body, "ds-nav-resources.html", "ds-brand-norbielink-logo.html")


# ═══════════════════════════════════════════════════════════════════
# 2 — Norbielink Logo
# ═══════════════════════════════════════════════════════════════════
body = ""
body += section("types", "Types",
    SOURCE_NOTE.format(url="https://zeroheight.com/741749006/p/966964-norbielink-logo",
                       label="Norbielink Logo")
    + h3("Icon")
    + p("An icon is an image or symbol that represents a brand or app. It generally does not "
        "contain the name of the brand or app.")
    + shots([N + "img/icon.png"])
    + files([N + "Norbielink_logo_N.png", (N + "Norbirlink_logo_N.svg", "Norbirlink_logo_N.svg")])
    + h3("Lockup")
    + p("A lockup is the combination of wordmark (the brand or app name) and its icon, generally "
        "referred altogether as a logo.")
    + shots([(N + "img/lockup-dark.png", "Norbielink_lockup on Dark"),
             (N + "img/lockup-white.png", "Norbielink_lockup on White")], cols=2)
    + files([N + "NorbieLink-ALL_NL-btis.png", N + "NorbieLink-ALL_NL-btis.svg",
             (N + "NorbieLink-ALL_NL-btis-on_white.png", "NorbieLink-ALL_NL-btis-on white.png"),
             (N + "NorbieLink-ALL_NL-btis-on_white.svg", "NorbieLink-ALL_NL-btis-on white.svg")]))

body += section("appearance", "Appearance",
    p(APPEARANCE_LEAD)
    + h3("Brand")
    + p("Brand app logos are used in situations that demand a bold brand presence against a "
        "neutral background.")
    + shots([N + "img/brand-1.png", N + "img/brand-2.png"], cols=2)
    + files([N + "NorbieLink-Brandlogo-onWhite.png",
             (N + "NorbieLink-Brandlogo-on_white.svg", "NorbieLink-Brandlogo-on white.svg"),
             N + "Norbielink_Brandlogo-Dark.png", N + "Norbielink_Brandlogo-Dark.svg"])
    + h3("Neutral")
    + p("Neutral app logos can be used when the hierarchy calls for the logo to recede, but should "
        "always be evaluated for adequate contrast.")
    + shots([N + "img/neutral-1.png", N + "img/neutral-2.png"], cols=2)
    + files([N + "Norbielink_Dark.png", N + "Norbielink_Dark.svg",
             N + "Norbielink_white.png", N + "Norbielink_white.svg"]))

body += section("dos", "Do's",
    p("Here are our do's, and also the BTIS logo exists mainly in the two-color version.")
    + dodont([
        ("do", N + "img/do-1.png", "The primary color logo is preferred over all others."),
        ("do", N + "img/do-2.png", "If necessary, it can be represented on our purple background with white letters"),
        ("do", N + "img/do-3.png", "For strictly black and white situations, the entire logo will contrast with the black or white background."),
        ("do", N + "img/do-4.png", "For strictly black and white situations, the entire logo will contrast with the black or white background."),
        ("do", N + "img/do-5.png", "When specifically referencing the Marketplace or its features, the full BTIS Marketplace logo may be used."),
        ("do", N + "img/do-6.png", "When specifically referencing the Marketplace or its features, the full BTIS Marketplace logo may be used."),
        ("do", N + "img/do-7.jpg", "The “b” mark can be used situationally as a background element or in social media."),
        ("do", N + "img/do-8.jpg", "The “b” mark can be used situationally as a background element or in social media."),
    ]))

body += section("donts", "Don'ts",
    p("Ouch.... These are some painful examples of unacceptable uses of the BTIS logo.")
    + dodont([(k, N + "img/" + f, c) for k, f, c in DONTS]))

page("ds-brand-norbielink-logo.html", "Norbielink Logo",
     "A logo is a visual representation of a brand or app. It can be a word, an image, or a "
     "combination of both.",
     [("types", "Types"), ("appearance", "Appearance"), ("dos", "Do's"), ("donts", "Don'ts")],
     body, "ds-brand-logo.html", "ds-brand-characters.html")

# ═══════════════════════════════════════════════════════════════════
# 3 — Brand Characters (Norbie / AI-Norbie)
# ═══════════════════════════════════════════════════════════════════
def tabwrap(tabs):
    """tabs: list of (pane_id, label, html)."""
    bar = "".join(
        '      <button class="ba-tab%s" data-pane="%s" onclick="baTab(this,\'%s\')">%s</button>\n'
        % (" active" if i == 0 else "", pid, pid, html.escape(lbl))
        for i, (pid, lbl, _) in enumerate(tabs))
    panes = "".join(
        '    <div class="ba-pane%s" id="%s">\n%s    </div>\n'
        % (" active" if i == 0 else "", pid, inner)
        for i, (pid, _, inner) in enumerate(tabs))
    return ('  <div class="ba-tabwrap">\n    <div class="ba-tabs">\n%s    </div>\n%s  </div>\n\n'
            % (bar, panes))


norbie = (
    h3("Usage")
    + p("Norbie can be used to call attention to, or answer questions about, a particularly "
        "noteworthy piece of information or need for motivation.")
    + h3("Norbie")
    + shots([C + "img/norbie-hero.png"], cols=1)
    + p("We use two different versions of Norbie. This version is primarily for our BTIS website, "
        "social media, and podcast. If you’re looking for the Norbie used in NorbieLink, see "
        "the <strong>AI-Norbie</strong> tab.")
    + files([C + "Norbie.svg", C + "Norbie.png",
             (C + "gorilla-all-rgb_Grad-01-Norbie.png", "gorilla-all-rgb_Grad 01 Norbie.png"),
             (C + "gorilla-all-rgb_Grad-02-Norbie.png", "gorilla-all-rgb_Grad 02 Norbie.png"),
             (C + "gorilla-all-rgb_Grad-03-Norbie.png", "gorilla-all-rgb_Grad 03 Norbie.png"),
             C + "gorilla-all-cmyk.ai"])
    + h3("More formats")
    + links([("Canva Asset Link", "Norbie’s Canva assets folder.",
              "https://www.canva.com/folder/FAFIa4luGRg"),
             ("Dropbox Asset Link", "Norbie’s Dropbox assets folder (more formats).",
              "https://www.dropbox.com/scl/fo/2hqzjf28b9c5tk1cwqt3u/h?rlkey=0gdaemg90medqwgnp7uwnzmjl&st=ciyjud9n&dl=0")])
    + h3("Do's &amp; Don'ts")
    + dodont([
        ("do",   C + "img/norbie-do-gradient.png", "You can use our brand color to add gradient effect to Norbie."),
        ("dont", C + "img/norbie-dont-color.png",  "Please don't use other color beside our brand color."),
        ("do",   C + "img/norbie-do-dressup.jpg",  "You may dress Norbie up with relevant items (like hats or glasses) to match the theme."),
        ("dont", C + "img/norbie-dont-style.jpg",  "Do not change the illustration style or modify Norbie's physical form."),
    ]))

ainorbie = (
    h3("Usage")
    + p("AI-Norbie can be used to call attention to, or answer questions about, a particularly "
        "noteworthy piece of information or need for motivation.")
    + h3("AI-Norbie")
    + shots([C + "img/ainorbie-hero.jpeg"], cols=1)
    + p("The AI version of Norbie is used mainly for Norbielink and any other Norbielink "
        "promotions. The AI-Norbie persona embodies the intelligence and precision of Norbielink. "
        "He represents a high-tech, efficient partner that agents can trust to power their success.")
    + files([C + "Norbieface.png", C + "Norbieface.svg",
             C + "Norbieface_Teal.png", C + "Norbieface_Teal.svg",
             C + "Norbieface_Raspberry.png",
             (C + "Norbirlink_Raspberry.svg", "Norbirlink_Raspberry.svg"),
             C + "Dark.gif", C + "Light.gif"])
    + '    <div class="ba-note"><span class="material-icons-round">info</span>'
      '<span><strong>Dark.gif</strong> and <strong>Light.gif</strong> are the full-resolution '
      'animations — 40.7&nbsp;MB and 9&nbsp;MB. They download directly, but they are large; the '
      'Dropbox link below carries lighter exports.</span></div>\n'
    + h3("More formats")
    + links([("Notion code Link", "Norbie’s Canva assets folder.",
              "https://www.canva.com/folder/FAFIa4luGRg"),
             ("Dropbox Asset Link", "Norbie’s Dropbox assets folder (more formats).",
              "https://www.dropbox.com/scl/fo/2hqzjf28b9c5tk1cwqt3u/h?rlkey=0gdaemg90medqwgnp7uwnzmjl&st=ciyjud9n&dl=0"),
             ("Dropbox GIF Link", "The Norbielink GIF folder on Dropbox.",
              "https://www.dropbox.com/scl/fo/rqkfon1t16s4rawwe14in/AHnAisEa7rBRIRS6v6xsfXQ?rlkey=0y1h74loegvwdn15v9d8his37&st=1r1g2lt2&dl=0")]))

body = ('  <div class="ds-section" id="characters">\n'
        + SOURCE_NOTE.format(url="https://zeroheight.com/741749006/p/02fa9b-norbie", label="Norbie")
        + p("Norbie is a tribute to Norbert Hohlbein, the original owner of btis and father of our "
            "co-presidents, Paul and Jeff Hohlbein. Norbert was known for his boldness, sternness, "
            "and likability. Norbert was affectionately referred to as a gorilla by those who knew "
            "him, and his legacy lives on through our new mascot.")
        + '  </div>\n\n'
        + tabwrap([("tab-norbie", "Norbie", norbie), ("tab-ainorbie", "AI-Norbie", ainorbie)]))

page("ds-brand-characters.html", "Brand Characters",
     "Norbie and AI-Norbie — the two mascots, their usage rules, and every exported format.",
     [("characters", "Brand Characters"),
      ("tab-norbie", "Norbie", True),
      ("tab-ainorbie", "AI-Norbie", True)],
     body, "ds-brand-norbielink-logo.html", "ds-brand-visual-elements.html")


# ═══════════════════════════════════════════════════════════════════
# 4 — Visual Elements
# ═══════════════════════════════════════════════════════════════════
# 21 lines of business. 16 ship a separate dark-mode drawing; the other 5 use
# the same file in both themes — exactly as the brand guide warns.
LOBS = [
    ("Bonds",                  "Bonds.svg",                  None),
    ("Builders Risk",          "Builders_Risk.svg",          "Builders_Risk_Dark.svg"),
    ("Business Owners",        "Business_Owners.svg",        "Business_Owners_Dark.svg"),
    ("Cannabis",               "Cannabis.svg",               "Cannabis_Dark.svg"),
    ("Cell Phone Stores",      "Cell_Phone_Stores.svg",      None),
    ("Commercial Auto",        "Commercial_Auto.svg",        "Commercial_Auto_Dark.svg"),
    ("Cyber",                  "Cyber.svg",                  "Cyber_Dark.svg"),
    ("Excess",                 "Excess.svg",                 "Excess_Dark.svg"),
    ("General Liability",      "General_Liability.svg",      "General_Liability_Dark.svg"),
    ("Home Based Business",    "Home_Based_Business.svg",    "Home_Based_Business_Dark.svg"),
    ("Inland Marine",          "Inland_Marine.svg",          "Inland_Marine_Dark.svg"),
    ("Lessor's Risk",          "Lessor_s_Risk.svg",          "Lessor_s_Risk_Dark.svg"),
    ("Marine Contractors",     "Marine_Contractors.svg",     "Marine_Contractors_Dark.svg"),
    ("Non-Profit",             "Non-Profit.svg",             "Non-Profit_Dark.svg"),
    ("Pollution",              "Pollution.svg",              "Pollution_Dark.svg"),
    ("Professional Liability", "Professional_Liability.svg", "Professional_Liability_Dark.svg"),
    ("Special Events",         "Special_Events.svg",         None),
    ("Sports Advantage",       "Sports_Advantage.svg",       None),
    ("Truckers GL",            "Truckers_GL.svg",            "Truckers_GL_Dark.svg"),
    ("Vacant Risks",           "Vacant_Risks.svg",           "Vacant_Risks_Dark.svg"),
    ("Worker's Comp",          "Worker_s_Comp.svg",          None),
]

def tile_display():
    """The set, with each drawing's own files attached to it."""
    out = ['    <div class="ba-tilegrid">\n']
    for name, light, dark in LOBS:
        art = '<img class="light-art" src="%s%s" alt="%s" loading="lazy">' % (V, light, html.escape(name))
        if dark:
            art += '<img class="dark-art" src="%s%s" alt="" loading="lazy">' % (V, dark)
        def pill(path, label):
            return ('<a href="%s%s" download>'
                    '<span class="material-icons-round">download</span>%s</a>' % (V, path, label))
        dl = pill(light, "Light") + pill(dark, "Dark") if dark else pill(light, "SVG")
        out.append('      <figure class="ba-tilecell">\n'
                   '        <div class="ba-tilecell-art%s">%s</div>\n'
                   '        <figcaption>%s<span class="ba-tilecell-dl">%s</span></figcaption>\n'
                   '      </figure>\n'
                   % (" has-dark" if dark else "", art, html.escape(name), dl))
    out.append("    </div>\n")
    return "".join(out)


# The brand guide's own order: the two Illustrator sources, then every tile
# alphabetically with each line's dark drawing ahead of its light one.
DISPLAY = {light: name for name, light, _ in LOBS}
DISPLAY.update({dark: name + " Dark" for name, _, dark in LOBS if dark})

TILE_ORDER = [
    "cat-ill-trade.ai", "category-all-illustrations-Revised.ai",
    "Bonds.svg",
    "Builders_Risk_Dark.svg", "Builders_Risk.svg",
    "Business_Owners_Dark.svg", "Business_Owners.svg",
    "Cannabis_Dark.svg", "Cannabis.svg",
    "Commercial_Auto_Dark.svg", "Commercial_Auto.svg",
    "Excess_Dark.svg", "Excess.svg",
    "General_Liability_Dark.svg", "General_Liability.svg",
    "Home_Based_Business_Dark.svg", "Home_Based_Business.svg",
    "Inland_Marine_Dark.svg", "Inland_Marine.svg",
    "Lessor_s_Risk_Dark.svg", "Lessor_s_Risk.svg",
    "Marine_Contractors_Dark.svg", "Marine_Contractors.svg",
    "Non-Profit_Dark.svg", "Non-Profit.svg",
    "Pollution_Dark.svg", "Pollution.svg",
    "Professional_Liability_Dark.svg", "Professional_Liability.svg",
    "Special_Events.svg", "Sports_Advantage.svg",
    "Truckers_GL_Dark.svg", "Truckers_GL.svg",
    "Vacant_Risks_Dark.svg", "Vacant_Risks.svg",
    "Worker_s_Comp.svg", "Cell_Phone_Stores.svg",
    "Cyber_Dark.svg", "Cyber.svg",
]


def tile_files():
    rows = []
    for f in TILE_ORDER:
        label = DISPLAY.get(f)
        rows.append((V + f, label + ".svg") if label else V + f)
    return files(rows)


CANVA_DROPBOX = links([
    ("Canva Assets link", "The Canva assets folder.", "https://www.canva.com/folder/FAFIa4luGRg"),
    ("Dropbox Assets Link", "More formats of the assets live here.",
     "https://www.dropbox.com/scl/fo/2hqzjf28b9c5tk1cwqt3u/h?rlkey=0gdaemg90medqwgnp7uwnzmjl&st=ciyjud9n&dl=0"),
])

tiles_pane = (
    h3("Usage")
    + p("These tiles act as the visual representation of our product suite. They serve as intuitive "
        "entry points, designed to help users instantly recognize and navigate to specific lines of "
        "business.")
    + shots([V + "img/tiles-hero.png"], cols=1)
    + CANVA_DROPBOX
    + '    <div class="ba-note"><span class="material-icons-round">error</span>'
      '<span>Norbielink has a dark mode and a light mode. A file named <code>Abc Dark</code> is the '
      'dark-mode drawing; anything else is the light-mode one. Where only a light version exists, '
      'the same file is used in both themes. The grid below already does the swap — toggle the '
      'theme to see it.</span></div>\n'
    + h3("Lines of business")
    + tile_display()
    + h3("Illustration sources")
    + files([V + "cat-ill-trade.ai", V + "category-all-illustrations-Revised.ai"]))

LEAVES_USAGE = ("These items aren’t used everywhere. They’re primarily used to tie the "
                "brand together. Examples would be leaves on an initial page or entry point to a "
                "branding piece, like letterhead, envelopes, business cards, the home page of the "
                "website, or the cover of a quarterly report.")
MONSTERA_P = ("Monstera leaves. Named from the Latin word for “monstrous” or "
              "“abnormal”, referring to the unusually large leaves, they are native to "
              "Norbie’s environment.")

monstera = (h3("Usage") + p(LEAVES_USAGE) + h3("Monstera Leaves")
            + shots([V + "img/monstera-hero.png"], cols=1) + p(MONSTERA_P)
            + files([V + "Leaves.svg", V + "Leaves.png", V + "leaf.ai"]))

banana = (h3("Usage") + p(LEAVES_USAGE) + h3("Banana")
          + shots([V + "img/banana-hero.png"], cols=1)
          + files([V + "Banana.png"]))

awning = (h3("Usage")
          + p("This graphic is used specifically in conjunction with the BTIS Marketplace logo, and "
              "is present within the digital insurance marketplaces. It may also be used when "
              "describing the Marketplace, lines of business, or ease of use associated with the "
              "online raters.")
          + h3("Marketplace awning")
          + shots([V + "img/awning-hero.png"], cols=1)
          + files([(V + "Marketplace_awning.svg", "Marketplace awning.svg"),
                   (V + "Marketplace_awning.png", "Marketplace awning.png")]))

jungle = (h3("Usage")
          + p("We utilize a jungle background across social media, email campaigns, and promotional "
              "materials to establish Norbie’s home environment. Designers are encouraged to "
              "explore different colors and formats to keep the visuals dynamic, provided the "
              "setting remains unmistakably a lush tropical rainforest.")
          + h3("Jungle Background")
          + shots([V + "img/jungle-hero.png"], cols=1) + p(MONSTERA_P)
          + files([V + "Background.png"]))

body = ('  <div class="ds-section" id="visual-elements">\n'
        + SOURCE_NOTE.format(url="https://zeroheight.com/741749006/p/580419-visual-elements",
                             label="Visual elements")
        + p("Along with our logo, these visual cues were created to emphasize our brand on printed "
            "and digital materials.")
        + '  </div>\n\n'
        + tabwrap([("tab-tiles", "Tiles / Product icon", tiles_pane),
                   ("tab-monstera", "\U0001F334 Monstera Leaves", monstera),
                   ("tab-banana", "\U0001F34C Banana", banana),
                   ("tab-awning", "Marketplace awning", awning),
                   ("tab-jungle", "Jungle Background", jungle)]))

page("ds-brand-visual-elements.html", "Visual Elements",
     "Product tiles, Monstera leaves, the banana, the Marketplace awning and the jungle "
     "background — every brand illustration, with its light and dark drawing.",
     [("visual-elements", "Visual Elements"),
      ("tab-tiles", "Tiles / Product icon", True),
      ("tab-monstera", "Monstera Leaves", True),
      ("tab-banana", "Banana", True),
      ("tab-awning", "Marketplace awning", True),
      ("tab-jungle", "Jungle Background", True)],
     body, "ds-brand-characters.html", "ds-nav-resources.html")
