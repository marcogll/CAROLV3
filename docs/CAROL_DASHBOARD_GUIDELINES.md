# CAROL — Dashboard Design Guidelines

**System:** CAROL Assessment System v2  
**UI Framework:** Tabler v1.0.0-beta17  
**Authors:** M. Gallegos / F. Salazar

---

## 1. Design Philosophy

The CAROL dashboard serves plant managers, HR directors, and engineering leads who need to make fast, high-confidence decisions about workforce competency. The design must be:

- **Data-dense but scannable** — Show many candidates without overwhelming. Hierarchy through color and weight, not visual noise.
- **Action-oriented** — Every screen answers a question and offers a next step. No dead ends.
- **Trust-building** — Industrial context demands precision: exact scores, explicit thresholds, clear pass/fail. No ambiguity.
- **Mobile-aware** — Plant managers may check from phone during floor walks. Core KPIs must be readable at 360px width.

Aesthetic direction: **utilitarian precision**. Tabler's clean grid as the foundation. No decorative elements that don't carry information. Data is the decoration.

---

## 2. Color System

### 2.1 CAROL Brand Palette

```css
:root {
  /* Primary brand */
  --carol-navy:      #0D1B2A;   /* Page headers, nav background, hero sections */
  --carol-blue:      #1B4F72;   /* Advanced level badge, primary CTAs */
  --carol-teal:      #00B894;   /* Basic level badge, success states, pass indicators */
  --carol-amber:     #E67E22;   /* Medium level badge, warning states, training flags */

  /* Status */
  --carol-pass:      #00B894;   /* Passed assessments — same as teal */
  --carol-fail:      #C0392B;   /* Failed assessments */
  --carol-critical:  #C0392B;   /* Category score < 55% */
  --carol-weak:      #E67E22;   /* Category score 55–70% */
  --carol-ok:        #27AE60;   /* Category score 70–85% */
  --carol-strong:    #00B894;   /* Category score > 85% */

  /* Category colors (consistent across all charts) */
  --cat-machine:     #1B4F72;
  --cat-process:     #00B894;
  --cat-quality:     #E67E22;
  --cat-safety:      #C0392B;
  --cat-materials:   #8E44AD;
  --cat-efficiency:  #2980B9;
  --cat-waste:       #27AE60;
  --cat-mold:        #D35400;

  /* Neutral scale */
  --gray-50:   #f8fafc;
  --gray-100:  #f1f5f9;
  --gray-200:  #e2e8f0;
  --gray-300:  #cbd5e1;
  --gray-400:  #94a3b8;
  --gray-500:  #64748b;
  --gray-700:  #334155;
  --gray-900:  #0f172a;
}
```

### 2.2 Semantic Usage Rules

| Variable | Use | Never use for |
|----------|-----|---------------|
| `--carol-navy` | Page background, nav, card headers on hero | Body text color |
| `--carol-teal` | Pass badge, success toast, Básico level tag | Error states |
| `--carol-amber` | Medio level tag, warning, training-needed flag | Success states |
| `--carol-blue` | Avanzado level tag, primary buttons | Destructive actions |
| `--carol-fail` | Fail badge, critical category, alert background | Pass indicators |
| `--carol-critical` | Bar fill when cat pct < 55% | Anything passing |
| `--carol-weak` | Bar fill when cat pct 55–70% | Perfect scores |

### 2.3 Score → Color Mapping (Consistent Everywhere)

```
Score ≥ 85%  →  #00B894  (strong / teal)
70% – 84%    →  #27AE60  (ok / green)
55% – 69%    →  #E67E22  (weak / amber)
< 55%        →  #C0392B  (critical / red)
```

Apply this mapping identically in: heatmap cells, bar fills, badge backgrounds, donut arcs, table row highlights.

---

## 3. Typography

```css
/* Load via Google Fonts CDN */
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap');

:root {
  --font-body:    'IBM Plex Sans', system-ui, sans-serif;
  --font-mono:    'IBM Plex Mono', monospace;   /* Scores, IDs, percentages */
}
```

**Why IBM Plex Sans:** Industrial, legible at small sizes, has a mono variant for numeric data. Communicates precision without corporate blandness.

### 3.1 Type Scale

