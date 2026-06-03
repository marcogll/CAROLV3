#!/usr/bin/env python3
"""
CAROL Unified Senior Engineer Report
Generates a single PDF covering all three assessment levels with:
  • Executive cross-level dashboard (cover + summary)
  • Per-level breakdown with charts, category tables, diagnostics
  • Consolidated action plan and wrong-question review
Usage:
    python generate_unified_report.py [--output path.pdf] [--seed N]
"""

import json, random, math, io, os, sys, argparse
from datetime import datetime, date

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether, CondPageBreak,
)

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
PW, PH = A4
MARGIN = 1.6 * cm
W = PW - 2 * MARGIN          # usable page width

BRAND = {
    "navy":      colors.HexColor("#0D1B2A"),
    "blue":      colors.HexColor("#1B4F72"),
    "teal":      colors.HexColor("#00B894"),
    "teal_lt":   colors.HexColor("#D0F0EA"),
    "amber":     colors.HexColor("#E67E22"),
    "amber_lt":  colors.HexColor("#FEF0E3"),
    "red":       colors.HexColor("#C0392B"),
    "red_lt":    colors.HexColor("#FDECEA"),
    "purple":    colors.HexColor("#6C3483"),
    "gray":      colors.HexColor("#7F8C8D"),
    "gray_lt":   colors.HexColor("#F0F3F4"),
    "gray_md":   colors.HexColor("#D5D8DC"),
    "white":     colors.white,
    "ink":       colors.HexColor("#1C2833"),
}

# Get script directory to find assessments relative to it
_script_dir = os.path.dirname(os.path.abspath(__file__))
_assessments_dir = os.path.join(_script_dir, "..", "assessments")

LEVEL = {
    "basic": {
        "label": "Básico",  "role": "Operadores de Piso",
        "pass_pct": 75,     "time_min": 50,
        "hex": "#00B894",   "rl": colors.HexColor("#00B894"),
        "lt": colors.HexColor("#D0F0EA"),
        "file": os.path.join(_assessments_dir, "carol_basic_prod.json"),
    },
    "medium": {
        "label": "Medio",   "role": "Técnicos de Proceso",
        "pass_pct": 75,     "time_min": 60,
        "hex": "#E67E22",   "rl": colors.HexColor("#E67E22"),
        "lt": colors.HexColor("#FEF0E3"),
        "file": os.path.join(_assessments_dir, "carol_medium_prod.json"),
    },
    "advanced": {
        "label": "Avanzado","role": "Ingenieros y Líderes",
        "pass_pct": 80,     "time_min": 75,
        "hex": "#1B4F72",   "rl": colors.HexColor("#1B4F72"),
        "lt": colors.HexColor("#D6EAF8"),
        "file": os.path.join(_assessments_dir, "carol_advanced_prod.json"),
    },
}

CAT_HEX = {
    "Machine": "#1B4F72", "Process": "#00B894",
    "Quality": "#E67E22", "Safety":  "#C0392B",
    "Materials": "#8E44AD","Efficiency":"#2980B9",
    "Waste": "#27AE60",   "Mold Engineering": "#D35400",
}
CAT_ES = {
    "Machine": "Máquina", "Process": "Proceso",
    "Quality": "Calidad", "Safety":  "Seguridad",
    "Materials": "Materiales","Efficiency":"Eficiencia",
    "Waste": "Desperdicios","Mold Engineering":"Ing. Moldes",
}

# ─────────────────────────────────────────────────────────────────────────────
# STYLE FACTORY
# ─────────────────────────────────────────────────────────────────────────────
_styles = getSampleStyleSheet()
_sid = 0

def S(base="Normal", **kw):
    global _sid
    _sid += 1
    parent = _styles.get(base, _styles["Normal"])
    return ParagraphStyle(f"_s{_sid}", parent=parent, **kw)

def P(text, **kw):
    return Paragraph(text, S(**kw))

# ─────────────────────────────────────────────────────────────────────────────
# DATA SIMULATION
# ─────────────────────────────────────────────────────────────────────────────

def simulate(questions, seed):
    rng = random.Random(seed)
    cat_acc = {
        "Machine": rng.uniform(.58,.88), "Process": rng.uniform(.48,.80),
        "Quality": rng.uniform(.60,.90), "Safety":  rng.uniform(.68,.95),
        "Materials": rng.uniform(.38,.75),"Efficiency":rng.uniform(.52,.85),
        "Waste": rng.uniform(.58,.88),   "Mold Engineering":rng.uniform(.33,.70),
    }
    answers = []
    for q in questions:
        acc = cat_acc.get(q["category"], .65)
        correct = rng.random() < acc
        if correct:
            chosen = q["correct_index"]
        else:
            opts = [i for i in range(len(q["options"])) if i != q["correct_index"]]
            chosen = rng.choice(opts)
        answers.append({
            "id": q["id"], "category": q["category"], "type": q["type"],
            "question": q["question"], "options": q["options"],
            "correct_index": q["correct_index"], "chosen_index": chosen,
            "correct": correct,
            "score_earned": q["score"] if correct else 0,
            "score_max": q["score"], "reasoning": q["reasoning"],
        })
    cats = {}
    for a in answers:
        c = a["category"]
        cats.setdefault(c, {"correct":0,"total":0,"earned":0.0,"max":0.0})
        cats[c]["total"] += 1
        cats[c]["max"] += a["score_max"]
        if a["correct"]:
            cats[c]["correct"] += 1
            cats[c]["earned"] += a["score_earned"]
    earned = sum(a["score_earned"] for a in answers)
    mx     = sum(a["score_max"]    for a in answers)
    return {"answers": answers, "categories": cats,
            "earned": earned, "max": mx, "pct": round(earned/mx*100,1)}

# ─────────────────────────────────────────────────────────────────────────────
# CHART HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _png(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    buf.seek(0); plt.close(fig)
    return buf


# ── 1. Three-level summary bar chart ─────────────────────────────────────────
def chart_level_bars(all_results):
    labels  = [LEVEL[k]["label"] for k in ("basic","medium","advanced")]
    pcts    = [all_results[k]["pct"] for k in ("basic","medium","advanced")]
    passes  = [LEVEL[k]["pass_pct"] for k in ("basic","medium","advanced")]
    bar_clr = [LEVEL[k]["hex"] for k in ("basic","medium","advanced")]

    fig, ax = plt.subplots(figsize=(5.5, 2.6), facecolor="none")
    ax.set_facecolor("#FAFBFC")
    x = np.arange(3)
    bars = ax.bar(x, pcts, width=.46, color=bar_clr, zorder=3,
                  edgecolor="white", linewidth=1.5)
    for bar, pct, pp in zip(bars, pcts, passes):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1.8,
                f"{pct:.1f}%", ha="center", va="bottom",
                fontsize=10, fontweight="bold", color="#1C2833")
        ax.plot([bar.get_x(), bar.get_x()+bar.get_width()],
                [pp, pp], "--", color="#C0392B", lw=1.3, zorder=4)
    ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=10, fontweight="bold")
    ax.set_ylim(0, 115); ax.set_ylabel("% Puntaje", fontsize=9)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linestyle="--", alpha=.35, zorder=0)
    ax.set_title("Resultado por Nivel", fontsize=11, fontweight="bold", color="#0D1B2A", pad=8)
    fig.tight_layout(pad=.6)
    return _png(fig)


