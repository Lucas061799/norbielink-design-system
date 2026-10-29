/* ═══════════════════════════════════════════════════
   NORBIELINK DESIGN SYSTEM — Shared JavaScript
   • TOC smooth scroll + active highlight
   • Search overlay
   • Dark mode toggle
   ═══════════════════════════════════════════════════ */

/* ─── SEARCH INDEX ─── */
const DS_SEARCH_INDEX = [
  // Foundations
  { title: 'Color',            section: 'Foundations', href: 'ds-01-color.html',      icon: 'palette' },
  { title: 'Typography',       section: 'Foundations', href: 'ds-02-typography.html', icon: 'text_fields' },
  { title: 'Elevation',        section: 'Foundations', href: 'ds-03-elevation.html',  icon: 'flip_to_front' },
  { title: 'Shape',            section: 'Foundations', href: 'ds-04-shape.html',       icon: 'rounded_corner' },
  { title: 'Spacing',          section: 'Foundations', href: 'ds-05-spacing.html',     icon: 'space_bar' },
  // Components
  { title: 'Buttons',          section: 'Components',  href: 'ds-06-buttons.html',     icon: 'smart_button' },
  { title: 'Navigation',       section: 'Components',  href: 'ds-07-navigation.html',  icon: 'menu' },
  { title: 'Text Fields',      section: 'Components',  href: 'ds-08-textfields.html',  icon: 'text_fields' },
  { title: 'Badges',           section: 'Components',  href: 'ds-09-badges.html',      icon: 'new_releases' },
  { title: 'Tabs',             section: 'Components',  href: 'ds-11-tabs.html',        icon: 'tab' },
  { title: 'Switches',         section: 'Components',  href: 'ds-12-switches.html',    icon: 'toggle_on' },
  { title: 'Cards',            section: 'Components',  href: 'ds-10-cards.html',               icon: 'dashboard' },
  { title: 'Checkbox',         section: 'Components',  href: 'ds-15-checkbox.html',    icon: 'check_box' },
  { title: 'Chart',            section: 'Components',  href: 'ds-34-chart.html',               icon: 'bar_chart' },
  { title: 'Chips',            section: 'Components',  href: 'ds-16-chips.html',       icon: 'label' },
  { title: 'Dialogs',          section: 'Components',  href: 'ds-17-dialogs.html',     icon: 'open_in_new' },
  { title: 'Divider',          section: 'Components',  href: 'ds-18-divider.html',     icon: 'horizontal_rule' },
  { title: 'Lists',            section: 'Components',  href: 'ds-19-lists.html',       icon: 'list' },
  { title: 'Progress',         section: 'Components',  href: 'ds-20-progress.html',    icon: 'hourglass_empty' },
  { title: 'Menus',            section: 'Components',  href: 'ds-21-menus.html',       icon: 'menu_open' },
  { title: 'Radio Button',     section: 'Components',  href: 'ds-22-radio.html',       icon: 'radio_button_checked' },
  { title: 'Sliders',          section: 'Components',  href: 'ds-23-sliders.html',     icon: 'linear_scale' },
  { title: 'Snackbar',         section: 'Components',  href: 'ds-24-snackbar.html',    icon: 'notifications' },
  { title: 'Tooltips',         section: 'Components',  href: 'ds-25-tooltips.html',    icon: 'tips_and_updates' },
  { title: 'Accordion',        section: 'Components',  href: 'ds-26-accordion.html',   icon: 'expand_more' },
  { title: 'Alert',            section: 'Components',  href: 'ds-27-alert.html',       icon: 'warning_amber' },
  { title: 'Alert Dialog',     section: 'Components',  href: 'ds-28-alert-dialog.html',icon: 'report_problem' },
  { title: 'App Bars',         section: 'Components',  href: 'ds-14-appbar.html',              icon: 'web_asset' },
  { title: 'Avatar',           section: 'Components',  href: 'ds-29-avatar.html',      icon: 'account_circle' },
  { title: 'Breadcrumb',       section: 'Components',  href: 'ds-30-breadcrumb.html',  icon: 'chevron_right' },
  { title: 'Button Group',     section: 'Components',  href: 'ds-31-button-group.html',icon: 'view_column' },
  { title: 'Calendar',         section: 'Components',  href: 'ds-32-calendar.html',    icon: 'calendar_today' },
  { title: 'Carousel',         section: 'Components',  href: 'ds-33-carousel.html',    icon: 'view_carousel' },
  { title: 'Collapsible',      section: 'Components',  href: 'ds-35-collapsible.html', icon: 'unfold_more' },
  { title: 'Combobox',         section: 'Components',  href: 'ds-36-combobox.html',    icon: 'arrow_drop_down' },
  { title: 'Context Menu',     section: 'Components',  href: 'ds-38-context-menu.html',icon: 'more_vert' },
  { title: 'Date Picker',      section: 'Components',  href: 'ds-39-date-picker.html', icon: 'event' },
  { title: 'Drawer',           section: 'Components',  href: 'ds-40-drawer.html',      icon: 'menu_open' },
  { title: 'Dropdown',         section: 'Components',  href: 'ds-41-dropdown.html',    icon: 'arrow_drop_down_circle' },
  { title: 'Empty State',      section: 'Components',  href: 'ds-42-empty-state.html', icon: 'inbox' },
  { title: 'Hover Card',       section: 'Components',  href: 'ds-43-hover-card.html',          icon: 'ads_click' },
  { title: 'Input OTP',        section: 'Components',  href: 'ds-44-input-otp.html',   icon: 'pin' },
  { title: 'Label',            section: 'Components',  href: 'ds-46-label.html',       icon: 'label_outline' },
  { title: 'Menubar',          section: 'Components',  href: 'ds-47-menubar.html',     icon: 'menu' },
  { title: 'Pagination',       section: 'Components',  href: 'ds-48-pagination.html',  icon: 'last_page' },
  { title: 'Popover',          section: 'Components',  href: 'ds-49-popover.html',     icon: 'chat_bubble_outline' },
  { title: 'Resizable',        section: 'Components',  href: 'ds-50-resizable.html',   icon: 'open_with' },
  { title: 'Scroll Area',      section: 'Components',  href: 'ds-51-scroll-area.html', icon: 'swap_vert' },
  { title: 'Select',           section: 'Components',  href: 'ds-52-select.html',      icon: 'arrow_drop_down' },
  { title: 'Sheet',            section: 'Components',  href: 'ds-53-sheet.html',       icon: 'table_rows' },
  { title: 'Skeleton',         section: 'Components',  href: 'ds-54-skeleton.html',    icon: 'crop_landscape' },
  { title: 'Spinner',          section: 'Components',  href: 'ds-55-spinner.html',     icon: 'autorenew' },
  { title: 'Textarea',         section: 'Components',  href: 'ds-56-textarea.html',    icon: 'notes' },
  { title: 'Toggle',           section: 'Components',  href: 'ds-57-toggle.html',      icon: 'toggle_off' },
  // Resources
  { title: 'Norbielink Logo',  section: 'Resources',   href: 'ds-brand-norbielink-logo.html', icon: 'auto_awesome' },
  { title: 'BTIS Logo',        section: 'Resources',   href: 'ds-brand-logo.html',            icon: 'workspace_premium' },
  { title: 'Brand Characters', section: 'Resources',   href: 'ds-brand-characters.html',      icon: 'emoji_emotions' },
  { title: 'Visual Elements',  section: 'Resources',   href: 'ds-brand-visual-elements.html', icon: 'category' },
];

