# CAROL — Agent Task Definitions

**System:** CAROL Assessment System v2  
**Authors:** M. Gallegos / F. Salazar  
**Purpose:** Defines every automated agent, its trigger, inputs, outputs, and n8n implementation notes.

---

## Overview

CAROL relies on three types of agents:

| Type | Tool | Role |
|------|------|------|
| **Workflow Agents** | n8n | Data routing, grading, delivery, storage |
| **AI Agents** | Claude API | Narrative report generation, coaching messages |
| **Scheduler Agents** | n8n (cron) | Reminders, re-assessment nudges, cohort reports |

Each agent is defined below with its full specification.

---

## Agent 1 — Registration Router

**ID:** `agent-registration-router`  
**Trigger:** `POST /webhook/carol-registration`  
**Tool:** n8n Workflow  
**SLA:** < 3 seconds response

### Purpose

Receives the candidate registration payload, computes derived fields, assigns the assessment level, stores the record, and returns the assessment URL to redirect the candidate.

### Input (from carol_platform.html or Formbricks)

```json
{
  "survey_id": "carol_registration_v2",
  "submitted_at": "ISO-8601",
  "respondent": {
    "full_name": "string",
    "employee_id": "string",
    "birth_year": "string (YYYY)",
    "birth_month": "string (MM) | null",
    "department": "enum",
    "job_role": "enum",
    "shift": "enum | null",
    "years_experience": "integer",
    "self_evaluation": "integer (0-100)",
    "machine_brands": "string[]",
    "materials_worked": "string[]",
    "has_scientific_molding": "boolean",
    "has_loto_training": "boolean",
    "confidence_area": "enum | null",
    "improvement_area": "enum | null",
    "learning_goal": "enum | null"
  }
}
```

### n8n Node Sequence

```
[Webhook — POST /webhook/carol-registration]
        │
        ▼
[Function — Compute Fields]
  • age_at_assessment = currentYear - birth_year
  • exact_age = (birth_month provided) ? precise calc : null
  • generation_cohort = map birth_year to cohort
  • experience_vs_age_ratio = years_experience / age_at_assessment
  • anomaly_flag = ratio > 0.8 (started at 16 or younger)
        │
        ▼
[Function — Assign Level]
  Rule engine:
  IF job_role IN [operator, setup_tech] OR
     (years_experience < 2 AND self_evaluation < 40) OR
     self_evaluation < 35
  → level = "basic"

  ELIF job_role IN [process_tech, supervisor] OR
       (years_experience >= 2 AND years_experience < 6 AND
        self_evaluation BETWEEN 40 AND 70)
  → level = "medium"

  ELIF job_role IN [process_eng, mold_eng, quality_eng, plant_manager] OR
       (years_experience >= 6 AND self_evaluation > 70)
  → level = "advanced"

  ELSE → level = "basic"  // safe default

  self_eval_delta = self_evaluation - ROLE_BASELINES[job_role]
  // ROLE_BASELINES: operator=25, setup_tech=35, process_tech=50,
  //   supervisor=55, process_eng=70, mold_eng=75, quality_eng=70
        │
        ▼
[Google Sheets / Airtable — Insert Row]
  Columns: candidate_id (uuid), full_name, employee_id,
           department, job_role, birth_year, age_at_assessment,
           generation_cohort, years_experience, self_evaluation,
           assigned_level, self_eval_delta, anomaly_flag,
           registration_at, status="registered"
        │
        ▼
[Respond to Webhook]
  {
    "success": true,
    "candidate_id": "uuid",
    "assigned_level": "medium",
    "assessment_url": "https://carol.yourdomain.com?level=medium&cid=uuid",
    "message_es": "Tu evaluación asignada es Nivel Medio. ¡Buena suerte!"
  }
```

### Output

- Candidate record stored with `status = "registered"`
- `assessment_url` returned to client for redirect
- Optional: welcome email sent (see Agent 5)

### Error Handling

- Missing required fields → `400` with field list
- `birth_year` produces `age < 16` or `age > 75` → flag as anomaly, still proceed
- DB write failure → retry once, then alert admin via Slack/email

---

## Agent 2 — Assessment Grader & Results Dispatcher

**ID:** `agent-results-dispatcher`  
**Trigger:** `POST /webhook/carol-results`  
**Tool:** n8n Workflow  
**SLA:** < 10 seconds (PDF generation adds ~3s)

### Purpose

Receives completed assessment submission, validates integrity, grades answers, generates the PDF report, emails it to the candidate and HR, and updates the candidate record.

### Input

```json
{
  "survey_id": "carol_assessment_v2",
  "submitted_at": "ISO-8601",
  "candidate": { "...all registration fields + candidate_id..." },
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
    "Proceso de Inyección": { "correct": 5, "total": 9, "pct": 56 }
  },
  "wrong_question_ids": ["proc_4", "proc_14", "mat_41"]
}
```

