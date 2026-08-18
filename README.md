<p align="center">
  <a href="https://soul23.mx">
    <picture>
      <source
        media="(prefers-color-scheme: dark)"
        srcset="https://raw.githubusercontent.com/marcogll/mg_data_storage/refs/heads/main/soul23/logo/soul23_logo_wh.png">
      <source
        media="(prefers-color-scheme: light)"
        srcset="https://raw.githubusercontent.com/marcogll/mg_data_storage/refs/heads/main/soul23/logo/soul23_logo_blk.png">
      <img
        src="https://raw.githubusercontent.com/marcogll/mg_data_storage/refs/heads/main/soul23/logo/soul23_logo_blk.png"
        width="110"
        alt="Soul:23">
    </picture>
  </a>
</p>

<h1 align="center">CAROL — Assessment System</h1>

<p align="center">
  Technical skills evaluation platform for injection molding manufacturing companies with automated scoring and PDF reporting.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/HTML5-3a3a3a?style=flat-square&logo=html5&logoColor=white">
  <img src="https://img.shields.io/badge/Python-3a3a3a?style=flat-square&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Docker-3a3a3a?style=flat-square&logo=docker&logoColor=white">
  <img src="https://img.shields.io/badge/n8n-3a3a3a?style=flat-square&logo=n8n&logoColor=white">
</p>

---

## Description

CAROL is a domain-specific technical assessment system for injection molding plants. It replaces informal, subjective skill evaluations with a structured, data-driven process that produces objective competency scores, category-level diagnostics, and actionable development plans — automatically.

Three assessment levels (basic, medium, advanced) with 43–60 questions each, delivered through a self-contained HTML web app with routing logic. Results post to n8n workflows that grade answers, generate PDF reports with Python, and notify candidates and HR. No build step, no backend required for the quiz itself.

## What is CAROL?

CAROL is a domain-specific technical assessment system for injection molding plants. It replaces informal, subjective skill evaluations with a structured, data-driven process that produces objective competency scores, category-level diagnostics, and actionable development plans — automatically.

Think of it as a **technical TOEFL for injection molding**: a standardized test with routing logic, scored results, and a development roadmap — tailored to the realities of plastic processing on the plant floor.

---

## Repository Structure

```
carol/
│
├── assessments/
│   ├── carol_basic_prod.json        # 57 questions — Operadores de Piso
│   ├── carol_medium_prod.json       # 60 questions — Técnicos de Proceso
│   └── carol_advanced_prod.json     # 43 questions — Ingenieros y Líderes
│
├── registration/
│   └── carol_funnel_registration_v2.json   # Registration form schema + routing logic
│
├── web/
│   └── carol_platform.html          # Self-contained assessment web app
│
├── reports/
│   ├── carol_generate_report.py     # Per-level PDF report generator
│   └── carol_generate_unified_report.py  # Multi-level unified PDF
│
├── docs/
│   ├── README.md                    # This file
│   ├── CAROL_PRD.md                 # Full product requirements document
│   ├── CAROL_AGENTS.md              # Agent task definitions (n8n, AI, automation)
│   └── CAROL_DASHBOARD_GUIDELINES.md  # Tabler dashboard design system
│
└── quiz_docs/
    ├── carol_basic_quiz.md          # Basic level — full question bank with answers
    ├── carol_medium_quiz.md         # Medium level — full question bank with answers
    └── carol_advanced_quiz.md       # Advanced level — full question bank with answers
```

---

## Quick Start

### Option A — Run as standalone web app

1. Open `carol_platform.html` in any modern browser (Chrome, Firefox, Safari)
2. Select a level, complete registration, take the quiz
3. Results appear immediately with scores, category breakdown, and development plan
4. Configure your n8n webhook URL in the JavaScript:
   ```js
   // In carol_platform.html, find:
   S.webhookUrl = 'https://your-n8n-instance.com/webhook/carol-assessment';
   ```

### Option B — Use with Formbricks

1. Create a new Formbricks survey using the schema in `carol_funnel_registration_v2.json`
2. Map field types using the table in the PRD (Section 5.4)
3. Add a webhook under Settings → Integrations → Webhooks
4. Point it to your n8n Catch Webhook node

### Option C — Host on any static server

The `carol_platform.html` file is fully self-contained (HTML + CSS + JS + data embedded). Drop it on:
- GitHub Pages
- Netlify / Vercel (drag-and-drop)
- Any web server with HTTPS
- SharePoint / internal portal

No build step. No dependencies. No backend required for the quiz itself.

---

## Assessment Levels

### 🟢 Básico — Operadores de Piso

| Property | Value |
|----------|-------|
| Target audience | General operators, setup technicians (0–2 years experience) |
| Questions | 57 |
| Max score | 69.0 pts |
| Pass threshold | 75% (≥52 pts) |
| Estimated time | 50 minutes |
| Knowledge areas | 7 categories |

**Categories covered:**
- Máquina e Inyectora (14 questions)
- Proceso de Inyección (11 questions)
- Calidad y Defectos (10 questions)
- Desperdicios (Muda) (6 questions)
- Materiales Plásticos (6 questions)
- Eficiencia y Lean (5 questions)
- Seguridad Industrial (5 questions)

---

### 🟡 Medio — Técnicos de Proceso

| Property | Value |
|----------|-------|
| Target audience | Process technicians, production supervisors (2–6 years experience) |
| Questions | 60 |
| Max score | 76.0 pts |
| Pass threshold | 75% (≥57 pts) |
| Estimated time | 60 minutes |
| Knowledge areas | 7 categories |

