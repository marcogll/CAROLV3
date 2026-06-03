#!/usr/bin/env python3
"""
CAROL Report Engine — wrappers around existing PDF generators
so server.py can call them with live DB data.
"""
import os, sys, json, tempfile

# Allow importing sibling report scripts
_script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _script_dir)

from carol_generate_report import build_pdf as _build_single_pdf, generate_ai_analysis as _single_ai
from carol_generate_unified_report import build_pdf as _build_unified_pdf, ai_analysis as _unified_ai

CAT_MAP_ES_TO_EN = {
    "Máquina e Inyectora": "Machine",
    "Proceso de Inyección": "Process",
    "Calidad y Defectos": "Quality",
    "Seguridad Industrial": "Safety",
    "Materiales Plásticos": "Materials",
    "Eficiencia y Lean": "Efficiency",
    "Desperdicios (Muda)": "Waste",
    "Ingeniería de Moldes": "Mold Engineering",
}

LEVEL_META = {
    "basic":    {"label": "Básico",    "pass_pct": 75},
    "medium":   {"label": "Medio",     "pass_pct": 75},
    "advanced": {"label": "Avanzado",  "pass_pct": 80},
}


def _transform_answers(answers_map: dict) -> list:
    """Convert server-side answers dict to report script format."""
    out = []
    for qid, a in answers_map.items():
        cat_en = CAT_MAP_ES_TO_EN.get(a.get("category", ""), a.get("category", ""))
        out.append({
            "id": qid,
            "category": cat_en,
            "type": a.get("type", "Teórico"),
            "question": a.get("question", ""),
            "options": a.get("options", []),
            "correct_index": a.get("correct_index", 0),
            "chosen_index": a.get("chosen_index", -1),
            "correct": bool(a.get("correct", False)),
            "score_earned": a.get("score", 0) if a.get("correct") else 0,
            "score_max": a.get("score", 0),
            "reasoning": a.get("reasoning", ""),
        })
    return out


def _build_categories(answers_list: list) -> dict:
    cats = {}
    for a in answers_list:
        c = a["category"]
        if c not in cats:
            cats[c] = {"correct": 0, "total": 0, "earned": 0.0, "max": 0.0}
        cats[c]["total"] += 1
        cats[c]["max"] += a["score_max"]
        if a["correct"]:
            cats[c]["correct"] += 1
            cats[c]["earned"] += a["score_earned"]
    return cats


def _make_candidate(candidate_json: dict, submitted_at: str) -> dict:
    return {
        "full_name": candidate_json.get("full_name", "Candidato"),
        "employee_id": candidate_json.get("employee_id", "—"),
        "department": candidate_json.get("department", "—"),
        "job_role": candidate_json.get("job_role", "—"),
        "years_experience": str(candidate_json.get("years_experience", "—")),
        "date": submitted_at[:10] if submitted_at else "—",
    }


def generate_single_report(result_row: dict, output_path: str):
    """
    result_row: flat dict from DB/JSON with keys:
      candidate, assessment, results, category_breakdown, wrong_question_ids, answers, submitted_at
    """
    c = _make_candidate(result_row.get("candidate", {}), result_row.get("submitted_at", ""))
    level = result_row.get("assessment", {}).get("level", "basic")
    answers_list = _transform_answers(result_row.get("answers", {}))
    cats = _build_categories(answers_list)
    total_earned = sum(a["score_earned"] for a in answers_list)
    total_max = sum(a["score_max"] for a in answers_list)
    pct = round(total_earned / total_max * 100, 1) if total_max else 0

    results = {
        "answers": answers_list,
        "categories": cats,
        "total_earned": total_earned,
        "total_max": total_max,
        "pct": pct,
    }
    analysis = _single_ai(results, level, c)
    _build_single_pdf(output_path, level, c, results, analysis)
    return output_path


def generate_unified_report(result_rows: list, output_path: str):
    """
    result_rows: list of result dicts (basic, medium, advanced) for the same candidate.
    """
    if not result_rows:
        raise ValueError("No result rows provided")

    c = _make_candidate(result_rows[0].get("candidate", {}), result_rows[0].get("submitted_at", ""))
    c["full_name"] = result_rows[0].get("candidate", {}).get("full_name", "Candidato")

    all_questions = {}
    all_results = {}
    all_analysis = {}

    for row in result_rows:
        level = row.get("assessment", {}).get("level", "basic")
        answers_list = _transform_answers(row.get("answers", {}))
        cats = _build_categories(answers_list)
        total_earned = sum(a["score_earned"] for a in answers_list)
        total_max = sum(a["score_max"] for a in answers_list)
        pct = round(total_earned / total_max * 100, 1) if total_max else 0

        results = {
            "answers": answers_list,
            "categories": cats,
            "total_earned": total_earned,
            "total_max": total_max,
            "pct": pct,
        }
        all_results[level] = results
        all_analysis[level] = _unified_ai(results, level, c["full_name"])
        # For question list we keep answers as pseudo-questions for the report
        all_questions[level] = answers_list

    _build_unified_pdf(output_path, all_questions, all_results, all_analysis, c)
    return output_path
