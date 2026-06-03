import re, pathlib

BASE = pathlib.Path('/Users/marco/Documents/code/CAROLV3/web')

def patch_carol_platform():
    p = BASE / 'carol_platform.html'
    html = p.read_text(encoding='utf-8')

    # 1. Head fonts
    old_head = '''<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CAROL — Sistema de Evaluación Técnica</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/core@1.0.0-beta17/dist/css/tabler.min.css">'''
    new_head = '''<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CAROL — Sistema de Evaluación Técnica</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0&display=swap">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/core@1.0.0-beta17/dist/css/tabler.min.css">'''
    assert old_head in html, 'Head block not found'
    html = html.replace(old_head, new_head)

    # 2. Body font
    html = html.replace(
        "body{background:#f0f4f8;font-family:'Inter',system-ui,sans-serif;}",
        "body{background:#f0f4f8;font-family:'Roboto','Inter',system-ui,sans-serif;}"
    )

    # 3. CSS Results section (from /* ── Results ── */ up to /* Utilities */)
    old_css = '''/* ── Results ── */
#screen-results{display:none;opacity:0;}
.results-layout{max-width:900px;margin:0 auto;padding:2rem 1rem;}
.results-hero{background:var(--carol-navy);border-radius:16px;padding:2rem;margin-bottom:1.5rem;display:flex;align-items:center;gap:2rem;color:#fff;flex-wrap:wrap;}
.results-donut-wrap{position:relative;width:110px;height:110px;flex-shrink:0;}
.results-donut-wrap svg{transform:rotate(-90deg);}
.donut-center{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;}
.donut-pct{font-size:1.5rem;font-weight:800;color:#fff;}
.donut-status{font-size:.65rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;margin-top:1px;}
.results-info h2{font-size:1.4rem;font-weight:800;margin:0 0 .25rem;}
.results-info p{margin:0;color:#94a3b8;font-size:.88rem;}
.results-kpis{display:flex;gap:1.25rem;margin-top:1rem;flex-wrap:wrap;}
.results-kpi{text-align:center;}
.results-kpi-val{font-size:1.3rem;font-weight:800;display:block;}
.results-kpi-label{font-size:.7rem;color:#94a3b8;text-transform:uppercase;letter-spacing:.05em;}

.results-grid{display:grid;grid-template-columns:1fr 1fr;gap:1.25rem;margin-bottom:1.5rem;}
@media(max-width:640px){.results-grid{grid-template-columns:1fr;}}

.results-card{background:#fff;border-radius:12px;padding:1.25rem;box-shadow:0 2px 8px rgba(0,0,0,.06);}
.results-card h4{font-size:.85rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:#94a3b8;margin:0 0 1rem;}

.cat-result-row{display:flex;align-items:center;gap:.6rem;margin-bottom:.75rem;}
.cat-result-row:last-child{margin:0;}
.cat-result-label{font-size:.8rem;font-weight:600;color:#374151;width:150px;flex-shrink:0;}
.cat-bar-wrap{flex:1;height:8px;background:#f1f5f9;border-radius:99px;overflow:hidden;}
.cat-bar-fill{height:100%;border-radius:99px;transition:width 1s;}
.cat-result-pct{font-size:.78rem;font-weight:700;width:36px;text-align:right;}
.cat-result-pass{font-size:.68rem;font-weight:700;padding:.1rem .4rem;border-radius:99px;}

.wrong-review{background:#fff;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,.06);margin-bottom:1.5rem;overflow:hidden;}
.wrong-review-header{padding:1rem 1.5rem;border-bottom:1px solid #f1f5f9;display:flex;align-items:center;gap:.75rem;}
.wrong-review-header h4{font-size:.95rem;font-weight:700;color:#1e293b;margin:0;}
.wrong-review-header .badge{font-size:.75rem;}
.wrong-item{padding:1rem 1.5rem;border-bottom:1px solid #f8fafc;}
.wrong-item:last-child{border:none;}
.wrong-item-meta{display:flex;gap:.5rem;align-items:center;margin-bottom:.4rem;flex-wrap:wrap;}
.wrong-q-text{font-size:.88rem;font-weight:600;color:#1e293b;margin-bottom:.5rem;line-height:1.4;}
.wrong-options{display:grid;grid-template-columns:1fr 1fr;gap:.35rem;}
.wrong-opt{font-size:.78rem;padding:.3rem .6rem;border-radius:6px;display:flex;align-items:center;gap:.4rem;}
.wrong-opt.chosen{background:#fef2f2;color:#991b1b;}
.wrong-opt.correct{background:#f0fdf4;color:#166534;}
.wrong-opt .ti{font-size:.85rem;flex-shrink:0;}
.wrong-reasoning{margin-top:.6rem;font-size:.79rem;color:#78350f;background:#fffbeb;border:1px solid #fde68a;border-radius:6px;padding:.5rem .75rem;display:flex;gap:.5rem;align-items:flex-start;}
.wrong-reasoning .ti{flex-shrink:0;margin-top:1px;}

.action-plan{background:#fff;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,.06);margin-bottom:1.5rem;}
.action-plan-header{padding:1rem 1.5rem;border-bottom:1px solid #f1f5f9;}
.action-plan-header h4{font-size:.95rem;font-weight:700;color:#1e293b;margin:0;}
.action-step{padding:1rem 1.5rem;border-bottom:1px solid #f8fafc;display:flex;gap:1rem;}
.action-step:last-child{border:none;}
.step-priority{width:80px;flex-shrink:0;text-align:center;}
.step-priority-badge{display:inline-block;padding:.2rem .6rem;border-radius:6px;font-size:.68rem;font-weight:800;text-transform:uppercase;letter-spacing:.04em;}
.step-content h5{font-size:.88rem;font-weight:700;color:#1e293b;margin:0 0 .35rem;}
.step-content ul{margin:0;padding-left:1.1rem;font-size:.8rem;color:#475569;line-height:1.6;}
.step-kpi{margin-top:.4rem;font-size:.76rem;color:#92400e;background:#fef3c7;padding:.25rem .6rem;border-radius:4px;display:inline-flex;align-items:center;gap:.3rem;}

.results-footer{display:flex;gap:1rem;flex-wrap:wrap;justify-content:center;padding:0 1rem;}
.btn-action{padding:.6rem 1.25rem;border-radius:8px;font-size:.88rem;font-weight:700;border:none;cursor:pointer;transition:all .15s;display:flex;align-items:center;gap:.4rem;white-space:nowrap;}
.save-status{font-size:.82rem;font-weight:600;padding:.5rem 1rem;border-radius:8px;margin-bottom:1rem;text-align:center;display:none;}
.save-status.show{display:block;}
.save-status.ok{background:#dcfce7;color:#166534;}
.save-status.err{background:#fee2e2;color:#991b1b;}
.btn-restart{background:#f1f5f9;color:#475569;}
.btn-restart:hover{background:#e2e8f0;}
.btn-print{background:var(--carol-navy);color:#fff;}
.btn-print:hover{filter:brightness(1.15);}
.btn-webhook{background:var(--carol-teal);color:#fff;}
.btn-webhook:hover{filter:brightness(1.1);}

/* Utilities */'''

    new_css = '''/* ── Results ── */
#screen-results{display:none;opacity:0;}
.results-layout{max-width:960px;margin:0 auto;padding:1rem;}
@media(min-width:640px){.results-layout{padding:1.5rem;}}

.mui-paper{background:#fff;border-radius:12px;box-shadow:0px 1px 3px 0px rgba(0,0,0,0.12),0px 1px 1px 0px rgba(0,0,0,0.14),0px 2px 1px -1px rgba(0,0,0,0.2);overflow:hidden;margin-bottom:1rem;transition:box-shadow 300ms cubic-bezier(0.4, 0, 0.2, 1);}
.mui-card{padding:0;border-radius:12px;background:#fff;box-shadow:0px 1px 3px 0px rgba(0,0,0,0.12),0px 1px 1px 0px rgba(0,0,0,0.14),0px 2px 1px -1px rgba(0,0,0,0.2);margin-bottom:1rem;overflow:hidden;}

.results-hero{background:var(--carol-navy);border-radius:16px;padding:1.5rem;margin-bottom:1.25rem;color:#fff;display:flex;align-items:center;gap:1.5rem;flex-wrap:wrap;}
.results-donut-wrap{position:relative;width:100px;height:100px;flex-shrink:0;}
.results-donut-wrap svg{transform:rotate(-90deg);width:100%;height:100%;}
.donut-center{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;}
.donut-pct{font-size:1.3rem;font-weight:800;color:#fff;}
.donut-status{font-size:.6rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;margin-top:1px;}
.results-info{flex:1;min-width:220px;}
.results-info h2{font-size:1.25rem;font-weight:800;margin:0 0 .25rem;}
.results-info p{margin:0;color:#94a3b8;font-size:.85rem;}
.results-kpis{display:flex;gap:1rem;margin-top:1rem;flex-wrap:wrap;}
.results-kpi{text-align:center;flex:1;min-width:70px;background:rgba(255,255,255,.08);border-radius:8px;padding:.5rem;}
.results-kpi-val{font-size:1.1rem;font-weight:800;display:block;}
.results-kpi-label{font-size:.65rem;color:#94a3b8;text-transform:uppercase;letter-spacing:.05em;}

.cat-result-row{display:flex;align-items:center;gap:.75rem;margin-bottom:1rem;padding:1rem;background:#fff;border-radius:12px;box-shadow:0px 1px 3px rgba(0,0,0,.1);flex-wrap:wrap;}
.cat-result-row:last-child{margin-bottom:0;}
.cat-result-header{display:flex;justify-content:space-between;align-items:center;width:100%;margin-bottom:.5rem;}
.cat-result-label{font-size:.85rem;font-weight:700;color:#1e293b;}
.cat-result-ratio{font-size:.75rem;color:#64748b;font-weight:600;}
.cat-bar-wrap{flex:1;height:10px;background:#e2e8f0;border-radius:99px;overflow:hidden;min-width:100px;}
.cat-bar-fill{height:100%;border-radius:99px;transition:width 1s ease;}
.cat-result-footer{display:flex;justify-content:space-between;align-items:center;width:100%;margin-top:.35rem;}
.cat-result-pct{font-size:.85rem;font-weight:700;}
.cat-result-pass{font-size:.68rem;font-weight:700;padding:.15rem .5rem;border-radius:99px;}

.mui-accordion{border:1px solid rgba(0,0,0,.08);border-radius:10px;margin-bottom:.6rem;overflow:hidden;background:#fff;box-shadow:0px 1px 2px rgba(0,0,0,.06);}
.mui-accordion-summary{padding:.85rem 1rem;display:flex;align-items:center;justify-content:space-between;cursor:pointer;gap:.5rem;background:#fff;touch-action:manipulation;}
.mui-accordion-summary:hover{background:#f8fafc;}
.mui-accordion-summary-text{flex:1;font-size:.85rem;font-weight:600;color:#1e293b;line-height:1.3;}
.mui-accordion-summary-meta{display:flex;gap:.4rem;align-items:center;flex-shrink:0;}
.mui-accordion-details{padding:0 1rem 1rem;display:none;font-size:.85rem;color:#475569;}
.mui-accordion-details.open{display:block;}
.mui-accordion-details-body{padding:.75rem;background:#f8fafc;border-radius:8px;}
.mui-chip{height:22px;padding:0 8px;border-radius:12px;font-size:.7rem;font-weight:700;display:inline-flex;align-items:center;justify-content:center;gap:4px;}
.mui-chip-teal{background:#e6f7f2;color:#00695c;}
.mui-chip-amber{background:#fff3e0;color:#e65100;}
.mui-chip-red{background:#ffebee;color:#c62828;}
.mui-chip-blue{background:#e3f2fd;color:#1565c0;}
.mui-chip-gray{background:#f1f5f9;color:#475569;}

.action-step{padding:1rem;display:flex;gap:1rem;background:#fff;border-radius:12px;margin-bottom:.75rem;box-shadow:0px 1px 3px rgba(0,0,0,.1);flex-wrap:wrap;}
.step-priority{width:80px;flex-shrink:0;text-align:center;}
.step-priority-badge{display:inline-block;padding:.25rem .6rem;border-radius:6px;font-size:.68rem;font-weight:800;text-transform:uppercase;letter-spacing:.04em;}
.step-content{flex:1;min-width:200px;}
.step-content h5{font-size:.9rem;font-weight:700;color:#1e293b;margin:0 0 .35rem;}
.step-content ul{margin:0;padding-left:1.1rem;font-size:.82rem;color:#475569;line-height:1.6;}
.step-kpi{margin-top:.4rem;font-size:.76rem;color:#92400e;background:#fef3c7;padding:.35rem .6rem;border-radius:4px;display:inline-flex;align-items:center;gap:.3rem;}

.results-footer{display:flex;gap:.75rem;flex-wrap:wrap;justify-content:center;padding:0 1rem;margin-bottom:1.5rem;}
.btn-action{padding:.65rem 1.1rem;border-radius:8px;font-size:.85rem;font-weight:700;border:none;cursor:pointer;transition:all .15s;display:flex;align-items:center;gap:.4rem;white-space:nowrap;text-transform:uppercase;letter-spacing:.02em;}
.save-status{font-size:.82rem;font-weight:600;padding:.6rem 1rem;border-radius:8px;margin-bottom:1rem;text-align:center;display:none;}
.save-status.show{display:block;}
.save-status.ok{background:#dcfce7;color:#166534;}
.save-status.err{background:#fee2e2;color:#991b1b;}
.btn-restart{background:#f1f5f9;color:#475569;}
.btn-restart:hover{background:#e2e8f0;}
.btn-print{background:var(--carol-navy);color:#fff;}
.btn-print:hover{filter:brightness(1.15);}
.btn-webhook{background:var(--carol-teal);color:#fff;}
.btn-webhook:hover{filter:brightness(1.1);}

/* Utilities */'''
    assert old_css in html, 'CSS Results block not found'
    html = html.replace(old_css, new_css)

    # 4. HTML Results section
    old_html_results = '''<!-- ══════════════════════════════════════════════════ RESULTS ══ -->
<div id="screen-results" class="page-wrapper">
  <div id="inter-level-banner" class="d-none" style="background:var(--carol-navy);color:#fff;border-radius:12px;padding:1.25rem 1.5rem;margin-bottom:1.25rem;display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap;">
    <div style="display:flex;align-items:center;gap:.75rem;">
      <i id="inter-level-icon" class="ti ti-check-circle" style="font-size:1.5rem;color:#00B894;"></i>
      <div>
        <div style="font-size:1rem;font-weight:700;" id="inter-level-title">Nivel Completado</div>
        <div style="font-size:.82rem;color:#94a3b8;" id="inter-level-subtitle"></div>
      </div>
    </div>
    <div style="display:flex;gap:1rem;align-items:center;">
      <div style="text-align:center;min-width:60px;">
        <div style="font-size:1.3rem;font-weight:700;color:#00B894;" id="inter-level-score">—</div>
        <div style="font-size:.65rem;color:#94a3b8;">Score</div>
      </div>
      <button class="btn-action btn-webhook" id="inter-level-btn" onclick="startCooldownNextLevel()" style="background:#00B894;color:#fff;padding:.65rem 1.5rem;font-size:.95rem;">
        <i class="ti ti-player-play"></i> Siguiente Nivel
      </button>
    </div>
  </div>
  <div class="results-layout">
    <!-- Hero -->
    <div class="results-hero" id="results-hero">
      <div class="results-donut-wrap">
        <svg width="110" height="110" viewBox="0 0 110 110">
          <circle cx="55" cy="55" r="44" fill="none" stroke="rgba(255,255,255,.15)" stroke-width="12"/>
          <circle id="donut-arc" cx="55" cy="55" r="44" fill="none" stroke="#00B894" stroke-width="12"
            stroke-dasharray="276.46" stroke-dashoffset="276.46" stroke-linecap="round"/>
        </svg>
        <div class="donut-center">
          <div class="donut-pct" id="result-pct">0%</div>
          <div class="donut-status" id="result-status-icon">—</div>
        </div>
      </div>
      <div class="results-info" style="flex:1;">
        <h2 id="result-name">Resultado</h2>
        <p id="result-subtitle">Nivel — Candidato</p>
        <div class="results-kpis">
          <div class="results-kpi"><span class="results-kpi-val" id="kpi-pts">—</span><span class="results-kpi-label">Pts. Obtenidos</span></div>
          <div class="results-kpi"><span class="results-kpi-val" id="kpi-max">—</span><span class="results-kpi-label">Pts. Máximos</span></div>
          <div class="results-kpi"><span class="results-kpi-val" id="kpi-correct">—</span><span class="results-kpi-label">Correctas</span></div>
          <div class="results-kpi"><span class="results-kpi-val" id="kpi-time">—</span><span class="results-kpi-label">Tiempo usado</span></div>
        </div>
      </div>
    </div>

    <!-- Category breakdown + Type breakdown -->
    <div class="results-grid">
      <div class="results-card" style="grid-column:1/-1;">
        <h4>Desempeño por Área de Conocimiento</h4>
        <div id="cat-breakdown"></div>
      </div>
    </div>

    <!-- Wrong questions -->
    <div class="wrong-review" id="wrong-review">
      <div class="wrong-review-header">
        <i class="ti ti-x-circle" style="font-size:1.2rem;color:#dc2626;"></i>
        <h4>Preguntas Incorrectas — Revisión de Aprendizaje</h4>
        <span class="badge bg-red text-white" id="wrong-count-badge">0</span>
      </div>
      <div id="wrong-list"></div>
    </div>

    <!-- Action plan -->
    <div class="action-plan" id="action-plan">
      <div class="action-plan-header">
        <h4>Plan de Acción Recomendado</h4>
      </div>
      <div id="action-steps"></div>
    </div>

    <!-- Save status -->
    <div id="save-status" class="save-status"></div>

    <!-- Footer actions -->
    <div class="results-footer" id="results-footer">
      <button class="btn-action btn-restart" onclick="showSplash()"><i class="ti ti-home"></i> Inicio</button>
      <button class="btn-action btn-print" onclick="window.print()"><i class="ti ti-printer"></i> Imprimir Reporte</button>
      <button class="btn-action btn-webhook" id="btn-send-results" onclick="sendToWebhook()"><i class="ti ti-send"></i> Enviar Resultados</button>
    </div>
  </div>
</div>'''

    new_html_results = '''<!-- ══════════════════════════════════════════════════ RESULTS ══ -->
<div id="screen-results" class="page-wrapper">
  <div id="inter-level-banner" class="d-none" style="background:var(--carol-navy);color:#fff;border-radius:12px;padding:1.25rem 1.5rem;margin-bottom:1.25rem;display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap;">
    <div style="display:flex;align-items:center;gap:.75rem;">
      <i id="inter-level-icon" class="ti ti-check-circle" style="font-size:1.5rem;color:#00B894;"></i>
      <div>
        <div style="font-size:1rem;font-weight:700;" id="inter-level-title">Nivel Completado</div>
        <div style="font-size:.82rem;color:#94a3b8;" id="inter-level-subtitle"></div>
      </div>
    </div>
    <div style="display:flex;gap:1rem;align-items:center;">
      <div style="text-align:center;min-width:60px;">
        <div style="font-size:1.3rem;font-weight:700;color:#00B894;" id="inter-level-score">—</div>
        <div style="font-size:.65rem;color:#94a3b8;">Score</div>
      </div>
      <button class="btn-action btn-webhook" id="inter-level-btn" onclick="startCooldownNextLevel()" style="background:#00B894;color:#fff;padding:.65rem 1.5rem;font-size:.95rem;">
        <i class="ti ti-player-play"></i> Siguiente Nivel
      </button>
    </div>
  </div>

  <div class="results-layout">
    <!-- Hero -->
    <div class="mui-paper" id="results-hero" style="background:linear-gradient(135deg,#0D1B2A 0%,#1B4F72 100%);color:#fff;border-radius:16px;padding:1.5rem;margin-bottom:1.25rem;">
      <div style="display:flex;align-items:center;gap:1.5rem;flex-wrap:wrap;">
        <div class="results-donut-wrap">
          <svg viewBox="0 0 110 110">
            <circle cx="55" cy="55" r="44" fill="none" stroke="rgba(255,255,255,.15)" stroke-width="12"/>
            <circle id="donut-arc" cx="55" cy="55" r="44" fill="none" stroke="#00B894" stroke-width="12"
              stroke-dasharray="276.46" stroke-dashoffset="276.46" stroke-linecap="round"/>
          </svg>
          <div class="donut-center">
            <div class="donut-pct" id="result-pct">0%</div>
            <div class="donut-status" id="result-status-icon">—</div>
          </div>
        </div>
        <div class="results-info" style="flex:1;min-width:220px;">
          <h2 id="result-name">Resultado</h2>
          <p id="result-subtitle">Nivel — Candidato</p>
          <div class="results-kpis">
            <div class="results-kpi"><span class="results-kpi-val" id="kpi-pts">—</span><span class="results-kpi-label">Pts. Obtenidos</span></div>
            <div class="results-kpi"><span class="results-kpi-val" id="kpi-max">—</span><span class="results-kpi-label">Pts. Máximos</span></div>
            <div class="results-kpi"><span class="results-kpi-val" id="kpi-correct">—</span><span class="results-kpi-label">Correctas</span></div>
            <div class="results-kpi"><span class="results-kpi-val" id="kpi-time">—</span><span class="results-kpi-label">Tiempo usado</span></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Category breakdown -->
    <div class="mui-paper" style="padding:1.25rem;margin-bottom:1.25rem;">
      <h4 style="font-size:.85rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:#94a3b8;margin:0 0 1rem;">Desempeño por Área de Conocimiento</h4>
      <div id="cat-breakdown"></div>
    </div>

    <!-- Wrong questions -->
    <div class="mui-paper" id="wrong-review" style="margin-bottom:1.25rem;">
      <div style="padding:1rem 1.25rem;border-bottom:1px solid #f1f5f9;display:flex;align-items:center;gap:.75rem;">
        <i class="ti ti-x-circle" style="font-size:1.2rem;color:#dc2626;"></i>
        <h4 style="font-size:.95rem;font-weight:700;color:#1e293b;margin:0;">Preguntas Incorrectas — Revisión de Aprendizaje</h4>
        <span class="mui-chip mui-chip-red" id="wrong-count-badge">0</span>
      </div>
      <div style="padding:1rem;" id="wrong-list"></div>
    </div>

    <!-- Action plan -->
    <div class="mui-paper" id="action-plan" style="margin-bottom:1.25rem;">
      <div style="padding:1rem 1.25rem;border-bottom:1px solid #f1f5f9;">
        <h4 style="font-size:.95rem;font-weight:700;color:#1e293b;margin:0;">Plan de Acción Recomendado</h4>
      </div>
      <div style="padding:1rem;" id="action-steps"></div>
    </div>

    <!-- Save status -->
    <div id="save-status" class="save-status"></div>

    <!-- Footer actions -->
    <div class="results-footer" id="results-footer">
      <button class="btn-action btn-restart" onclick="showSplash()"><i class="ti ti-home"></i> Inicio</button>
      <button class="btn-action btn-print" onclick="window.print()"><i class="ti ti-printer"></i> Imprimir Reporte</button>
      <button class="btn-action btn-webhook" id="btn-send-results" onclick="sendToWebhook()"><i class="ti ti-send"></i> Enviar Resultados</button>
    </div>
  </div>
</div>'''
    assert old_html_results in html, 'HTML Results block not found'
    html = html.replace(old_html_results, new_html_results)

    # 5. JS renderResults()
    old_render = '''function renderResults(){
  document.getElementById('inter-level-banner').classList.add('d-none');
  const {earned,maxPts,correct,pct,passed,catStats,timeUsed}=S.result;
  const d=CAROL_DATA[S.level];
  const color=d.meta.badge_color;
  // Hero
  document.getElementById('results-hero').style.background=`linear-gradient(135deg,#0D1B2A 0%,${color}cc 100%)`;
  const circ=276.46;
  document.getElementById('donut-arc').style.stroke=passed?'#00B894':'#E74C3C';
  setTimeout(()=>{document.getElementById('donut-arc').style.strokeDashoffset=circ*(1-pct/100);},200);
  document.getElementById('result-pct').textContent=pct+'%';
  document.getElementById('result-status-icon').textContent=passed?'✓ APROBADO':'✗ NO APROBÓ';
  document.getElementById('result-status-icon').style.color=passed?'#6ee7b7':'#fca5a5';
  document.getElementById('result-name').textContent=S.candidate.full_name;
  document.getElementById('result-subtitle').textContent=d.meta.name_es+' · '+(passed?'APROBADO':'NO APROBÓ')+' (mínimo '+d.meta.pass_pct+'%)';
  document.getElementById('kpi-pts').textContent=earned.toFixed(1);
  document.getElementById('kpi-max').textContent=maxPts.toFixed(1);
  document.getElementById('kpi-correct').textContent=correct+'/'+S.questions.length;
  const m=Math.floor(timeUsed/60);const s=timeUsed%60;
  document.getElementById('kpi-time').textContent=m+'m '+s+'s';
  // Category breakdown
  const bd=document.getElementById('cat-breakdown');bd.innerHTML='';
  Object.entries(catStats).sort((a,b)=>a[1].correct/a[1].total-b[1].correct/b[1].total).forEach(([cat,st])=>{
    const catPct=Math.round(st.correct/st.total*100);
    const catColor=CAT_COLORS[cat]||'#64748b';
    const passing=catPct>=65;
    const row=document.createElement('div');row.className='cat-result-row';
    row.innerHTML=`
      <span class="cat-result-label">${cat}</span>
      <div class="cat-bar-wrap"><div class="cat-bar-fill" style="width:0%;background:${catColor};" data-w="${catPct}"></div></div>
      <span class="cat-result-pct" style="color:${passing?'#16a34a':'#dc2626'}">${catPct}%</span>
      <span class="cat-result-pass" style="background:${passing?'#dcfce7':'#fee2e2'};color:${passing?'#166534':'#991b1b'}">${st.correct}/${st.total}</span>`;
    bd.appendChild(row);
    setTimeout(()=>{row.querySelector('.cat-bar-fill').style.width=catPct+'%';},300);
  });
  // Wrong questions
  const wrongList=document.getElementById('wrong-list');wrongList.innerHTML='';
  const wrongs=S.questions.filter(q=>S.answers[q.id]!==S.answerKey[q.id].correct_index);
  document.getElementById('wrong-count-badge').textContent=wrongs.length+' preguntas';
  const letters=['A','B','C','D'];
  wrongs.forEach(q=>{
    const ak=S.answerKey[q.id];const chosen=S.answers[q.id];
    const div=document.createElement('div');div.className='wrong-item';
    const wrongOpts=q.options.map((opt,i)=>{
      if(i===chosen && chosen!==ak.correct_index)return`<div class="wrong-opt chosen"><i class="ti ti-x"></i>${letters[i]}. ${opt}</div>`;
      return'';
    }).join('');
    div.innerHTML=`
      <div class="wrong-item-meta">
        <span class="q-cat-badge">${q.category}</span>
        <span class="q-type-badge ${q.type==='Teórico'?'teorico':'practico'}">${q.type}</span>
        <span style="font-size:.72rem;color:#94a3b8;">${q.score} pts</span>
      </div>
      <div class="wrong-q-text">${q.question}</div>
      <div class="wrong-options">${wrongOpts}</div>
      <div class="wrong-reasoning"><i class="ti ti-bulb"></i>${ak.reasoning}</div>`;
    wrongList.appendChild(div);
  });
  if(!wrongs.length)document.getElementById('wrong-review').style.display='none';
  // Action plan
  const weakCats=Object.entries(catStats).filter(([,st])=>st.correct/st.total<0.7).sort((a,b)=>a[1].correct/a[1].total-b[1].correct/b[1].total);
  const steps=document.getElementById('action-steps');steps.innerHTML='';
  if(!weakCats.length){
    steps.innerHTML='<div style="padding:1.25rem 1.5rem;color:#16a34a;font-size:.9rem;display:flex;gap:.5rem;align-items:center;"><i class="ti ti-check-circle"></i> Excelente desempeño en todas las áreas. Se recomienda mantener y compartir conocimiento con el equipo.</div>';
  }else{
    weakCats.forEach(([cat,st])=>{
      const plan=ACTION_PLANS[cat]||{duration:'1 semana',actions:['Revisión teórica del área.','Práctica supervisada en piso.'],kpi:'Superar 70% en re-evaluación del área.'};
      const pct=Math.round(st.correct/st.total*100);
      const isCrit=pct<55;
      const sc=isCrit?'#dc2626':'#f59e0b';const scBg=isCrit?'#fee2e2':'#fef3c7';
      const div=document.createElement('div');div.className='action-step';
      div.innerHTML=`
        <div class="step-priority">
          <div class="step-priority-badge" style="background:${scBg};color:${sc};">${isCrit?'CRÍTICO':'MEJORA'}</div>
          <div style="font-size:.7rem;color:#64748b;margin-top:.35rem;">${plan.duration}</div>
          <div style="font-size:.75rem;font-weight:700;color:${sc};margin-top:.2rem;">${pct}%</div>
        </div>
        <div class="step-content">
          <h5>${cat}</h5>
          <ul>${plan.actions.map(a=>'<li>'+a+'</li>').join('')}</ul>
          <div class="step-kpi"><i class="ti ti-target"></i>${plan.kpi}</div>
        </div>`;
      steps.appendChild(div);
    });
  }
}'''

    new_render = '''function renderResults(){
  document.getElementById('inter-level-banner').classList.add('d-none');
  const {earned,maxPts,correct,pct,passed,catStats,timeUsed}=S.result;
  const d=CAROL_DATA[S.level];
  const color=d.meta.badge_color;
  // Hero
  document.getElementById('results-hero').style.background=`linear-gradient(135deg,#0D1B2A 0%,${color}cc 100%)`;
  const circ=276.46;
  document.getElementById('donut-arc').style.stroke=passed?'#00B894':'#E74C3C';
  setTimeout(()=>{document.getElementById('donut-arc').style.strokeDashoffset=circ*(1-pct/100);},200);
  document.getElementById('result-pct').textContent=pct+'%';
  document.getElementById('result-status-icon').textContent=passed?'✓ APROBADO':'✗ NO APROBÓ';
  document.getElementById('result-status-icon').style.color=passed?'#6ee7b7':'#fca5a5';
  document.getElementById('result-name').textContent=S.candidate.full_name;
  document.getElementById('result-subtitle').textContent=d.meta.name_es+' · '+(passed?'APROBADO':'NO APROBÓ')+' (mínimo '+d.meta.pass_pct+'%)';
  document.getElementById('kpi-pts').textContent=earned.toFixed(1);
  document.getElementById('kpi-max').textContent=maxPts.toFixed(1);
  document.getElementById('kpi-correct').textContent=correct+'/'+S.questions.length;
  const m=Math.floor(timeUsed/60);const s=timeUsed%60;
  document.getElementById('kpi-time').textContent=m+'m '+s+'s';
  // Category breakdown
  const bd=document.getElementById('cat-breakdown');bd.innerHTML='';
  Object.entries(catStats).sort((a,b)=>a[1].correct/a[1].total-b[1].correct/b[1].total).forEach(([cat,st])=>{
    const catPct=Math.round(st.correct/st.total*100);
    const catColor=CAT_COLORS[cat]||'#64748b';
    const passing=catPct>=65;
    const row=document.createElement('div');row.className='cat-result-row';
    row.innerHTML=`
      <div class="cat-result-header">
        <span class="cat-result-label">${cat}</span>
        <span class="cat-result-ratio">${st.correct}/${st.total}</span>
      </div>
      <div class="cat-bar-wrap"><div class="cat-bar-fill" style="width:0%;background:${catColor};" data-w="${catPct}"></div></div>
      <div class="cat-result-footer">
        <span class="cat-result-pct" style="color:${passing?'#16a34a':'#dc2626'}">${catPct}%</span>
        <span class="cat-result-pass" style="background:${passing?'#dcfce7':'#fee2e2'};color:${passing?'#166534':'#991b1b'}">${passing?'Aprobado':'Requiere refuerzo'}</span>
      </div>`;
    bd.appendChild(row);
    setTimeout(()=>{row.querySelector('.cat-bar-fill').style.width=catPct+'%';},300);
  });
  // Wrong questions — SIN revelar respuesta correcta
  const wrongList=document.getElementById('wrong-list');wrongList.innerHTML='';
  const wrongs=S.questions.filter(q=>S.answers[q.id]!==S.answerKey[q.id].correct_index);
  document.getElementById('wrong-count-badge').textContent=wrongs.length+' preguntas';
  const letters=['A','B','C','D'];
  wrongs.forEach((q,idx)=>{
    const chosen=S.answers[q.id];
    const div=document.createElement('div');div.className='mui-accordion';
    const summary=document.createElement('div');summary.className='mui-accordion-summary';
    summary.setAttribute('role','button');
    summary.innerHTML=`
      <div style="display:flex;align-items:center;gap:.5rem;flex:1;overflow:hidden;">
        <span class="q-cat-badge" style="flex-shrink:0;">${q.category}</span>
        <span class="q-type-badge ${q.type==='Teórico'?'teorico':'practico'}" style="flex-shrink:0;">${q.type}</span>
        <span class="mui-accordion-summary-text" style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${q.question}</span>
      </div>
      <div class="mui-accordion-summary-meta">
        <span class="mui-chip mui-chip-red">${letters[chosen]}</span>
        <i class="ti ti-chevron-down" style="color:#94a3b8;font-size:1rem;transition:transform .2s;"></i>
      </div>`;
    const details=document.createElement('div');details.className='mui-accordion-details';
    details.innerHTML=`
      <div class="mui-accordion-details-body">
        <div style="font-size:.78rem;color:#64748b;margin-bottom:.5rem;">${q.description}</div>
        <div style="font-size:.9rem;font-weight:600;color:#1e293b;margin-bottom:.75rem;line-height:1.4;">${q.question}</div>
        <div style="display:flex;flex-wrap:wrap;gap:.4rem;margin-bottom:.75rem;">
          ${q.options.map((opt,i)=>`<span class="mui-chip ${i===chosen?'mui-chip-red':'mui-chip-gray'}">${letters[i]}. ${opt}</span>`).join('')}
        </div>
        <div style="font-size:.8rem;color:#92400e;background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:.75rem;display:flex;align-items:flex-start;gap:.5rem;">
          <i class="ti ti-book" style="flex-shrink:0;margin-top:2px;"></i>
          <span>Revisa el material de estudio de <b>${q.category}</b> para reforzar este tema antes de la re-evaluación.</span>
        </div>
      </div>`;
    summary.onclick=()=>{
      const isOpen=details.classList.contains('open');
      document.querySelectorAll('.mui-accordion-details.open').forEach(el=>el.classList.remove('open'));
      document.querySelectorAll('.mui-accordion-summary .ti-chevron-down').forEach(el=>el.style.transform='rotate(0deg)');
      if(!isOpen){
        details.classList.add('open');
        summary.querySelector('.ti-chevron-down').style.transform='rotate(180deg)';
      }
    };
    div.appendChild(summary);
    div.appendChild(details);
    wrongList.appendChild(div);
  });
  if(!wrongs.length)document.getElementById('wrong-review').style.display='none';
  else document.getElementById('wrong-review').style.display='block';
  // Action plan
  const weakCats=Object.entries(catStats).filter(([,st])=>st.correct/st.total<0.7).sort((a,b)=>a[1].correct/a[1].total-b[1].correct/b[1].total);
  const steps=document.getElementById('action-steps');steps.innerHTML='';
  if(!weakCats.length){
    steps.innerHTML='<div style="padding:1rem;color:#16a34a;font-size:.9rem;display:flex;gap:.5rem;align-items:center;"><i class="ti ti-check-circle"></i> Excelente desempeño en todas las áreas. Se recomienda mantener y compartir conocimiento con el equipo.</div>';
  }else{
    weakCats.forEach(([cat,st])=>{
      const plan=ACTION_PLANS[cat]||{duration:'1 semana',actions:['Revisión teórica del área.','Práctica supervisada en piso.'],kpi:'Superar 70% en re-evaluación del área.'};
      const pct=Math.round(st.correct/st.total*100);
      const isCrit=pct<55;
      const sc=isCrit?'#dc2626':'#f59e0b';const scBg=isCrit?'#fee2e2':'#fef3c7';
      const div=document.createElement('div');div.className='action-step';
      div.innerHTML=`
        <div class="step-priority">
          <div class="step-priority-badge" style="background:${scBg};color:${sc};">${isCrit?'CRÍTICO':'MEJORA'}</div>
          <div style="font-size:.7rem;color:#64748b;margin-top:.35rem;">${plan.duration}</div>
          <div style="font-size:.75rem;font-weight:700;color:${sc};margin-top:.2rem;">${pct}%</div>
        </div>
        <div class="step-content">
          <h5>${cat}</h5>
          <ul>${plan.actions.map(a=>'<li>'+a+'</li>').join('')}</ul>
          <div class="step-kpi"><i class="ti ti-target"></i>${plan.kpi}</div>
        </div>`;
      steps.appendChild(div);
    });
  }
}'''
    assert old_render in html, 'renderResults() block not found'
    html = html.replace(old_render, new_render)

    # 6. JS generateReportHTML wrongHtml block
    old_wrong_block = '''  let wrongHtml='';
  const wrongs=S.questions.filter(q=>S.answers[q.id]!==S.answerKey[q.id].correct_index);
  if(wrongs.length){
    wrongHtml='<h3 style="font-size:1rem;color:#0D1B2A;margin:1.5rem 0 .5rem;">❌ Preguntas Incorrectas — Revisión</h3>';
    wrongs.forEach(q=>{
      const ak=S.answerKey[q.id];const chosen=S.answers[q.id];
      wrongHtml+=`<div style="padding:.75rem 0;border-bottom:1px solid #f1f5f9;">
        <div style="font-size:.78rem;color:#64748b;margin-bottom:.25rem;">${q.category} · ${q.type} · ${q.score} pts</div>
        <div style="font-size:.85rem;font-weight:600;color:#1e293b;line-height:1.4;margin-bottom:.25rem;">${q.question}</div>
        <div style="font-size:.78rem;padding:.25rem .5rem;border-radius:6px;background:#fee2e2;color:#991b1b;display:inline-block;"><b>Tu respuesta:</b> ${letters[chosen]}. ${q.options[chosen]}</div>
        <div style="font-size:.78rem;color:#78350f;background:#fffbeb;border:1px solid #fde68a;border-radius:6px;padding:.5rem .75rem;margin-top:.35rem;">💡 ${ak.reasoning}</div>
      </div>`;
    });
  }else{
    wrongHtml='<div style="color:#16a34a;font-weight:700;padding:1rem 0;">✅ Sin preguntas incorrectas — excelente desempeño.</div>';
  }'''

    new_wrong_block = '''  let wrongHtml='';
  const wrongs=S.questions.filter(q=>S.answers[q.id]!==S.answerKey[q.id].correct_index);
  if(wrongs.length){
    wrongHtml='<h3 style="font-size:1rem;color:#0D1B2A;margin:1.5rem 0 .5rem;">❌ Preguntas Incorrectas — Revisión</h3>';
    wrongs.forEach(q=>{
      const chosen=S.answers[q.id];
      wrongHtml+=`<div style="padding:.75rem 0;border-bottom:1px solid #f1f5f9;">
        <div style="font-size:.78rem;color:#64748b;margin-bottom:.25rem;">${q.category} · ${q.type} · ${q.score} pts</div>
        <div style="font-size:.85rem;font-weight:600;color:#1e293b;line-height:1.4;margin-bottom:.25rem;">${q.question}</div>
        <div style="font-size:.78rem;padding:.25rem .5rem;border-radius:6px;background:#fee2e2;color:#991b1b;display:inline-block;"><b>Tu respuesta:</b> ${letters[chosen]}. ${q.options[chosen]}</div>
        <div style="font-size:.78rem;color:#78350f;background:#fffbeb;border:1px solid #fde68a;border-radius:6px;padding:.5rem .75rem;margin-top:.35rem;">📚 Revisa el material de estudio de <b>${q.category}</b> para reforzar este tema.</div>
      </div>`;
    });
  }else{
    wrongHtml='<div style="color:#16a34a;font-weight:700;padding:1rem 0;">✅ Sin preguntas incorrectas — excelente desempeño.</div>';
  }'''
    assert old_wrong_block in html, 'generateReportHTML wrong block not found'
    html = html.replace(old_wrong_block, new_wrong_block)

    p.write_text(html, encoding='utf-8')
    print('carol_platform.html patched OK')