# ── 2. Heatmap: all categories × all levels ──────────────────────────────────
def chart_heatmap(all_results):
    levels = ["basic","medium","advanced"]
    # Collect union of categories (ordered)
    cat_order = ["Machine","Process","Quality","Safety","Materials","Efficiency","Waste","Mold Engineering"]
    # Rows = levels, cols = cats
    data = np.full((len(levels), len(cat_order)), np.nan)
    for ri, lk in enumerate(levels):
        cats = all_results[lk]["categories"]
        for ci, cat in enumerate(cat_order):
            if cat in cats:
                data[ri, ci] = cats[cat]["correct"]/cats[cat]["total"]*100

    fig, ax = plt.subplots(figsize=(8.5, 2.2), facecolor="none")
    ax.set_facecolor("none")
    cmap = plt.cm.RdYlGn
    cmap.set_bad("#ECECEC")
    im = ax.imshow(data, aspect="auto", cmap=cmap, vmin=0, vmax=100)

    ax.set_xticks(range(len(cat_order)))
    ax.set_xticklabels([CAT_ES.get(c,c) for c in cat_order], fontsize=8.5, fontweight="bold")
    ax.set_yticks(range(len(levels)))
    ax.set_yticklabels([LEVEL[k]["label"] for k in levels], fontsize=8.5, fontweight="bold")
    ax.tick_params(length=0)

    for ri in range(len(levels)):
        for ci in range(len(cat_order)):
            val = data[ri, ci]
            if not np.isnan(val):
                txt_c = "white" if val < 45 or val > 80 else "#1C2833"
                ax.text(ci, ri, f"{val:.0f}%", ha="center", va="center",
                        fontsize=8, fontweight="bold", color=txt_c)

    cbar = fig.colorbar(im, ax=ax, orientation="vertical",
                        fraction=0.025, pad=0.02)
    cbar.ax.tick_params(labelsize=7)
    cbar.set_label("% Aciertos", fontsize=7)
    ax.set_title("Mapa de Calor: Aciertos por Área y Nivel", fontsize=10,
                 fontweight="bold", color="#0D1B2A", pad=6)
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.tight_layout(pad=.5)
    return _png(fig)


# ── 3. Radar per level ────────────────────────────────────────────────────────
def chart_radar(cats, color_hex):
    labels  = [CAT_ES.get(c, c) for c in cats]
    values  = [cats[c]["correct"]/cats[c]["total"]*100 for c in cats]
    N = len(labels)
    angles  = [n/N*2*math.pi for n in range(N)]
    angles += angles[:1]
    vals    = values + values[:1]

    fig, ax = plt.subplots(figsize=(3.6, 3.6), subplot_kw=dict(polar=True), facecolor="none")
    ax.set_facecolor("#F8FAFB")
    ax.set_theta_offset(math.pi/2); ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=7.5, fontweight="bold", color="#1C2833")
    ax.set_ylim(0,100)
    ax.set_yticks([25,50,75,100])
    ax.set_yticklabels(["25","50","75","100"], fontsize=6.5, color="#AAB0B7")
    ax.yaxis.grid(True, color="#DDE1E4", linestyle="--", lw=.7)
    ax.xaxis.grid(True, color="#DDE1E4", linestyle="-",  lw=.4)
    ax.plot(angles, vals, "o-", lw=2, color=color_hex, markersize=4)
    ax.fill(angles, vals, alpha=.18, color=color_hex)
    ax.plot(angles, [75]*(N+1), "--", lw=1, color="#C0392B", alpha=.6)
    fig.tight_layout(pad=.3)
    return _png(fig)


# ── 4. Horizontal category bars (compact) ────────────────────────────────────
def chart_cat_bars(cats, color_hex, pass_pct=75):
    labels = [CAT_ES.get(c,c) for c in cats]
    pcts   = [cats[c]["correct"]/cats[c]["total"]*100 for c in cats]
    clrs   = [CAT_HEX.get(c,"#95A5A6") for c in cats]

    fig, ax = plt.subplots(figsize=(4.2, max(2.2, len(labels)*0.38)), facecolor="none")
    ax.set_facecolor("#FAFBFC")
    y = np.arange(len(labels))
    bars = ax.barh(y, pcts, height=.52, color=clrs, edgecolor="white", lw=.8, zorder=3)
    ax.barh(y, [100-p for p in pcts], height=.52, left=pcts,
            color="#E8EAED", edgecolor="white", lw=.8, zorder=3)
    for bar, p in zip(bars, pcts):
        ax.text(p/2, bar.get_y()+bar.get_height()/2,
                f"{p:.0f}%", ha="center", va="center",
                fontsize=7.5, fontweight="bold", color="white")
    ax.axvline(pass_pct, color="#C0392B", lw=1.3, linestyle="--", alpha=.8, zorder=4)
    ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=8)
    ax.set_xlim(0,100); ax.invert_yaxis()
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.grid(axis="x", linestyle="--", alpha=.3, zorder=0)
    ax.tick_params(axis="x", labelsize=7.5)
    fig.tight_layout(pad=.5)
    return _png(fig)


# ── 5. Donut ─────────────────────────────────────────────────────────────────
def chart_donut(pct, color_hex):
    fig, ax = plt.subplots(figsize=(2.5, 2.5), facecolor="none")
    ax.set_facecolor("none")
    ax.pie([pct, 100-pct], colors=[color_hex, "#E8EAED"],
           startangle=90, counterclock=False,
           wedgeprops=dict(width=.36, edgecolor="white", linewidth=1.5))
    ax.text(0, 0.06, f"{pct:.1f}%", ha="center", va="center",
            fontsize=16, fontweight="bold", color="#1C2833")
    ax.set(aspect="equal")
    fig.tight_layout(pad=0)
    return _png(fig)


