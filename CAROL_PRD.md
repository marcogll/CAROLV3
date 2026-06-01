# CAROL — Product Requirements Document

**Version:** 2.0  
**Date:** June 2025  
**Authors:** M. Gallegos / F. Salazar  
**Status:** Active Development

---

## 1. Product Overview

### 1.1 What is CAROL?

CAROL (Competency Assessment & Reporting for Operations and Learning) is a technical skills assessment platform purpose-built for injection molding manufacturing companies. It enables HR, engineering leadership, and plant managers to objectively measure, track, and develop the technical capabilities of their workforce — from floor operators to senior engineers.

CAROL is not a generic LMS. It is a domain-specific assessment engine with curated question banks, automated routing, AI-generated development plans, and structured reporting — all centered on the technical realities of injection molding production.

### 1.2 Problem Statement

Injection molding companies face a consistent and costly talent gap:

- **No objective baseline.** Skills are assessed informally through observation or seniority, not measured competency.
- **Inconsistent training investment.** Training is often uniform across roles rather than targeted at real gaps.
- **No traceability.** There is no audit trail of who has been assessed, when, and at what level.
- **High cost of errors.** Operators and technicians with knowledge gaps produce scrap, create safety incidents, and reduce OEE — all measurable losses.
- **Promotion without validation.** Technicians are promoted to process engineers without confirming their technical depth.

CAROL solves this by providing a structured, repeatable, data-driven competency measurement system.

### 1.3 Vision

Every injection molding plant has a real-time, role-appropriate picture of workforce technical competency — and uses that data to drive targeted development, smarter promotions, and measurable reduction in quality and safety incidents.

---

## 2. Target Users

### 2.1 Primary Users (Assessment Takers)

| Role | Level | Experience |
|------|-------|-----------|
| Operador General | Básico | 0–2 years |
| Técnico de Montaje (Set-Up) | Básico | 0–2 years |
| Técnico de Procesos | Medio | 2–6 years |
| Supervisor de Producción | Medio | 2–6 years |
| Ingeniero de Procesos | Avanzado | 6+ years |
| Ingeniero de Moldes | Avanzado | 6+ years |
| Ingeniero de Calidad | Avanzado | 6+ years |

### 2.2 Secondary Users (Administrators & Viewers)

| Role | Needs |
|------|-------|
| HR Manager | Bulk results export, cohort comparisons, training ROI |
| Plant Manager / Director | Dashboard overview, team-level competency heatmap |
| Process Engineering Lead | Identify technical gaps before assigning critical projects |
| Training Coordinator | Generate and schedule targeted training plans |
| Quality Manager | Correlate assessment results with defect / OEE trends |

### 2.3 User Context

- Assessment takers are primarily Spanish-speaking, hourly or salaried manufacturing workers in Mexico.
- May have limited computer literacy — interface must be mobile-friendly, direct, and jargon-light.
- Administrators are bilingual (ES/EN) and may access from desktop.

---

## 3. Assessment Architecture

### 3.1 Three-Level System

```
┌─────────────────────────────────────────────────────────────┐
│                    CAROL ASSESSMENT LEVELS                   │
├──────────────┬──────────────────┬───────────────────────────┤
│   BÁSICO     │     MEDIO        │        AVANZADO           │
│              │                  │                           │
│ Operadores   │ Técnicos de      │ Ingenieros y              │
│ de Piso      │ Proceso          │ Líderes Técnicos          │
├──────────────┼──────────────────┼───────────────────────────┤
│ 57 preguntas │ 60 preguntas     │ 43 preguntas              │
│ 69.0 pts máx │ 76.0 pts máx     │ 52.5 pts máx              │
│ 75% aprobat. │ 75% aprobatorio  │ 80% aprobatorio           │
│ 50 min est.  │ 60 min estimado  │ 75 min estimado           │
└──────────────┴──────────────────┴───────────────────────────┘
```

### 3.2 Routing Logic

Level assignment is automatic based on three inputs: `job_role`, `years_experience`, and `self_evaluation` score.

```
IF job_role IN [operator, setup_tech]
   OR (years_experience < 2 AND self_evaluation < 40)
→ ASSIGN: Básico

IF job_role IN [process_tech, supervisor]
   OR (years_experience ≥ 2 AND years_experience < 6 AND self_evaluation 40–70)
→ ASSIGN: Medio

IF job_role IN [process_eng, mold_eng, quality_eng, plant_manager]
   OR (years_experience ≥ 6 AND self_evaluation > 70)
→ ASSIGN: Avanzado

OVERRIDE: IF self_evaluation < 35 → ASSIGN: Básico regardless of role
```

