#!/usr/bin/env python3
"""
CAROL Assessment Report Generator
Generates a full HTML + PDF report for a candidate assessment result.
Usage: python generate_report.py [--level basic|medium|advanced] [--output report.pdf]
"""

import json
import random
import math
import io
import base64
import os
import sys
import argparse
from datetime import datetime, date

# ── matplotlib (charts) ──────────────────────────────────────────────────────
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

# ── reportlab (PDF) ──────────────────────────────────────────────────────────
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.graphics.shapes import Drawing, Rect, String, Line
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing

# ─────────────────────────────────────────────────────────────────────────────
# BRAND COLORS
# ─────────────────────────────────────────────────────────────────────────────
BRAND = {
    "navy":     colors.HexColor("#0D1B2A"),
    "blue":     colors.HexColor("#1B4F72"),
    "teal":     colors.HexColor("#1ABC9C"),
    "teal_lt":  colors.HexColor("#D5F5E3"),
    "amber":    colors.HexColor("#F39C12"),
    "amber_lt": colors.HexColor("#FEF9E7"),
    "red":      colors.HexColor("#E74C3C"),
    "red_lt":   colors.HexColor("#FDEDEC"),
    "gray":     colors.HexColor("#7F8C8D"),
    "gray_lt":  colors.HexColor("#F4F6F7"),
    "white":    colors.white,
    "black":    colors.HexColor("#1A1A1A"),
}

CAT_COLORS_HEX = {
    "Machine":          "#1B4F72",
    "Process":          "#1ABC9C",
    "Quality":          "#F39C12",
    "Safety":           "#E74C3C",
    "Materials":        "#8E44AD",
    "Efficiency":       "#2980B9",
    "Waste":            "#27AE60",
    "Mold Engineering": "#E67E22",
}

CAT_LABELS_ES = {
    "Machine":          "Máquina",
    "Process":          "Proceso",
    "Quality":          "Calidad",
    "Safety":           "Seguridad",
    "Materials":        "Materiales",
    "Efficiency":       "Eficiencia",
    "Waste":            "Desperdicios",
    "Mold Engineering": "Ing. Moldes",
}

LEVEL_META = {
    "basic": {
        "label": "Básico",
        "role": "Operadores de Piso",
        "pass_pct": 75,
        "time_min": 50,
        "color": BRAND["teal"],
        "color_hex": "#1ABC9C",
    },
    "medium": {
        "label": "Medio",
        "role": "Técnicos de Proceso",
        "pass_pct": 75,
        "time_min": 60,
        "color": BRAND["amber"],
        "color_hex": "#F39C12",
    },
    "advanced": {
        "label": "Avanzado",
        "role": "Ingenieros y Líderes",
        "pass_pct": 80,
        "time_min": 75,
        "color": BRAND["blue"],
        "color_hex": "#1B4F72",
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# SAMPLE DATA GENERATOR
# ─────────────────────────────────────────────────────────────────────────────

def generate_sample_results(questions: list, seed: int = 42) -> dict:
    """
    Simulate a candidate taking the test.
    Returns a result dict with per-question correctness and per-category stats.
    """
    rng = random.Random(seed)

    # Simulate varying accuracy by category (realistic weak spots)
    cat_accuracy = {
        "Machine":          rng.uniform(0.60, 0.90),
        "Process":          rng.uniform(0.50, 0.80),
        "Quality":          rng.uniform(0.65, 0.90),
        "Safety":           rng.uniform(0.70, 0.95),
        "Materials":        rng.uniform(0.40, 0.75),
        "Efficiency":       rng.uniform(0.55, 0.85),
        "Waste":            rng.uniform(0.60, 0.88),
        "Mold Engineering": rng.uniform(0.35, 0.70),
    }

    answers = []
    for q in questions:
        cat = q["category"]
        acc = cat_accuracy.get(cat, 0.65)
        correct = rng.random() < acc
        chosen = q["correct_index"] if correct else rng.choice(
            [i for i in range(len(q["options"])) if i != q["correct_index"]]
        )
        answers.append({
            "id": q["id"],
            "category": cat,
            "type": q["type"],
            "question": q["question"],
            "options": q["options"],
            "correct_index": q["correct_index"],
            "chosen_index": chosen,
            "correct": correct,
            "score_earned": q["score"] if correct else 0,
            "score_max": q["score"],
            "reasoning": q["reasoning"],
        })

    # Aggregate per category
    cats = {}
    for a in answers:
        c = a["category"]
        if c not in cats:
            cats[c] = {"correct": 0, "total": 0, "earned": 0.0, "max": 0.0}
        cats[c]["total"] += 1
        cats[c]["max"] += a["score_max"]
        if a["correct"]:
            cats[c]["correct"] += 1
            cats[c]["earned"] += a["score_earned"]

    total_earned = sum(a["score_earned"] for a in answers)
    total_max = sum(a["score_max"] for a in answers)

    return {
        "answers": answers,
        "categories": cats,
        "total_earned": total_earned,
        "total_max": total_max,
        "pct": round(total_earned / total_max * 100, 1),
    }

# ─────────────────────────────────────────────────────────────────────────────
# CHART GENERATORS (matplotlib → base64 PNG)
# ─────────────────────────────────────────────────────────────────────────────

def fig_to_png_bytes(fig) -> bytes:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    buf.seek(0)
    return buf.read()


def make_donut_chart(pct: float, passed: bool, level_color_hex: str) -> bytes:
    """Large center donut showing overall score."""
    fig, ax = plt.subplots(figsize=(4, 4), facecolor="none")
    ax.set_facecolor("none")

    fill_color = level_color_hex
    empty_color = "#E8EAED"

    ax.pie(
        [pct, 100 - pct],
        colors=[fill_color, empty_color],
        startangle=90,
        counterclock=False,
        wedgeprops=dict(width=0.38, edgecolor="white", linewidth=2),
    )

    status_icon = "✓" if passed else "✗"
    status_color = "#1ABC9C" if passed else "#E74C3C"
    ax.text(0, 0.08, f"{pct:.1f}%", ha="center", va="center",
            fontsize=28, fontweight="bold", color="#1A1A1A")
    ax.text(0, -0.28, status_icon, ha="center", va="center",
            fontsize=18, fontweight="bold", color=status_color)

    ax.set(aspect="equal")
    plt.tight_layout(pad=0)
    data = fig_to_png_bytes(fig)
    plt.close(fig)
    return data


def make_category_radar(cats: dict, cat_colors: dict) -> bytes:
    """Spider / radar chart of category accuracy %."""
    labels = [CAT_LABELS_ES.get(c, c) for c in cats]
    values = [cats[c]["correct"] / cats[c]["total"] * 100 for c in cats]

    N = len(labels)
    angles = [n / float(N) * 2 * math.pi for n in range(N)]
    angles += angles[:1]
    values_plot = values + values[:1]

    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True),
                           facecolor="none")
    ax.set_facecolor("#F8FAFB")
    ax.set_theta_offset(math.pi / 2)
    ax.set_theta_direction(-1)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=8.5, fontweight="bold", color="#1A1A1A")
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(["20%", "40%", "60%", "80%", "100%"],
                       fontsize=7, color="#AAB0B7")
    ax.yaxis.grid(True, color="#DDE1E4", linestyle="--", linewidth=0.8)
    ax.xaxis.grid(True, color="#DDE1E4", linestyle="-", linewidth=0.5)

    ax.plot(angles, values_plot, "o-", linewidth=2.5,
            color="#1B4F72", markersize=5)
    ax.fill(angles, values_plot, alpha=0.22, color="#1B4F72")

    # Passing threshold ring at 75%
    pass_ring = [75] * (N + 1)
    ax.plot(angles, pass_ring, "--", linewidth=1.2, color="#E74C3C", alpha=0.6)

    plt.tight_layout(pad=1)
    data = fig_to_png_bytes(fig)
    plt.close(fig)
    return data


