#!/usr/bin/env python3
"""
Add prev/next nav + title-row actions to all component pages.
Force-replaces any existing ds-page-nav block.
"""
import os, re

BASE = "/Users/lucasye/Documents/Norbielink Design system"

PAGES = [
    ("ds-00-home.html",         "Introduction"),
    ("ds-01-color.html",        "Colors"),
    ("ds-02-typography.html",   "Typography"),
    ("ds-03-elevation.html",    "Elevation"),
    ("ds-04-shape.html",        "Shape"),
    ("ds-05-spacing.html",      "Spacing"),
    ("ds-26-accordion.html",    "Accordion"),
    ("ds-27-alert.html",        "Alert"),
    ("ds-28-alert-dialog.html", "Alert Dialog"),
    ("ds-14-appbar.html",       "App Bars"),
    ("ds-29-avatar.html",       "Avatar"),
    ("ds-09-badges.html",       "Badge"),
    ("ds-30-breadcrumb.html",   "Breadcrumb"),
    ("ds-06-buttons.html",      "Button"),
    ("ds-31-button-group.html", "Button Group"),
    ("ds-32-calendar.html",     "Calendar"),
    ("ds-10-cards.html",        "Card"),
    ("ds-33-carousel.html",     "Carousel"),
    ("ds-34-chart.html",        "Chart"),
    ("ds-15-checkbox.html",     "Checkbox"),
    ("ds-16-chips.html",        "Chips"),
    ("ds-35-collapsible.html",  "Collapsible"),
    ("ds-36-combobox.html",     "Combobox"),
    ("ds-37-command.html",      "Command"),
    ("ds-38-context-menu.html", "Context Menu"),
    ("ds-13-datatable.html",    "Data Table"),
    ("ds-39-date-picker.html",  "Date Picker"),
    ("ds-17-dialogs.html",      "Dialog"),
    ("ds-18-divider.html",      "Divider"),
    ("ds-40-drawer.html",       "Drawer"),
    ("ds-41-dropdown.html",     "Dropdown Menu"),
    ("ds-42-empty-state.html",  "Empty State"),
    ("ds-43-hover-card.html",   "Hover Card"),
    ("ds-44-input-otp.html",    "Input OTP"),
    ("ds-45-kbd.html",          "Kbd"),
    ("ds-46-label.html",        "Label"),
    ("ds-19-lists.html",        "Lists"),
    ("ds-20-progress.html",     "Loading & Progress"),
    ("ds-47-menubar.html",      "Menubar"),
    ("ds-21-menus.html",        "Menus"),
    ("ds-07-navigation.html",   "Navigation"),
    ("ds-48-pagination.html",   "Pagination"),
    ("ds-49-popover.html",      "Popover"),
    ("ds-22-radio.html",        "Radio Group"),
    ("ds-50-resizable.html",    "Resizable"),
    ("ds-51-scroll-area.html",  "Scroll Area"),
    ("ds-52-select.html",       "Select"),
    ("ds-53-sheet.html",        "Sheet"),
    ("ds-54-skeleton.html",     "Skeleton"),
    ("ds-23-sliders.html",      "Slider"),
    ("ds-24-snackbar.html",     "Snackbar"),
    ("ds-55-spinner.html",      "Spinner"),
    ("ds-12-switches.html",     "Switch"),
    ("ds-11-tabs.html",         "Tabs"),
    ("ds-08-textfields.html",   "Text Fields"),
    ("ds-56-textarea.html",     "Textarea"),
    ("ds-57-toggle.html",       "Toggle"),
    ("ds-58-toggle-group.html", "Toggle Group"),
    ("ds-25-tooltips.html",     "Tooltip"),
]

def make_bottom_nav(idx):
    prev_btn = ''
    next_btn = ''
    if idx > 0:
        pf, pn = PAGES[idx - 1]
        prev_btn = f'<a class="ds-page-nav-btn prev" href="{pf}">\n      <span class="ds-page-nav-label">← Previous</span>\n      <span class="ds-page-nav-name">{pn}</span>\n    </a>'
    else:
        prev_btn = '<span></span>'
    if idx < len(PAGES) - 1:
        nf, nn = PAGES[idx + 1]
        next_btn = f'<a class="ds-page-nav-btn next" href="{nf}">\n      <span class="ds-page-nav-label">Next →</span>\n      <span class="ds-page-nav-name">{nn}</span>\n    </a>'
    else:
        next_btn = '<span></span>'
    return (
        '\n    <!-- ── Prev / Next navigation ── -->\n'
        '    <div class="ds-page-nav">\n'
        f'    {prev_btn}\n'
        f'    {next_btn}\n'
        '    </div>'
    )

def make_title_actions(idx):
    prev_href = f'href="{PAGES[idx-1][0]}"' if idx > 0 else ''
    next_href = f'href="{PAGES[idx+1][0]}"' if idx < len(PAGES)-1 else ''
    prev_btn = (f'<a class="ds-nav-arrow-btn" {prev_href} title="Previous"><span class="material-icons-round">arrow_back</span></a>'
                if idx > 0 else
                '<span class="ds-nav-arrow-btn disabled"><span class="material-icons-round">arrow_back</span></span>')
    next_btn = (f'<a class="ds-nav-arrow-btn" {next_href} title="Next"><span class="material-icons-round">arrow_forward</span></a>'
                if idx < len(PAGES)-1 else
                '<span class="ds-nav-arrow-btn disabled"><span class="material-icons-round">arrow_forward</span></span>')
    return (
        '    <div class="ds-title-actions">\n'
        '      <button class="ds-copy-page-btn" onclick="copyPageLink()">\n'
        '        <span class="material-icons-round">content_copy</span> Copy Page\n'
        '        <span class="material-icons-round chevron">expand_more</span>\n'
        '      </button>\n'
        f'      {prev_btn}\n'
        f'      {next_btn}\n'
        '    </div>'
    )