Tiebreaker: `self_evaluation` takes precedence when rules overlap.

### 3.3 Knowledge Areas (Categories)

| Category | Básico | Medio | Avanzado |
|----------|:------:|:-----:|:--------:|
| Máquina e Inyectora | 14 | 9 | 6 |
| Proceso de Inyección | 11 | 9 | 7 |
| Calidad y Defectos | 10 | 9 | 5 |
| Seguridad Industrial | 5 | 9 | 5 |
| Materiales Plásticos | 6 | 8 | 5 |
| Eficiencia y Lean | 5 | 8 | 5 |
| Desperdicios (Muda) | 6 | 8 | 5 |
| Ingeniería de Moldes | — | — | 5 |
| **Total** | **57** | **60** | **43** |

### 3.4 Scoring System

- **Teórico (Theoretical):** 1.0 point — conceptual knowledge
- **Práctico (Practical):** 1.5 points — applied diagnosis, calculation, or decision-making
- All questions: 4-option single-select (one correct answer)
- No negative marking
- Questions presented in category-grouped order

### 3.5 Question Quality Standards

Every question must have:
- A `description` field: 1–2 sentences of technical context explaining the concept being tested
- Dual terminology where applicable: e.g. "runner (colada / canal)", "sprue (bebedero / colada principal)"
- A `reasoning` field: explains WHY the correct answer is correct and why distractors are wrong
- Distractors that are plausible but technically incorrect (not absurd or obviously wrong)
- An `id` field with category prefix and sequence number (e.g. `mach_3`, `proc_11`)

---

## 4. Registration Funnel

### 4.1 Fields

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `full_name` | text | ✅ | Candidate identification |
| `employee_id` | text | ✅ | HR record linkage |
| `birth_year` | select (2010→1956) | ✅ | Age calculation for analytics |
| `birth_month` | select | ❌ | Exact age, cohort tracking |
| `department` | select | ✅ | Segmentation |
| `job_role` | select | ✅ | Level routing (HIGH weight) |
| `shift` | select | ❌ | Scheduling retakes |
| `years_experience` | number 0–50 | ✅ | Level routing (HIGH weight) |
| `machine_brands` | multi-select | ❌ | Contextual analytics |
| `materials_worked` | multi-select | ❌ | Contextual analytics |
| `has_scientific_molding` | boolean | ❌ | Training history |
| `has_loto_training` | boolean | ❌ | Safety baseline |
| `self_evaluation` | slider 0–100% | ✅ | Level routing (HIGH weight) |
| `confidence_area` | select | ❌ | Report personalization |
| `improvement_area` | select | ❌ | Training plan seeding |
| `learning_goal` | select | ❌ | Motivation tracking |

### 4.2 Computed Fields (n8n / backend)

| Field | Formula |
|-------|---------|
| `age_at_assessment` | `current_year - birth_year` |
| `exact_age` | Computed when `birth_month` present |
| `generation_cohort` | Baby Boomer / Gen X / Millennial / Gen Z |
| `experience_vs_age_ratio` | `years_experience / age_at_assessment` — flags anomalies |
| `assigned_level` | Output of routing logic |
| `self_eval_vs_role_delta` | Self-score minus role baseline — detects over/under-confidence |

---

## 5. Data Flow & Integration

### 5.1 System Architecture

```
[Web App / Formbricks]
        │
        ▼ POST /webhook/carol-registration
[n8n Workflow — Registration]
        │
        ├── Compute age, assigned_level, delta fields
        ├── Store candidate in DB / sheet
        └── Serve assessment URL with level param
        
[Assessment Web App — carol_platform.html]
        │
        ▼ POST /webhook/carol-results
[n8n Workflow — Results]
        │
        ├── Grade answers
        ├── Generate PDF report (Python script)
        ├── Send report via email
        └── Update candidate record
```

### 5.2 Webhook Payload — Registration

```json
{
  "survey_id": "carol_registration_v2",
  "submitted_at": "2025-06-01T10:32:00Z",
  "respondent": {
    "full_name": "Juan García",
    "employee_id": "EMP-1234",
    "birth_year": "1990",
    "birth_month": "07",
    "department": "production",
    "job_role": "process_tech",
    "shift": "morning",
    "years_experience": 5,
    "self_evaluation": 60,
    "machine_brands": ["engel", "haitian"],
    "materials_worked": ["pp", "abs", "pa"],
    "has_scientific_molding": true,
    "has_loto_training": true
  },
  "computed": {
    "age_at_assessment": 35,
    "generation_cohort": "Millennial",
    "assigned_level": "medium",
    "self_eval_vs_role_delta": 10
  }
}
```