# ── 6. Overall gauge (big donut for cover) ───────────────────────────────────
def chart_overall_gauge(all_results):
    """Triple-ring donut: outer=basic, mid=medium, inner=advanced."""
    levels = ["basic", "medium", "advanced"]
    pcts   = [all_results[k]["pct"] for k in levels]
    clrs   = [LEVEL[k]["hex"] for k in levels]

    fig, ax = plt.subplots(figsize=(4.5, 4.5), facecolor="none")
    ax.set_facecolor("none")

    radii  = [1.0, 0.72, 0.44]
    widths = [0.22, 0.22, 0.22]

    for (r, w, p, c, lk) in zip(radii, widths, pcts, clrs, levels):
        ax.pie([p, 100-p], colors=[c, "#E8EAED"],
               startangle=90, counterclock=False,
               radius=r, wedgeprops=dict(width=w, edgecolor="white", linewidth=2))

    # Labels
    for i, (lk, r, p) in enumerate(zip(levels, [1.11, 0.83, 0.55], pcts)):
        angle = 90 - (p/100)*360/2   # midpoint angle of filled arc
        ax.text(0, r*0.95 - 0.88 + i*0.3,  # stack them vertically in center area
                f"{LEVEL[lk]['label']}: {p:.1f}%",
                ha="center", va="center", fontsize=8,
                fontweight="bold", color=LEVEL[lk]["hex"])

    ax.set(aspect="equal")
    ax.text(0, -1.45, "CAROL — Vista Global", ha="center", va="center",
            fontsize=9, color="#7F8C8D")
    fig.tight_layout(pad=0)
    return _png(fig)


# ─────────────────────────────────────────────────────────────────────────────
# AI ANALYSIS (rule-based)
# ─────────────────────────────────────────────────────────────────────────────

def ai_analysis(results, level_key, name):
    meta = LEVEL[level_key]
    cats = results["categories"]
    pct  = results["pct"]
    passed = pct >= meta["pass_pct"]

    cat_pcts = {c: cats[c]["correct"]/cats[c]["total"]*100 for c in cats}
    sorted_cats = sorted(cat_pcts.items(), key=lambda x: x[1])
    weak     = [c for c,p in sorted_cats if p < 70]
    critical = [c for c,p in sorted_cats if p < 55]
    strong   = [c for c,p in sorted_cats if p >= 82]

    # Status
    gap = pct - meta["pass_pct"]
    if passed:
        if pct >= 90:
            verdict = f"Desempeño sobresaliente ({pct:.1f}%). Capacidad de operar y entrenar de forma autónoma."
        elif pct >= 80:
            verdict = f"Aprobado con margen sólido ({pct:.1f}%). Domina la mayoría de competencias del nivel."
        else:
            verdict = f"Aprobado ajustado ({pct:.1f}%), {abs(gap):.1f}pp sobre el mínimo. Refuerzo puntual recomendado."
    else:
        verdict = f"No aprobado ({pct:.1f}%), {abs(gap):.1f}pp por debajo del umbral ({meta['pass_pct']}%). Requiere plan de capacitación."

    # Per-cat tags
    insights = []
    for cat, p in sorted_cats:
        label = CAT_ES.get(cat, cat)
        cd = cats[cat]
        if p >= 85:   tag,tc = "FORTALEZA", "#00B894"
        elif p >= 70: tag,tc = "ACEPTABLE", "#E67E22"
        elif p >= 55: tag,tc = "DÉBIL",     "#D35400"
        else:         tag,tc = "CRÍTICO",   "#C0392B"

        if p >= 85:   note = f"Dominio sólido. Puede mentorear en esta área."
        elif p >= 70: note = f"Competencia funcional; refuerzo práctico recomendado."
        elif p >= 55: note = f"Brecha técnica. Necesita capacitación estructurada ({cd['correct']}/{cd['total']} correctas)."
        else:         note = f"Brecha crítica. Riesgo operativo. Intervención prioritaria ({cd['correct']}/{cd['total']} correctas)."

        insights.append({"cat": label, "pct": p, "tag": tag, "tc": tc,
                          "note": note, "correct": cd["correct"], "total": cd["total"]})

    # Training steps
    steps = []
    ACTION_PLANS = {
        "Machine":    ["Identificación física de componentes en máquina real.",
                       "Práctica: lectura de manómetros hidráulicos y alarmas.",
                       "Ejercicio de ajuste de termopar y boquilla."],
        "Process":    ["Revisión de parámetros primarios (T, V, P, t).",
                       "Estudio VPT guiado en máquina real.",
                       "Simulación de diagnóstico con defecto dado."],
        "Quality":    ["Catálogo de 12 defectos con muestra física (boundary samples).",
                       "Ejercicio causa-raíz: ajuste de proceso por defecto.",
                       "Revisión de SPC y cartas de control en línea."],
        "Safety":     ["Entrenamiento LOTO con candadeo físico supervisado.",
                       "Simulacro: derrame hidráulico y fuego eléctrico.",
                       "Revisión NOM-004-STPS y EPP por tarea."],
        "Materials":  ["Taller amorfos vs semicristalinos (PP, ABS, PC, PA, POM).",
                       "Práctica de secado: temperatura, tiempo, punto de rocío.",
                       "Identificación visual: degradado, húmedo, contaminado."],
        "Efficiency": ["Cálculo OEE con datos reales de turno.",
                       "SMED: clasificar actividades internas/externas en cambio real.",
                       "Análisis de tiempos muertos + contramedidas."],
        "Waste":      ["Auditoría 5S en celda con foto antes/después.",
                       "Identificación 8 Mudas en video de proceso real.",
                       "Kaizen de 1 semana: eliminar un desperdicio documentado."],
        "Mold Engineering": ["Anatomía de molde: canales, compuertas, venteos.",
                             "Cálculo N° Reynolds para sistema de refrigeración.",
                             "Caso: diagnóstico de pandeo por enfriamiento diferencial."],
    }
    KPI = {
        "Machine":"≥90% en evaluación práctica de componentes.",
        "Process":"Completar estudio VPT documentado sin asistencia.",
        "Quality":"Identificar ≥85% de defectos en evaluación visual.",
        "Safety":"Aprobar lista de verificación de seguridad al 100%.",
        "Materials":"Seleccionar condiciones de secado para 5 materiales.",
        "Efficiency":"Calcular OEE y proponer mejora ≥5pp documentada.",
        "Waste":"Kaizen con reducción documentada de ≥1 desperdicio.",
        "Mold Engineering":"Resolver caso de ingeniería de molde documentado.",
    }
    for cat, p in sorted_cats:
        if p < 70:
            sev = "CRÍTICO" if p < 55 else "MEJORA"
            sc  = "#C0392B" if p < 55 else "#E67E22"
            steps.append({
                "priority": sev, "color": sc,
                "area": CAT_ES.get(cat, cat),
                "duration": "2 semanas" if p < 55 else "1 semana",
                "actions": ACTION_PLANS.get(cat, ["Revisión teórica.","Práctica supervisada."]),
                "kpi": KPI.get(cat, "Superar 75% en re-evaluación."),
            })
    if not steps:
        steps.append({
            "priority": "MANTENIMIENTO", "color": "#00B894",
            "area": "Todas las áreas", "duration": "Continua",
            "actions": ["Sesiones mensuales de actualización técnica.",
                        "Documentar casos atípicos en base de conocimiento.",
                        "Mentoría a personal de menor experiencia."],
            "kpi": "OEE > 85% y scrap < 1.5% sostenido.",
        })

    recs = []
    if passed:
        recs = ["Certificar formalmente con RRHH / Ingeniería.",
                "Asignar proyecto de mejora como aplicación práctica." ,
                "Re-evaluación en 6 meses para seguimiento.",
                "Considerar rol de entrenador interno (Train-the-Trainer)." if pct >= 85
                else "Inscribir en programa de desarrollo técnico avanzado."]
    else:
        wks = {"basic": 4, "medium": 6, "advanced": 8}[level_key]
        recs = [f"Plan de capacitación de {wks} semanas con acompañamiento técnico.",
                "Asignar tutor/shadowing con técnico o ingeniero senior.",
                "Revisar SOPs de áreas críticas con el candidato.",
                "Re-evaluación al concluir el plan de capacitación.",
                "Seguimiento semanal con supervisor directo documentado."]

    return {"passed": passed, "verdict": verdict,
            "insights": insights, "steps": steps, "recs": recs}