| Token | Size | Weight | Line Height | Use |
|-------|------|--------|------------|-----|
| `--text-xs` | 11px | 500 | 1.4 | Labels, chip text, table sub-labels |
| `--text-sm` | 13px | 400 | 1.5 | Table body, card body, description text |
| `--text-base` | 15px | 400 | 1.6 | Page body text |
| `--text-md` | 17px | 600 | 1.4 | Card titles, section headers |
| `--text-lg` | 21px | 700 | 1.3 | Page section titles |
| `--text-xl` | 28px | 800 | 1.2 | KPI numbers, hero scores |
| `--text-2xl` | 40px | 800 | 1.1 | Hero score on detail page |

### 3.2 Numeric Display Rule

All scores, percentages, and counts use `font-family: var(--font-mono)`. This creates visual distinction between data and labels and aligns numbers in columns without CSS tricks.

```css
.score-value,
.pct-value,
.count-value {
  font-family: var(--font-mono);
  font-weight: 600;
  font-variant-numeric: tabular-nums;
}
```

---

## 4. Spacing & Layout Grid

CAROL uses Tabler's 12-column grid. Key breakpoints:

| Breakpoint | Width | Columns | Use case |
|-----------|-------|---------|---------|
| Mobile | < 576px | 1 | KPI stacks, table scrolls |
| Tablet | 576–992px | 2 | Side-by-side KPIs |
| Desktop | 992–1400px | 12 | Full dashboard |
| Wide | > 1400px | 12 + max-width 1320px | No edge-to-edge stretch |

### 4.1 Spacing Tokens

```css
:root {
  --space-1:   4px;
  --space-2:   8px;
  --space-3:   12px;
  --space-4:   16px;
  --space-5:   20px;
  --space-6:   24px;
  --space-8:   32px;
  --space-10:  40px;
  --space-12:  48px;
}
```

### 4.2 Card Anatomy

All dashboard cards follow this internal structure:

```
┌─────────────────────────────────────────────────────┐
│ Card Header (padding: 16px 20px 12px)               │
│   Title [--text-md, 600]  ·  Optional subtitle      │
│   Optional: filter controls right-aligned            │
├─────────────────────────────────────────────────────┤
│ Card Body (padding: 0 20px 20px)                    │
│   Content — chart, table, list, etc.                │
│                                                     │
├─────────────────────────────────────────────────────┤
│ Card Footer (padding: 12px 20px)  [optional]        │
│   Secondary info · Links · Export button            │
└─────────────────────────────────────────────────────┘
```

Card border-radius: `8px`. Box-shadow: `0 1px 4px rgba(0,0,0,.06)`. No heavy drop shadows.

---

## 5. Component Specifications

### 5.1 KPI Card

Used in the hero row at the top of every page.

```
┌──────────────────────────────┐
│  Icon (24px, brand color)    │
│                              │
│  42                          │  ← --text-xl, mono, brand color
│  Candidates Assessed         │  ← --text-xs, gray-500, uppercase
│                              │
│  ▲ 8 vs last month           │  ← trend indicator (green/red)
└──────────────────────────────┘
```

**Tabler class base:** `card card-sm`  
**Do:** Use exactly 4 KPI cards per hero row.  
**Don't:** Add charts inside KPI cards — they are numbers only.

### 5.2 Level Badge

Always inline with candidate name or in the level column of tables.

```css
.badge-level-basic    { background: #d1fae5; color: #065f46; }
.badge-level-medium   { background: #fef3c7; color: #78350f; }
.badge-level-advanced { background: #dbeafe; color: #1e3a5f; }
```

Size: `font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 99px; text-transform: uppercase; letter-spacing: 0.05em;`

### 5.3 Pass/Fail Badge

```css
.badge-pass { background: #d1fae5; color: #065f46; }  /* ✓ APROBADO */
.badge-fail { background: #fee2e2; color: #991b1b; }  /* ✗ NO APROBÓ */
```

Same sizing as level badge. Always paired with score in tables.

### 5.4 Score Bar

Used in candidate detail view and category breakdown tables.

```
Label           ████████████░░░░░░░  72%
                ↑ color = score→color map
```