def make_pie_chart(cats: dict) -> bytes:
    """Pie chart: distribution of correct vs incorrect per category."""
    labels = [CAT_LABELS_ES.get(c, c) for c in cats]
    earned = [cats[c]["earned"] for c in cats]
    missed = [cats[c]["max"] - cats[c]["earned"] for c in cats]
    colors_list = [CAT_COLORS_HEX.get(c, "#95A5A6") for c in cats]

    fig, axes = plt.subplots(1, 2, figsize=(9, 4.2), facecolor="none")

    # Left: pts earned per category (pie)
    ax = axes[0]
    wedges, texts, autotexts = ax.pie(
        earned,
        labels=None,
        colors=colors_list,
        autopct=lambda p: f"{p:.0f}%" if p > 5 else "",
        startangle=140,
        wedgeprops=dict(edgecolor="white", linewidth=1.5),
        pctdistance=0.78,
    )
    for at in autotexts:
        at.set_fontsize(8)
        at.set_color("white")
        at.set_fontweight("bold")
    ax.set_title("Puntos obtenidos\npor área", fontsize=10,
                 fontweight="bold", color="#1A1A1A", pad=10)

    # Legend
    patches = [mpatches.Patch(color=colors_list[i], label=labels[i])
               for i in range(len(labels))]
    ax.legend(handles=patches, loc="lower left",
              fontsize=7.5, framealpha=0.9,
              bbox_to_anchor=(-0.55, -0.15), ncol=2)

    # Right: correct vs incorrect horizontal bars
    ax2 = axes[1]
    y_pos = np.arange(len(labels))
    bar_h = 0.45
    correct_pcts = [cats[c]["correct"] / cats[c]["total"] * 100 for c in cats]
    incorrect_pcts = [100 - p for p in correct_pcts]

    bars_c = ax2.barh(y_pos, correct_pcts, bar_h,
                      color=colors_list, edgecolor="white", linewidth=0.8)
    ax2.barh(y_pos, incorrect_pcts, bar_h, left=correct_pcts,
             color="#E8EAED", edgecolor="white", linewidth=0.8)

    for i, (bar, pct) in enumerate(zip(bars_c, correct_pcts)):
        ax2.text(pct / 2, i, f"{pct:.0f}%", ha="center", va="center",
                 fontsize=8, fontweight="bold", color="white")

    ax2.axvline(75, color="#E74C3C", linestyle="--", linewidth=1.3,
                alpha=0.8, label="Mínimo aprobatorio (75%)")
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(labels, fontsize=8.5)
    ax2.set_xlim(0, 100)
    ax2.set_xlabel("% Respuestas correctas", fontsize=8.5)
    ax2.set_title("Aciertos por área", fontsize=10,
                  fontweight="bold", color="#1A1A1A", pad=10)
    ax2.legend(fontsize=7.5, loc="lower right")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.grid(axis="x", linestyle="--", alpha=0.4)
    ax2.invert_yaxis()

    plt.tight_layout(pad=1.5)
    data = fig_to_png_bytes(fig)
    plt.close(fig)
    return data


