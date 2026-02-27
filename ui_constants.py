# ui_constants.py — v6: Premium Glassmorphism Redesign

PAGE_CONFIG = dict(
    page_title="DataChat — AI Data Intelligence",
    page_icon="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path fill='%236366f1' d='M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z'/></svg>",
    layout="wide",
    initial_sidebar_state="collapsed",
)

LAYOUT_RATIO = [2.2, 5, 2.8]

SESSION_DEFAULTS = {
    "df":             None,
    "rag_indexed":    False,
    "auto_insights":  [],
    "chat_history":   [],
    "current_chart":  None,
    "query_history":  [],
    "server_status":  "unknown",
    "file_size_kb":   0.0,
    "rerun_query":    None,
}

DTYPE_BADGE_COLORS = {
    "i": "bdg-blue",  "u": "bdg-blue",  "f": "bdg-blue",
    "O": "bdg-slate", "b": "bdg-teal",  "M": "bdg-rose",
    "m": "bdg-rose",  "c": "bdg-blue",  "S": "bdg-slate", "U": "bdg-slate",
}

def svg(path_d: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" '
        f'viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        f'{path_d}</svg>'
    )

ICON = {
    "database":  svg('<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>'),
    "server":    svg('<rect x="2" y="2" width="20" height="8" rx="2"/><rect x="2" y="14" width="20" height="8" rx="2"/><line x1="6" y1="6" x2="6.01" y2="6"/><line x1="6" y1="18" x2="6.01" y2="18"/>'),
    "chart":     svg('<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/><line x1="2" y1="20" x2="22" y2="20"/>'),
    "message":   svg('<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>'),
    "upload":    svg('<polyline points="16 16 12 12 8 16"/><line x1="12" y1="12" x2="12" y2="21"/><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/>'),
    "check":     svg('<polyline points="20 6 9 17 4 12"/>'),
    "x-circle":  svg('<circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/>'),
    "refresh":   svg('<polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>'),
    "user":      svg('<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>'),
    "bot":       svg('<rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="5" r="2"/><path d="M12 7v4"/><line x1="8" y1="16" x2="8.01" y2="16"/><line x1="16" y1="16" x2="16.01" y2="16"/>'),
    "code":      svg('<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>'),
    "layers":    svg('<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>'),
    "file":      svg('<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>'),
    "lightbulb": svg('<line x1="9" y1="18" x2="15" y2="18"/><line x1="10" y1="22" x2="14" y2="22"/><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 0 1 8.91 14"/>'),
    "send":      svg('<line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/>'),
    "sparkle":   svg('<path d="M12 2l2.4 7.4H22l-6.2 4.5 2.4 7.4L12 17l-6.2 4.3 2.4-7.4L2 9.4h7.6z"/>'),
    "zap":       svg('<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>'),
}

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ═══════════════════════════════════════════════
   DESIGN TOKENS
═══════════════════════════════════════════════ */
:root {
  --bg:          #07090f;
  --surface:     #0d1117;
  --panel:       #0f1623;
  --card:        rgba(255,255,255,0.04);
  --hover:       rgba(255,255,255,0.07);
  --border:      rgba(255,255,255,0.07);
  --border-hi:   rgba(99,102,241,0.4);

  --accent:      #6366f1;
  --accent-lt:   #818cf8;
  --accent-glow: rgba(99,102,241,0.2);
  --blue:        #3b82f6;
  --blue-glow:   rgba(59,130,246,0.2);
  --cyan:        #22d3ee;
  --green:       #10b981;
  --amber:       #f59e0b;
  --red:         #ef4444;

  --txt:         #f1f5f9;
  --txt-2:       #94a3b8;
  --txt-3:       #475569;

  --r:           10px;
  --r-sm:        7px;
  --r-pill:      999px;

  --blur:        blur(20px);
  --shadow:      0 4px 24px rgba(0,0,0,0.5), 0 1px 0 rgba(255,255,255,0.04) inset;
  --t:           all 0.2s cubic-bezier(.4,0,.2,1);
}

/* ═══════════════════════════════════════════════
   RESET & GLOBAL
═══════════════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; }

/* scrollbar */
::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 3px; }