### 5.3 Webhook Payload — Assessment Results

```json
{
  "survey_id": "carol_assessment_v2",
  "submitted_at": "2025-06-01T11:15:00Z",
  "candidate": { "...registration fields..." },
  "assessment": {
    "level": "medium",
    "level_name": "Medio — Técnicos de Proceso",
    "total_questions": 60,
    "pass_pct": 75
  },
  "results": {
    "earned_pts": 54.5,
    "max_pts": 76.0,
    "pct_score": 72,
    "passed": false,
    "correct_answers": 42,
    "time_seconds": 2847
  },
  "category_breakdown": {
    "Máquina e Inyectora": { "correct": 7, "total": 9, "pct": 78 },
    "Proceso de Inyección": { "correct": 5, "total": 9, "pct": 56 },
    "...": "..."
  },
  "wrong_question_ids": ["proc_4", "proc_14", "mat_41", "..."]
}
```

### 5.4 Formbricks Alternative

If using Formbricks instead of a custom web form:

| CAROL Type | Formbricks Type |
|-----------|----------------|
| text | openText |
| select | singleSelect |
| multi_select | multipleChoiceMulti |
| number | openText (numeric validation) |
| slider | rating (mapped 0–20 → 0–100%) |
| boolean | yesNo |

Configure webhook under: **Settings → Integrations → Webhooks → n8n Catch Webhook URL**

---

## 6. Report System

### 6.1 Report Types

| Report | Audience | Format | Trigger |
|--------|----------|--------|---------|
| Individual Assessment Report | Candidate + HR | PDF (Python/ReportLab) | Auto on submission |
| Unified Senior Report | Eng. Lead / HR Director | PDF (multi-level) | On-demand |
| Team Cohort Dashboard | Plant Manager | Web (Tabler) | Real-time |

### 6.2 Individual Report Contents

1. **Candidate header** — Name, ID, department, role, date, experience
2. **Overall score** — Donut chart, KPI cards (pts earned / max / pass threshold / status)
3. **Executive summary** — AI-generated narrative (rule-based, deterministic)
4. **Category analysis** — Radar/spider chart + horizontal bar chart + detail table with FORTALEZA / ACEPTABLE / DÉBIL / CRÍTICO tags
5. **Wrong question review** — Every incorrect answer with correct option marked and reasoning shown
6. **Prioritized training plan** — Per weak area: actions, duration estimate, KPI of success
7. **Signature block** — Evaluator + candidate signature fields

### 6.3 Unified Multi-Level Report Contents

Designed for engineering leads reviewing a candidate across all three levels:

1. Triple-ring donut gauge (one ring per level)
2. Cross-level summary bar chart with pass threshold lines
3. Heatmap: all knowledge areas × all three levels
4. Per-level sections (same as individual report, compacted)
5. Consolidated action plan table
6. Global verdict (passes X of 3 levels)

---

## 7. Functional Requirements

### 7.1 Assessment Web App

| # | Requirement | Priority |
|---|------------|----------|
| F-01 | Candidate completes registration form before accessing quiz | P0 |
| F-02 | Level assigned automatically from registration inputs | P0 |
| F-03 | Instructions screen shown before quiz with level-specific content | P0 |
| F-04 | Questions displayed one at a time with sidebar navigation | P0 |
| F-05 | Countdown timer shown; auto-submits at expiry | P0 |
| F-06 | Progress bar reflects % of questions answered | P1 |
| F-07 | Sidebar shows per-question state: pending / answered / current | P1 |
| F-08 | After submit: correct/wrong feedback + reasoning shown per question | P0 |
| F-09 | Results screen with score, category breakdown, wrong review, action plan | P0 |
| F-10 | Results payload POSTed to configurable webhook URL | P0 |
| F-11 | Print-ready results layout | P1 |
| F-12 | Candidate cannot change answers after submission | P0 |
| F-13 | No answer key exposed client-side before submission | P0 |

### 7.2 Admin Dashboard

| # | Requirement | Priority |
|---|------------|----------|
| D-01 | View all assessment results per candidate | P0 |
| D-02 | Filter by level, department, date range, pass/fail | P0 |
| D-03 | Category heatmap across all candidates | P1 |
| D-04 | Export results as CSV | P1 |
| D-05 | Re-assessment scheduling per candidate | P2 |
| D-06 | Team-level competency trend over time | P2 |