def make_question_type_bar(answers: list) -> bytes:
    """Bar: Teórico vs Práctico accuracy."""
    types = {"Teórico": {"c": 0, "t": 0}, "Práctico": {"c": 0, "t": 0}}
    for a in answers:
        t = a["type"]
        if t in types:
            types[t]["t"] += 1
            if a["correct"]:
                types[t]["c"] += 1

    labels = list(types.keys())
    pcts = [types[l]["c"] / types[l]["t"] * 100 for l in labels]
    totals = [types[l]["t"] for l in labels]

    fig, ax = plt.subplots(figsize=(4, 2.8), facecolor="none")
    ax.set_facecolor("none")

    bar_colors = ["#1B4F72", "#1ABC9C"]
    bars = ax.bar(labels, pcts, width=0.45, color=bar_colors,
                  edgecolor="white", linewidth=1.5, zorder=3)

    for bar, pct, total in zip(bars, pcts, totals):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 2,
                f"{pct:.1f}%\n({total} preg.)",
                ha="center", va="bottom", fontsize=9, fontweight="bold",
                color="#1A1A1A")

    ax.axhline(75, color="#E74C3C", linestyle="--",
               linewidth=1.3, alpha=0.8, zorder=4)
    ax.set_ylim(0, 115)
    ax.set_ylabel("% Aciertos", fontsize=9)
    ax.set_title("Teórico vs Práctico", fontsize=10,
                 fontweight="bold", color="#1A1A1A")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linestyle="--", alpha=0.4, zorder=0)

    plt.tight_layout(pad=0.8)
    data = fig_to_png_bytes(fig)
    plt.close(fig)
    return data

# ─────────────────────────────────────────────────────────────────────────────
# AI ANALYSIS ENGINE
# ─────────────────────────────────────────────────────────────────────────────

def generate_ai_analysis(results: dict, level: str, candidate: dict) -> dict:
    """Generate text-based AI analysis (rule-based, deterministic)."""
    cats = results["categories"]
    pct = results["pct"]
    meta = LEVEL_META[level]
    pass_pct = meta["pass_pct"]
    passed = pct >= pass_pct

    # Sort categories by accuracy
    cat_scores = {c: cats[c]["correct"] / cats[c]["total"] * 100 for c in cats}
    sorted_cats = sorted(cat_scores.items(), key=lambda x: x[1])
    weak_cats = [c for c, p in sorted_cats if p < 70]
    strong_cats = [c for c, p in sorted_cats if p >= 80]
    critical_cats = [c for c, p in sorted_cats if p < 55]

    # Executive summary
    name = candidate.get("full_name", "El candidato")
    status_text = "APROBÓ" if passed else "NO APROBÓ"
    status_color = "#1ABC9C" if passed else "#E74C3C"
    gap = pct - pass_pct

    summary_lines = []
    if passed:
        if pct >= 90:
            summary_lines.append(f"{name} demostró un dominio sobresaliente del proceso de moldeo por inyección, superando ampliamente el umbral de aprobación con {pct:.1f}%. Sus resultados indican capacidad para operar, diagnosticar y tomar decisiones técnicas de forma autónoma.")
        elif pct >= 80:
            summary_lines.append(f"{name} aprobó la evaluación con {pct:.1f}%, demostrando competencia sólida en la mayoría de las áreas evaluadas. Existen oportunidades de refuerzo en áreas específicas para alcanzar nivel de excelencia.")
        else:
            summary_lines.append(f"{name} aprobó con {pct:.1f}%, superando el mínimo requerido ({pass_pct}%) por {gap:.1f} puntos porcentuales. Se recomienda refuerzo en las áreas de menor desempeño para consolidar las competencias.")
    else:
        summary_lines.append(f"{name} no alcanzó el puntaje mínimo requerido ({pass_pct}%), obteniendo {pct:.1f}% ({abs(gap):.1f}pp por debajo del umbral). Se requiere un plan de capacitación estructurado antes de una re-evaluación.")

    if strong_cats:
        strong_labels = [CAT_LABELS_ES.get(c, c) for c in strong_cats]
        summary_lines.append(f"Áreas de fortaleza identificadas: {', '.join(strong_labels)}.")
    if weak_cats:
        weak_labels = [CAT_LABELS_ES.get(c, c) for c in weak_cats]
        summary_lines.append(f"Áreas que requieren atención: {', '.join(weak_labels)}.")

    # Per-category insights
    cat_insights = []
    for cat, pct_c in sorted_cats:
        label = CAT_LABELS_ES.get(cat, cat)
        c_data = cats[cat]
        acc = pct_c

        if acc >= 85:
            insight = f"Dominio sólido. {c_data['correct']}/{c_data['total']} respuestas correctas. Puede ser referente para pares."
            level_tag = "FORTALEZA"
            tag_color = "#1ABC9C"
        elif acc >= 70:
            insight = f"Desempeño aceptable con áreas de mejora puntuales. {c_data['correct']}/{c_data['total']} correctas. Refuerzo en conceptos prácticos recomendado."
            level_tag = "ACEPTABLE"
            tag_color = "#F39C12"
        elif acc >= 55:
            insight = f"Desempeño por debajo del estándar. {c_data['correct']}/{c_data['total']} correctas. Requiere capacitación estructurada."
            level_tag = "DÉBIL"
            tag_color = "#E67E22"
        else:
            insight = f"Brecha crítica de conocimiento. {c_data['correct']}/{c_data['total']} correctas. Riesgo operativo / de calidad. Prioridad alta de intervención."
            level_tag = "CRÍTICO"
            tag_color = "#E74C3C"

        cat_insights.append({
            "category": label,
            "accuracy": acc,
            "correct": c_data["correct"],
            "total": c_data["total"],
            "insight": insight,
            "tag": level_tag,
            "tag_color": tag_color,
        })

    # Training plan
    training_steps = []
    if critical_cats:
        for cat in critical_cats:
            label = CAT_LABELS_ES.get(cat, cat)
            step = _training_step(cat, label, "critical")
            training_steps.append(step)

    for cat in weak_cats:
        if cat not in critical_cats:
            label = CAT_LABELS_ES.get(cat, cat)
            step = _training_step(cat, label, "weak")
            training_steps.append(step)

    if not training_steps:
        training_steps.append({
            "priority": "MANTENIMIENTO",
            "color": "#1ABC9C",
            "area": "Todas las áreas",
            "duration": "Continua",
            "actions": [
                "Participar en sesiones mensuales de actualización técnica",
                "Documentar casos de proceso atípicos para base de conocimiento",
                "Fungir como mentor para personal de menor experiencia",
            ],
            "kpi": "Mantener OEE > 85% y scrap < 1.5%",
        })

    # General recommendations
    general_recs = []
    if passed:
        general_recs = [
            "Certificar competencias formalmente con el equipo de RRHH / Ingeniería.",
            "Asignar un proyecto de mejora como aplicación práctica del conocimiento.",
            "Programar re-evaluación en 6 meses para seguimiento de desarrollo.",
            "Considerar al candidato para roles de entrenador interno (Train-the-Trainer)." if pct >= 85 else "Inscribir en programa de desarrollo técnico avanzado.",
        ]
    else:
        weeks = 4 if level == "basic" else 6 if level == "medium" else 8
        general_recs = [
            f"Implementar plan de capacitación de {weeks} semanas con acompañamiento técnico.",
            "Asignar tutor / shadowing con técnico o ingeniero senior.",
            "Revisar y reforzar procedimientos estándar de operación (SOPs) en áreas críticas.",
            "Programar re-evaluación al concluir el plan de capacitación.",
            "Documentar el plan y dar seguimiento semanal con supervisor directo.",
        ]

    return {
        "passed": passed,
        "status_text": status_text,
        "status_color": status_color,
        "summary": " ".join(summary_lines),
        "cat_insights": cat_insights,
        "training_steps": training_steps,
        "general_recs": general_recs,
    }