/* ─── SEARCH ─── */
let focusedIndex = -1;

function openSearch() {
  const overlay = document.getElementById('search-overlay');
  if (!overlay) return;
  overlay.classList.add('open');
  setTimeout(() => document.getElementById('search-input').focus(), 50);
  renderResults('');
}
function toggleSearch() {
  const overlay = document.getElementById('search-overlay');
  if (!overlay) return;
  if (overlay.classList.contains('open')) closeSearch(); else openSearch();
}
function closeSearch() {
  const overlay = document.getElementById('search-overlay');
  if (overlay) overlay.classList.remove('open');
  focusedIndex = -1;
}
function renderResults(query) {
  const container = document.getElementById('search-results');
  if (!container) return;
  const q = query.trim().toLowerCase();
  const filtered = q
    ? DS_SEARCH_INDEX.filter(item =>
        item.title.toLowerCase().includes(q) ||
        item.section.toLowerCase().includes(q))
    : DS_SEARCH_INDEX;

  if (filtered.length === 0) {
    container.innerHTML = '<div class="search-empty">No results for "' + query + '"</div>';
    return;
  }
  focusedIndex = -1;
  container.innerHTML = filtered.map((item, i) => `
    <div class="search-result-item" data-href="${item.href}" onclick="goTo('${item.href}')">
      <div class="sri-icon"><span class="material-icons-round">${item.icon}</span></div>
      <div>
        <div class="search-result-title">${item.title}</div>
        <div class="search-result-section">${item.section}</div>
      </div>
      <span class="material-icons-round sri-arrow">arrow_forward</span>
    </div>`).join('');
}
function searchKeydown(e) {
  const items = document.querySelectorAll('.search-result-item');
  if (e.key === 'ArrowDown') {
    e.preventDefault();
    focusedIndex = Math.min(focusedIndex + 1, items.length - 1);
  } else if (e.key === 'ArrowUp') {
    e.preventDefault();
    focusedIndex = Math.max(focusedIndex - 1, 0);
  } else if (e.key === 'Enter') {
    if (focusedIndex >= 0 && items[focusedIndex]) {
      goTo(items[focusedIndex].dataset.href);
    } else if (items.length === 1) {
      goTo(items[0].dataset.href);
    }
    return;
  } else if (e.key === 'Escape') {
    closeSearch(); return;
  }
  items.forEach((el, i) => el.classList.toggle('focused', i === focusedIndex));
  if (items[focusedIndex]) items[focusedIndex].scrollIntoView({ block: 'nearest' });
}
function goTo(href) {
  window.location.href = href;
}