/* ═══════════════════════════════════════════════
   STREAMLIT OVERRIDES — full-bleed, zero chrome
═══════════════════════════════════════════════ */
body, .stApp { background: var(--bg) !important; }

.main .block-container {
  padding: 0 !important;
  max-width: 100% !important;
  margin: 0 !important;
}
[data-testid="stAppViewBlockContainer"] { padding: 0 !important; }
[data-testid="stHeader"],
[data-testid="stDecoration"],
[data-testid="stToolbar"],
#MainMenu { display: none !important; }

[data-testid="stHorizontalBlock"] {
  align-items: flex-start !important;
  gap: 0 !important;
  flex-wrap: nowrap !important;
}
/* Column containers — base */
[data-testid="stColumn"] {
  padding: 0 !important;
  margin: 0 !important;
  min-height: 100vh !important;
  position: relative !important;
}

/* Inner content wrapper that Streamlit uses */
[data-testid="stColumn"] > div {
  height: 100vh !important;
  overflow-y: auto !important;
  overflow-x: hidden !important;
  display: flex !important;
  flex-direction: column !important;
  padding: 0 !important;
}

/* LEFT panel (1st column) */
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(1) > div {
  background: var(--panel) !important;
  border-right: 1px solid var(--border) !important;
}

/* CENTER panel (2nd column) */
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(2) > div {
  background:
    radial-gradient(ellipse 70% 45% at 80% -5%, rgba(99,102,241,0.07) 0%, transparent 65%),
    radial-gradient(ellipse 50% 35% at 15% 95%, rgba(59,130,246,0.05) 0%, transparent 65%),
    var(--surface) !important;
}

/* RIGHT panel (3rd column) */
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(3) > div {
  background: var(--panel) !important;
  border-left: 1px solid var(--border) !important;
}

/* Streamlit element padding inside columns */
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(1) > div > *,
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(3) > div > * {
  /* let our custom html elements control their own padding */
}

/* File uploader — no extra outer margin */
[data-testid="stFileUploader"] {
  background: transparent !important;
  padding: 0 14px 4px !important;
}

[data-testid="stFileUploader"] > div {
  background: rgba(99,102,241,0.04) !important;
  border: 2px dashed rgba(99,102,241,0.25) !important;
  border-radius: var(--r) !important;
  padding: 10px !important;
  transition: var(--t) !important;
}
[data-testid="stFileUploader"] > div:hover {
  border-color: rgba(99,102,241,0.55) !important;
  background: rgba(99,102,241,0.08) !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] { color: var(--txt-3) !important; font-size: 0.78rem !important; }
[data-testid="stFileUploaderDropzoneInstructions"] small { display: none !important; }
.uploadedFileName { color: var(--txt-2) !important; font-size: 0.75rem !important; }

/* Chat input */
[data-testid="stChatInput"] {
  background: transparent !important;
  padding: 0 6% 20px !important; /* Added horizontal padding to reduce the bar size a little */
}
[data-testid="stChatInput"] > div {
  background: rgba(15, 22, 35, 0.95) !important;
  border: 1px solid var(--border-hi) !important;
  border-radius: var(--r-pill) !important;
  backdrop-filter: var(--blur) !important;
  box-shadow: 0 0 0 4px rgba(99,102,241,0.06), var(--shadow) !important;
  padding: 4px 6px !important;
}

/* Force all inner wrappers to be transparent so the default white background is gone */
[data-testid="stChatInput"] div[data-baseweb],
[data-testid="stChatInput"] div[data-baseweb] > div {
  background: transparent !important;
}

[data-testid="stChatInput"] textarea {
  font-family: 'Inter', sans-serif !important;
  font-size: 0.88rem !important;
  color: var(--txt) !important;
  background: transparent !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: var(--txt-3) !important; }