def patch_report_email():
    p = BASE / 'report_email_template.html'
    html = p.read_text(encoding='utf-8')

    old_block = '''  let wrongHtml='';
  const wrongIds=data.wrong_question_ids||[];
  if(wrongIds.length){
    wrongHtml='<h3 class="section-title">❌ Preguntas Incorrectas — Revisión</h3>';
    wrongIds.forEach(qid=>{
      const ans=answers[qid];
      if(!ans)return;
      const chosenOpt=ans.options[ans.chosen_index]||'Sin respuesta';
      wrongHtml+=`<div class="wrong-item">
        <div class="wrong-meta">
          <span>${ans.category}</span>
          <span>${ans.type}</span>
          <span>${ans.score} pts</span>
        </div>
        <div class="wrong-q">${ans.question}</div>
        <div class="wrong-opt chosen"><b>Tu respuesta:</b> ${letters[ans.chosen_index]}. ${chosenOpt}</div>
        <div class="wrong-reasoning">💡 ${ans.reasoning}</div>
      </div>`;
    });
  }else{'''

    new_block = '''  let wrongHtml='';
  const wrongIds=data.wrong_question_ids||[];
  if(wrongIds.length){
    wrongHtml='<h3 class="section-title">❌ Preguntas Incorrectas — Revisión</h3>';
    wrongIds.forEach(qid=>{
      const ans=answers[qid];
      if(!ans)return;
      const chosenOpt=ans.options[ans.chosen_index]||'Sin respuesta';
      wrongHtml+=`<div class="wrong-item">
        <div class="wrong-meta">
          <span>${ans.category}</span>
          <span>${ans.type}</span>
          <span>${ans.score} pts</span>
        </div>
        <div class="wrong-q">${ans.question}</div>
        <div class="wrong-opt chosen"><b>Tu respuesta:</b> ${letters[ans.chosen_index]}. ${chosenOpt}</div>
        <div class="wrong-reasoning">📚 Revisa el material de estudio de <b>${ans.category}</b> para reforzar este tema.</div>
      </div>`;
    });
  }else{'''
    assert old_block in html, 'report email wrong block not found'
    html = html.replace(old_block, new_block)

    p.write_text(html, encoding='utf-8')
    print('report_email_template.html patched OK')


if __name__ == '__main__':
    patch_carol_platform()
    patch_report_email()
