import streamlit as st
import pandas as pd
from ui_constants import (
    PAGE_CONFIG, LAYOUT_RATIO, SESSION_DEFAULTS,
    DTYPE_BADGE_COLORS, CUSTOM_CSS, ICON,
)

# must be first
st.set_page_config(**PAGE_CONFIG)

# ── Backend Mock/Imports ───────────────────────────────────────────────────
try:
    from llm_client import check_server_health
    from rag_engine import build_rag_index
    from data_engine import run_auto_insights, answer_question
except ImportError:
    def check_server_health(): return "online"
    def build_rag_index(df): pass
    def run_auto_insights(df):
        return [{"question": "Dataset Preview", "answer": "Data loaded and indexed successfully."}]
    def answer_question(df, question, history):
        return {
            "answer": "Analysis complete. Here are the key findings from your dataset.",
            "code": "df.describe()",
            "explanation": "Summary statistics computed.",
            "chart": None,
        }

# ── Session Init ───────────────────────────────────────────────────────────
def _init():
    for k, v in SESSION_DEFAULTS.items():
        if k not in st.session_state:
            st.session_state[k] = v

# ── Question handler ───────────────────────────────────────────────────────
def _handle_question(df, question: str):
    st.session_state.chat_history.append({"role": "user", "content": question})
    st.session_state.query_history.append(question)
    result = answer_question(df, question, list(st.session_state.chat_history))
    st.session_state.chat_history.append({
        "role": "assistant",
        "answer":      result.get("answer"),
        "code":        result.get("code"),
        "explanation": result.get("explanation"),
        "chart":       result.get("chart"),
    })
    st.session_state.current_chart = result.get("chart")
    st.rerun()


