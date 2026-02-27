# visualizer.py — auto-chart generation from query results
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def auto_chart(question: str, result, df: pd.DataFrame):
    """Generate a Plotly figure from a query result.
    
    Accepts result as: pd.Series, pd.DataFrame, scalar, or None.
    Returns a plotly Figure or None.
    """
    if result is None:
        return None

    q = question.lower()

    try:
        # ── Series result → bar chart ────────────────────────
        if isinstance(result, pd.Series):
            if len(result) > 30:
                result = result.head(20)

            fig = px.bar(
                x=result.index.astype(str),
                y=result.values,
                labels={"x": result.index.name or "Category", "y": "Value"},
                title=question[:80],
                color_discrete_sequence=["#6366f1"],
            )
            _style(fig)
            return fig

        # ── DataFrame result → bar or table ──────────────────
        if isinstance(result, pd.DataFrame):
            if result.empty:
                return None
            if len(result) > 30:
                result = result.head(20)

            num_cols = result.select_dtypes(include="number").columns.tolist()
            cat_cols = result.select_dtypes(exclude="number").columns.tolist()

            if num_cols and cat_cols:
                fig = px.bar(
                    result,
                    x=cat_cols[0],
                    y=num_cols[0],
                    title=question[:80],
                    color_discrete_sequence=["#6366f1"],
                )
            elif num_cols:
                fig = px.bar(
                    result,
                    y=num_cols[0],
                    title=question[:80],
                    color_discrete_sequence=["#6366f1"],
                )
            else:
                # All categorical — make a horizontal bar of value counts
                col = cat_cols[0]
                vc = result[col].value_counts().head(15)
                fig = px.bar(
                    x=vc.values,
                    y=vc.index.astype(str),
                    orientation="h",
                    title=question[:80],
                    labels={"x": "Count", "y": col},
                    color_discrete_sequence=["#6366f1"],
                )
            _style(fig)
            return fig

        # ── Scalar result → indicator card ───────────────────
        if isinstance(result, (int, float)):
            fig = go.Figure(go.Indicator(
                mode="number",
                value=result,
                title={"text": question[:60]},
            ))
            _style(fig, height=250)
            return fig

        # ── String / other → no chart ────────────────────────
        return None

    except Exception:
        return None


def _style(fig, height: int = 380):
    """Apply dark-mode chart styling."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=12, color="#94a3b8"),
        title_font=dict(size=14, color="#f1f5f9"),
        height=height,
        margin=dict(l=20, r=20, t=50, b=30),
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
    )