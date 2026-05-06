<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SIG — Réseau Routier Hann Bel-Air</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Syne:wght@400;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
:root{
  --bg:#0a0e1a;--surface:#111827;--surface2:#1a2235;--border:#1e2d45;
  --accent:#00d4aa;--text:#e2e8f0;--text-dim:#64748b;
  --red:#ef4444;--orange:#f97316;--blue:#3b82f6;--green:#22c55e;--yellow:#eab308;
}
*{margin:0;padding:0;box-sizing:border-box;}
body{background:var(--bg);color:var(--text);font-family:'Space Grotesk',sans-serif;height:100vh;display:flex;flex-direction:column;overflow:hidden;}

/* ── HEADER ── */
header{background:var(--surface);border-bottom:1px solid var(--border);padding:0 20px;height:56px;display:flex;align-items:center;justify-content:space-between;flex-shrink:0;z-index:1000;}
.h-left{display:flex;align-items:center;gap:14px;}
.logo{background:linear-gradient(135deg,var(--accent),#0099cc);width:34px;height:34px;border-radius:9px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:13px;color:#000;font-family:'Syne',sans-serif;}
.h-title{font-family:'Syne',sans-serif;font-weight:800;font-size:15px;letter-spacing:-.3px;}
.h-sub{font-size:10px;color:var(--text-dim);text-transform:uppercase;letter-spacing:.5px;margin-top:1px;}
.h-stats{display:flex;gap:20px;align-items:center;}
.stat{text-align:center;}
.stat-v{font-family:'Syne',sans-serif;font-size:17px;font-weight:700;color:var(--accent);line-height:1;}
.stat-l{font-size:10px;color:var(--text-dim);text-transform:uppercase;letter-spacing:.4px;margin-top:1px;}
.sdiv{width:1px;height:28px;background:var(--border);}

/* ── MAIN ── */
.main{display:flex;flex:1;overflow:hidden;}

/* ── SIDEBAR ── */
.sidebar{width:290px;background:var(--surface);border-right:1px solid var(--border);display:flex;flex-direction:column;overflow:hidden;flex-shrink:0;z-index:500;}
.tabs{display:flex;border-bottom:1px solid var(--border);flex-shrink:0;}
.tab{flex:1;padding:9px;text-align:center;font-size:10px;font-weight:700;color:var(--text-dim);cursor:pointer;border-bottom:2px solid transparent;transition:all .15s;text-transform:uppercase;letter-spacing:.5px;}
.tab.active{color:var(--accent);border-bottom-color:var(--accent);}
.tc{display:none;overflow-y:auto;flex:1;}
.tc.active{display:flex;flex-direction:column;}
.sec{padding:14px;border-bottom:1px solid var(--border);}
.sec-t{font-size:9px;font-weight:700;color:var(--text-dim);text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;}

/* ── BASEMAP ── */
.bm-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;}
.bm-btn{padding:7px;border:1px solid var(--border);border-radius:7px;background:var(--surface2);color:var(--text-dim);font-family:'Space Grotesk',sans-serif;font-size:11px;cursor:pointer;transition:all .15s;text-align:center;font-weight:500;}
.bm-btn:hover{border-color:var(--accent);color:var(--text);}
.bm-btn.active{border-color:var(--accent);color:var(--accent);background:rgba(0,212,170,.08);}

/* ── LAYER TOGGLE ── */
.layer-list{display:flex;flex-direction:column;gap:3px;}
.li{display:flex;align-items:center;gap:9px;padding:7px 9px;border-radius:7px;cursor:pointer;transition:background .15s;user-select:none;}
.li:hover{background:var(--surface2);}
.toggle{width:30px;height:16px;background:var(--border);border-radius:8px;position:relative;transition:background .2s;flex-shrink:0;}
.toggle::after{content:'';position:absolute;width:12px;height:12px;border-radius:6px;background:#fff;top:2px;left:2px;transition:transform .2s;}
.li.on .toggle{background:var(--accent);}
.li.on .toggle::after{transform:translateX(14px);}
.dot{width:9px;height:9px;border-radius:50%;flex-shrink:0;}
.dash{width:18px;height:3px;border-radius:2px;flex-shrink:0;}
.li-info{flex:1;}
.li-name{font-size:12px;font-weight:500;}
.li-count{font-size:10px;color:var(--text-dim);}

/* ── LEGEND ── */
.leg-item{display:flex;align-items:center;gap:8px;padding:5px 0;}
.leg-sym{width:22px;flex-shrink:0;display:flex;align-items:center;justify-content:center;}
.leg-c{width:11px;height:11px;border-radius:50%;}
.leg-l{width:22px;height:3px;border-radius:2px;}
.leg-txt{font-size:11px;color:var(--text-dim);}
.info-box{margin-top:8px;padding:10px;background:rgba(0,212,170,.05);border-radius:7px;border-left:3px solid var(--accent);}
.info-box-title{font-size:9px;color:var(--accent);font-weight:700;text-transform:uppercase;letter-spacing:.5px;margin-bottom:3px;}
.info-box-body{font-size:10px;color:var(--text-dim);line-height:1.5;}

/* ── ANALYSE TAB ── */
.card{background:var(--surface2);border-radius:8px;padding:11px;border:1px solid var(--border);margin-bottom:8px;}
.card.danger{background:rgba(239,68,68,.07);border-color:rgba(239,68,68,.2);}
.card.ok{background:rgba(0,212,170,.06);border-color:rgba(0,212,170,.15);}
.card.blue{background:rgba(59,130,246,.06);border-color:rgba(59,130,246,.15);}
.card.warn{background:rgba(245,158,11,.06);border-color:rgba(245,158,11,.2);}
.card-t{font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;margin-bottom:5px;}
.card-b{font-size:11px;color:var(--text);line-height:1.6;}

/* ── MAP ── */
#map{flex:1;z-index:0;position:relative;}
.leaflet-control-zoom{border:1px solid var(--border)!important;border-radius:9px!important;overflow:hidden;}
.leaflet-control-zoom a{background:var(--surface)!important;color:var(--text)!important;border-color:var(--border)!important;width:32px!important;height:32px!important;line-height:32px!important;}
.leaflet-control-zoom a:hover{background:var(--surface2)!important;color:var(--accent)!important;}
.leaflet-control-attribution{background:rgba(10,14,26,.85)!important;color:var(--text-dim)!important;font-size:10px!important;border-radius:5px!important;}
.leaflet-control-scale-line{background:rgba(10,14,26,.8)!important;border-color:var(--accent)!important;color:var(--text)!important;font-size:10px!important;}
.leaflet-popup-content-wrapper{background:var(--surface)!important;border:1px solid var(--border)!important;border-radius:10px!important;box-shadow:0 10px 40px rgba(0,0,0,.5)!important;color:var(--text)!important;}
.leaflet-popup-tip{background:var(--surface)!important;}

/* ── POPUP ── */
.pu{font-family:'Space Grotesk',sans-serif;}
.pu-type{font-size:9px;text-transform:uppercase;letter-spacing:.8px;font-weight:700;margin-bottom:3px;}
.pu-title{font-family:'Syne',sans-serif;font-size:13px;font-weight:700;}
.pu-coord{font-size:10px;color:var(--text-dim);margin-top:3px;font-family:monospace;}

/* ── FLOATING TOOLS ── */
.mtools{position:absolute;top:14px;right:14px;display:flex;flex-direction:column;gap:7px;z-index:1000;}
.mtool{width:36px;height:36px;background:var(--surface);border:1px solid var(--border);border-radius:9px;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:15px;transition:all .15s;color:var(--text-dim);}
.mtool:hover{border-color:var(--accent);color:var(--accent);}
.mtool.active{border-color:var(--accent);color:var(--accent);background:rgba(0,212,170,.1);}

/* ── BADGE ── */
.badge{position:absolute;bottom:36px;left:14px;background:rgba(10,14,26,.9);backdrop-filter:blur(12px);border:1px solid var(--border);border-radius:10px;padding:10px 13px;z-index:1000;max-width:270px;}
.badge-t{font-family:'Syne',sans-serif;font-size:12px;font-weight:800;color:var(--accent);margin-bottom:2px;}
.badge-s{font-size:10px;color:var(--text-dim);line-height:1.4;}

/* ── STAT PANEL ── */
.statpanel{position:absolute;top:14px;left:14px;background:var(--surface);border:1px solid var(--border);border-radius:11px;padding:13px;z-index:1000;width:200px;display:none;}
.statpanel.show{display:block;}
.sp-t{font-size:9px;font-weight:700;color:var(--text-dim);text-transform:uppercase;letter-spacing:.5px;margin-bottom:10px;}
.bar-row{display:flex;align-items:center;gap:7px;margin-bottom:5px;}
.bar-label{font-size:9px;color:var(--text-dim);width:68px;flex-shrink:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.bar-wrap{flex:1;height:5px;background:var(--surface2);border-radius:3px;overflow:hidden;}
.bar-fill{height:100%;border-radius:3px;}
.bar-num{font-size:9px;color:var(--text);width:22px;text-align:right;}

/* ── STATUS BAR ── */
.status{height:26px;background:var(--surface);border-top:1px solid var(--border);display:flex;align-items:center;padding:0 14px;gap:14px;flex-shrink:0;font-size:10px;color:var(--text-dim);}
.si{display:flex;align-items:center;gap:4px;}
.sdot{width:6px;height:6px;border-radius:50%;background:var(--accent);}
.sdot.w{background:var(--orange);}
#coords{margin-left:auto;font-family:monospace;font-size:10px;}

/* ── PULSE ── */
@keyframes pulse{0%{transform:scale(.7);opacity:.9}70%{transform:scale(2.2);opacity:0}100%{transform:scale(2.2);opacity:0}}
.pulse-ring{animation:pulse 1.6s ease-out infinite;}
</style>
</head>
<body>

<!-- HEADER -->
<header>
  <div class="h-left">
    <div class="logo">SIG</div>
    <div>
      <div class="h-title">Hann Bel-Air — Réseau Routier</div>
      <div class="h-sub">Commune de Hann Bel-Air · Dakar, Sénégal · 2025–2026</div>
    </div>
  </div>
  <div class="h-stats">
    <div class="stat"><div class="stat-v">106</div><div class="stat-l">Arrêts bus</div></div>
    <div class="sdiv"></div>
    <div class="stat"><div class="stat-v">18</div><div class="stat-l">Itinéraires</div></div>
    <div class="sdiv"></div>
    <div class="stat"><div class="stat-v" style="color:var(--red)">7</div><div class="stat-l">Congestions</div></div>
    <div class="sdiv"></div>
    <div class="stat"><div class="stat-v" style="color:var(--orange)">26</div><div class="stat-l">Dégâts routiers</div></div>
    <div class="sdiv"></div>
    <div class="stat"><div class="stat-v">10</div><div class="stat-l">Hôpitaux</div></div>
  </div>
</header>

<div class="main">
  <!-- SIDEBAR -->
  <div class="sidebar">
    <div class="tabs">
      <div class="tab active" onclick="switchTab('layers')">Couches</div>
      <div class="tab" onclick="switchTab('legend')">Légende</div>
      <div class="tab" onclick="switchTab('analyse')">Analyse</div>
    </div>

    <!-- TAB COUCHES -->
    <div id="tab-layers" class="tc active">
      <div class="sec">
        <div class="sec-t">Fond de carte</div>
        <div class="bm-grid">
          <button class="bm-btn active" onclick="setBasemap('osm',this)">🗺 OSM</button>
          <button class="bm-btn" onclick="setBasemap('sat',this)">🛰 Satellite</button>
          <button class="bm-btn" onclick="setBasemap('dark',this)">🌑 Sombre</button>
          <button class="bm-btn" onclick="setBasemap('topo',this)">⛰ Topo</button>
        </div>
      </div>

      <div class="sec">
        <div class="sec-t">Réseau de transport</div>
        <div class="layer-list">
          <div class="li on" onclick="toggle('itineraires',this)">
            <div class="toggle"></div><div class="dash" style="background:#3b82f6"></div>
            <div class="li-info"><div class="li-name">Itinéraires AFTU</div><div class="li-count">18 lignes</div></div>
          </div>
          <div class="li on" onclick="toggle('arrets',this)">
            <div class="toggle"></div><div class="dot" style="background:#00d4aa"></div>
            <div class="li-info"><div class="li-name">Arrêts de bus</div><div class="li-count">106 points</div></div>
          </div>
          <div class="li on" onclick="toggle('intersections',this)">
            <div class="toggle"></div><div class="dot" style="background:#a855f7"></div>
            <div class="li-info"><div class="li-name">Intersections</div><div class="li-count">18 nœuds</div></div>
          </div>
          <div class="li on" onclick="toggle('axes_entrees',this)">
            <div class="toggle"></div><div class="dash" style="background:#22c55e"></div>
            <div class="li-info"><div class="li-name">Axes d'entrées</div><div class="li-count">4 axes</div></div>
          </div>
          <div class="li on" onclick="toggle('axes_sorties',this)">
            <div class="toggle"></div><div class="dash" style="background:#f97316"></div>
            <div class="li-info"><div class="li-name">Axes de sorties</div><div class="li-count">5 axes</div></div>
          </div>
        </div>
      </div>

      <div class="sec">
        <div class="sec-t">Problèmes de circulation</div>
        <div class="layer-list">
          <div class="li on" onclick="toggle('congestions',this)">
            <div class="toggle"></div><div class="dot" style="background:#ef4444"></div>
            <div class="li-info"><div class="li-name">Zones de congestion</div><div class="li-count">7 points critiques</div></div>
          </div>
          <div class="li on" onclick="toggle('encombrements',this)">
            <div class="toggle"></div><div class="dot" style="background:#f59e0b"></div>
            <div class="li-info"><div class="li-name">Zones d'encombrement</div><div class="li-count">3 points</div></div>
          </div>
          <div class="li on" onclick="toggle('degats',this)">
            <div class="toggle"></div><div class="dot" style="background:#dc2626"></div>
            <div class="li-info"><div class="li-name">Dégâts routiers</div><div class="li-count">26 points</div></div>
          </div>
        </div>
      </div>

      <div class="sec">
        <div class="sec-t">Services &amp; équipements</div>
        <div class="layer-list">
          <div class="li on" onclick="toggle('hopitaux',this)">
            <div class="toggle"></div><div class="dot" style="background:#ec4899"></div>
            <div class="li-info"><div class="li-name">Hôpitaux &amp; cliniques</div><div class="li-count">10 établissements</div></div>
          </div>
          <div class="li on" onclick="toggle('ecoles',this)">
            <div class="toggle"></div><div class="dot" style="background:#eab308"></div>
            <div class="li-info"><div class="li-name">Écoles</div><div class="li-count">10 établissements</div></div>
          </div>
          <div class="li on" onclick="toggle('pompiers',this)">
            <div class="toggle"></div><div class="dot" style="background:#ff6b35"></div>
            <div class="li-info"><div class="li-name">Casernes de pompiers</div><div class="li-count">2 casernes</div></div>
          </div>
          <div class="li on" onclick="toggle('stations',this)">
            <div class="toggle"></div><div class="dot" style="background:#64748b"></div>
            <div class="li-info"><div class="li-name">Stations-service</div><div class="li-count">10 stations</div></div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB LÉGENDE -->
    <div id="tab-legend" class="tc" style="padding:14px;">
      <div class="sec-t">Symbologie des couches</div>
      <div style="margin-bottom:8px;font-size:10px;color:var(--text-dim);font-style:italic;">Transport</div>
      <div class="leg-item"><div class="leg-sym"><div class="leg-l" style="background:#3b82f6"></div></div><span class="leg-txt">Itinéraires réseau AFTU</span></div>
      <div class="leg-item"><div class="leg-sym"><div class="leg-l" style="background:#22c55e"></div></div><span class="leg-txt">Axes d'entrées dans la commune</span></div>
      <div class="leg-item"><div class="leg-sym"><div class="leg-l" style="background:#f97316"></div></div><span class="leg-txt">Axes de sorties de la commune</span></div>
      <div class="leg-item"><div class="leg-sym"><div class="leg-c" style="background:#00d4aa"></div></div><span class="leg-txt">Arrêts de bus</span></div>
      <div class="leg-item"><div class="leg-sym"><div class="leg-c" style="background:#a855f7"></div></div><span class="leg-txt">Intersections / carrefours</span></div>
      <div style="margin:8px 0;font-size:10px;color:var(--text-dim);font-style:italic;">Circulation &amp; dégâts</div>
      <div class="leg-item"><div class="leg-sym"><div class="leg-c" style="background:#ef4444"></div></div><span class="leg-txt">Zone de congestion (critique)</span></div>
      <div class="leg-item"><div class="leg-sym"><div class="leg-c" style="background:#f59e0b"></div></div><span class="leg-txt">Zone d'encombrement</span></div>
      <div class="leg-item"><div class="leg-sym"><div class="leg-c" style="background:#dc2626;border:2px dashed #fca5a5;border-radius:50%"></div></div><span class="leg-txt">Dégâts routiers (chaussée)</span></div>
      <div style="margin:8px 0;font-size:10px;color:var(--text-dim);font-style:italic;">Équipements</div>
      <div class="leg-item"><div class="leg-sym"><div class="leg-c" style="background:#ec4899"></div></div><span class="leg-txt">Hôpital / Clinique</span></div>
      <div class="leg-item"><div class="leg-sym"><div class="leg-c" style="background:#eab308"></div></div><span class="leg-txt">École</span></div>
      <div class="leg-item"><div class="leg-sym"><div class="leg-c" style="background:#ff6b35"></div></div><span class="leg-txt">Caserne de pompiers / sapeurs</span></div>
      <div class="leg-item"><div class="leg-sym"><div class="leg-c" style="background:#64748b"></div></div><span class="leg-txt">Station-service</span></div>
      <div class="info-box" style="margin-top:12px;">
        <div class="info-box-title">Projection</div>
        <div class="info-box-body">WGS 84 (EPSG:4326)<br>Couches Arrêts &amp; Axes converties depuis UTM Zone 28N (EPSG:32628)</div>
      </div>
    </div>

    <!-- TAB ANALYSE -->
    <div id="tab-analyse" class="tc" style="padding:14px;">
      <div class="card">
        <div class="card-t" style="color:var(--text-dim);">Zone d'étude</div>
        <div class="card-b"><strong>Commune de Hann Bel-Air</strong><br><span style="color:var(--text-dim)">Dakar Est · ~