# ══════════════════════════════════════════════════════════════════════════
# LEFT PANEL
# ══════════════════════════════════════════════════════════════════════════
def render_left(df):
    indexed = st.session_state.rag_indexed

    # ── Brand strip ───────────────────────────────────────────────────────
    st.markdown("""
        <div class="lp-brand">
            <div class="lp-brand-ico">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                     viewBox="0 0 24 24" fill="none" stroke="#fff"
                     stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                </svg>
            </div>
            <span class="lp-brand-name">DataChat</span>
            <span class="lp-brand-tag">AI</span>
        </div>
    """, unsafe_allow_html=True)

    # ── Upload header ─────────────────────────────────────────────────────
    st.markdown("""
        <div class="lp-shdr">
            <svg xmlns="http://www.w3.org/2000/svg" width="11" height="11"
                 viewBox="0 0 24 24" fill="none" stroke="currentColor"
                 stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="16 16 12 12 8 16"/>
              <line x1="12" y1="12" x2="12" y2="21"/>
              <path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/>
            </svg>
            Data Source
        </div>
    """, unsafe_allow_html=True)

    # ── File uploader (native Streamlit widget) ───────────────────────────
    uploaded = st.file_uploader(
        "Upload CSV",
        type=["csv"],
        label_visibility="collapsed",
    )

    if uploaded:
        new_size = round(uploaded.size / 1024, 2)
        if st.session_state.file_size_kb != new_size:
            df_new = pd.read_csv(uploaded)
            st.session_state.update({
                "df": df_new, "file_size_kb": new_size, "rag_indexed": False,
                "chat_history": [], "query_history": [], "current_chart": None
            })
            build_rag_index(df_new)
            st.session_state.auto_insights = run_auto_insights(df_new)
            st.session_state.rag_indexed = True
            st.rerun()

    # ── Metrics header ────────────────────────────────────────────────────
    st.markdown("""
        <div class="lp-shdr" style="margin-top:6px;">
            <svg xmlns="http://www.w3.org/2000/svg" width="11" height="11"
                 viewBox="0 0 24 24" fill="none" stroke="currentColor"
                 stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polygon points="12 2 2 7 12 12 22 7 12 2"/>
              <polyline points="2 17 12 22 22 17"/>
              <polyline points="2 12 12 17 22 12"/>
            </svg>
            Dataset Metrics
        </div>
    """, unsafe_allow_html=True)

    # ── Metrics 2×2 grid (pure HTML) ──────────────────────────────────────
    rows  = f"{len(df):,}"       if df is not None else "—"
    cols  = str(len(df.columns)) if df is not None else "—"
    nulls = str(df.isnull().sum().sum()) if df is not None else "—"
    size_kb = st.session_state.file_size_kb if st.session_state.file_size_kb else "—"

    st.markdown(f"""
        <div class="mg">
            <div class="mc">
                <div class="mc-ico blue">
                    <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13"
                         viewBox="0 0 24 24" fill="none" stroke="currentColor"
                         stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/>
                      <line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/>
                      <line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/>
                    </svg>
                </div>
                <div class="mc-val">{rows}</div>
                <div class="mc-lbl">Rows</div>
            </div>
            <div class="mc">
                <div class="mc-ico indigo">
                    <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13"
                         viewBox="0 0 24 24" fill="none" stroke="currentColor"
                         stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <rect x="3" y="3" width="18" height="18" rx="2"/>
                      <line x1="12" y1="3" x2="12" y2="21"/>
                    </svg>
                </div>
                <div class="mc-val">{cols}</div>
                <div class="mc-lbl">Columns</div>
            </div>
            <div class="mc">
                <div class="mc-ico cyan">
                    <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13"
                         viewBox="0 0 24 24" fill="none" stroke="currentColor"
                         stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                      <polyline points="7 10 12 15 17 10"/>
                      <line x1="12" y1="15" x2="12" y2="3"/>
                    </svg>
                </div>
                <div class="mc-val">{size_kb}</div>
                <div class="mc-lbl">KB</div>
            </div>
            <div class="mc">
                <div class="mc-ico amber">
                    <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13"
                         viewBox="0 0 24 24" fill="none" stroke="currentColor"
                         stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <circle cx="12" cy="12" r="10"/>
                      <line x1="12" y1="8" x2="12" y2="12"/>
                      <line x1="12" y1="16" x2="12.01" y2="16"/>
                    </svg>
                </div>
                <div class="mc-val">{nulls}</div>
                <div class="mc-lbl">Nulls</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ── Schema section ────────────────────────────────────────────────────
    st.markdown("""
        <div class="lp-shdr">
            <svg xmlns="http://www.w3.org/2000/svg" width="11" height="11"
                 viewBox="0 0 24 24" fill="none" stroke="currentColor"
                 stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <ellipse cx="12" cy="5" rx="9" ry="3"/>
              <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>
              <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>
            </svg>
            Schema
        </div>
    """, unsafe_allow_html=True)

    if df is not None:
        html = "<div class='bwrap'>"
        for col, dtype in df.dtypes.items():
            kind = DTYPE_BADGE_COLORS.get(getattr(dtype, "kind", "O"), "bdg-slate")
            col_safe = str(col).replace("<", "&lt;").replace(">", "&gt;")
            html += f"<span class='bdg {kind}' title='{col_safe}'>{col_safe}</span>"
        st.markdown(html + "</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="padding:0 14px 14px; font-size:0.73rem; color:#475569; line-height:1.6;">
                Upload a CSV to inspect column types.
            </div>
        """, unsafe_allow_html=True)

    # ── Auto-Insights ─────────────────────────────────────────────────────
    if st.session_state.auto_insights:
        st.markdown("""
            <div class="lp-shdr">
                <svg xmlns="http://www.w3.org/2000/svg" width="11" height="11"
                     viewBox="0 0 24 24" fill="none" stroke="currentColor"
                     stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="9" y1="18" x2="15" y2="18"/>
                  <line x1="10" y1="22" x2="14" y2="22"/>
                  <path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 0 1 8.91 14"/>
                </svg>
                Auto Insights
            </div>
        """, unsafe_allow_html=True)
        for i, insight in enumerate(st.session_state.auto_insights[:4]):
            q = str(insight.get("question", ""))[:60]
            a = str(insight.get("answer", ""))[:110]
            q_s = q.replace("<", "&lt;").replace(">", "&gt;")
            a_s = a.replace("<", "&lt;").replace(">", "&gt;")
            st.markdown(f"""
                <div style="margin:0 14px 8px; background:rgba(255,255,255,0.025);
                            border:1px solid rgba(255,255,255,0.07); border-radius:8px;
                            padding:10px 12px;">
                    <div style="font-size:0.71rem; font-weight:600;
                                color:#818cf8; margin-bottom:4px;">Q{i+1} · {q_s}</div>
                    <div style="font-size:0.69rem; color:#64748b; line-height:1.5;">{a_s}</div>
                </div>
            """, unsafe_allow_html=True)

    # ── Status footer ─────────────────────────────────────────────────────
    dot_cls  = "sdot" if indexed else "sdot offline"
    status_t = "RAG Indexed · Ready" if indexed else "Waiting for upload…"
    st.markdown(f"""
        <div class="lp-status">
            <div class="{dot_cls}"></div>
            <span>{status_t}</span>
        </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# CENTER PANEL
# ══════════════════════════════════════════════════════════════════════════
def render_center(df):
    indexed  = st.session_state.rag_indexed
    pill_cls = "ready" if indexed else "waiting"
    pill_txt = "● Ready" if indexed else "○ Waiting…"

    # ── Top bar ───────────────────────────────────────────────────────────
    st.markdown(f"""
        <div class="cp-top">
            <div class="cp-top-left">
                <div class="cp-top-ico">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14"
                         viewBox="0 0 24 24" fill="none" stroke="currentColor"
                         stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                    </svg>
                </div>
                <div>
                    <div class="cp-top-title">Conversation</div>
                    <div class="cp-top-sub">AI-powered data analysis</div>
                </div>
            </div>
            <div class="cp-status-pill {pill_cls}">{pill_txt}</div>
        </div>
    """, unsafe_allow_html=True)

    # ── Message display ───────────────────────────────────────────────────
    if df is None:
        st.markdown("""
            <div class="cp-empty">
                <div class="cp-empty-ico">✦</div>
                <div class="cp-empty-title">Upload a dataset to begin</div>
                <div class="cp-empty-sub">
                    Ask questions in plain English. DataChat reasons over your
                    data and responds with insights, statistics, and charts.
                </div>
                <div class="cp-chips">
                    <span class="cp-chip">📈 Revenue trend over time</span>
                    <span class="cp-chip">🔍 Missing values audit</span>
                    <span class="cp-chip">🔗 Top correlations</span>
                    <span class="cp-chip">📊 Column distributions</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.chat_history:
            role = msg["role"]
            if role == "user":
                content = str(msg.get("content", "")).replace("<", "&lt;").replace(">", "&gt;")
                st.markdown(f"""
                    <div class="msg-u">
                        <div class="bubble-u">{content}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                answer = str(msg.get("answer") or "").replace("<", "&lt;").replace(">", "&gt;")
                st.markdown(f"""
                    <div class="msg-a">
                        <div class="ai-ava">
                            <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13"
                                 viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                 stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                              <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
                            </svg>
                        </div>
                        <div class="bubble-a">{answer}</div>
                    </div>
                """, unsafe_allow_html=True)

    # ── Pinned input (native Streamlit widget) ────────────────────────────
    query = st.chat_input(
        "Ask about your data…",
        disabled=(df is None),
    )
    if query:
        _handle_question(df, query)


# ══════════════════════════════════════════════════════════════════════════
# RIGHT PANEL
# ══════════════════════════════════════════════════════════════════════════
def render_right():
    # ── Right panel header ────────────────────────────────────────────────
    st.markdown("""
        <div class="rp-top">
            <div class="rp-title">
                <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12"
                     viewBox="0 0 24 24" fill="none" stroke="currentColor"
                     stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="18" y1="20" x2="18" y2="10"/>
                  <line x1="12" y1="20" x2="12" y2="4"/>
                  <line x1="6" y1="20" x2="6" y2="14"/>
                  <line x1="2" y1="20" x2="22" y2="20"/>
                </svg>
                Visual Output
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ── Chart area ────────────────────────────────────────────────────────
    if st.session_state.current_chart:
        st.plotly_chart(
            st.session_state.current_chart,
            width="stretch",
            config={"displayModeBar": False},
        )
    else:
        st.markdown("""
            <div class="rp-placeholder">
                <div class="rp-ph-ico">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                         viewBox="0 0 24 24" fill="none" stroke="currentColor"
                         stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                      <line x1="18" y1="20" x2="18" y2="10"/>
                      <line x1="12" y1="20" x2="12" y2="4"/>
                      <line x1="6" y1="20" x2="6" y2="14"/>
                      <line x1="2" y1="20" x2="22" y2="20"/>
                    </svg>
                </div>
                <div class="rp-ph-lbl">Charts appear here when<br>your query generates one</div>
            </div>
        """, unsafe_allow_html=True)

    # ── Query history ─────────────────────────────────────────────────────
    history = st.session_state.query_history
    if history:
        st.markdown("""
            <div class="hist-wrap" style="margin-top:14px;">
                <div class="hist-hdr">
                    <svg xmlns="http://www.w3.org/2000/svg" width="11" height="11"
                         viewBox="0 0 24 24" fill="none" stroke="currentColor"
                         stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <circle cx="12" cy="12" r="10"/>
                      <polyline points="12 6 12 12 16 14"/>
                    </svg>
                    Query History
                </div>
        """, unsafe_allow_html=True)
        for i, q in enumerate(reversed(history[-8:])):
            q_safe = str(q).replace("<", "&lt;").replace(">", "&gt;")
            num = len(history) - i
            st.markdown(f"""
                <div class="hist-item">
                    <span class="hist-num">#{num}</span>
                    <span>{q_safe}</span>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════
def main():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    _init()

    col_l, col_c, col_r = st.columns(LAYOUT_RATIO)

    with col_l:
        render_left(st.session_state.df)

    with col_c:
        render_center(st.session_state.df)

    with col_r:
        render_right()


if __name__ == "__main__":
    main()