### 7.3 Report Generation

| # | Requirement | Priority |
|---|------------|----------|
| R-01 | PDF auto-generated on submission | P0 |
| R-02 | PDF emailed to candidate and HR | P0 |
| R-03 | Unified multi-level report on demand | P1 |
| R-04 | Reports stored and accessible from admin dashboard | P1 |

---

## 8. Non-Functional Requirements

| Category | Requirement |
|----------|------------|
| **Performance** | Quiz loads in < 2s on 4G mobile connection |
| **Compatibility** | Works on Chrome, Firefox, Safari (desktop + mobile) |
| **Language** | Spanish primary; English labels in data fields for n8n compatibility |
| **Accessibility** | WCAG 2.1 AA: contrast ratios, keyboard navigation, focus management |
| **Security** | Answer key never exposed in client-side JS before submission |
| **Data retention** | Assessment results stored for minimum 2 years |
| **Offline** | Not required — assumes stable WiFi in plant environment |
| **Concurrency** | Support 50 simultaneous assessment sessions |

---

## 9. Out of Scope (v2)

- Video or audio question formats
- Adaptive testing (difficulty adjusting per answer)
- LMS integration (SCORM, xAPI)
- Direct HRIS sync
- Multi-language (EN) assessment content
- Peer/supervisor 360° assessments
- Custom question builder UI for admins

---

## 10. Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Assessment completion rate | > 90% | `submitted / started` |
| Time-to-result | < 5 minutes post-submission | n8n workflow timing |
| Report delivery success | > 98% | Email delivery logs |
| Candidate re-assessment improvement | > 15% avg score gain | Score delta tracking |
| HR adoption | 3+ plants live within 6 months | Active organizations |
| Training correlation | Plants using CAROL show > 10% scrap reduction at 6mo | OEE / quality KPIs |

---

## 11. Milestones

| Milestone | Deliverable | Status |
|-----------|-------------|--------|
| M1 | Question bank v2 — all 3 levels | ✅ Complete |
| M2 | Registration funnel JSON + routing logic | ✅ Complete |
| M3 | Assessment web app (carol_platform.html) | ✅ Complete |
| M4 | PDF report generator (Python/ReportLab) | ✅ Complete |
| M5 | n8n workflow — registration routing | 🔄 In Progress |
| M6 | n8n workflow — results + email | 🔄 In Progress |
| M7 | Admin dashboard (Tabler) | 📋 Defined |
| M8 | Multi-plant pilot (3 companies) | 🔜 Planned |
| M9 | OEE correlation analysis tool | 🔜 Planned |

---

## 12. Glossary

| Term | Definition |
|------|-----------|
| **CAROL** | Competency Assessment & Reporting for Operations and Learning |
| **Nivel Básico** | Entry-level assessment for floor operators and setup technicians |
| **Nivel Medio** | Intermediate assessment for process technicians and supervisors |
| **Nivel Avanzado** | Advanced assessment for engineers and technical leaders |
| **VPT** | Velocity-Pressure Transfer — the switchover point in the injection cycle |
| **OEE** | Overall Equipment Effectiveness = Availability × Performance × Quality |
| **SMED** | Single Minute Exchange of Die — changeover time reduction methodology |
| **LOTO** | Lockout/Tagout — energy isolation safety procedure |
| **Regrind** | Recycled/reground plastic material from sprues, runners, and rejects |
| **Runner / Colada** | Secondary channels distributing melt from sprue to gate |
| **Sprue / Bebedero** | Primary conical channel from nozzle to runner system |
| **Gate / Compuerta** | Restricted entry point from runner into the mold cavity |
| **Cushion / Cojín** | Residual material in front of screw at end of injection phase |
| **Warpage / Pandeo** | Post-ejection dimensional distortion from internal stresses |
| **Sink Mark / Rechupado** | Surface depression caused by volumetric shrinkage in thick sections |
| **Flash / Rebaba** | Excess material escaping through parting line due to insufficient clamp force |
| **Shear Thinning** | Viscosity decrease under shear — key property of polymer melts |
| **Cpk** | Process capability index measuring how well a process fits within spec limits |
| **Hot Runner** | Heated manifold system eliminating solidified runner waste each cycle |
| **Cold Runner** | Conventional unheated channel system — generates sprue/runner scrap |