### n8n Node Sequence

```
[Webhook — POST /webhook/carol-results]
        │
        ▼
[Function — Validate & Enrich]
  • Verify candidate_id exists in DB
  • Compute weak_categories (pct < 70%)
  • Compute critical_categories (pct < 55%)
  • Compute time_used_min = time_seconds / 60
  • Compute performance_vs_time_ratio
        │
        ▼
[Execute Command — Generate PDF]
  python3 /carol/reports/carol_generate_report.py \
    --level {{ $json.assessment.level }} \
    --candidate_json '{{ JSON.stringify($json.candidate) }}' \
    --results_json '{{ JSON.stringify($json.results) }}' \
    --output /tmp/carol_{{ $json.candidate.employee_id }}_{{ now }}.pdf
        │
        ▼
[Read Binary File — Load PDF]
        │
        ├─────────────────────────────────────────┐
        ▼                                         ▼
[Gmail / SMTP — Email Candidate]        [Gmail / SMTP — Email HR]
  To: {{ candidate.email }}              To: hr@company.com
  Subject: Tu resultado CAROL —          Subject: Resultado CAROL —
    Nivel {{ level }}                      {{ candidate.full_name }}
  Body: personalized template             Body: HR summary template
  Attach: PDF report                      Attach: PDF report
        │                                         │
        └─────────────────┬───────────────────────┘
                          ▼
[Google Sheets — Update Row]
  Find by candidate_id:
  • assessment_level, score_pct, passed, earned_pts
  • correct_answers, time_seconds, weak_categories
  • assessment_at, status = "completed"
        │
        ▼
[Respond to Webhook]
  { "success": true, "report_url": "...", "email_sent": true }
```

### Output

- PDF report generated and emailed
- Candidate record updated with `status = "completed"` + full results
- Dashboard data refreshed (if using live sheet)

### Error Handling

- PDF generation fails → skip attachment, send email with inline summary, flag for manual retry
- Email bounce → log to `failed_deliveries` sheet, alert HR
- Duplicate submission (same candidate\_id, same level, within 24h) → reject with `409 Conflict`

---

## Agent 3 — AI Report Narrative Generator

**ID:** `agent-ai-narrative`  
**Trigger:** Called from Agent 2 (results pipeline)  
**Tool:** Claude API (`claude-sonnet-4-6`)  
**SLA:** < 8 seconds

### Purpose

Generates a personalized, human-readable narrative for the assessment report. Replaces rule-based text with contextually aware coaching language.

### When to Call

Called from Agent 2 after grading, before PDF generation. Pass the graded results; receive narrative text blocks for the PDF.

### Prompt Template

```
System:
You are CAROL, a technical competency advisor for injection molding manufacturing.
Write concise, professional, motivating Spanish text. Be specific to the data provided.
Never use generic phrases. Reference actual scores and categories. Respond ONLY with
valid JSON matching the output schema below.

User:
Generate assessment narrative for:

Candidate: {{ candidate.full_name }}
Role: {{ candidate.job_role }}
Level: {{ assessment.level_name }}
Score: {{ results.pct_score }}% ({{ results.passed ? 'APROBADO' : 'NO APROBADO' }})
Pass threshold: {{ assessment.pass_pct }}%

Category results (worst to best):
{{ category_breakdown | formatted_list }}

Weak categories (pct < 70%): {{ weak_categories | join(', ') }}
Critical categories (pct < 55%): {{ critical_categories | join(', ') }}
Strong categories (pct >= 82%): {{ strong_categories | join(', ') }}

Output JSON schema:
{
  "executive_summary": "2-3 sentences. State result, highlight strongest area, flag biggest gap.",
  "strength_note": "1 sentence. Specific callout of best category performance.",
  "gap_note": "1 sentence. Honest, constructive note on biggest gap.",
  "coaching_message": "2-3 sentences. Direct, actionable, motivating. Avoid clichés.",
  "hr_recommendation": "1 sentence for HR/supervisor. Action: certify / train / re-evaluate."
}
```

### Output Schema

```json
{
  "executive_summary": "string",
  "strength_note": "string",
  "gap_note": "string",
  "coaching_message": "string",
  "hr_recommendation": "string"
}
```

### Integration in n8n

```
[HTTP Request — Claude API]
  POST https://api.anthropic.com/v1/messages
  Headers:
    x-api-key: {{ $credentials.anthropic.apiKey }}
    anthropic-version: 2023-06-01
  Body:
    model: claude-sonnet-4-6
    max_tokens: 600
    messages: [{ role: "user", content: "{{ prompt }}" }]
        │
        ▼
[Function — Parse JSON from response]
  const text = $json.content[0].text;
  const narrative = JSON.parse(text);
  return narrative;
```

### Fallback