```css
.score-bar-track {
  height: 6px;
  background: var(--gray-100);
  border-radius: 99px;
  overflow: hidden;
}
.score-bar-fill {
  height: 100%;
  border-radius: 99px;
  transition: width 0.6s ease;
  /* color set via JS based on score value */
}
```

**Threshold line:** Draw a 1px vertical line at the pass threshold (75% or 80%) in `var(--carol-fail)`. Every score bar shows this line.

### 5.5 Category Heatmap

The most important data visualization in CAROL. Shows all candidates × all categories as a color grid.

**Structure:**

```
            Máq.  Proc.  Cal.  Seg.  Mat.  Efic.  Desp.
García J.   78%   56%   89%   100%  67%   72%    83%
López M.    91%   78%   67%   89%   55%   84%    76%
Pérez R.    45%   34%   56%   78%   43%   65%    54%
...
```

**Rendering rules:**
- Cell size: `min 40px × 36px`
- Cell background: score→color map (5 steps: critical / weak / ok / strong)
- Cell text: percentage value, mono font, white if bg is dark, dark gray if bg is light
- Row header: candidate name + level badge + overall score
- Column header: category abbreviation + category icon
- Hover state: tooltip with full category name, score, and correct/total

**Color thresholds for heatmap cells:**

| Score range | Background | Text |
|-------------|-----------|------|
| < 40% | `#7f1d1d` | `#fff` |
| 40–54% | `#C0392B` | `#fff` |
| 55–69% | `#E67E22` | `#fff` |
| 70–84% | `#27AE60` | `#fff` |
| ≥ 85% | `#00B894` | `#fff` |
| N/A | `#f1f5f9` | `#94a3b8` |

### 5.6 Candidate Table

Main data table. Tabler class: `table table-vcenter table-hover`.

**Column order:**

| Column | Width | Content |
|--------|-------|---------|
| Candidate | 200px | Avatar initials + Name + Employee ID (gray, small) |
| Level | 90px | Level badge |
| Score | 100px | Score bar + percentage (mono) |
| Status | 90px | Pass/Fail badge |
| Department | 120px | Text |
| Date | 100px | Relative time ("3 days ago") |
| Actions | 80px | View · PDF icons |

**Row states:**
- Default: white background
- Hover: `var(--gray-50)`
- Critical (score < 55%): left border `3px solid var(--carol-critical)`
- Selected: `background: #f0f9ff`

### 5.7 Navigation (Tabler Sidebar)

```
CAROL                                    ← logo, navy bg

  Overview                    ← active: teal left border
  Candidates              42
  Assessments
  Reports
  ─────────────
  Settings
  Help
```

**Sidebar width:** 240px collapsed, hidden on mobile (hamburger menu).  
**Active state:** `border-left: 3px solid var(--carol-teal); background: rgba(0,184,148,.08); color: var(--carol-teal);`  
**Badge on Candidates:** unread/new count, teal background.

---

## 6. Page Templates

### 6.1 Overview Page (Home Dashboard)

```
┌─ Nav ──────────────────────────────────────────────────────────────┐
│ CAROL Dashboard     Plant: ACME Monterrey     Jun 2025     [Export]│
└────────────────────────────────────────────────────────────────────┘

┌── KPI Row (4 cards) ───────────────────────────────────────────────┐
│ Total Assessed  │ Pass Rate   │ Avg Score   │ Pending Review        │
│ 142             │ 67%         │ 71.4%       │ 8                     │
└────────────────────────────────────────────────────────────────────┘

┌── Level Distribution (3 cards) ────────────────────────────────────┐
│ 🟢 Básico        │ 🟡 Medio        │ 🔵 Avanzado                   │
│ 58 candidates    │ 64 candidates   │ 20 candidates                  │
│ 72% pass rate    │ 61% pass rate   │ 55% pass rate                  │
│ [mini bar chart] │ [mini bar chart]│ [mini bar chart]               │
└────────────────────────────────────────────────────────────────────┘

┌── Heatmap: Team Competency ─────────────────────┐ ┌── Recent ────┐
│ Category heatmap — all departments              │ │ Activity     │
│ (scrollable, up to 20 rows visible)             │ │ feed         │
│                                                 │ │ (last 10)    │
└─────────────────────────────────────────────────┘ └──────────────┘

┌── Weakest Areas (ranked) ──────────────────────────────────────────┐
│ Category          Avg Score    Candidates < 70%    Action           │
│ Proceso de Iny.   58%          34 / 64             [View Training]  │
│ Materiales        61%          28 / 64             [View Training]  │
│ ...                                                                 │
└────────────────────────────────────────────────────────────────────┘
```