def _training_step(cat: str, label: str, severity: str) -> dict:
    plans = {
        "Machine": {
            "actions": [
                "Identificación física de componentes en máquina real (husillo, barril, check ring, válvulas).",
                "Ejercicio práctico: cambio de boquilla y ajuste de termopar.",
                "Taller: lectura e interpretación de manómetros hidráulicos y alarmas de máquina.",
            ],
            "kpi": "Identificar ≥90% de componentes en evaluación práctica.",
        },
        "Process": {
            "actions": [
                "Revisión de los 4 parámetros primarios: Temp., Velocidad, Presión, Tiempo.",
                "Práctica de estudio científico VPT (Velocity-Pressure Transfer).",
                "Simulación de ajuste de proceso con defecto dado (ejercicio de diagnóstico).",
            ],
            "kpi": "Completar estudio VPT documentado sin asistencia.",
        },
        "Quality": {
            "actions": [
                "Sesión de reconocimiento visual de 12 defectos principales (catálogo físico).",
                "Ejercicio de causa-raíz: asignar ajuste de proceso correcto a cada defecto.",
                "Práctica con límites de muestra (boundary samples) en piso.",
            ],
            "kpi": "Identificar y diagnosticar ≥85% de defectos presentados.",
        },
        "Safety": {
            "actions": [
                "Entrenamiento obligatorio LOTO con candadeo físico supervisado.",
                "Simulacro de emergencia: derrame hidráulico y fuego eléctrico.",
                "Revisión de NOM-004-STPS y EPP requerido por tarea.",
            ],
            "kpi": "Aprobar lista de verificación de seguridad al 100%.",
        },
        "Materials": {
            "actions": [
                "Taller: diferencias entre amorfos y semicristalinos (PP, ABS, PC, PA, POM).",
                "Práctica de secado correcto: temperatura, tiempo y punto de rocío.",
                "Identificación visual de material degradado, húmedo y contaminado.",
            ],
            "kpi": "Seleccionar condiciones de secado correctas para 5 materiales distintos.",
        },
        "Efficiency": {
            "actions": [
                "Cálculo de OEE con datos reales de turno (Disponibilidad × Desempeño × Calidad).",
                "Ejercicio SMED: clasificar actividades internas/externas en un cambio real.",
                "Análisis de tiempos muertos del mes y propuesta de contramedidas.",
            ],
            "kpi": "Calcular OEE y proponer mejora ≥5pp en área de oportunidad.",
        },
        "Waste": {
            "actions": [
                "Auditoría 5S en celda asignada con fotografía antes/después.",
                "Identificación de los 8 desperdicios (Muda) en un video de proceso real.",
                "Proyecto kaizen de 1 semana: eliminar un desperdicio identificado.",
            ],
            "kpi": "Completar kaizen con reducción documentada de ≥1 desperdicio.",
        },
        "Mold Engineering": {
            "actions": [
                "Revisión de anatomía de molde: canales de enfriamiento, compuertas, sistema de venteo.",
                "Ejercicio: cálculo de número de Reynolds para sistema de refrigeración.",
                "Análisis de caso: diagnóstico de pandeo/deformación usando principios de enfriamiento diferencial.",
            ],
            "kpi": "Resolver caso de estudio de ingeniería de molde documentado.",
        },
    }

    default_plan = plans.get(cat, {
        "actions": ["Revisión teórica con material de apoyo.", "Práctica supervisada.", "Evaluación de comprensión."],
        "kpi": "Superar 75% en re-evaluación del área.",
    })

    return {
        "priority": "CRÍTICO" if severity == "critical" else "MEJORA",
        "color": "#E74C3C" if severity == "critical" else "#F39C12",
        "area": label,
        "duration": "2 semanas" if severity == "critical" else "1 semana",
        "actions": default_plan["actions"],
        "kpi": default_plan["kpi"],
    }

# ─────────────────────────────────────────────────────────────────────────────
# PDF BUILDER
# ─────────────────────────────────────────────────────────────────────────────