/* ─── DARK MODE ─── */
function applyLogoTheme(isDark) {
  const logos = document.querySelectorAll('.btis-logo-img');
  logos.forEach(el => { el.src = isDark ? 'BTIS_Darkmode_Logo.png' : 'BTIS.png'; });
}

/* Fix hardcoded inline white backgrounds and dark child text in dark mode */
const DARK_TEXT_COLORS = ['141F1E','141f1e','253835','3A4F4D','3a4f4d','536563','374151','1A1A2E','1a1a2e','1F2937','111827','1e293b','0f172a','#111','#222','#333','#444','#555','#666'];
function fixInlineWhiteBgs(isDark) {
  const bgSel = [
    '[style*="background:white"]','[style*="background: white"]',
    '[style*="background:#fff"]','[style*="background: #fff"]',
    '[style*="background:#FFF"]','[style*="background: #FFF"]',
    '[style*="background:#ffffff"]','[style*="background: #ffffff"]',
    '[style*="background-color:white"]','[style*="background-color: white"]',
    '[style*="background-color:#fff"]','[style*="background-color: #fff"]'
  ].join(',');
  const skipClasses = ['sw-thumb','ds-sl-t','btis-logo-img','dm-surf','dm-soft','dm-bdr'];
  // Only override border-color if it's a known light gray (preserve brand colors like #A614C3, #EF4444, etc.)
  const LIGHT_GRAY_BORDERS = ['#e5e7eb','#e0e0e0','#ddd','#eef2f0','#f3f4f6','#d1d5db','#f0f0f0','#ebebeb','#e8e8e8','#dce4e1'];
  if (isDark) {
    document.querySelectorAll(bgSel).forEach(el => {
      if (skipClasses.some(c => el.classList.contains(c))) return;
      // Also skip elements that have any dm-* class (explicit dark-mode handlers)
      if ([...el.classList].some(c => c.startsWith('dm-'))) return;
      el.dataset.origStyle = el.getAttribute('style');
      el.style.setProperty('background', '#1e1e22', 'important');
      // Smart border-color override: only override neutral grays, preserve brand colors
      const origStyle = (el.dataset.origStyle || '').toLowerCase();
      const hasLightGrayBorder = LIGHT_GRAY_BORDERS.some(g => origStyle.includes(g));
      const hasBrandBorder = /border[^;]*#(a614c3|5c2ed4|74c3b7|ef4444|10b981|f59e0b|3b82f6|dc2626|0a0a0a|111)/i.test(origStyle);
      if (hasLightGrayBorder && !hasBrandBorder) {
        el.style.setProperty('border-color', 'rgba(255,255,255,0.08)', 'important');
      }
      fixDarkTextEl(el, isDark);
      el.querySelectorAll('[style]').forEach(child => fixDarkTextEl(child, isDark));
    });
  } else {
    document.querySelectorAll('[data-orig-style]').forEach(el => {
      el.setAttribute('style', el.dataset.origStyle);
      delete el.dataset.origStyle;
      el.querySelectorAll('[data-orig-color]').forEach(child => {
        child.style.color = child.dataset.origColor;
        delete child.dataset.origColor;
      });
    });
    document.querySelectorAll('[data-orig-color]').forEach(child => {
      child.style.color = child.dataset.origColor;
      delete child.dataset.origColor;
    });
  }
}
function fixDarkTextEl(el, isDark) {
  if (!el.style.color) return;
  // Read raw inline attribute (browser normalizes el.style.color to rgb(...) which
  // doesn't match our hex-based DARK_TEXT_COLORS list)
  const rawStyle = (el.getAttribute('style') || '').toLowerCase();
  const computed = (el.style.color || '').toLowerCase();
  // Match against either the raw hex in the attribute OR known rgb() equivalents
  const RGB_DARKS = ['rgb(26, 26, 46)','rgb(20, 31, 30)','rgb(37, 56, 53)','rgb(58, 79, 77)','rgb(83, 101, 99)','rgb(55, 65, 81)','rgb(31, 41, 55)','rgb(17, 24, 39)','rgb(15, 23, 42)','rgb(30, 41, 59)'];
  const hexHit = DARK_TEXT_COLORS.some(dc => rawStyle.includes(dc.toLowerCase()));
  const rgbHit = RGB_DARKS.some(rgb => computed.includes(rgb));
  if (hexHit || rgbHit) {
    el.dataset.origColor = el.style.color;
    el.style.setProperty('color', 'rgba(255,255,255,0.78)', 'important');
  }
}