### 6.2 Candidates List Page

```
┌── Filters ─────────────────────────────────────────────────────────┐
│ [Search by name/ID]  [Level ▼]  [Department ▼]  [Pass/Fail ▼]      │
│ [Date range]                          Showing 142 candidates       │
└────────────────────────────────────────────────────────────────────┘

┌── Candidates Table ────────────────────────────────────────────────┐
│ Candidate          Level    Score          Status   Dept    Date    │
│ JG  Juan García    🟡 Medio  ████░ 72%   ✗ FAIL   Prod.  3d ago  │
│ ML  María López    🔵 Adv.   ██████ 88%  ✓ PASS   Eng.   1w ago  │
│ ...                                                                 │
└────────────────────────────────────────────────────────────────────┘
```

### 6.3 Candidate Detail Page

```
┌── Candidate Header ────────────────────────────────────────────────┐
│ [←]  Juan García · EMP-1234 · Técnico de Procesos · Producción     │
│      🟡 Nivel Medio · 72% · ✗ NO APROBÓ · June 1 2025            │
│      [Download PDF]  [Schedule Retake]                             │
└────────────────────────────────────────────────────────────────────┘

┌── Score Hero ──────────────────────────────────────────────────────┐
│  [Donut 72%]   54.5 / 76.0 pts   42/60 correct   47m 27s          │
│  Pass threshold: 75% (57 pts) — 2.5 pts short                      │
└────────────────────────────────────────────────────────────────────┘

┌── Category Breakdown ──────────────────────────────────────────────┐
│ Máquina e Inyectora      ███████░ 78%   7/9   ✓ OK               │
│ Seguridad Industrial      ████████ 89%  8/9   ✓ STRONG           │
│ Proceso de Inyección      ████░░░  56%   5/9   ⚠ DÉBIL           │
│ Materiales Plásticos      ███░░░░  44%   4/9   🔴 CRÍTICO        │
└────────────────────────────────────────────────────────────────────┘

┌── Wrong Questions (18) ────────────────────────────────────────────┐
│ [Grouped by category — collapsible]                                │
│ ▼ Proceso de Inyección (4 wrong)                                   │
│   proc_4 · ✗ Chosen: "Reduce backpressure" · ✓ Correct: "..."    │
│   💡 Reasoning shown inline                                        │
└────────────────────────────────────────────────────────────────────┘

┌── Training Plan ───────────────────────────────────────────────────┐
│ 🔴 CRÍTICO  Materiales Plásticos   2 weeks                         │
│    1. Taller amorfos vs semicristalinos (PP, ABS, PC, PA, POM)     │
│    2. Práctica de secado: temperatura, tiempo, punto de rocío      │
│    3. Identificación visual: degradado, húmedo, contaminado        │
│    KPI: Seleccionar condiciones de secado para 5 materiales ✓     │
│                                                                     │
│ ⚠ MEJORA   Proceso de Inyección    1 week                         │
│    ...                                                              │
└────────────────────────────────────────────────────────────────────┘
```

---

## 7. Data Visualization Standards

### 7.1 Chart Library

**Use:** Chart.js (already in Tabler CDN bundle) for standard charts.  
**Use:** Custom CSS + HTML for heatmaps and score bars (more control, lighter).  
**Avoid:** D3.js (too heavy for this use case), Highcharts (licensing).

### 7.2 Chart Type Selection

| Data type | Chart | Notes |
|-----------|-------|-------|
| Single candidate, all categories | Horizontal bar chart | Category on Y, score on X |
| All candidates, all categories | Heatmap (CSS grid) | Color = score |
| Pass rate over time | Line chart | One line per level |
| Level distribution | Doughnut chart | 3 segments |
| Department comparison | Grouped bar chart | Category × department |
| Score distribution | Histogram | Bucket by 10% intervals |

### 7.3 Chart Defaults