def build_pdf(output_path: str, level: str, candidate: dict,
              results: dict, analysis: dict):

    meta = LEVEL_META[level]
    level_color = meta["color"]
    level_color_hex = meta["color_hex"]

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=1.8 * cm,
        rightMargin=1.8 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.8 * cm,
        title=f"Reporte CAROL – {candidate.get('full_name', 'Candidato')}",
        author="Sistema CAROL",
    )

    W = A4[0] - 3.6 * cm  # usable width

    styles = getSampleStyleSheet()

    def S(name, **kw):
        """Quick style builder."""
        base = styles.get(name, styles["Normal"])
        return ParagraphStyle(
            f"custom_{name}_{id(kw)}",
            parent=base,
            **kw,
        )

    title_style = S("Title",
                    fontSize=22, leading=28, textColor=BRAND["navy"],
                    fontName="Helvetica-Bold", alignment=TA_LEFT)
    h1_style = S("Heading1",
                 fontSize=14, leading=18, textColor=BRAND["navy"],
                 fontName="Helvetica-Bold", spaceBefore=14, spaceAfter=6)
    h2_style = S("Heading2",
                 fontSize=11, leading=14, textColor=BRAND["blue"],
                 fontName="Helvetica-Bold", spaceBefore=10, spaceAfter=4)
    body_style = S("Normal",
                   fontSize=9.5, leading=14, textColor=BRAND["black"],
                   fontName="Helvetica")
    small_style = S("Normal",
                    fontSize=8, leading=12, textColor=BRAND["gray"],
                    fontName="Helvetica")
    bold_style = S("Normal",
                   fontSize=9.5, leading=14, textColor=BRAND["black"],
                   fontName="Helvetica-Bold")
    caption_style = S("Normal",
                      fontSize=8.5, leading=12, textColor=BRAND["gray"],
                      fontName="Helvetica", alignment=TA_CENTER)

    story = []

    # ── HEADER BAND ──────────────────────────────────────────────────────────
    header_table_data = [[
        Paragraph(
            f"<font color='#FFFFFF'><b>CAROL</b></font> "
            f"<font color='#AAAAAA' size='10'>Assessment System</font>",
            S("Normal", fontSize=16, leading=20,
              textColor=BRAND["white"], fontName="Helvetica-Bold")
        ),
        Paragraph(
            f"<font color='#FFFFFF'><b>Nivel {meta['label']}</b></font><br/>"
            f"<font color='#AAAAAA' size='8'>{meta['role']}</font>",
            S("Normal", fontSize=12, leading=16,
              textColor=BRAND["white"], fontName="Helvetica",
              alignment=TA_RIGHT)
        ),
    ]]
    header_table = Table(header_table_data, colWidths=[W * 0.6, W * 0.4])
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BRAND["navy"]),
        ("TOPPADDING", (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("LEFTPADDING", (0, 0), (0, -1), 16),
        ("RIGHTPADDING", (-1, 0), (-1, -1), 16),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 10))

    # ── CANDIDATE INFO ROW ───────────────────────────────────────────────────
    candidate_rows = [
        [
            Paragraph("<b>Candidato</b>", bold_style),
            Paragraph(candidate.get("full_name", "—"), body_style),
            Paragraph("<b>ID Empleado</b>", bold_style),
            Paragraph(candidate.get("employee_id", "—"), body_style),
        ],
        [
            Paragraph("<b>Departamento</b>", bold_style),
            Paragraph(candidate.get("department", "—"), body_style),
            Paragraph("<b>Puesto</b>", bold_style),
            Paragraph(candidate.get("job_role", "—"), body_style),
        ],
        [
            Paragraph("<b>Fecha</b>", bold_style),
            Paragraph(candidate.get("date", date.today().strftime("%d/%m/%Y")), body_style),
            Paragraph("<b>Experiencia</b>", bold_style),
            Paragraph(f"{candidate.get('years_experience', '—')} años en moldeo", body_style),
        ],
    ]
    cw = [W * 0.18, W * 0.32, W * 0.18, W * 0.32]
    cand_table = Table(candidate_rows, colWidths=cw)
    cand_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BRAND["gray_lt"]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#DDE1E4")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1),
         [BRAND["gray_lt"], colors.white]),
    ]))
    story.append(cand_table)
    story.append(Spacer(1, 14))

    # ── SECTION 1: RESULTADO GENERAL ─────────────────────────────────────────
    story.append(Paragraph("1. Resultado General", h1_style))
    story.append(HRFlowable(width=W, thickness=2, color=level_color, spaceAfter=8))

    # Donut + KPI cards side by side
    donut_bytes = make_donut_chart(results["pct"], analysis["passed"], level_color_hex)
    donut_img = Image(io.BytesIO(donut_bytes), width=4.5 * cm, height=4.5 * cm)

    passed_color = BRAND["teal"] if analysis["passed"] else BRAND["red"]
    status_label = "APROBADO ✓" if analysis["passed"] else "NO APROBADO ✗"

    kpi_data = [
        [Paragraph(f"<b>Puntaje obtenido</b>", caption_style),
         Paragraph(f"<b>Puntaje máximo</b>", caption_style),
         Paragraph(f"<b>Mínimo aprobatorio</b>", caption_style),
         Paragraph(f"<b>Resultado</b>", caption_style)],
        [
            Paragraph(f"<font size='18' color='#1B4F72'><b>{results['total_earned']:.1f}</b></font>",
                      S("Normal", alignment=TA_CENTER, fontSize=18, fontName="Helvetica-Bold")),
            Paragraph(f"<font size='18' color='#7F8C8D'><b>{results['total_max']:.1f}</b></font>",
                      S("Normal", alignment=TA_CENTER, fontSize=18, fontName="Helvetica-Bold")),
            Paragraph(f"<font size='18' color='#E74C3C'><b>{meta['pass_pct']}%</b></font>",
                      S("Normal", alignment=TA_CENTER, fontSize=18, fontName="Helvetica-Bold")),
            Paragraph(f"<b>{status_label}</b>",
                      S("Normal", alignment=TA_CENTER, fontSize=10,
                        fontName="Helvetica-Bold",
                        textColor=BRAND["teal"] if analysis["passed"] else BRAND["red"])),
        ],
    ]

    kpi_col_w = [(W - 5 * cm) / 4] * 4
    kpi_table = Table(kpi_data, colWidths=kpi_col_w)
    kpi_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BRAND["navy"]),
        ("TEXTCOLOR", (0, 0), (-1, 0), BRAND["white"]),
        ("BACKGROUND", (0, 1), (-1, 1), colors.white),
        ("BOX", (0, 0), (-1, -1), 1, BRAND["gray"]),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#DDE1E4")),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    result_row = [[donut_img, kpi_table]]
    result_layout = Table(result_row, colWidths=[5.2 * cm, W - 5.2 * cm])
    result_layout.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (0, 0), 0),
        ("LEFTPADDING", (1, 0), (1, 0), 8),
    ]))
    story.append(result_layout)
    story.append(Spacer(1, 12))

    # Summary box
    summary_para = Paragraph(analysis["summary"], body_style)
    summary_table = Table([[summary_para]], colWidths=[W])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1),
         BRAND["teal_lt"] if analysis["passed"] else BRAND["red_lt"]),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("BOX", (0, 0), (-1, -1), 2,
         BRAND["teal"] if analysis["passed"] else BRAND["red"]),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 16))

    # ── SECTION 2: ANÁLISIS POR ÁREA ─────────────────────────────────────────
    story.append(Paragraph("2. Análisis por Área de Conocimiento", h1_style))
    story.append(HRFlowable(width=W, thickness=2, color=level_color, spaceAfter=10))

    # Charts: pie + radar side by side
    pie_bytes = make_pie_chart(results["categories"])
    radar_bytes = make_category_radar(results["categories"], CAT_COLORS_HEX)

    pie_img = Image(io.BytesIO(pie_bytes), width=W * 0.64, height=4.8 * cm)
    radar_img = Image(io.BytesIO(radar_bytes), width=W * 0.34, height=4.8 * cm)

    chart_row = [[pie_img, radar_img]]
    chart_layout = Table(chart_row, colWidths=[W * 0.65, W * 0.35])
    chart_layout.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(chart_layout)
    story.append(Spacer(1, 6))
    story.append(Paragraph("Figura 1. Distribución de puntos y porcentaje de aciertos por área. La línea roja discontinua indica el umbral de aprobación (75%).", caption_style))
    story.append(Spacer(1, 14))

    # Category detail table
    cat_header = [
        Paragraph("<b>Área</b>", S("Normal", fontName="Helvetica-Bold",
                                   fontSize=8.5, textColor=BRAND["white"], alignment=TA_CENTER)),
        Paragraph("<b>Correctas</b>", S("Normal", fontName="Helvetica-Bold",
                                        fontSize=8.5, textColor=BRAND["white"], alignment=TA_CENTER)),
        Paragraph("<b>Total</b>", S("Normal", fontName="Helvetica-Bold",
                                    fontSize=8.5, textColor=BRAND["white"], alignment=TA_CENTER)),
        Paragraph("<b>% Acierto</b>", S("Normal", fontName="Helvetica-Bold",
                                         fontSize=8.5, textColor=BRAND["white"], alignment=TA_CENTER)),
        Paragraph("<b>Pts. Obtenidos</b>", S("Normal", fontName="Helvetica-Bold",
                                              fontSize=8.5, textColor=BRAND["white"], alignment=TA_CENTER)),
        Paragraph("<b>Pts. Máximos</b>", S("Normal", fontName="Helvetica-Bold",
                                            fontSize=8.5, textColor=BRAND["white"], alignment=TA_CENTER)),
        Paragraph("<b>Estado</b>", S("Normal", fontName="Helvetica-Bold",
                                     fontSize=8.5, textColor=BRAND["white"], alignment=TA_CENTER)),
    ]
    cat_rows = [cat_header]

    # Build reverse lookup: Spanish label -> raw key in results["categories"]
    label_to_key = {}
    for raw_key in results["categories"]:
        es_label = CAT_LABELS_ES.get(raw_key, raw_key)
        label_to_key[es_label] = raw_key
        label_to_key[raw_key] = raw_key

    for ci in analysis["cat_insights"]:
        pct_c = ci["accuracy"]
        tag_color = colors.HexColor(ci["tag_color"])

        raw_key = label_to_key.get(ci["category"], None)
        if raw_key and raw_key in results["categories"]:
            earned_str = f"{results['categories'][raw_key]['earned']:.1f}"
            max_str    = f"{results['categories'][raw_key]['max']:.1f}"
        else:
            earned_str = "—"
            max_str    = "—"

        row = [
            Paragraph(ci["category"],
                      S("Normal", fontName="Helvetica-Bold", fontSize=8.5)),
            Paragraph(str(ci["correct"]),
                      S("Normal", fontSize=8.5, alignment=TA_CENTER)),
            Paragraph(str(ci["total"]),
                      S("Normal", fontSize=8.5, alignment=TA_CENTER)),
            Paragraph(f"{pct_c:.1f}%",
                      S("Normal", fontSize=8.5, alignment=TA_CENTER,
                        fontName="Helvetica-Bold",
                        textColor=BRAND["teal"] if pct_c >= 75 else BRAND["red"])),
            Paragraph(earned_str,
                      S("Normal", fontSize=8.5, alignment=TA_CENTER)),
            Paragraph(max_str,
                      S("Normal", fontSize=8.5, alignment=TA_CENTER)),
            Paragraph(f"<b>{ci['tag']}</b>",
                      S("Normal", fontSize=8, alignment=TA_CENTER,
                        fontName="Helvetica-Bold",
                        textColor=tag_color)),
        ]
        cat_rows.append(row)

    col_w = [W * 0.20, W * 0.10, W * 0.07, W * 0.12, W * 0.13, W * 0.13, W * 0.13]  # adjusted
    cat_table = Table(cat_rows, colWidths=col_w, repeatRows=1)
    cat_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BRAND["navy"]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#DDE1E4")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, BRAND["gray_lt"]]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(cat_table)
    story.append(Spacer(1, 16))

    # ── SECTION 3: ANÁLISIS DETALLADO ────────────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph("3. Diagnóstico Detallado por Área", h1_style))
    story.append(HRFlowable(width=W, thickness=2, color=level_color, spaceAfter=10))

    type_bar_bytes = make_question_type_bar(results["answers"])
    type_bar_img = Image(io.BytesIO(type_bar_bytes), width=7 * cm, height=4.5 * cm)

    story.append(Paragraph("3.1 Desempeño Teórico vs Práctico", h2_style))
    story.append(type_bar_img)
    story.append(Paragraph("Figura 2. Porcentaje de aciertos separado por tipo de pregunta.", caption_style))
    story.append(Spacer(1, 12))

    story.append(Paragraph("3.2 Diagnóstico por Área", h2_style))

    for ci in analysis["cat_insights"]:
        tag_color_rl = colors.HexColor(ci["tag_color"])
        # Category insight card
        card_data = [[
            Paragraph(f"<b>{ci['category']}</b>  "
                      f"<font size='8' color='{ci['tag_color']}'><b>[{ci['tag']}]</b></font>",
                      S("Normal", fontSize=10, fontName="Helvetica-Bold")),
            Paragraph(f"<b>{ci['accuracy']:.1f}%</b>  ({ci['correct']}/{ci['total']})",
                      S("Normal", fontSize=10, fontName="Helvetica-Bold",
                        alignment=TA_RIGHT,
                        textColor=BRAND["teal"] if ci["accuracy"] >= 75 else BRAND["red"])),
        ], [
            Paragraph(ci["insight"], body_style),
            Paragraph(""),
        ]]
        card = Table(card_data, colWidths=[W * 0.75, W * 0.25])
        card.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), BRAND["gray_lt"]),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#DDE1E4")),
            ("LEFTPADDING", (0, 0), (0, -1), 14),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("SPAN", (0, 1), (1, 1)),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        story.append(card)
        story.append(Spacer(1, 5))

    story.append(Spacer(1, 10))

    # ── SECTION 4: REVISIÓN DE RESPUESTAS ────────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph("4. Revisión de Respuestas", h1_style))
    story.append(HRFlowable(width=W, thickness=2, color=level_color, spaceAfter=8))
    story.append(Paragraph(
        "Detalle de respuestas marcadas y respuestas correctas para auditoría y seguimiento.",
        body_style))
    story.append(Spacer(1, 10))

    # Group by category
    answers_by_cat = {}
    for a in results["answers"]:
        c = a["category"]
        answers_by_cat.setdefault(c, []).append(a)

    q_num = 1
    for cat, answers in answers_by_cat.items():
        story.append(Paragraph(CAT_LABELS_ES.get(cat, cat), h2_style))
        for a in answers:
            q_block = []
            status_text = "Correcta" if a["correct"] else "Incorrecta"
            status_color = "#1ABC9C" if a["correct"] else "#E74C3C"
            q_block.append(Paragraph(
                f"<b>P{q_num}.</b> <font color='{status_color}'>[{status_text}]</font> {a['question']}",
                S("Normal", fontSize=9, leading=13, fontName="Helvetica-Bold")
            ))
            q_block.append(Spacer(1, 3))

            # Options
            opt_rows = []
            for idx, opt in enumerate(a["options"]):
                if idx == a["correct_index"]:
                    marker = "✓"
                    opt_color = "#1ABC9C"
                    opt_font = "Helvetica-Bold"
                elif idx == a["chosen_index"]:
                    marker = "✗"
                    opt_color = "#E74C3C"
                    opt_font = "Helvetica"
                else:
                    marker = "○"
                    opt_color = "#7F8C8D"
                    opt_font = "Helvetica"

                opt_rows.append([
                    Paragraph(f"<font color='{opt_color}'><b>{marker}</b></font>",
                              S("Normal", fontSize=9, fontName="Helvetica-Bold",
                                alignment=TA_CENTER)),
                    Paragraph(f"<font color='{opt_color}' face='{opt_font}'>{opt}</font>",
                              S("Normal", fontSize=8.5, fontName=opt_font,
                                textColor=colors.HexColor(opt_color))),
                ])

            opt_table = Table(opt_rows, colWidths=[0.5 * cm, W - 1.5 * cm])
            opt_table.setStyle(TableStyle([
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]))
            q_block.append(opt_table)
            q_block.append(Spacer(1, 3))

            # Reasoning
            reason_para = Paragraph(
                f"<i><font color='#1B4F72'>💡 {a['reasoning']}</font></i>",
                S("Normal", fontSize=8.5, leading=12,
                  leftIndent=10, rightIndent=10)
            )
            q_block.append(reason_para)
            q_block.append(Spacer(1, 8))

            story.extend(q_block)
            q_num += 1

    # ── SECTION 5: PLAN DE ACCIÓN ─────────────────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph("5. Plan de Acción y Recomendaciones", h1_style))
    story.append(HRFlowable(width=W, thickness=2, color=level_color, spaceAfter=10))

    story.append(Paragraph("5.1 Plan de Capacitación Priorizado", h2_style))

    for step in analysis["training_steps"]:
        priority_color = colors.HexColor(step["color"])

        # Header row
        step_header = Table(
            [[
                Paragraph(f"<font color='white'><b>  {step['priority']}  </b></font>",
                          S("Normal", fontSize=9, fontName="Helvetica-Bold",
                            textColor=BRAND["white"])),
                Paragraph(f"<b>Área: {step['area']}</b>",
                          S("Normal", fontSize=10, fontName="Helvetica-Bold")),
                Paragraph(f"Duración estimada: <b>{step['duration']}</b>",
                          S("Normal", fontSize=9, alignment=TA_RIGHT)),
            ]],
            colWidths=[2.5 * cm, W * 0.55, W * 0.25]
        )
        step_header.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), priority_color),
            ("BACKGROUND", (1, 0), (-1, 0), BRAND["gray_lt"]),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BOX", (0, 0), (-1, -1), 1, priority_color),
        ]))
        story.append(step_header)

        # Actions
        action_items = []
        for i, action in enumerate(step["actions"], 1):
            action_items.append([
                Paragraph(f"<b>{i}.</b>",
                          S("Normal", fontSize=8.5, fontName="Helvetica-Bold",
                            alignment=TA_CENTER)),
                Paragraph(action, S("Normal", fontSize=8.5)),
            ])

        actions_table = Table(action_items, colWidths=[0.6 * cm, W - 0.6 * cm])
        actions_table.setStyle(TableStyle([
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BACKGROUND", (0, 0), (-1, -1), colors.white),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#DDE1E4")),
        ]))
        story.append(actions_table)

        # KPI row
        kpi_table = Table(
            [[Paragraph(f"<b>KPI de éxito:</b> {step['kpi']}",
                        S("Normal", fontSize=8.5, fontName="Helvetica"))]],
            colWidths=[W]
        )
        kpi_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), BRAND["amber_lt"]),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("BOX", (0, 0), (-1, -1), 0.5, BRAND["amber"]),
        ]))
        story.append(kpi_table)
        story.append(Spacer(1, 10))

    story.append(Spacer(1, 8))
    story.append(Paragraph("5.2 Recomendaciones Generales", h2_style))

    for i, rec in enumerate(analysis["general_recs"], 1):
        rec_row = Table(
            [[
                Paragraph(f"<b>{i}</b>",
                          S("Normal", fontSize=11, fontName="Helvetica-Bold",
                            textColor=BRAND["white"], alignment=TA_CENTER)),
                Paragraph(rec, body_style),
            ]],
            colWidths=[0.8 * cm, W - 0.8 * cm]
        )
        rec_row.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), level_color),
            ("BACKGROUND", (1, 0), (1, 0), colors.white),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#DDE1E4")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        story.append(rec_row)
        story.append(Spacer(1, 4))

    # ── FOOTER SIGNATURE ─────────────────────────────────────────────────────
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width=W, thickness=1,
                             color=BRAND["gray"], spaceAfter=10))

    sig_data = [[
        Paragraph(
            f"Reporte generado por <b>CAROL Assessment System</b><br/>"
            f"<font size='7' color='#7F8C8D'>"
            f"Fecha de emisión: {datetime.now().strftime('%d/%m/%Y %H:%M')} | "
            f"Nivel: {meta['label']} | Confidencial</font>",
            S("Normal", fontSize=8, leading=12, textColor=BRAND["gray"])
        ),
        Paragraph(
            "Firma del Evaluador<br/><br/>"
            "_______________________<br/>"
            "<font size='7'>Nombre y cargo</font>",
            S("Normal", fontSize=8, leading=12,
              textColor=BRAND["gray"], alignment=TA_CENTER)
        ),
    ]]
    sig_table = Table(sig_data, colWidths=[W * 0.65, W * 0.35])
    sig_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(sig_table)

    # ── BUILD ─────────────────────────────────────────────────────────────────
    def on_page(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(BRAND["navy"])
        canvas.rect(0, 0, A4[0], 0.5 * cm, fill=1, stroke=0)
        canvas.setFillColor(BRAND["white"])
        canvas.setFont("Helvetica", 7)
        canvas.drawCentredString(
            A4[0] / 2, 0.15 * cm,
            f"CAROL | {candidate.get('full_name', '')} | Página {doc.page}"
        )
        canvas.restoreState()

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"✅ PDF generado: {output_path}")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="CAROL Report Generator")
    parser.add_argument("--level", choices=["basic", "medium", "advanced"],
                        default="medium")
    parser.add_argument("--output", default="reports/carol_report.pdf")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    # Get script directory to find assessments relative to it
    script_dir = os.path.dirname(os.path.abspath(__file__))
    assessments_dir = os.path.join(script_dir, "..", "assessments")

    file_map = {
        "basic":    os.path.join(assessments_dir, "carol_basic_prod.json"),
        "medium":   os.path.join(assessments_dir, "carol_medium_prod.json"),
        "advanced": os.path.join(assessments_dir, "carol_advanced_prod.json"),
    }

    with open(file_map[args.level]) as f:
        questions = json.load(f)

    # Sample candidate
    candidate = {
        "full_name": "M. Gallegos",
        "employee_id": "EMP-2247",
        "department": "Producción",
        "job_role": "Técnico de Procesos",
        "years_experience": "6",
        "date": datetime.now().strftime("%d/%m/%Y"),
    }

    results = generate_sample_results(questions, seed=args.seed)
    analysis = generate_ai_analysis(results, args.level, candidate)

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    build_pdf(args.output, args.level, candidate, results, analysis)

    print(f"   Puntaje: {results['total_earned']:.1f}/{results['total_max']:.1f} ({results['pct']}%)")
    print(f"   Estado:  {analysis['status_text']}")


if __name__ == "__main__":
    main()