# ─────────────────────────────────────────────────────────────────────────────
# PDF BUILDER
# ─────────────────────────────────────────────────────────────────────────────

def img(buf, w, h):
    buf.seek(0)
    return Image(buf, width=w*cm, height=h*cm)

def hr(color=BRAND["gray_md"], thick=1.0):
    return HRFlowable(width=W, thickness=thick, color=color, spaceAfter=6, spaceBefore=2)

def section_title(text, color=BRAND["navy"]):
    return Paragraph(text, S("Heading1", fontSize=13, fontName="Helvetica-Bold",
                              textColor=color, spaceBefore=14, spaceAfter=4))

def subsection(text, color=BRAND["blue"]):
    return Paragraph(text, S("Normal", fontSize=10.5, fontName="Helvetica-Bold",
                              textColor=color, spaceBefore=10, spaceAfter=3))

def body(text):
    return Paragraph(text, S("Normal", fontSize=9, leading=13.5, textColor=BRAND["ink"]))

def caption(text):
    return Paragraph(text, S("Normal", fontSize=7.5, leading=11,
                              textColor=BRAND["gray"], alignment=TA_CENTER))

def callout(text, bg, border):
    t = Table([[body(text)]], colWidths=[W])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), bg),
        ("BOX",(0,0),(-1,-1), 2, border),
        ("TOPPADDING",(0,0),(-1,-1), 8),("BOTTOMPADDING",(0,0),(-1,-1), 8),
        ("LEFTPADDING",(0,0),(-1,-1), 12),("RIGHTPADDING",(0,0),(-1,-1), 12),
    ]))
    return t

def kpi_card(label, value, color):
    return Table([[
        Paragraph(label, S("Normal", fontSize=7.5, fontName="Helvetica",
                            textColor=BRAND["gray"], alignment=TA_CENTER)),
        Paragraph(f"<b>{value}</b>", S("Normal", fontSize=15, fontName="Helvetica-Bold",
                                        textColor=color, alignment=TA_CENTER)),
    ]], colWidths=[W/6, W/6])