function toggleDarkMode() {
  const body = document.body;
  const icon = document.getElementById('darkModeIcon');
  const btn  = document.getElementById('darkModeBtn');
  body.classList.toggle('dark-mode');
  const isDark = body.classList.contains('dark-mode');
  if (icon) icon.textContent = isDark ? 'light_mode' : 'dark_mode';
  if (btn)  btn.classList.toggle('active', isDark);
  applyLogoTheme(isDark);
  fixInlineWhiteBgs(isDark);
  try { localStorage.setItem('ds-dark-mode', isDark ? '1' : '0'); } catch(e) {}
}

/* ─── TOC SCROLL + ACTIVE HIGHLIGHT ─── */
function toggleSidenavSection(btn) {
  const sec = btn.closest('.ds-sidenav-group');
  const open = sec.classList.toggle('open');
  btn.setAttribute('aria-expanded', open ? 'true' : 'false');
}

function initTOC() {
  const tocLinks = document.querySelectorAll('.ds-toc-item[href^="#"]');
  if (!tocLinks.length) return;

  // Smooth scroll
  tocLinks.forEach(link => {
    link.addEventListener('click', e => {
      const id = link.getAttribute('href').slice(1);
      const target = document.getElementById(id);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // IntersectionObserver — highlight active section
  const sectionIds = Array.from(tocLinks).map(l => l.getAttribute('href').slice(1));
  const sections   = sectionIds.map(id => document.getElementById(id)).filter(Boolean);
  if (!sections.length) return;

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.id;
        tocLinks.forEach(l => l.classList.toggle('active', l.getAttribute('href') === '#' + id));
      }
    });
  }, { rootMargin: '-10% 0px -70% 0px', threshold: 0 });

  sections.forEach(s => observer.observe(s));
}

