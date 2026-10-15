# Norbielink — Authoritative Style Spec

Transcribed from the live app at https://norbielink.vercel.app by reading
computed styles off the real DOM (Marketplace / Quotes / Agencies, light + dark)
and by reading the component source out of the shipped JS bundle.

**The product is the source of truth. Where this file and the DS disagree, the DS is wrong.**
Line-of-business apps (workers-comp, inlandmarine, gl-bop, con-gl, …) are NOT evidence.

Captured 2026-10-14.

---

## 1. Type

Only four weights exist. **800 and 900 do not appear anywhere.**

| Weight | Use |
|---|---|
| 400 | body, table cells, tab labels |
| 500 | nav items, secondary labels, status chips |
| 600 | buttons, badges, emphasis, card titles |
| 700 | KPI numbers, section headings (sparing — 6 occurrences site-wide) |

Sizes in use: `24, 22, 15, 13, 12.5, 12, 11.5, 11, 10, 9` px.
`13px` is the workhorse. Font is Montserrat throughout.

## 2. Colour

### Text
| Role | Light | Dark |
|---|---|---|
| Primary | `#1F2937` | `#F9FAFB` |
| Muted | `#6B7280` | `#8B8FA8` |
| Faint | `#9CA3AF` | `#8B8FA8` |
| Brand | `#A614C3` | `#C084FC` |
| Teal | `#73C9B7` | `#73C9B7` |

### Surface
| Role | Light | Dark |
|---|---|---|
| Page | `#FFFFFF` | `#0F1120` |
| Card | `#FFFFFF` | `#1E2240` |
| Raised / rail | `#F9FAFB` | `#191D35` |
| Recessed track | `#F3F4F6` | `rgba(255,255,255,0.05)` |

### Border
| | Light | Dark |
|---|---|---|
| Default | `1px #E5E7EB` | `1px rgba(255,255,255,0.12)` |
| Subtle | `1px #F3F4F6` | `1px rgba(255,255,255,0.04–0.08)` |
| Strong | `1.5px #D1D5DB` | `1.5px rgba(255,255,255,0.18)` |

### The product's own token names

The app's theme object names its colours. Use these, not DS inventions:

| Token | Light | Dark | Note |
|---|---|---|---|
| `razz` | `#A614C3` | `#A614C3` | **The name for the magenta.** Gradient ids in the bundle read `alert-razz-pending`. |
| `razzTintBg` | `rgba(168,85,247,0.08)` | `rgba(168,85,247,0.14)` | a violet tint, not razz itself |
| `softBg` / `softBorder` | `rgba(166,20,195,0.08)` / `0.22` | `0.14` / `0.30` | razz tints |
| `green` | `#73C9B7` | `#8FDBC9` | **named `green` in the theme although it reads teal** |
| `greenBg` / `greenBorder` | `rgba(115,201,183,0.14)` / `0.30` | `0.18` / `0.35` | |
| `amber` | `#B45309` | `#B45309` | amber **text**; `#F59E0B` is the fill |
| `amberBg` | `rgba(245,158,11,0.10)` | `rgba(245,158,11,0.15)` | |
| `bodyText` | `#4B5563` | `#C5CAD8` | between `text` and `muted` |
| `softDivider` | `#F3F4F6` | `rgba(255,255,255,0.05)` | |
| `helperBg` | `#F9FAFB` | `rgba(255,255,255,0.03)` | |

### Brand gradients
- Solid: `linear-gradient(90deg, #5C2ED4 0%, #A614C3 65%)`
- Tonal / text: `linear-gradient(88.54deg, #5C2ED4 0.1%, #A614C3 63.88%)`
- Dark text: `linear-gradient(88.54deg, #A855F7 0.1%, #D946EF 63.88%)`
- Dark page wash: `radial-gradient(171.32% 99.33% at 33.13% -9%, #282550 0%, #191735 55.82%, …)`

### Semantic colour — CORRECTED 2026-10-14

An earlier revision of this file claimed Norbielink has no semantic colour
system. **That was wrong.** It was based on a DOM sweep of three screens where
none of these states happened to be on screen. Reading the shipped bundle
reveals a complete status map in component `eP`:

| Status | Text | Fill |
|---|---|---|
| Active, Approved | `#73C9B7` | `rgba(115,201,183,0.10)` |
| Upcoming Renewal(s) | `#74C3B7` | `rgba(116,195,183,0.10)` |
| Pending, Pending/Action Req. | `#F59E0B` | `rgba(245,158,11,0.08)` |
| Declined, Cancelled | `#EF4444` | `rgba(239,68,68,0.08)` |
| Inactive, Expired | `#9CA3AF` / dark `#8B8FA8` | `#F3F4F6` / dark `rgba(255,255,255,0.06)` |
| Prospect | brand gradient text | 5% brand gradient wash |
| *(fallback)* | `#9CA3AF` | `#F3F4F6` |

**Positive state is TEAL, not green.** There is no green in the status system.
There is no blue, and no info state.

Other reds and ambers, each with a specific job:
- `#DC2626` — form-field validation only: `border-color:#DC2626`, `box-shadow:0 0 0 1px rgba(220,38,38,0.15)`, message `11px #DC2626`
- `#EF4444` — destructive confirm dialogs, delete items in menus, PDF file icon
- `#F59E0B` — the Pending status above, and the filled "starred" icon
- `#22C55E` — non-PDF file-type icon only (`rgba(34,197,94,0.10)` disc)

Activity-feed type colours (icon + 12% tint, decorative, not semantic):
`policy #74C3B7` · `quote #A78BFA` · `document #60A5FA` · `email #F59E0B` · `call #34D399` · `note #F97316`

Marketing tag colours on promo cards are content data, not UI tokens (e.g. `#3B82F6` on a "WEBINAR" tag).

