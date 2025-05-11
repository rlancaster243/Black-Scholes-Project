import streamlit as st
import numpy as np
import pandas as pd
from scipy.stats import norm
import plotly.graph_objects as go

# ─── Black-Scholes Computation ──────────────────────────────────────────────────
@st.experimental_memo
def compute_option_matrices(S_range, σ_range, T, K, r):
    S, σ = np.meshgrid(S_range, σ_range)
    vt = σ * np.sqrt(T)
    d1 = (np.log(S/K) + (r + 0.5 * σ**2)*T) / vt
    d2 = d1 - vt
    df = np.exp(-r * T)
    call = S * norm.cdf(d1) - K * df * norm.cdf(d2)
    put  = K * df * norm.cdf(-d2) - S * norm.cdf(-d1)
    return call, put

# ─── Plotly Heatmap Function ──────────────────────────────────────────────────
def plotly_heatmap(z, x, y, title, colorscale="Viridis"):
    fig = go.Figure(
        go.Heatmap(
            z=z,
            x=np.round(x, 2),
            y=np.round(y, 2),
            colorscale=colorscale,
            hovertemplate="Spot: %{x}<br>Vol: %{y}<br>Price: %{z:.2f}<extra></extra>"
        )
    )
    fig.update_layout(
        title=title,
        xaxis_title="Spot Price",
        yaxis_title="Volatility",
        margin=dict(l=60, r=20, t=50, b=60)
    )
    return fig

# ─── Streamlit UI ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="BS Model Heatmap", layout="wide")
st.title("Interactive Black-Scholes Heatmaps")

# Sidebar inputs
with st.sidebar:
    st.header("Model Parameters")
    S0 = st.number_input("Current Price",  value=100.0)
    K  = st.number_input("Strike Price",   value=100.0)
    T  = st.number_input("Time to Maturity (yrs)", value=1.0)
    σ0 = st.number_input("Volatility (σ)",  value=0.2)
    r  = st.number_input("Risk-Free Rate", value=0.05)
    st.markdown("---")
    st.header("Heatmap Ranges")
    S_min = st.number_input("Min Spot", value=S0 * 0.8)
    S_max = st.number_input("Max Spot", value=S0 * 1.2)
    σ_min = st.slider("Min Vol", 0.01, 1.0, σ0 * 0.5)
    σ_max = st.slider("Max Vol", 0.01, 1.0, σ0 * 1.5)

# Build grids
spot_grid = np.linspace(S_min, S_max, 50)
vol_grid  = np.linspace(σ_min, σ_max, 50)

# Compute matrices (cached)
call_matrix, put_matrix = compute_option_matrices(spot_grid, vol_grid, T, K, r)

# Show single-point prices
st.subheader("Spot & Vol at Current Values")
call0, put0 = compute_option_matrices(
    np.array([S0]), np.array([σ0]), T, K, r
)
col1, col2 = st.columns(2)
col1.metric("Call Price", f"${call0[0,0]:.2f}")
col2.metric("Put Price",  f"${put0[0,0]:.2f}")

st.markdown("---")
st.subheader("Call Price Heatmap")
st.plotly_chart(
    plotly_heatmap(call_matrix, spot_grid, vol_grid, "CALL Prices"),
    use_container_width=True
)

st.subheader("Put Price Heatmap")
st.plotly_chart(
    plotly_heatmap(put_matrix, spot_grid, vol_grid, "PUT Prices", colorscale="Magma"),
    use_container_width=True
)