def build_pdf(output_path, all_questions, all_results, all_analysis, candidate):
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=1.4*cm, bottomMargin=1.8*cm,
        title=f"CAROL Report Unificado — {candidate['full_name']}",
        author="CAROL Assessment System",
    )

    story = []

    # ── PAGE FOOTER callback ─────────────────────────────────────────────────
    def on_page(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(BRAND["navy"])
        canvas.rect(0, 0, PW, .45*cm, fill=1, stroke=0)
        canvas.setFillColor(BRAND["white"])
        canvas.setFont("Helvetica", 6.5)
        canvas.drawString(.8*cm, .14*cm,
            f"CAROL Assessment System  |  {candidate['full_name']}  |  {candidate['date']}")
        canvas.drawRightString(PW-.8*cm, .14*cm, f"Página {doc.page}")
        canvas.restoreState()

    # ════════════════════════════════════════════════════════════════════════
    # COVER PAGE
    # ════════════════════════════════════════════════════════════════════════
    # Cover header block
    cover_header = Table(
        [[Paragraph(
            "<font color='#FFFFFF' size='22'><b>CAROL</b></font>&nbsp;&nbsp;"
            "<font color='#7FB3D3' size='13'>Assessment System</font><br/>"
            "<font color='#AAC4D8' size='9'>Reporte Técnico Unificado · Vista de Ing. Senior</font>",
            S("Normal", fontName="Helvetica-Bold", leading=30)
        )]],
        colWidths=[W]
    )
    cover_header.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), BRAND["navy"]),
        ("TOPPADDING",(0,0),(-1,-1), 22),("BOTTOMPADDING",(0,0),(-1,-1), 22),
        ("LEFTPADDING",(0,0),(-1,-1), 18),
    ]))
    story.append(cover_header)
    story.append(Spacer(1, 14))

    # Candidate card
    cand_rows = [
        [P("<b>Candidato</b>", fontSize=8, textColor=BRAND["gray"]),
         P(candidate["full_name"], fontSize=11, fontName="Helvetica-Bold"),
         P("<b>ID Empleado</b>", fontSize=8, textColor=BRAND["gray"]),
         P(candidate["employee_id"], fontSize=11, fontName="Helvetica-Bold")],
        [P("<b>Departamento</b>", fontSize=8, textColor=BRAND["gray"]),
         P(candidate["department"], fontSize=9),
         P("<b>Puesto</b>", fontSize=8, textColor=BRAND["gray"]),
         P(candidate["job_role"], fontSize=9)],
        [P("<b>Experiencia</b>", fontSize=8, textColor=BRAND["gray"]),
         P(f"{candidate['years_experience']} años en moldeo", fontSize=9),
         P("<b>Fecha</b>", fontSize=8, textColor=BRAND["gray"]),
         P(candidate["date"], fontSize=9)],
    ]
    cw4 = [W*.15, W*.35, W*.15, W*.35]
    ct = Table(cand_rows, colWidths=cw4)
    ct.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), BRAND["gray_lt"]),
        ("GRID",(0,0),(-1,-1), .4, BRAND["gray_md"]),
        ("TOPPADDING",(0,0),(-1,-1), 5),("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING",(0,0),(-1,-1), 8),
        ("ROWBACKGROUNDS",(0,0),(-1,-1), [BRAND["gray_lt"], colors.white]),
    ]))
    story.append(ct)
    story.append(Spacer(1, 16))

    # Triple-ring gauge + level bars side by side
    gauge_buf = chart_overall_gauge(all_results)
    bars_buf  = chart_level_bars(all_results)

    gauge_img = img(gauge_buf, 6.2, 6.2)
    bars_img  = img(bars_buf,  9.2, 4.4)

    # Level summary score cards (3 cards)
    def score_card(level_key):
        meta = LEVEL[level_key]
        r    = all_results[level_key]
        passed = r["pct"] >= meta["pass_pct"]
        status_color = BRAND["teal"] if passed else BRAND["red"]
        status_label = "APROBADO" if passed else "NO APROBADO"
        card = Table([
            [Paragraph(f"<b>Nivel {meta['label']}</b>",
                        S("Normal", fontSize=9, fontName="Helvetica-Bold",
                          textColor=BRAND["white"]))],
            [Paragraph(f"<b>{r['pct']:.1f}%</b>",
                        S("Normal", fontSize=18, fontName="Helvetica-Bold",
                          textColor=BRAND["white"], alignment=TA_CENTER))],
            [Paragraph(f"{r['earned']:.1f}/{r['max']:.1f} pts",
                        S("Normal", fontSize=8, textColor=colors.HexColor("#AECFD6"),
                          alignment=TA_CENTER))],
            [Paragraph(f"<b>{status_label}</b>",
                        S("Normal", fontSize=8, fontName="Helvetica-Bold",
                          textColor=BRAND["white"] if passed else colors.HexColor("#FFB3B3"),
                          alignment=TA_CENTER))],
        ], colWidths=[W/3 - .4*cm])
        card.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,-1), colors.HexColor(meta["hex"])),
            ("TOPPADDING",(0,0),(-1,-1), 6),("BOTTOMPADDING",(0,0),(-1,-1), 6),
            ("LEFTPADDING",(0,0),(-1,-1), 10),("RIGHTPADDING",(0,0),(-1,-1), 10),
            ("ROWBACKGROUNDS",(0,0),(-1,-1),
             [colors.HexColor(meta["hex"])]*4),
            ("BOX",(0,0),(-1,-1), .5, colors.HexColor("#FFFFFF")),
        ]))
        return card

    score_cards = Table(
        [[score_card("basic"), score_card("medium"), score_card("advanced")]],
        colWidths=[W/3]*3, hAlign="LEFT"
    )
    score_cards.setStyle(TableStyle([
        ("LEFTPADDING",(0,0),(-1,-1), 3),("RIGHTPADDING",(0,0),(-1,-1), 3),
    ]))

    # Combine gauge + right column (bars + cards)
    right_col = Table([
        [bars_img],
        [Spacer(1, 8)],
        [score_cards],
    ], colWidths=[W - 6.6*cm])
    right_col.setStyle(TableStyle([
        ("LEFTPADDING",(0,0),(-1,-1), 0),("RIGHTPADDING",(0,0),(-1,-1), 0),
        ("TOPPADDING",(0,0),(-1,-1), 0),("BOTTOMPADDING",(0,0),(-1,-1), 0),
    ]))

    cover_charts = Table([[gauge_img, right_col]],
                         colWidths=[6.6*cm, W - 6.6*cm])
    cover_charts.setStyle(TableStyle([
        ("VALIGN",(0,0),(-1,-1), "MIDDLE"),
        ("LEFTPADDING",(0,0),(-1,-1), 0),("RIGHTPADDING",(0,0),(-1,-1), 0),
    ]))
    story.append(cover_charts)
    story.append(Spacer(1, 14))

    # Heatmap
    hm_buf = chart_heatmap(all_results)
    hm_img = img(hm_buf, W/cm, 3.4)
    story.append(hm_img)
    story.append(caption("Figura 1. Mapa de calor: % aciertos por área de conocimiento y nivel de evaluación. Verde ≥ 80%, Rojo < 50%."))
    story.append(Spacer(1, 10))

    # Executive summary
    story.append(subsection("Resumen Ejecutivo", BRAND["navy"]))
    lvl_summary = []
    for lk in ("basic","medium","advanced"):
        r  = all_results[lk]; a = all_analysis[lk]
        st = "✓ APROBÓ" if a["passed"] else "✗ NO APROBÓ"
        lvl_summary.append(f"<b>Nivel {LEVEL[lk]['label']}:</b> {r['pct']:.1f}% — {st}. {a['verdict']}")
    story.append(callout("<br/>".join(lvl_summary), BRAND["gray_lt"], BRAND["gray_md"]))

    # ════════════════════════════════════════════════════════════════════════
    # PER-LEVEL SECTIONS
    # ════════════════════════════════════════════════════════════════════════
    for lk in ("basic", "medium", "advanced"):
        story.append(PageBreak())
        meta   = LEVEL[lk]
        r      = all_results[lk]
        a      = all_analysis[lk]
        cats   = r["categories"]

        # ── Level header band ──────────────────────────────────────────────
        lv_header = Table([[
            Paragraph(f"<font color='white' size='15'><b>Nivel {meta['label']}</b></font><br/>"
                      f"<font color='#DDDDDD' size='8'>{meta['role']}</font>",
                      S("Normal", fontName="Helvetica-Bold", leading=22)),
            Paragraph(f"<font color='white' size='11'><b>{r['pct']:.1f}%</b></font><br/>"
                      f"<font color='#DDDDDD' size='8'>{'APROBADO ✓' if a['passed'] else 'NO APROBADO ✗'}</font>",
                      S("Normal", fontName="Helvetica-Bold", leading=20, alignment=TA_RIGHT)),
        ]], colWidths=[W*.65, W*.35])
        lv_header.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,-1), colors.HexColor(meta["hex"])),
            ("TOPPADDING",(0,0),(-1,-1), 14),("BOTTOMPADDING",(0,0),(-1,-1), 14),
            ("LEFTPADDING",(0,0),(0,-1), 16),("RIGHTPADDING",(-1,0),(-1,-1), 16),
            ("VALIGN",(0,0),(-1,-1), "MIDDLE"),
        ]))
        story.append(lv_header)
        story.append(Spacer(1, 10))

        # ── KPI row ────────────────────────────────────────────────────────
        kpi_data = [[
            P("<b>Pts. Obtenidos</b>", fontSize=7.5, textColor=BRAND["gray"], alignment=TA_CENTER),
            P("<b>Pts. Máximos</b>",   fontSize=7.5, textColor=BRAND["gray"], alignment=TA_CENTER),
            P("<b>Mínimo Aprobatorio</b>",fontSize=7.5, textColor=BRAND["gray"], alignment=TA_CENTER),
            P("<b>Preguntas</b>",      fontSize=7.5, textColor=BRAND["gray"], alignment=TA_CENTER),
            P("<b>Tiempo Est.</b>",    fontSize=7.5, textColor=BRAND["gray"], alignment=TA_CENTER),
        ],[
            P(f"<b>{r['earned']:.1f}</b>",  fontSize=14, fontName="Helvetica-Bold",
              textColor=colors.HexColor(meta["hex"]), alignment=TA_CENTER),
            P(f"<b>{r['max']:.1f}</b>",     fontSize=14, fontName="Helvetica-Bold",
              textColor=BRAND["gray"], alignment=TA_CENTER),
            P(f"<b>{meta['pass_pct']}%</b>",fontSize=14, fontName="Helvetica-Bold",
              textColor=BRAND["red"], alignment=TA_CENTER),
            P(f"<b>{len(r['answers'])}</b>", fontSize=14, fontName="Helvetica-Bold",
              textColor=BRAND["ink"], alignment=TA_CENTER),
            P(f"<b>{meta['time_min']} min</b>",fontSize=11, fontName="Helvetica-Bold",
              textColor=BRAND["ink"], alignment=TA_CENTER),
        ]]
        kpi_t = Table(kpi_data, colWidths=[W/5]*5)
        kpi_t.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0), BRAND["navy"]),
            ("TEXTCOLOR",(0,0),(-1,0), BRAND["white"]),
            ("BACKGROUND",(0,1),(-1,1), colors.white),
            ("BOX",(0,0),(-1,-1), .8, BRAND["gray_md"]),
            ("INNERGRID",(0,0),(-1,-1), .4, BRAND["gray_md"]),
            ("TOPPADDING",(0,0),(-1,-1), 6),("BOTTOMPADDING",(0,0),(-1,-1), 6),
            ("VALIGN",(0,0),(-1,-1), "MIDDLE"),
        ]))
        story.append(kpi_t)
        story.append(Spacer(1, 8))

        # Verdict box
        bg = meta["lt"] if a["passed"] else BRAND["red_lt"]
        brd = colors.HexColor(meta["hex"]) if a["passed"] else BRAND["red"]
        story.append(callout(a["verdict"], bg, brd))
        story.append(Spacer(1, 12))

        # ── Charts row: donut + radar + cat bars ───────────────────────────
        story.append(subsection("Análisis por Área", colors.HexColor(meta["hex"])))
        story.append(hr(colors.HexColor(meta["hex"])))

        donut_buf = chart_donut(r["pct"], meta["hex"])
        radar_buf = chart_radar(cats, meta["hex"])
        catbar_buf= chart_cat_bars(cats, meta["hex"], meta["pass_pct"])

        d_img = img(donut_buf,  3.6, 3.6)
        r_img = img(radar_buf,  4.8, 4.8)
        b_img = img(catbar_buf, 5.6, max(3.8, len(cats)*0.52))

        charts_row = Table([[d_img, r_img, b_img]],
                           colWidths=[3.8*cm, 5.0*cm, W - 8.8*cm])
        charts_row.setStyle(TableStyle([
            ("VALIGN",(0,0),(-1,-1), "MIDDLE"),
            ("LEFTPADDING",(0,0),(-1,-1), 0),("RIGHTPADDING",(0,0),(-1,-1), 2),
        ]))
        story.append(charts_row)
        story.append(caption("Figura. Izq: puntaje global | Centro: perfil de competencias por área | Der: % aciertos por área (línea roja = mínimo)."))
        story.append(Spacer(1, 10))

        # ── Category table ─────────────────────────────────────────────────
        cat_hdr = [
            P("<b>Área</b>",         fontSize=8, textColor=BRAND["white"], fontName="Helvetica-Bold"),
            P("<b>Correctas</b>",    fontSize=8, textColor=BRAND["white"], fontName="Helvetica-Bold", alignment=TA_CENTER),
            P("<b>Total</b>",        fontSize=8, textColor=BRAND["white"], fontName="Helvetica-Bold", alignment=TA_CENTER),
            P("<b>% Acierto</b>",    fontSize=8, textColor=BRAND["white"], fontName="Helvetica-Bold", alignment=TA_CENTER),
            P("<b>Pts. Obt.</b>",    fontSize=8, textColor=BRAND["white"], fontName="Helvetica-Bold", alignment=TA_CENTER),
            P("<b>Pts. Máx.</b>",    fontSize=8, textColor=BRAND["white"], fontName="Helvetica-Bold", alignment=TA_CENTER),
            P("<b>Estado</b>",       fontSize=8, textColor=BRAND["white"], fontName="Helvetica-Bold", alignment=TA_CENTER),
            P("<b>Diagnóstico</b>",  fontSize=8, textColor=BRAND["white"], fontName="Helvetica-Bold"),
        ]
        cat_rows_tbl = [cat_hdr]
        for ins in a["insights"]:
            raw_key = next((k for k,v in CAT_ES.items() if v == ins["cat"]), ins["cat"])
            cd = cats.get(raw_key, {})
            earned_s = f"{cd.get('earned', 0):.1f}" if cd else "—"
            max_s    = f"{cd.get('max',    0):.1f}" if cd else "—"
            tc = colors.HexColor(ins["tc"])
            cat_rows_tbl.append([
                P(f"<b>{ins['cat']}</b>", fontSize=8, fontName="Helvetica-Bold"),
                P(str(ins["correct"]),    fontSize=8, alignment=TA_CENTER),
                P(str(ins["total"]),      fontSize=8, alignment=TA_CENTER),
                P(f"<b>{ins['pct']:.1f}%</b>", fontSize=8, fontName="Helvetica-Bold",
                  alignment=TA_CENTER,
                  textColor=BRAND["teal"] if ins["pct"]>=75 else BRAND["red"]),
                P(earned_s, fontSize=8, alignment=TA_CENTER),
                P(max_s,    fontSize=8, alignment=TA_CENTER),
                P(f"<b>{ins['tag']}</b>", fontSize=7.5, fontName="Helvetica-Bold",
                  alignment=TA_CENTER, textColor=tc),
                P(ins["note"], fontSize=7.5),
            ])
        cw_cat = [W*.15, W*.08, W*.06, W*.09, W*.08, W*.08, W*.09, W*.37]
        cat_tbl = Table(cat_rows_tbl, colWidths=cw_cat, repeatRows=1)
        cat_tbl.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0), BRAND["navy"]),
            ("GRID",(0,0),(-1,-1), .35, BRAND["gray_md"]),
            ("ROWBACKGROUNDS",(0,1),(-1,-1), [colors.white, BRAND["gray_lt"]]),
            ("TOPPADDING",(0,0),(-1,-1), 4),("BOTTOMPADDING",(0,0),(-1,-1), 4),
            ("LEFTPADDING",(0,0),(-1,-1), 5),("RIGHTPADDING",(0,0),(-1,-1), 5),
            ("VALIGN",(0,0),(-1,-1), "TOP"),
        ]))
        story.append(cat_tbl)
        story.append(Spacer(1, 14))

        # ── Answer review (compact) ────────────────────────────────────────
        all_answers = r["answers"]
        if all_answers:
            story.append(CondPageBreak(8*cm))
            story.append(subsection("Revisión de Respuestas", colors.HexColor(meta["hex"])))
            story.append(hr(colors.HexColor(meta["hex"])))

            answers_by_cat = {}
            for ans in all_answers:
                answers_by_cat.setdefault(ans["category"], []).append(ans)

            qn = 1
            for cat, w_list in answers_by_cat.items():
                story.append(P(f"<b>{CAT_ES.get(cat, cat)}</b>",
                               fontSize=9, textColor=colors.HexColor(CAT_HEX.get(cat,"#555")),
                               fontName="Helvetica-Bold", spaceBefore=6))
                for ans in w_list:
                    status = "Correcta" if ans["correct"] else "Incorrecta"
                    status_color = "#00B894" if ans["correct"] else "#C0392B"
                    # Question row
                    q_rows = [
                        [P(f"<b>P{qn}.</b>", fontSize=8.5, fontName="Helvetica-Bold"),
                         P(f"<font color='{status_color}'><b>[{status}]</b></font> {ans['question']}", fontSize=8.5, fontName="Helvetica-Bold")],
                    ]
                    for idx, opt in enumerate(ans["options"]):
                        if idx == ans["correct_index"]:   mk, fc = "✓", "#00B894"
                        elif idx == ans["chosen_index"]:  mk, fc = "✗", "#C0392B"
                        else:                              mk, fc = "·", "#7F8C8D"
                        q_rows.append([
                            P(f"<font color='{fc}'><b>{mk}</b></font>",
                              fontSize=8.5, alignment=TA_CENTER),
                            P(f"<font color='{fc}'>{opt}</font>", fontSize=8),
                        ])
                    q_rows.append([
                        P(""),
                        P(f"<i><font color='#1B4F72'>💡 {ans['reasoning']}</font></i>",
                          fontSize=7.5),
                    ])
                    q_tbl = Table(q_rows, colWidths=[.6*cm, W - .6*cm])
                    q_tbl.setStyle(TableStyle([
                        ("BACKGROUND",(0,0),(-1,0), BRAND["gray_lt"]),
                        ("BOX",(0,0),(-1,-1), .4, BRAND["gray_md"]),
                        ("TOPPADDING",(0,0),(-1,-1), 2),("BOTTOMPADDING",(0,0),(-1,-1), 2),
                        ("LEFTPADDING",(0,0),(-1,-1), 4),
                        ("VALIGN",(0,0),(-1,-1), "TOP"),
                    ]))
                    story.append(q_tbl)
                    story.append(Spacer(1, 4))
                    qn += 1

        story.append(Spacer(1, 14))

        # ── Training plan (compact) ────────────────────────────────────────
        story.append(CondPageBreak(6*cm))
        story.append(subsection("Plan de Acción", colors.HexColor(meta["hex"])))
        story.append(hr(colors.HexColor(meta["hex"])))

        for step in a["steps"]:
            sc = colors.HexColor(step["color"])
            step_tbl = Table([
                [P(f"<font color='white'><b> {step['priority']} </b></font>",
                   fontSize=8, fontName="Helvetica-Bold"),
                 P(f"<b>{step['area']}</b>", fontSize=9, fontName="Helvetica-Bold"),
                 P(f"Duración: <b>{step['duration']}</b>",
                   fontSize=8, alignment=TA_RIGHT)],
                ["",
                 Table([[P(f"  {i+1}. {act}", fontSize=8)]
                        for i, act in enumerate(step["actions"])],
                       colWidths=[W*.72]),
                 ""],
                ["",
                 P(f"<b>KPI:</b> {step['kpi']}",
                   fontSize=7.5, textColor=BRAND["amber"]),
                 ""],
            ], colWidths=[2.2*cm, W*.72, W*.18])
            step_tbl.setStyle(TableStyle([
                ("BACKGROUND",(0,0),(0,0), sc),
                ("BACKGROUND",(1,0),(-1,0), BRAND["gray_lt"]),
                ("BACKGROUND",(0,1),(-1,1), colors.white),
                ("BACKGROUND",(0,2),(-1,2), BRAND["amber_lt"]),
                ("SPAN",(0,1),(0,2)), ("SPAN",(2,1),(2,2)),
                ("BOX",(0,0),(-1,-1), .8, sc),
                ("TOPPADDING",(0,0),(-1,-1), 4),("BOTTOMPADDING",(0,0),(-1,-1), 4),
                ("LEFTPADDING",(0,0),(-1,-1), 6),
                ("VALIGN",(0,0),(-1,-1), "TOP"),
            ]))
            story.append(step_tbl)
            story.append(Spacer(1, 5))

        # Recs
        story.append(Spacer(1, 4))
        rec_rows = [[
            P(f"<b>{i+1}.</b>", fontSize=8.5, fontName="Helvetica-Bold",
              textColor=BRAND["white"], alignment=TA_CENTER),
            P(rec, fontSize=8.5),
        ] for i, rec in enumerate(a["recs"])]
        rec_t = Table(rec_rows, colWidths=[.7*cm, W - .7*cm])
        rec_t.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(0,-1), colors.HexColor(meta["hex"])),
            ("BACKGROUND",(1,0),(1,-1), colors.white),
            ("BOX",(0,0),(-1,-1), .4, BRAND["gray_md"]),
            ("INNERGRID",(0,0),(-1,-1), .3, BRAND["gray_md"]),
            ("TOPPADDING",(0,0),(-1,-1), 5),("BOTTOMPADDING",(0,0),(-1,-1), 5),
            ("LEFTPADDING",(0,0),(-1,-1), 6),
            ("VALIGN",(0,0),(-1,-1), "MIDDLE"),
        ]))
        story.append(rec_t)

    # ════════════════════════════════════════════════════════════════════════
    # CONSOLIDATED ACTION PLAN  (last page)
    # ════════════════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Table([[
        Paragraph("<font color='white' size='14'><b>Plan de Acción Consolidado</b></font><br/>"
                  "<font color='#AAAAAA' size='8'>Resumen ejecutivo para Ing. Senior / RRHH</font>",
                  S("Normal", fontName="Helvetica-Bold", leading=22))
    ]], colWidths=[W]))
    story[-1].setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), BRAND["navy"]),
        ("TOPPADDING",(0,0),(-1,-1), 16),("BOTTOMPADDING",(0,0),(-1,-1), 16),
        ("LEFTPADDING",(0,0),(-1,-1), 16),
    ]))
    story.append(Spacer(1, 12))

    # Cross-level status table
    xhdr = [P(col, fontSize=8, textColor=BRAND["white"], fontName="Helvetica-Bold",
               alignment=TA_CENTER)
            for col in ["Nivel","Rol","Puntaje","Estado","Áreas Críticas","Acción Inmediata"]]
    xrows = [xhdr]
    for lk in ("basic","medium","advanced"):
        meta = LEVEL[lk]; r = all_results[lk]; a = all_analysis[lk]
        crit = [ins["cat"] for ins in a["insights"] if ins["tag"] in ("CRÍTICO","DÉBIL")]
        crit_str = ", ".join(crit[:3]) + ("..." if len(crit)>3 else "") if crit else "Ninguna"
        action = "Re-evaluación post-capacitación" if not a["passed"] else "Certificación + siguiente nivel"
        passed_c = BRAND["teal"] if a["passed"] else BRAND["red"]
        xrows.append([
            P(f"<b>{meta['label']}</b>", fontSize=8, fontName="Helvetica-Bold",
              textColor=colors.HexColor(meta["hex"])),
            P(meta["role"], fontSize=7.5),
            P(f"<b>{r['pct']:.1f}%</b>", fontSize=9, fontName="Helvetica-Bold",
              textColor=colors.HexColor(meta["hex"]), alignment=TA_CENTER),
            P(f"<b>{'✓' if a['passed'] else '✗'}</b>", fontSize=11,
              fontName="Helvetica-Bold", textColor=passed_c, alignment=TA_CENTER),
            P(crit_str, fontSize=7.5),
            P(action, fontSize=7.5),
        ])

    xw = [W*.10, W*.18, W*.10, W*.08, W*.26, W*.28]
    xt = Table(xrows, colWidths=xw, repeatRows=1)
    xt.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0), BRAND["navy"]),
        ("GRID",(0,0),(-1,-1), .35, BRAND["gray_md"]),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [colors.white, BRAND["gray_lt"]]),
        ("TOPPADDING",(0,0),(-1,-1), 5),("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("LEFTPADDING",(0,0),(-1,-1), 6),
        ("VALIGN",(0,0),(-1,-1), "MIDDLE"),
    ]))
    story.append(xt)
    story.append(Spacer(1, 16))

    # Overall recommendation
    total_passed = sum(1 for lk in LEVEL if all_analysis[lk]["passed"])
    if total_passed == 3:
        global_note = "✅ <b>Candidato APRUEBA los 3 niveles.</b> Perfil apto para roles senior y mentoría técnica. Recomendado para certificación avanzada y proyectos de mejora de proceso."
        g_bg, g_brd = BRAND["teal_lt"], BRAND["teal"]
    elif total_passed == 2:
        global_note = "⚠️ <b>Candidato aprueba 2 de 3 niveles.</b> Competencias sólidas con brechas en nivel superior. Capacitación focalizada recomendada antes de promover."
        g_bg, g_brd = BRAND["amber_lt"], BRAND["amber"]
    elif total_passed == 1:
        global_note = "🔴 <b>Candidato aprueba 1 de 3 niveles.</b> Requiere plan de desarrollo estructurado. No apto para ascenso en este momento."
        g_bg, g_brd = BRAND["red_lt"], BRAND["red"]
    else:
        global_note = "🔴 <b>Candidato no aprueba ningún nivel.</b> Brechas críticas de conocimiento. Plan de capacitación integral requerido. Evaluación de continuidad en puesto recomendada."
        g_bg, g_brd = BRAND["red_lt"], BRAND["red"]

    story.append(callout(global_note, g_bg, g_brd))
    story.append(Spacer(1, 20))

    # Signature row
    story.append(hr())
    sig = Table([[
        P(f"Generado por <b>CAROL Assessment System</b><br/>"
          f"<font size='7' color='#7F8C8D'>Emisión: {datetime.now().strftime('%d/%m/%Y %H:%M')} · Confidencial</font>",
          fontSize=8, leading=12, textColor=BRAND["gray"]),
        P("Firma del Evaluador<br/><br/>_______________________<br/>"
          "<font size='7'>Nombre y cargo</font>",
          fontSize=8, leading=12, textColor=BRAND["gray"], alignment=TA_CENTER),
        P("Firma del Candidato<br/><br/>_______________________<br/>"
          "<font size='7'>Nombre y firma</font>",
          fontSize=8, leading=12, textColor=BRAND["gray"], alignment=TA_CENTER),
    ]], colWidths=[W*.5, W*.25, W*.25])
    sig.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP")]))
    story.append(sig)

    # Build
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"✅ PDF generado: {output_path}")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="CAROL Unified Report")
    parser.add_argument("--output", default="reports/carol_unified_report.pdf")
    parser.add_argument("--seed",   type=int, default=42)
    args = parser.parse_args()

    all_questions, all_results, all_analysis = {}, {}, {}
    seeds = {"basic": args.seed, "medium": args.seed+1, "advanced": args.seed+2}

    candidate = {
        "full_name":        "M. Gallegos / F. Salazar",
        "employee_id":      "EMP-2247 / EMP-1981",
        "department":       "Ingeniería de Procesos",
        "job_role":         "Ingeniero Sr. / Líder Técnico",
        "years_experience": "8",
        "date":             datetime.now().strftime("%d/%m/%Y"),
    }

    for lk, meta in LEVEL.items():
        with open(meta["file"]) as f:
            qs = json.load(f)
        all_questions[lk] = qs
        all_results[lk]   = simulate(qs, seeds[lk])
        all_analysis[lk]  = ai_analysis(all_results[lk], lk, candidate["full_name"])

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    build_pdf(args.output, all_questions, all_results, all_analysis, candidate)

    for lk in ("basic","medium","advanced"):
        r = all_results[lk]; a = all_analysis[lk]
        print(f"  {LEVEL[lk]['label']:10s} {r['pct']:5.1f}%  {'APROBÓ' if a['passed'] else 'NO APROBÓ'}")


if __name__ == "__main__":
    main()