```javascript
// Chart.js global defaults for CAROL
Chart.defaults.font.family = "'IBM Plex Sans', system-ui, sans-serif";
Chart.defaults.font.size = 12;
Chart.defaults.color = '#64748b';
Chart.defaults.plugins.legend.display = false; // Use custom legends
Chart.defaults.animation.duration = 600;
Chart.defaults.plugins.tooltip.backgroundColor = '#0D1B2A';
Chart.defaults.plugins.tooltip.titleColor = '#fff';
Chart.defaults.plugins.tooltip.bodyColor = '#94a3b8';
Chart.defaults.plugins.tooltip.padding = 10;
Chart.defaults.plugins.tooltip.cornerRadius = 6;
```

### 7.4 Threshold Lines Rule

Every chart that shows scores **must** include a visual pass threshold line:

```javascript
// Add as annotation on all score charts
{
  type: 'line',
  yMin: 75, yMax: 75,  // or 80 for advanced
  borderColor: 'rgba(192, 57, 43, 0.6)',
  borderWidth: 1.5,
  borderDash: [6, 3],
  label: {
    content: 'Mínimo 75%',
    enabled: true,
    font: { size: 10, weight: '600' }
  }
}
```

---

## 8. Interaction & Motion

### 8.1 Principles

- **Purposeful only.** Animate to communicate state change, not for decoration.
- **Fast.** Transitions: 150ms for hover, 250ms for panel open/close, 600ms for data load animations.
- **Respects `prefers-reduced-motion`.**

### 8.2 Standard Transitions

```css
/* Hover states */
.card { transition: box-shadow 150ms ease; }
.card:hover { box-shadow: 0 4px 16px rgba(0,0,0,.10); }

/* Table rows */
.table-hover tbody tr { transition: background 100ms ease; }

/* Score bar fill on load */
.score-bar-fill { transition: width 600ms cubic-bezier(0.4, 0, 0.2, 1); }
/* Set width to 0 in CSS, then JS sets actual width after DOM ready */

/* Heatmap cell hover */
.heatmap-cell {
  transition: transform 100ms ease, box-shadow 100ms ease;
}
.heatmap-cell:hover {
  transform: scale(1.08);
  box-shadow: 0 2px 8px rgba(0,0,0,.2);
  z-index: 2;
}
```

### 8.3 Loading States

```html
<!-- Skeleton loader for table rows while data loads -->
<tr class="placeholder-glow">
  <td><span class="placeholder col-6"></span></td>
  <td><span class="placeholder col-3"></span></td>
  <td><span class="placeholder col-4"></span></td>
</tr>
```

Never show spinners for operations < 300ms. Use skeleton screens for data tables, skeleton cards for KPIs.

---

## 9. Responsive Behavior

### 9.1 Navigation

| Breakpoint | Behavior |
|-----------|---------|
| Desktop (≥ 992px) | Sidebar always visible, 240px wide |
| Tablet (768–991px) | Sidebar collapses, icon-only mode (48px wide) |
| Mobile (< 768px) | Sidebar hidden, hamburger toggle, full-screen drawer |

### 9.2 KPI Row

| Breakpoint | Layout |
|-----------|--------|
| Desktop | 4 columns in one row |
| Tablet | 2 × 2 grid |
| Mobile | 1 column, stacked |

### 9.3 Heatmap

| Breakpoint | Behavior |
|-----------|---------|
| Desktop | Full heatmap visible |
| Tablet | Horizontal scroll, sticky candidate column |
| Mobile | Show top 4 categories only, "View all" toggle |

### 9.4 Tables

On mobile, candidate tables collapse to card view:

```
┌────────────────────────────────┐
│ JG  Juan García    EMP-1234   │
│     🟡 Nivel Medio             │
│     72% · ✗ NO APROBÓ        │
│     Producción · June 1       │
│     [View] [PDF]              │
└────────────────────────────────┘
```

---

## 10. Accessibility

| Requirement | Implementation |
|------------|---------------|
| Color contrast | All text ≥ 4.5:1 on background. Score cells: always white text on colored bg. |
| Score meaning | Never convey pass/fail via color alone. Always pair with ✓/✗ icon + text label. |
| Heatmap | Each cell has `aria-label="Category: Process — 56% (5 of 9 correct)"` |
| Tables | `<th scope="col">` and `<th scope="row">` for all headers |
| Focus | All interactive elements have visible `:focus-visible` ring: `outline: 2px solid var(--carol-teal); outline-offset: 2px;` |
| Charts | Every chart has a text summary below it for screen readers |
| Language | `lang="es"` on root `<html>` element |

