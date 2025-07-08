"""
Enhanced Bitcoin MVRV Dashboard
Clean, readable charts with professional analysis
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
from my_database import MyPersonalDatabase
from my_mvrv_engine import MyMVRVEngine
from btc_brain import BitcoinBrain
import time

# Page setup
st.set_page_config(
    page_title="Bitcoin MVRV Analysis Dashboard",
    page_icon="₿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced styling
st.markdown("""
<style>
    .main-title {
        background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .metric-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border-left: 4px solid #f5576c;
        margin: 1rem 0;
    }
    
    .signal-card {
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.15);
    }
    
    .buy-signal {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .sell-signal {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
    }
    
    .hold-signal {
        background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
        color: white;
    }
    
    .caution-signal {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# Initialize system
@st.cache_resource
def init_system():
    return MyPersonalDatabase(), MyMVRVEngine(), BitcoinBrain()

my_db, my_engine, my_brain = init_system()

# Header
st.markdown('<div class="main-title">₿ Bitcoin MVRV Analysis Dashboard</div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.header("📊 Analysis Controls")

# Time controls
timeframe = st.sidebar.selectbox("Timeframe", ["Last 7 Days", "Last 30 Days", "Last 90 Days"])
chart_type = st.sidebar.selectbox("Chart Style", ["Line Chart", "Candlestick", "Area Chart"])

# Map timeframe to days
days_map = {"Last 7 Days": 7, "Last 30 Days": 30, "Last 90 Days": 90}
selected_days = days_map[timeframe]

# Update controls
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("🔄 Update Data"):
        with st.spinner("Updating..."):
            my_engine.run_my_hourly_analysis()
        st.success("Updated!")
        st.rerun()

with col2:
    if st.button("📊 Refresh"):
        st.rerun()

# Get current insights
insights = my_engine.get_my_mvrv_insights()

if insights:
    # Current metrics with better layout
    st.subheader("📈 Current Market Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        delta = f"{((insights['current_mvrv'] - insights['my_7d_average']) / insights['my_7d_average'] * 100):+.1f}%" if insights['my_7d_average'] > 0 else "N/A"
        st.metric(
            "MVRV Ratio",
            f"{insights['current_mvrv']:.3f}",
            delta=delta
        )
    
    with col2:
        latest = my_db.get_my_latest_mvrv()
        if latest:
            st.metric(
                "Market Cap",
                f"${latest['market_cap']/1e9:.1f}B"
            )
    
    with col3:
        if latest:
            st.metric(
                "Realized Cap",
                f"${latest['realized_cap']/1e9:.1f}B"
            )
    
    with col4:
        st.metric(
            "Data Quality",
            f"{insights['my_confidence_avg']:.0%}",
            delta=insights['data_quality'].title()
        )
    
    # Market signal
    st.subheader("🚦 Market Signal")
    
    signal = insights['my_current_signal']
    if 'BUY' in signal or 'FEAR' in signal:
        signal_class = "buy-signal"
    elif 'SELL' in signal or 'GREED' in signal:
        signal_class = "sell-signal"
    elif 'HOLD' in signal or 'NORMAL' in signal:
        signal_class = "hold-signal"
    else:
        signal_class = "caution-signal"
    
    st.markdown(f"""
    <div class="signal-card {signal_class}">
        {insights['my_current_signal']}<br>
        <strong>Action: {insights['my_current_action']}</strong><br>
        {insights['my_current_meaning']}
    </div>
    """, unsafe_allow_html=True)

# Enhanced Historical Analysis
st.subheader("📊 Historical MVRV Analysis")

# Get historical data
history = my_db.get_my_mvrv_history('hourly', selected_days * 24)

if history:
    df = pd.DataFrame(history)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Create main MVRV chart with better readability
    fig = go.Figure()
    
    if chart_type == "Line Chart":
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['ratio'],
            mode='lines',
            name='MVRV Ratio',
            line=dict(color='#667eea', width=3),
            hovertemplate='<b>MVRV Ratio</b><br>%{x}<br>%{y:.4f}<extra></extra>'
        ))
    
    elif chart_type == "Area Chart":
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['ratio'],
            mode='lines',
            name='MVRV Ratio',
            line=dict(color='#667eea', width=2),
            fill='tonexty',
            fillcolor='rgba(102, 126, 234, 0.1)',
            hovertemplate='<b>MVRV Ratio</b><br>%{x}<br>%{y:.4f}<extra></extra>'
        ))
    
    # Add reference zones with better colors
    fig.add_hline(y=1.0, line_dash="solid", line_color="gray", line_width=2,
                  annotation_text="Fair Value (1.0)", annotation_position="top right")
    fig.add_hline(y=2.4, line_dash="dash", line_color="orange", line_width=2,
                  annotation_text="Caution (2.4)", annotation_position="top right")
    fig.add_hline(y=3.7, line_dash="dash", line_color="red", line_width=2,
                  annotation_text="Overvalued (3.7)", annotation_position="top right")
    
    # Colored zones with transparency
    fig.add_hrect(y0=0, y1=1.0, fillcolor="rgba(102, 126, 234, 0.1)", 
                  annotation_text="Accumulation Zone", annotation_position="inside top")
    fig.add_hrect(y0=1.0, y1=2.4, fillcolor="rgba(76, 201, 196, 0.1)",
                  annotation_text="Normal Zone", annotation_position="inside top")
    fig.add_hrect(y0=2.4, y1=3.7, fillcolor="rgba(255, 165, 0, 0.1)",
                  annotation_text="Caution Zone", annotation_position="inside top")
    fig.add_hrect(y0=3.7, y1=10, fillcolor="rgba(255, 99, 132, 0.1)",
                  annotation_text="Distribution Zone", annotation_position="inside top")
    
    # Enhanced layout
    fig.update_layout(
        title=dict(
            text=f"Bitcoin MVRV Ratio - {timeframe}",
            font=dict(size=24, color='#333')
        ),
        xaxis=dict(
            title="Date",
            showgrid=True,
            gridcolor='rgba(128,128,128,0.2)',
            title_font=dict(size=14)
        ),
        yaxis=dict(
            title="MVRV Ratio",
            showgrid=True,
            gridcolor='rgba(128,128,128,0.2)',
            title_font=dict(size=14)
        ),
        height=600,
        showlegend=False,
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Secondary analysis charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Market vs Realized Cap")
        
        fig_caps = go.Figure()
        
        fig_caps.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['market_cap']/1e9,
            mode='lines',
            name='Market Cap',
            line=dict(color='#f5576c', width=3)
        ))
        
        fig_caps.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['realized_cap']/1e9,
            mode='lines',
            name='Realized Cap',
            line=dict(color='#4ecdc4', width=3)
        ))
        
        fig_caps.update_layout(
            xaxis_title="Date",
            yaxis_title="Billions USD",
            height=400,
            showlegend=True,
            legend=dict(x=0, y=1),
            plot_bgcolor='white'
        )
        
        st.plotly_chart(fig_caps, use_container_width=True)
    
    with col2:
        st.subheader("📊 MVRV Distribution")
        
        fig_hist = px.histogram(
            df, 
            x='ratio',
            nbins=20,
            title="",
            color_discrete_sequence=['#667eea']
        )
        
        fig_hist.update_layout(
            xaxis_title="MVRV Ratio",
            yaxis_title="Frequency",
            height=400,
            plot_bgcolor='white'
        )
        
        # Add vertical lines for key levels
        fig_hist.add_vline(x=1.0, line_dash="dash", line_color="gray")
        fig_hist.add_vline(x=2.4, line_dash="dash", line_color="orange")
        fig_hist.add_vline(x=3.7, line_dash="dash", line_color="red")
        
        st.plotly_chart(fig_hist, use_container_width=True)
    
    # MVRV trend analysis
    st.subheader("📈 Trend Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "7-Day Average",
            f"{insights['my_7d_average']:.3f}",
            delta=f"Range: {insights['my_7d_min']:.3f} - {insights['my_7d_max']:.3f}"
        )
    
    with col2:
        volatility = insights['my_volatility']
        vol_status = "High" if volatility > 0.5 else "Medium" if volatility > 0.2 else "Low"
        st.metric(
            "Volatility",
            f"{volatility:.3f}",
            delta=vol_status
        )
    
    with col3:
        trend_emoji = "📈" if insights['my_trend'] == 'rising' else "📉"
        st.metric(
            "Current Trend",
            f"{trend_emoji} {insights['my_trend'].title()}",
            delta=f"Confidence: {insights['my_confidence_avg']:.0%}"
        )