[data-testid="stChatInputSubmitButton"] button {
  background: linear-gradient(135deg, var(--accent), #4f46e5) !important;
  border-radius: 50% !important;
  box-shadow: 0 0 16px var(--accent-glow) !important;
}

/* Plotly */
.js-plotly-plot .plotly { background: transparent !important; }
.stPlotlyChart { background: transparent !important; }

/* ════════════════════════════════════════════════
   LEFT PANEL wrapper — applied to column directly via CSS nth-child
   All panel elements sit directly in the column's flex column
════════════════════════════════════════════════ */

/* Remove old wrapper styles — replaced by nth-child targeting above */


/* brand strip */
.lp-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 18px 18px 14px;
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}
.lp-brand-ico {
  width: 32px; height: 32px;
  border-radius: 9px;
  background: linear-gradient(135deg, var(--accent), #4338ca);
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 0 18px var(--accent-glow);
  flex-shrink: 0;
}
.lp-brand-name { font-size: 0.92rem; font-weight: 700; color: var(--txt); letter-spacing: -0.01em; }
.lp-brand-tag  { font-size: 0.62rem; color: var(--txt-3); font-weight: 500; margin-left: auto;
                  background: rgba(255,255,255,0.05); border: 1px solid var(--border);
                  border-radius: var(--r-pill); padding: 2px 8px; }

/* section header */
.lp-shdr {
  display: flex; align-items: center; gap: 6px;
  padding: 14px 18px 8px;
  font-size: 0.65rem; font-weight: 700;
  color: var(--txt-3);
  text-transform: uppercase; letter-spacing: 0.1em;
  flex-shrink: 0;
}

/* metrics grid */
.mg {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  padding: 0 14px 14px;
}
.mc {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--r-sm);
  padding: 12px 12px 10px;
  display: flex; flex-direction: column; gap: 2px;
  transition: var(--t);
}
.mc:hover { background: var(--hover); border-color: rgba(255,255,255,0.12); transform: translateY(-1px); }
.mc-val { font-size: 1.2rem; font-weight: 700; color: var(--txt); line-height: 1; }
.mc-lbl { font-size: 0.62rem; font-weight: 600; color: var(--txt-3); text-transform: uppercase; letter-spacing: 0.07em; }
.mc-ico {
  font-size: 0.75rem; margin-bottom: 4px;
  width: 24px; height: 24px;
  border-radius: 6px;
  display: flex; align-items: center; justify-content: center;
}
.mc-ico.blue   { background: rgba(59,130,246,0.1);  color: var(--blue); }
.mc-ico.indigo { background: rgba(99,102,241,0.1);  color: var(--accent-lt); }
.mc-ico.cyan   { background: rgba(34,211,238,0.1);  color: var(--cyan); }
.mc-ico.amber  { background: rgba(245,158,11,0.1);  color: var(--amber); }

/* schema badges */
.bwrap { display: flex; flex-wrap: wrap; gap: 5px; padding: 0 14px 14px; }