/* ─── RESTORE DARK MODE ─── */
function restoreDarkMode() {
  try {
    const isDark = localStorage.getItem('ds-dark-mode') === '1';
    if (isDark) {
      document.body.classList.add('dark-mode');
      const icon = document.getElementById('darkModeIcon');
      const btn  = document.getElementById('darkModeBtn');
      if (icon) icon.textContent = 'light_mode';
      if (btn)  btn.classList.add('active');
    }
    applyLogoTheme(isDark);
    if (isDark) fixInlineWhiteBgs(true);
  } catch(e) {}
}

/* ─── KEYBOARD SHORTCUT: Cmd/Ctrl+K ─── */
document.addEventListener('keydown', e => {
  if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
    e.preventDefault();
    openSearch();
  }
  if (e.key === 'Escape') closeMobileMenu();
});

/* ─── MOBILE MENU ─── */
function openMobileMenu() {
  document.querySelector('.btis-mobile-backdrop')?.classList.add('open');
  document.getElementById('btis-mobile-drawer')?.classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closeMobileMenu() {
  document.querySelector('.btis-mobile-backdrop')?.classList.remove('open');
  document.getElementById('btis-mobile-drawer')?.classList.remove('open');
  document.body.style.overflow = '';
}

function initMobileMenu() {
  const headerInner = document.querySelector('.btis-header-inner');
  if (!headerInner) return;

  /* ── Hamburger button ── */
  const hamBtn = document.createElement('button');
  hamBtn.className = 'btis-ham-btn';
  hamBtn.setAttribute('aria-label', 'Open navigation menu');
  hamBtn.onclick = openMobileMenu;
  hamBtn.innerHTML = `<svg width="18" height="14" viewBox="0 0 18 14" fill="none">
    <rect width="18" height="2" rx="1" fill="currentColor"/>
    <rect y="6" width="14" height="2" rx="1" fill="currentColor"/>
    <rect y="12" width="18" height="2" rx="1" fill="currentColor"/>
  </svg>`;
  headerInner.insertBefore(hamBtn, headerInner.firstChild);

  /* ── Detect current page href ── */
  const currentHref = location.pathname.split('/').pop() || 'ds-00-home.html';

  /* ── Full nav structure: sections with all sub-pages ── */
  const NAV = [
    {
      label: 'Foundations', href: 'ds-nav-foundations.html',
      pages: [
        { label: 'Introduction', href: 'ds-00-home.html' },
        { label: 'Color',        href: 'ds-01-color.html' },
        { label: 'Typography',   href: 'ds-02-typography.html' },
        { label: 'Spacing',      href: 'ds-05-spacing.html' },
        { label: 'Shape',        href: 'ds-04-shape.html' },
        { label: 'Elevation',    href: 'ds-03-elevation.html' },
      ]
    },
    {
      label: 'Components', href: 'ds-nav-components.html',
      pages: [
        { label: 'Accordion',         href: 'ds-26-accordion.html' },
        { label: 'Alert',             href: 'ds-27-alert.html' },
        { label: 'Alert Dialog',      href: 'ds-28-alert-dialog.html' },
        { label: 'App Bars',             href: 'ds-14-appbar.html' },
        { label: 'Avatar',            href: 'ds-29-avatar.html' },
        { label: 'Badge',             href: 'ds-09-badges.html' },
        { label: 'Breadcrumb',        href: 'ds-30-breadcrumb.html' },
        { label: 'Button',            href: 'ds-06-buttons.html' },
        { label: 'Button Group',      href: 'ds-31-button-group.html' },
        { label: 'Calendar',          href: 'ds-32-calendar.html' },
        { label: 'Carousel',          href: 'ds-33-carousel.html' },
        { label: 'Cards',                href: 'ds-10-cards.html' },
        { label: 'Checkbox',          href: 'ds-15-checkbox.html' },
        { label: 'Chart',                href: 'ds-34-chart.html' },
        { label: 'Chips',             href: 'ds-16-chips.html' },
        { label: 'Collapsible',       href: 'ds-35-collapsible.html' },
        { label: 'Combobox',          href: 'ds-36-combobox.html' },
        { label: 'Context Menu',      href: 'ds-38-context-menu.html' },
        { label: 'Date Picker',       href: 'ds-39-date-picker.html' },
        { label: 'Dialog',            href: 'ds-17-dialogs.html' },
        { label: 'Divider',           href: 'ds-18-divider.html' },
        { label: 'Drawer',            href: 'ds-40-drawer.html' },
        { label: 'Dropdown Menu',     href: 'ds-41-dropdown.html' },
        { label: 'Empty State',       href: 'ds-42-empty-state.html' },
        { label: 'Hover Card',           href: 'ds-43-hover-card.html' },
        { label: 'Input OTP',         href: 'ds-44-input-otp.html' },
        { label: 'Label',             href: 'ds-46-label.html' },
        { label: 'Lists',             href: 'ds-19-lists.html' },
        { label: 'Loading & Progress',href: 'ds-20-progress.html' },
        { label: 'Menubar',           href: 'ds-47-menubar.html' },
        { label: 'Menus',             href: 'ds-21-menus.html' },
        { label: 'Navigation',        href: 'ds-07-navigation.html' },
        { label: 'Pagination',        href: 'ds-48-pagination.html' },
        { label: 'Popover',           href: 'ds-49-popover.html' },
        { label: 'Radio Group',       href: 'ds-22-radio.html' },
        { label: 'Resizable',         href: 'ds-50-resizable.html' },
        { label: 'Scroll Area',       href: 'ds-51-scroll-area.html' },
        { label: 'Select',            href: 'ds-52-select.html' },
        { label: 'Sheet',             href: 'ds-53-sheet.html' },
        { label: 'Skeleton',          href: 'ds-54-skeleton.html' },
        { label: 'Slider',            href: 'ds-23-sliders.html' },
        { label: 'Snackbar',          href: 'ds-24-snackbar.html' },
        { label: 'Spinner',           href: 'ds-55-spinner.html' },
        { label: 'Switch',            href: 'ds-12-switches.html' },
        { label: 'Tabs',              href: 'ds-11-tabs.html' },
        { label: 'Text Fields',       href: 'ds-08-textfields.html' },
        { label: 'Textarea',          href: 'ds-56-textarea.html' },
        { label: 'Toggle',            href: 'ds-57-toggle.html' },
        { label: 'Tooltip',           href: 'ds-25-tooltips.html' },
      ]
    },
    {
      label: 'Resources', href: 'ds-nav-resources.html',
      pages: [
        { label: 'Norbielink Logo',  href: 'ds-brand-norbielink-logo.html' },
        { label: 'BTIS Logo',        href: 'ds-brand-logo.html' },
        { label: 'Brand Characters', href: 'ds-brand-characters.html' },
        { label: 'Visual Elements',  href: 'ds-brand-visual-elements.html' },
      ]
    },
  ];

  /* ── Figure out which section is active ── */
  const activeTopLink = document.querySelector('.btis-top-nav-link.active');
  const activeSection = activeTopLink ? activeTopLink.textContent.trim() : '';

  /* ── Build section HTML with sub-pages ── */
  function buildSection(sec) {
    const isActive = sec.label === activeSection;
    const subLinks = sec.pages.map(p => {
      const isCurrentPage = p.href === currentHref;
      return `<a class="btis-mdr-sub${isCurrentPage ? ' active' : ''}" href="${p.href}">${p.label}</a>`;
    }).join('');

    const hasPages = sec.pages.length > 0;
    return `
      <div class="btis-mdr-sec${isActive ? ' open' : ''}">
        <div class="btis-mdr-sec-hd">
          <a class="btis-mdr-sec-link" href="${sec.href}">${sec.label}</a>
          ${hasPages ? `<button class="btis-mdr-toggle" aria-label="Toggle ${sec.label}" onclick="this.closest('.btis-mdr-sec').classList.toggle('open')">
            <svg class="btis-mdr-chevron" width="12" height="12" viewBox="0 0 12 12" fill="none">
              <path d="M3 4.5L6 7.5L9 4.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>` : ''}
        </div>
        ${hasPages ? `<div class="btis-mdr-sub-list">${subLinks}</div>` : ''}
      </div>`;
  }

  /* ── Drawer ── */
  const drawer = document.createElement('div');
  drawer.className = 'btis-mobile-drawer';
  drawer.id = 'btis-mobile-drawer';
  drawer.innerHTML = `
    <div class="btis-mdr-head">
      <a href="ds-00-home.html" style="display:flex;align-items:center;text-decoration:none;">
        <img class="btis-logo-img btis-mdr-logo" src="BTIS.png" style="height:24px;width:auto;" alt="NorbieLink">
      </a>
      <button class="btis-mdr-close" onclick="closeMobileMenu()" aria-label="Close menu">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
          <path d="M1 1l12 12M13 1L1 13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </button>
    </div>
    <div class="btis-mdr-body">
      ${NAV.map(buildSection).join('')}
    </div>`;
  document.body.appendChild(drawer);

  /* ── Backdrop ── */
  const backdrop = document.createElement('div');
  backdrop.className = 'btis-mobile-backdrop';
  backdrop.onclick = closeMobileMenu;
  document.body.appendChild(backdrop);
}

/* ─── FOOTER ─── */
function initFooter() {
  /* Don't double-inject */
  if (document.getElementById('btis-footer')) return;

  const footer = document.createElement('footer');
  footer.id = 'btis-footer';
  footer.innerHTML = `
    <div class="btis-footer-inner">
      <div class="btis-footer-left">
        <a href="ds-00-home.html" class="btis-footer-brand">
          <img class="btis-logo-img btis-footer-logo" src="BTIS.png" style="height:20px;width:auto;" alt="NorbieLink">
        </a>
        <span class="btis-footer-copy">© 2026 Norbielink. All rights reserved.</span>
      </div>
      <nav class="btis-footer-nav">
        <a class="btis-footer-link" href="ds-nav-foundations.html">Foundations</a>
        <a class="btis-footer-link" href="ds-nav-components.html">Components</a>
        <a class="btis-footer-link" href="ds-nav-resources.html">Resources</a>
      </nav>
    </div>`;

  /* Insert after .ds-shell or at end of body */
  const shell = document.querySelector('.ds-shell');
  if (shell) shell.after(footer);
  else document.body.appendChild(footer);
}

/* ─── INIT ─── */
(function init() {
  restoreDarkMode();
  initMobileMenu();
  initFooter();
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTOC);
  } else {
    initTOC();
  }
})();