**Categories covered (balanced distribution — 8–9 questions each):**
- Máquina e Inyectora (9 questions)
- Proceso de Inyección (9 questions)
- Calidad y Defectos (9 questions)
- Seguridad Industrial (9 questions)
- Materiales Plásticos (8 questions)
- Eficiencia y Lean (8 questions)
- Desperdicios (Muda) (8 questions)

---

### 🔵 Avanzado — Ingenieros y Líderes

| Property | Value |
|----------|-------|
| Target audience | Process engineers, mold engineers, technical leads (6+ years) |
| Questions | 43 |
| Max score | 52.5 pts |
| Pass threshold | 80% (≥42 pts) |
| Estimated time | 75 minutes |
| Knowledge areas | 8 categories (includes Mold Engineering) |

**Categories covered:**
- Proceso de Inyección (7 questions)
- Máquina e Inyectora (6 questions)
- Ingeniería de Moldes (5 questions)
- Calidad y Defectos (5 questions)
- Seguridad Industrial (5 questions)
- Materiales Plásticos (5 questions)
- Eficiencia y Lean (5 questions)
- Desperdicios (Muda) (5 questions)

---

## Question Format

Every question in the JSON follows this schema:

```json
{
  "id": "proc_4",
  "question_order_id": 12,
  "category": "Proceso de Inyección",
  "type": "Práctico",
  "description": "Context sentence explaining the concept being tested (shown above the question in the UI).",
  "question": "The actual question text?",
  "options": [
    "Option A",
    "Option B — correct answer",
    "Option C",
    "Option D"
  ],
  "correct_index": 1,
  "correct_answer": "Option B — correct answer",
  "reasoning": "Explanation of why B is correct and why A, C, D are wrong.",
  "score": 1.5
}
```

**Scoring:**
- `type: "Teórico"` → `score: 1.0`
- `type: "Práctico"` → `score: 1.5`

---

## Data Flow

```
Candidate
   │
   ▼
Registration Form (carol_platform.html or Formbricks)
   │  POST → n8n webhook
   ▼
n8n — Registration Workflow
   ├── Compute: age, assigned_level, self_eval_vs_role_delta
   ├── Save: candidate record (DB / Google Sheets / Airtable)
   └── Redirect: candidate to assessment URL
   │
   ▼
Assessment (carol_platform.html?level=medium)
   │  POST → n8n webhook
   ▼
n8n — Results Workflow
   ├── Grade answers, compute category breakdown
   ├── Generate PDF report (Python script via n8n Execute Command)
   ├── Send email: candidate + HR manager
   └── Update candidate record with results
   │
   ▼
Admin Dashboard (Tabler)
   └── Real-time view of all candidates, scores, team heatmaps
```

---

## n8n Integration

### Webhook: Registration
- **Trigger:** `POST /webhook/carol-registration`
- **Nodes:** HTTP Trigger → Function (compute fields) → Set (assign level) → DB Insert → Respond

### Webhook: Assessment Results
- **Trigger:** `POST /webhook/carol-results`
- **Nodes:** HTTP Trigger → Function (grade) → Execute Command (PDF) → Gmail/SMTP → DB Update

### Configuring the webhook URL

In `carol_platform.html`, locate and update:

```javascript
S.webhookUrl = 'https://your-n8n-instance.com/webhook/carol-assessment';
```

Or prompt the user for the URL via the "Enviar Resultados" button in the results screen.

---

## Reporting

### Auto-generated PDF Report

Run directly or triggered from n8n:

```bash
python3 carol_generate_report.py \
  --level medium \
  --output /reports/gallegos_2025-06.pdf \
  --seed 42
```

To pass real candidate data, replace the `candidate` dict and `generate_sample_results()` with your webhook payload.

### Unified Multi-Level Report

```bash
python3 carol_generate_unified_report.py \
  --output /reports/engineering_review_2025-06.pdf
```

Generates a single PDF covering all three levels — designed for engineering leads and HR directors.

---

## Design System

See `CAROL_DASHBOARD_GUIDELINES.md` for the full Tabler-based design system specification including:
- Color palette and CSS variables
- Typography scale
- Component patterns (cards, tables, heatmaps, charts)
- Layout grids
- Icon usage

---

## Terminology Reference

CAROL uses bilingual terminology to bridge English industry standards and Spanish plant-floor vocabulary.

| English | Spanish |
|---------|---------|
| Runner | Colada / Canal |
| Sprue | Bebedero / Colada principal |
| Gate | Compuerta / Entrada |
| Cushion | Cojín |
| Flash | Rebaba |
| Sink mark | Rechupado |
| Warpage | Pandeo / Alabeo |
| Short shot | Tiro corto |
| Weld line | Línea de soldadura / unión |
| Jetting | Efecto jet / Gusanito |
| Splay | Ráfagas |
| Regrind | Molienda / Material molido |
| Barrel | Barril / Cañón |
| Screw | Husillo / Tornillo |
| Check ring | Anillo de cierre / Válvula check |
| Nozzle | Boquilla |
| Platen | Platina |
| Ejector pin | Botador / Eyector |
| Back pressure | Contrapresión |
| Hold pressure | Presión de sostenimiento / Empaque |
| Switchover | Punto de transferencia / VPT |
| Hot runner | Colada caliente |
| Cold runner | Colada fría |

---

## Contributing

1. Question additions must follow the schema exactly (id, category, type, description, question, options\[4\], correct\_index, reasoning, score)
2. All new questions require: dual terminology where applicable, a context `description`, and a technically accurate `reasoning`
3. Category balance targets: Básico ≥5 per cat, Medio ≥8 per cat, Avanzado ≥5 per cat
4. Correct answers must be independently verified by a process engineer before merging

---

## License

Internal use — M. Gallegos / F. Salazar. Contact authors for licensing.