.bdg {
  display: inline-flex; align-items: center; gap: 3px;
  padding: 3px 9px; border-radius: var(--r-pill);
  font-size: 0.67rem; font-weight: 500;
  transition: var(--t); cursor: default; max-width: 100%;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.bdg:hover { transform: scale(1.05); filter: brightness(1.15); }
.bdg-blue  { background: rgba(59,130,246,0.1);  color: #60a5fa; border: 1px solid rgba(59,130,246,0.2); }
.bdg-slate { background: rgba(148,163,184,0.08); color: #94a3b8; border: 1px solid rgba(148,163,184,0.15); }
.bdg-teal  { background: rgba(20,184,166,0.1);  color: #2dd4bf; border: 1px solid rgba(20,184,166,0.2); }
.bdg-rose  { background: rgba(244,63,94,0.1);   color: #fb7185; border: 1px solid rgba(244,63,94,0.2); }

/* status row */
.lp-status {
  margin-top: auto;
  border-top: 1px solid var(--border);
  padding: 12px 18px;
  display: flex; align-items: center; gap: 8px;
  font-size: 0.72rem; color: var(--txt-3);
}
.sdot {
  width: 7px; height: 7px; border-radius: 50%;
  background: var(--green);
  box-shadow: 0 0 8px rgba(16,185,129,0.6);
  animation: spulse 2s ease-in-out infinite;
  flex-shrink: 0;
}
.sdot.offline { background: var(--txt-3); box-shadow: none; animation: none; }
@keyframes spulse { 0%,100%{opacity:1;} 50%{opacity:0.4;} }

/* left panel scrollable body */
.lp-body {
  flex: 1; overflow-y: auto; overflow-x: hidden;
}

/* ═══════════════════════════════════════════════
   CENTER PANEL
═══════════════════════════════════════════════ */
.cp {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background:
    radial-gradient(ellipse 70% 45% at 80% -5%, rgba(99,102,241,0.07) 0%, transparent 65%),
    radial-gradient(ellipse 50% 35% at 15% 95%, rgba(59,130,246,0.05) 0%, transparent 65%),
    var(--surface);
  overflow: hidden;
  position: relative;
}

/* topbar */
.cp-top {
  display: flex; align-items: center; justify-content: space-between;
  padding: 15px 22px;
  border-bottom: 1px solid var(--border);
  background: rgba(13,17,23,0.8);
  backdrop-filter: var(--blur);
  position: relative; z-index: 10;
  flex-shrink: 0;
}
.cp-top-left { display: flex; align-items: center; gap: 10px; }
.cp-top-ico {
  width: 28px; height: 28px;
  border-radius: 8px;
  background: linear-gradient(135deg, rgba(99,102,241,0.2), rgba(79,70,229,0.1));
  border: 1px solid rgba(99,102,241,0.25);
  display: flex; align-items: center; justify-content: center;
  color: var(--accent-lt);
}
.cp-top-title { font-size: 0.85rem; font-weight: 600; color: var(--txt); }
.cp-top-sub   { font-size: 0.7rem; color: var(--txt-3); margin-top: 1px; }
.cp-status-pill {
  display: inline-flex; align-items: center; gap: 5px;
  padding: 4px 11px;
  border-radius: var(--r-pill);
  font-size: 0.7rem; font-weight: 600;
  border: 1px solid;
}
.cp-status-pill.ready   { background: rgba(16,185,129,0.08); color: #10b981; border-color: rgba(16,185,129,0.25); }
.cp-status-pill.waiting { background: rgba(245,158,11,0.08);  color: #f59e0b; border-color: rgba(245,158,11,0.25); }

/* messages area */
.cp-msgs {
  flex: 1;
  overflow-y: auto;
  padding: 24px 20px 8px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

/* empty state */
.cp-empty {
  flex: 1; display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  gap: 16px; padding: 40px 24px;
  text-align: center;
}
.cp-empty-ico {
  width: 64px; height: 64px;
  border-radius: 18px;
  background: rgba(99,102,241,0.08);
  border: 1px solid rgba(99,102,241,0.15);
  display: flex; align-items: center; justify-content: center;
  color: var(--accent-lt);
  font-size: 1.6rem;
  box-shadow: 0 0 30px rgba(99,102,241,0.1);
}
.cp-empty-title { font-size: 1rem; font-weight: 600; color: var(--txt); }
.cp-empty-sub   { font-size: 0.8rem; color: var(--txt-3); max-width: 280px; line-height: 1.6; }
.cp-chips { display: flex; gap: 7px; flex-wrap: wrap; justify-content: center; margin-top: 6px; }
.cp-chip {
  background: rgba(99,102,241,0.07);
  border: 1px solid rgba(99,102,241,0.18);
  border-radius: var(--r-pill);
  padding: 5px 13px;
  font-size: 0.73rem; color: var(--accent-lt);
  cursor: pointer; transition: var(--t);
}
.cp-chip:hover { background: rgba(99,102,241,0.16); transform: translateY(-1px); }

/* user bubble */
.msg-u { display: flex; justify-content: flex-end; }
.bubble-u {
  background: linear-gradient(135deg, rgba(99,102,241,0.18), rgba(79,70,229,0.12));
  border: 1px solid rgba(99,102,241,0.28);
  border-radius: 16px 16px 4px 16px;
  padding: 11px 16px;
  font-size: 0.85rem; color: var(--txt);
  line-height: 1.55; max-width: 75%;
  box-shadow: 0 2px 14px rgba(99,102,241,0.12);
}

/* AI bubble */
.msg-a { display: flex; justify-content: flex-start; gap: 10px; }
.ai-ava {
  width: 28px; height: 28px; border-radius: 8px;
  background: linear-gradient(135deg, rgba(34,211,238,0.15), rgba(59,130,246,0.1));
  border: 1px solid rgba(34,211,238,0.2);
  display: flex; align-items: center; justify-content: center;
  color: var(--cyan); flex-shrink: 0; margin-top: 2px;
}
.bubble-a {
  background: rgba(255,255,255,0.03);
  border: 1px solid var(--border);
  border-radius: 4px 16px 16px 16px;
  padding: 11px 16px;
  font-size: 0.85rem; color: var(--txt-2);
  line-height: 1.6; max-width: 80%;
}

/* thinking dots */
.thinking { display: flex; gap: 4px; align-items: center; padding: 4px 0; }
.thinking span {
  width: 6px; height: 6px; border-radius: 50%;
  background: var(--accent-lt);
  animation: tdot 1.2s ease-in-out infinite;
}
.thinking span:nth-child(2) { animation-delay: 0.2s; }
.thinking span:nth-child(3) { animation-delay: 0.4s; }
@keyframes tdot { 0%,80%,100%{transform:scale(0.5);opacity:0.4;} 40%{transform:scale(1);opacity:1;} }

/* pinned input row */
.cp-input-row {
  padding: 14px 20px 16px;
  background: rgba(7,9,15,0.7);
  backdrop-filter: var(--blur);
  border-top: 1px solid var(--border);
  flex-shrink: 0;
}

/* ═══════════════════════════════════════════════
   RIGHT PANEL
═══════════════════════════════════════════════ */
.rp {
  height: 100vh;
  background: var(--panel);
  border-left: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.rp-top {
  display: flex; align-items: center; justify-content: space-between;
  padding: 15px 18px;
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}
.rp-title {
  display: flex; align-items: center; gap: 7px;
  font-size: 0.7rem; font-weight: 700;
  color: var(--txt-3); text-transform: uppercase; letter-spacing: 0.1em;
}
.rp-body { flex: 1; overflow-y: auto; padding: 14px; display: flex; flex-direction: column; gap: 14px; }

/* chart placeholder */
.rp-placeholder {
  flex: 1; display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  gap: 14px; padding: 40px 20px; text-align: center;
  border: 1px dashed var(--border);
  border-radius: var(--r);
  background: rgba(255,255,255,0.015);
  min-height: 220px;
}
.rp-ph-ico {
  width: 52px; height: 52px;
  border-radius: 14px;
  background: rgba(59,130,246,0.07);
  border: 1px solid rgba(59,130,246,0.15);
  display: flex; align-items: center; justify-content: center;
  color: rgba(59,130,246,0.4);
  animation: rph 3s ease-in-out infinite;
}
@keyframes rph { 0%,100%{opacity:0.5;} 50%{opacity:1;} }
.rp-ph-lbl { font-size: 0.75rem; color: var(--txt-3); }

/* history panel */
.hist-wrap {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--r);
  overflow: hidden;
}
.hist-hdr {
  padding: 10px 14px;
  border-bottom: 1px solid var(--border);
  font-size: 0.65rem; font-weight: 700;
  color: var(--txt-3); text-transform: uppercase; letter-spacing: 0.1em;
  display: flex; align-items: center; gap: 6px;
}
.hist-item {
  padding: 9px 14px;
  border-bottom: 1px solid var(--border);
  font-size: 0.73rem; color: var(--txt-2);
  cursor: pointer; transition: var(--t);
  display: flex; gap: 8px; align-items: flex-start; line-height: 1.4;
}
.hist-item:last-child { border-bottom: none; }
.hist-item:hover { background: var(--hover); color: var(--txt); }
.hist-num {
  font-size: 0.6rem; font-weight: 700; color: var(--accent-lt);
  background: rgba(99,102,241,0.1); border-radius: 4px;
  padding: 1px 5px; flex-shrink: 0; margin-top: 1px;
}
</style>
"""