If Claude API call fails or returns malformed JSON:
- Use rule-based narrative from `carol_generate_report.py` (already implemented)
- Log failure to monitoring
- Do not block PDF generation

---

## Agent 4 — Re-Assessment Reminder Scheduler

**ID:** `agent-reassessment-scheduler`  
**Trigger:** n8n Cron — runs daily at 08:00 (plant local time)  
**Tool:** n8n Workflow + Gmail/SMTP  
**SLA:** Batch, no real-time SLA

### Purpose

Automatically identifies candidates who did not pass their assessment and sends a reminder to take the re-assessment after completing their training plan. Also notifies supervisors of candidates who haven't been assessed yet.

### Logic

```
[Cron — Daily 08:00]
        │
        ▼
[Google Sheets — Query Candidates]
  WHERE status = "completed" AND passed = false
    AND assessment_at < (today - 28 days)  // 4 weeks post-fail
    AND reassessment_sent = false
        │
        ▼
[Loop — For Each Candidate]
        │
        ├─[Gmail — Reminder to Candidate]
        │   Subject: "Tu plan de capacitación CAROL — ¿Listo para re-evaluarte?"
        │   Body: personalized (name, level, weak areas, original score, link)
        │
        ├─[Gmail — Notify Supervisor]
        │   Subject: "Recordatorio: {{ name }} pendiente de re-evaluación CAROL"
        │   Body: candidate summary + weak categories + training plan link
        │
        └─[Google Sheets — Update]
              reassessment_sent = true
              reminder_sent_at = now
```

### Unassessed Candidates Alert

```
[Cron — Weekly Monday 09:00]
        │
        ▼
[Google Sheets — Query Active Employees]
  WHERE carol_assessed = false
    AND hire_date < (today - 30 days)  // > 1 month on floor
        │
        ▼
[Gmail — HR Manager Alert]
  Subject: "{{ count }} empleados sin evaluación CAROL esta semana"
  Body: list of names, departments, roles, hire dates
```

---

## Agent 5 — Welcome & Onboarding Messenger

**ID:** `agent-welcome-messenger`  
**Trigger:** Called from Agent 1 (registration complete)  
**Tool:** n8n → Gmail or WhatsApp Business API  
**SLA:** < 30 seconds

### Purpose

Sends a warm confirmation to the candidate immediately after registration, including their assigned level, a brief explanation of what to expect, and encouragement.

### Message Template (Email)

```
Subject: Tu evaluación CAROL está lista — Nivel {{ level_name }}

Hola {{ first_name }},

Tu registro en CAROL se completó exitosamente.

Se te ha asignado la evaluación de:
📋 {{ level_name }}
📊 {{ total_questions }} preguntas | {{ max_score }} puntos máximos
⏱ Tiempo estimado: {{ time_min }} minutos
✅ Puntaje aprobatorio: {{ pass_pct }}%

Recuerda:
• Lee cada pregunta con calma antes de responder
• Puedes navegar entre preguntas usando la barra lateral
• Tu resultado y plan de desarrollo te llegará por correo al terminar

¡Mucho éxito!
— El equipo CAROL
```

### WhatsApp Alternative (if configured)

```
Hola {{ first_name }} 👋

Tu evaluación CAROL está lista:
📋 Nivel: {{ level_name }}
⏱ Duración estimada: {{ time_min }} min
📎 Link: {{ assessment_url }}

¡Éxito! 🎯
```

---

## Agent 6 — Cohort Analytics Reporter

**ID:** `agent-cohort-reporter`  
**Trigger:** n8n Cron — First Monday of each month, 07:00  
**Tool:** n8n → Python → Gmail  
**SLA:** Batch, delivers by 08:00

### Purpose

Generates a monthly cohort summary report for HR and plant leadership showing: participation rate, pass rates by level and department, category heatmaps, and trend vs prior month.

### Data Pulled

```
[Google Sheets — Query All Assessments]
  WHERE assessment_at >= first_day_of_prior_month
    AND assessment_at <= last_day_of_prior_month
        │
        ▼
[Function — Compute Cohort Stats]
  • total_assessed, total_passed, overall_pass_rate
  • pass_rate by: level, department, job_role
  • avg_score by: level, department
  • weakest_category overall and by department
  • improvement vs prior month (if data exists)
        │
        ▼
[Execute Command — Generate Cohort PDF]
  python3 /carol/reports/carol_cohort_report.py \
    --month {{ prior_month }} \
    --data_json '{{ JSON.stringify(cohort_data) }}' \
    --output /tmp/carol_cohort_{{ prior_month }}.pdf
        │
        ▼
[Gmail — Monthly Report Email]
  To: hr@company.com, plant_manager@company.com
  Subject: "Reporte CAROL — {{ prior_month }} | {{ pass_rate }}% tasa de aprobación"
  Attach: cohort PDF
```