---

## 11. Tabler Integration Notes

### 11.1 Required Tabler Assets

```html
<!-- CSS -->
<link rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/@tabler/core@1.0.0-beta17/dist/css/tabler.min.css">

<!-- Icons -->
<link rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@2.44.0/tabler-icons.min.css">

<!-- JS (bottom of body) -->
<script src="https://cdn.jsdelivr.net/npm/@tabler/core@1.0.0-beta17/dist/js/tabler.min.js"></script>

<!-- Chart.js -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
```

### 11.2 CAROL Overrides

Load a `carol-overrides.css` after Tabler to apply brand colors:

```css
/* carol-overrides.css */

/* Navbar */
.navbar-dark { background: var(--carol-navy) !important; }

/* Sidebar active */
.nav-link.active {
  border-left: 3px solid var(--carol-teal);
  background: rgba(0, 184, 148, .08);
  color: var(--carol-teal) !important;
}

/* Primary buttons */
.btn-primary {
  background: var(--carol-navy);
  border-color: var(--carol-navy);
}
.btn-primary:hover {
  background: var(--carol-blue);
  border-color: var(--carol-blue);
}

/* Page header background */
.page-header { background: var(--carol-navy); color: #fff; }
.page-title { color: #fff; }
.page-pretitle { color: #94a3b8; }

/* Custom font */
body { font-family: 'IBM Plex Sans', system-ui, sans-serif; }
.text-mono { font-family: 'IBM Plex Mono', monospace; }
```

### 11.3 Tabler Components Used

| CAROL Component | Tabler Base |
|----------------|-------------|
| KPI cards | `card card-sm` |
| Candidate table | `table table-vcenter table-hover` |
| Level badges | `badge` |
| Pass/Fail badges | `badge` |
| Filter dropdowns | `dropdown` |
| Sidebar | `navbar-vertical` |
| Page headers | `page-header` |
| Alerts / toasts | `alert` + `toast` |
| Modals (detail view) | `modal` |
| Skeleton loaders | `placeholder placeholder-glow` |

---

## 12. Icon Usage

All icons from Tabler Icons (`ti ti-*`). Category → icon mapping:

| Category | Icon class |
|----------|-----------|
| Máquina e Inyectora | `ti-settings-cog` |
| Proceso de Inyección | `ti-activity` |
| Calidad y Defectos | `ti-microscope` |
| Seguridad Industrial | `ti-shield-check` |
| Materiales Plásticos | `ti-flask` |
| Eficiencia y Lean | `ti-trending-up` |
| Desperdicios (Muda) | `ti-trash-off` |
| Ingeniería de Moldes | `ti-tool` |

Status icons:

| State | Icon | Color |
|-------|------|-------|
| Passed | `ti-check-circle` | `var(--carol-pass)` |
| Failed | `ti-x-circle` | `var(--carol-fail)` |
| Critical | `ti-alert-triangle` | `var(--carol-critical)` |
| Pending | `ti-clock` | `var(--gray-400)` |
| Training needed | `ti-school` | `var(--carol-amber)` |
| Download PDF | `ti-file-type-pdf` | `var(--gray-500)` |
| Send email | `ti-send` | `var(--carol-teal)` |
| View candidate | `ti-eye` | `var(--gray-500)` |

---

## 13. Empty States

Every list/table view must have a designed empty state (not a blank screen):

```
┌─────────────────────────────────────────────┐
│                                             │
│          [ti-clipboard icon, 64px]          │
│                                             │
│        No hay evaluaciones aún              │
│                                             │
│  Cuando los candidatos completen su         │
│  evaluación, los resultados aparecerán      │
│  aquí automáticamente.                      │
│                                             │
│        [Invitar candidatos →]               │
│                                             │
└─────────────────────────────────────────────┘
```

Rules:
- Icon: 48–64px, `var(--gray-300)`
- Title: `--text-md`, `var(--gray-700)`
- Subtitle: `--text-sm`, `var(--gray-400)`, max 2 lines
- CTA button: only if there is a logical next action