### Colours that still DO NOT exist in Norbielink
The DS semantic four `#1D9E6B` `#E6A817` `#C0392B` `#2980B9`, the Tailwind green
`#10B981`, and `#4ECDC4` (the product's teal is `#73C9B7` / `#74C3B7`).

## 3. Shape

Radius scale, complete: `4px` `6px` `8px` `9px` `10px` `12px` `16px` `9999px`.
Nothing else appears — no `20px`, no fractional values.

| Radius | Used by |
|---|---|
| `4px` | checkbox |
| `6px` | status chip, segmented-control segment |
| `9px` | toast icon disc |
| `8px` | secondary button, toolbar button, filter track, alert action |
| `10px` | primary button |
| `12px` | card, alert banner, KPI tile |
| `16px` | large panel |
| `9999px` | badge, avatar, dot, filter pill, count pill |

## 4. Elevation

Norbielink is almost flat. Only two shadows occur:
- `0 1px 2px rgba(15,23,42,0.08)` — the raised segment of a segmented control
- a brand glow `rgba(166,20,195,0.4) 0 0 8px` on one focused control

Primary buttons have **no shadow**.

## 5. Icons

**0** elements use a filled icon font. 72 inline SVGs, **63 stroked**.
Icon language is 2px-stroke outlines on a 24 viewBox, round caps/joins.
Material Symbols Outlined (`FILL 0`) is the correct font substitute.

## 6. Components (verbatim from the app)

### Button — primary
`linear-gradient(90deg,#5C2ED4 0%,#A614C3 65%)` · white · `radius 10px` · `padding 9px 16px` · `13px/600` · **no shadow**

### Button — secondary
`#FFFFFF` / dark `#1E2240` · `1px #E5E7EB` / `rgba(255,255,255,.12)` · text `#1F2937` / `#F9FAFB` · `radius 8px` · `padding 6px 12px` · `12px/600`

### Segmented control (= Button Group = Toggle Group — ONE component)
Track `#F3F4F6` / `rgba(255,255,255,.05)`, `1px #E5E7EB` / `rgba(255,255,255,.06)`, `radius 8px`, `padding 4px`, `gap 4px`
Active segment `#FFFFFF` / `rgba(255,255,255,.10)`, `radius 6px`, `padding 4px 12px`, `12.5px/500`, shadow `0 1px 2px rgba(15,23,42,.08)` / `0 1px 2px rgba(0,0,0,.24)`
Inactive `#6B7280` / `#8B8FA8`, transparent

### Badge — pill
`radius 9999px` · `padding 3px 10px` · `11px/600` · `letter-spacing normal`
- PRO: transparent, `1px #74C3B7`, `#74C3B7`, `10px`, `padding 1px 6px`; dark = gradient border on `#1E2240`, text `#C084FC`
- NEW: solid brand gradient, white, `9px/700`, `letter-spacing .9px`, `padding 3px 8px`
- Brand: 5% gradient wash + gradient text; dark 20% wash, text `#A855F7→#D946EF`
- Teal: `rgba(115,201,183,.10)` + `#73C9B7`; dark `.22`

### Status chip
`radius 6px` · `padding 3px 8px` · `11px/500` · `gap 6px`
Chip always neutral: `#F9FAFB` / `#1F2937` / `1px #F3F4F6`; dark `rgba(255,255,255,.05)` / `#F9FAFB` / `1px rgba(255,255,255,.04)`
Dot `6×6` `9999px`, three colours only: `#73C9B7` done · `#A614C3` in-flight · `#9CA3AF` idle

### Checkbox
`16×16` · `radius 4px`
Unchecked: card bg, `1.5px #D1D5DB` / `rgba(255,255,255,.18)`
Checked: `linear-gradient(88.54deg,#5C2ED4,#A614C3)`, **no border**, tick `9×7` path `M1 3.5L3.5 6L8 1` stroke `#FFFFFF` width `1.8`

### Radio
`20×20` round · `2px` border · **transparent track**
Checked border `#8B3DD4` (dark `#A855F7`), unchecked `#D1D5DB` / `rgba(255,255,255,.18)`
Dot `10×10` brand gradient

### Avatar
`36×36` · `9999px` · `rgba(115,201,183,.10)` / dark `.18` · `2.5px #73C9B7` · initials `13px/600` gradient text `linear-gradient(135deg,#73C9B7 0%,#4FA897 100%)`

### Alert
ONE variant. `radius 12px` · `padding 16px` · `gap 12px` · `#F9FAFB` + `1px #E5E7EB`; dark `rgba(255,255,255,.04)` + `1px rgba(255,255,255,.12)`
Icon 20×20 stroked, gradient stroke · Title `13px/600` gradient text · Desc `12px` muted · optional action button, brand gradient, `radius 8px`, `padding 6px 12px`, `12px/600`

### Tab bar
Container `gap 4px`, `border-bottom 1px #E5E7EB`
Item `padding 12px 16px`, `13px/400`, `letter-spacing .01em`, muted; active `#A614C3` (dark `#fff`) + `2px` gradient underline
Optional count: `16×16` round, `rgba(166,20,195,.12)`

### Indicator icon
`18×18` round, icon `12×12`, trails a cell value at `gap 6px`, meaning via `title`
- New: `rgba(166,20,195,.10)` / dark `rgba(168,85,247,.32)`, gradient-filled glyph
- Dormant: `rgba(100,116,139,.12)` / dark `rgba(148,163,184,.30)`, `#64748B` / `#94A3B8`

### Status badge — tonal pill (component `eP`)
`inline-flex` · `radius 9999px` · `padding 3px 12px` · `11px/600` · `width fit-content`
Colour/fill from the status map above. `Prospect` is special-cased to the brand
gradient pill (5% wash + gradient text, `padding 3px 10px`).

This is a SECOND status component, distinct from the neutral chip + dot used in
the Quotes table. Both ship.

### Destructive confirm dialog
Overlay `rgba(0,0,0,0.4)` · panel `radius 16px` · `padding 24px` · `width 400px` · `shadow-2xl` · card bg
Icon disc `48×48` round, `rgba(239,68,68,0.10)`, icon `24×24` `#EF4444`
Title `17px/700`, `margin-bottom 4px` · Body `13px` muted, relaxed leading
Buttons right-aligned, `gap 12px`, both `padding 9px 17px` `radius 8px` `12px`
- Cancel: `1px #E5E7EB`, `#FFFFFF`, weight `400`
- Confirm: `#EF4444`, white, weight `600`

### Dropdown menu
`radius 12px` · `shadow-lg` · `min-width 180px` · `overflow hidden`
`#FFFFFF` / dark `#1E2240`, border `1px #E5E7EB` / `rgba(255,255,255,0.10)`
Item `padding 10px 14px` · `12px` · hover = theme hoverBg
**Items whose label contains "delete" render `#EF4444`.**

### Tooltip
**Does not exist as a component.** 54 native `title` attributes, 0 `role="tooltip"`,
0 Tooltip components in the bundle.

### Menubar
**Does not exist.** There is no File/Edit/View menu anywhere in the product.