COPY_JS = '''
function copyPageLink() {
  const url = window.location.href.split('?')[0];
  navigator.clipboard.writeText(url).then(() => {
    const btn = document.querySelector('.ds-copy-page-btn');
    if (btn) {
      const orig = btn.innerHTML;
      btn.innerHTML = '<span class="material-icons-round">check</span> Copied!';
      setTimeout(() => { btn.innerHTML = orig; }, 1800);
    }
  });
}'''

def process_file(fpath, idx):
    with open(fpath, encoding='utf-8') as f:
        html = f.read()

    # ── Strip ALL existing ds-page-nav blocks (any format) ──
    html = re.sub(r'\s*<!--[^>]*[Pp]rev[^>]*-->\s*<div class="ds-page-nav">.*?</div>\s*',
                  '', html, flags=re.DOTALL)
    # Also strip any bare ds-page-nav (no comment)
    html = re.sub(r'\s*<div class="ds-page-nav">.*?</div>\s*', '\n', html, flags=re.DOTALL)

    # ── Strip existing ds-title-row wrappers (unfold cleanly) ──
    # Remove opening tag and its ds-title-actions sibling, keep h1
    html = re.sub(r'<div class="ds-title-row">\s*', '', html)
    html = re.sub(r'\s*<div class="ds-title-actions">.*?</div>\s*</div>', '', html, flags=re.DOTALL)

    # ── Wrap h1 in title-row ──
    h1_pat = re.compile(r'(<h1 class="ds-page-title">.*?</h1>)', re.DOTALL)
    m = h1_pat.search(html)
    if m:
        old = m.group(1)
        actions = make_title_actions(idx)
        new = f'<div class="ds-title-row">\n    {old}\n{actions}\n  </div>'
        html = html[:m.start()] + new + html[m.end():]

    # ── Insert bottom nav before </div>\n</main> ──
    # Find the last </div> before </main>
    bottom_nav = make_bottom_nav(idx)
    if '</main>' in html:
        # Insert just before the closing </div></main> sequence
        html = re.sub(r'(\s*</div>\s*</main>)',
                      lambda m2: bottom_nav + '\n\n  </div>\n</main>',
                      html, count=1, flags=re.DOTALL)
        # Only replace the last occurrence
        # Better approach:

    # ── Ensure copyPageLink JS ──
    if 'copyPageLink' not in html:
        html = html.replace('</script>\n</body>', COPY_JS + '\n</script>\n</body>')
        html = html.replace('</script></body>', COPY_JS + '\n</script></body>')

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)

def process_file_v2(fpath, idx):
    """Cleaner two-pass: strip → rebuild."""
    with open(fpath, encoding='utf-8') as f:
        html = f.read()

    # ── Pass 1: strip any existing ds-page-nav ──
    html = re.sub(r'[ \t]*<!--[^\n]*[Pp]rev[^\n]*-->\n[ \t]*<div class="ds-page-nav">.*?</div>',
                  '', html, flags=re.DOTALL)
    html = re.sub(r'[ \t]*<div class="ds-page-nav">.*?</div>',
                  '', html, flags=re.DOTALL)

    # ── Pass 2: strip existing ds-title-row (remove wrapper, keep h1) ──
    # Pattern: <div class="ds-title-row">\n    <h1 ...>TITLE</h1>\n    <div class="ds-title-actions">...</div>\n  </div>
    def restore_h1(m):
        # Extract just the h1
        h1 = re.search(r'<h1 class="ds-page-title">.*?</h1>', m.group(0), re.DOTALL)
        return h1.group(0) if h1 else ''
    html = re.sub(r'<div class="ds-title-row">.*?</div>\s*</div>',
                  restore_h1, html, flags=re.DOTALL)

    # ── Pass 3: wrap h1 in new title-row ──
    h1_pat = re.compile(r'(<h1 class="ds-page-title">.*?</h1>)', re.DOTALL)
    m = h1_pat.search(html)
    if m:
        actions = make_title_actions(idx)
        new = f'<div class="ds-title-row">\n    {m.group(1)}\n{actions}\n  </div>'
        html = html[:m.start()] + new + html[m.end():]

    # ── Pass 4: insert bottom nav ──
    bottom_nav = make_bottom_nav(idx)
    # Find last </div>\n</main> and insert before it
    pos = html.rfind('</div>')
    if '</main>' in html:
        main_pos = html.rfind('</main>')
        # Find the </div> closest before </main>
        chunk = html[:main_pos]
        last_div = chunk.rfind('</div>')
        if last_div != -1:
            html = html[:last_div] + bottom_nav + '\n\n  ' + html[last_div:]

    # ── Pass 5: ensure copyPageLink JS ──
    if 'copyPageLink' not in html:
        for marker in ['</script>\n</body>', '</script></body>']:
            if marker in html:
                html = html.replace(marker, COPY_JS + '\n' + marker, 1)
                break

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)

updated = 0
skipped = 0
for idx, (fn, name) in enumerate(PAGES):
    fpath = os.path.join(BASE, fn)
    if not os.path.exists(fpath):
        print(f'  MISSING: {fn}')
        skipped += 1
        continue
    process_file_v2(fpath, idx)
    print(f'  ✓  [{idx:02d}] {fn}')
    updated += 1

print(f'\nDone. {updated} updated, {skipped} missing.')