# Data table with recent values
st.subheader("📋 Recent MVRV Data")

if history:
    recent_df = df.tail(10).copy()
    recent_df['Date'] = recent_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
    recent_df['MVRV'] = recent_df['ratio'].round(4)
    recent_df['Market Cap'] = (recent_df['market_cap']/1e9).round(1).astype(str) + 'B'
    recent_df['Realized Cap'] = (recent_df['realized_cap']/1e9).round(1).astype(str) + 'B'
    
    display_df = recent_df[['Date', 'MVRV', 'Market Cap', 'Realized Cap']].iloc[::-1]
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

# System status
st.sidebar.subheader("🔧 System Status")

brain_status = my_brain.check_my_connection()
if brain_status['brain_online']:
    st.sidebar.success("✅ Blockchain Connected")
else:
    st.sidebar.error("❌ Blockchain Offline")

db_stats = my_db.get_my_database_stats()
st.sidebar.info(f"📊 MVRV Records: {db_stats.get('my_mvrv_analysis', 0)}")
st.sidebar.info(f"🔍 UTXO Records: {db_stats.get('my_utxo_discoveries', 0)}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p><strong>Bitcoin MVRV Analysis Dashboard</strong></p>
    <p>Real blockchain data • Professional analysis • Updated hourly</p>
</div>
""", unsafe_allow_html=True)