---

## Agent 7 — Data Quality Validator

**ID:** `agent-data-validator`  
**Trigger:** Called from Agent 1 and Agent 2 before DB writes  
**Tool:** n8n Function node  
**SLA:** < 100ms

### Purpose

Validates all incoming data before it is stored. Flags anomalies without blocking the flow.

### Validation Rules

```javascript
function validate(payload) {
  const flags = [];

  // Age sanity
  const age = currentYear - parseInt(payload.birth_year);
  if (age < 16 || age > 75) flags.push('AGE_OUT_OF_RANGE');

  // Experience vs age
  if (payload.years_experience > age - 14)
    flags.push('EXPERIENCE_EXCEEDS_AGE');

  // Self-eval vs role baseline
  const baselines = {
    operator: 25, setup_tech: 35, process_tech: 50,
    supervisor: 55, process_eng: 70, mold_eng: 75,
    quality_eng: 70, plant_manager: 65
  };
  const delta = payload.self_evaluation - (baselines[payload.job_role] || 50);
  if (delta > 40) flags.push('SELF_EVAL_OVERCONFIDENT');
  if (delta < -40) flags.push('SELF_EVAL_UNDERCONFIDENT');

  // Score sanity (results payload)
  if (payload.results) {
    const computed_pct = payload.results.earned_pts / payload.results.max_pts * 100;
    if (Math.abs(computed_pct - payload.results.pct_score) > 1)
      flags.push('SCORE_MISMATCH');
    if (payload.results.time_seconds < 120)
      flags.push('SUSPICIOUSLY_FAST'); // < 2 min for 40+ questions
  }

  return { valid: flags.length === 0, flags };
}
```

### Output

Adds `_validation` object to payload before passing to next node:

```json
{
  "_validation": {
    "valid": true,
    "flags": [],
    "checked_at": "ISO-8601"
  }
}
```

Flags are stored in the DB for admin review but do not block processing.

---

## Agent 8 — Slack / Teams Notifier (Optional)

**ID:** `agent-slack-notifier`  
**Trigger:** Called from Agent 2 (on results)  
**Tool:** n8n → Slack or Microsoft Teams  
**SLA:** < 5 seconds, best-effort

### Purpose

Posts a brief notification to a designated Slack channel (e.g. `#carol-results`) when a notable result occurs.

### Trigger Conditions

| Condition | Message |
|-----------|---------|
| Score ≥ 90% | `🏆 {{ name }} scored {{ pct }}% on {{ level }} — Outstanding!` |
| Score < 55% (critical) | `🔴 {{ name }} scored {{ pct }}% on {{ level }} — Training plan needed` |
| All 3 levels passed | `✅ {{ name }} passed all 3 CAROL levels — Ready for senior role` |
| Same candidate fails twice | `⚠️ {{ name }} has failed {{ level }} twice — Escalation recommended` |

### n8n Node

```
[IF — Condition Met]
        │
        ▼
[Slack — Post Message]
  Channel: #carol-results
  Message: {{ template }}
  Icon: :carol:
```

---

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `CAROL_WEBHOOK_REGISTRATION` | n8n catch webhook URL for registration | `https://n8n.co/webhook/abc123` |
| `CAROL_WEBHOOK_RESULTS` | n8n catch webhook URL for results | `https://n8n.co/webhook/def456` |
| `CAROL_ANTHROPIC_KEY` | Claude API key for AI narrative agent | `sk-ant-...` |
| `CAROL_HR_EMAIL` | HR manager email for result copies | `hr@company.com` |
| `CAROL_GOOGLE_SHEET_ID` | Spreadsheet ID for candidate data | `1BxiM...` |
| `CAROL_SMTP_HOST` | SMTP server for email delivery | `smtp.gmail.com` |
| `CAROL_SLACK_WEBHOOK` | Slack incoming webhook URL | `https://hooks.slack.com/...` |
| `CAROL_REPORT_OUTPUT_DIR` | Server path for generated PDFs | `/var/carol/reports/` |

---

## Agent Dependency Map

```
Registration Form
      │
      ▼
Agent 1 (Registration Router)
      ├── Agent 7 (Validator) ← runs inline
      ├── Agent 5 (Welcome Messenger)
      └── [Candidate DB Record created]
            │
            ▼ (candidate completes quiz)
Agent 2 (Results Dispatcher)
      ├── Agent 7 (Validator) ← runs inline
      ├── Agent 3 (AI Narrative) ← async, with fallback
      ├── PDF Generator (Python script)
      ├── Email delivery
      └── [Candidate DB Record updated]
            │
            ├── Agent 8 (Slack Notifier) ← conditional
            │
            └── [Daily cron]
                  │
                  ├── Agent 4 (Re-Assessment Scheduler)
                  └── Agent 6 (Cohort Reporter) ← monthly
```
