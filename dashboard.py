import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
from database import MVRVDatabase
from mvrv_calculator import MVRVCalculator
from scheduler import MVRVScheduler
import time

# Page configuration
st.set_page_config(
    page_title="Bitcoin MVRV Dashboard",
    page_icon="₿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for colorful dashboard
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #FF6B35, #F7931E, #FFD700);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .signal-buy {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        font-weight: bold;
    }
    
    .signal-sell {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        font-weight: bold;
    }
    
    .signal-hold {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1rem;
        border-radius: 10px;
        color: #333;
        text-align: center;
        font-weight: bold;
    }
    
    .signal-caution {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1rem;
        border-radius: 10px;
        color: #333;
        text-align: center;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize components
@st.cache_resource
def init_components():
    db = MVRVDatabase()
    calculator = MVRVCalculator()
    scheduler = MVRVScheduler()
    return db, calculator, scheduler

db, calculator, scheduler = init_components()

# Header
st.markdown('<div class="main-header">₿ Bitcoin MVRV Analysis Dashboard</div>', unsafe_allow_html=True)

# Sidebar controls
st.sidebar.header("🎛️ Dashboard Controls")

# Auto-refresh toggle
auto_refresh = st.sidebar.checkbox("🔄 Auto-refresh (30s)", value=False)
if auto_refresh:
    time.sleep(30)
    st.rerun()

# Manual controls
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("📊 Update Now"):
        with st.spinner("Updating data..."):
            scheduler.run_manual_update()
        st.success("Data updated!")
        st.rerun()

with col2:
    if st.button("🔄 Refresh Dashboard"):
        st.rerun()

# Time range selector
st.sidebar.subheader("📅 Time Range")
timeframe = st.sidebar.selectbox("Select Timeframe", ["Hourly", "Daily"])
days_back = st.sidebar.slider("Days to Display", 1, 30, 7)

# Get current MVRV statistics
stats = calculator.get_mvrv_statistics()

if stats:
    # Current metrics row
    st.subheader("📈 Current Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🎯 MVRV Ratio",
            value=f"{stats['current']:.4f}",
            delta=f"{((stats['current'] - stats['avg_7d']) / stats['avg_7d'] * 100):+.1f}%" if stats['avg_7d'] > 0 else None
        )
    
    with col2:
        latest_data = db.get_latest_mvrv()
        if latest_data:
            st.metric(
                label="💰 Market Cap",
                value=f"${latest_data['market_cap']/1e9:.1f}B"
            )
    
    with col3:
        if latest_data:
            st.metric(
                label="🔄 Realized Cap",
                value=f"${latest_data['realized_cap']/1e9:.1f}B"
            )
    
    with col4:
        st.metric(
            label="📊 7D Average",
            value=f"{stats['avg_7d']:.4f}",
            delta=f"Range: {stats['min_7d']:.3f} - {stats['max_7d']:.3f}"
        )
    
    # Market signal
    st.subheader("🚦 Market Signal")
    
    signal_class = f"signal-{stats['signal'].lower()}"
    if stats['signal'] == 'BUY':
        signal_class = "signal-buy"
    elif stats['signal'] == 'SELL':
        signal_class = "signal-sell"
    elif stats['signal'] == 'HOLD':
        signal_class = "signal-hold"
    else:
        signal_class = "signal-caution"
    
    st.markdown(f"""
    <div class="{signal_class}">
        🎯 {stats['signal']} SIGNAL<br>
        {stats['signal_desc']}<br>
        Current MVRV: {stats['current']:.4f}
    </div>
    """, unsafe_allow_html=True)

# Historical charts
st.subheader("📊 Historical Analysis")

# Get historical data
timeframe_db = 'hourly' if timeframe == 'Hourly' else 'daily'
limit = days_back * 24 if timeframe == 'Hourly' else days_back
historical_data = db.get_mvrv_history(timeframe_db, limit)

if historical_data:
    df = pd.DataFrame(historical_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Main MVRV chart
    fig_mvrv = go.Figure()
    
    # MVRV line with gradient
    fig_mvrv.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['ratio'],
        mode='lines+markers',
        name='MVRV Ratio',
        line=dict(color='#FF6B35', width=3),
        marker=dict(size=6, color='#FF6B35'),
        hovertemplate='<b>MVRV Ratio</b><br>Date: %{x}<br>Ratio: %{y:.4f}<extra></extra>'
    ))
    
    # Reference lines with colors
    fig_mvrv.add_hline(y=1.0, line_dash="dash", line_color="blue", 
                       annotation_text="Break-even (1.0)", annotation_position="top right")
    fig_mvrv.add_hline(y=2.4, line_dash="dash", line_color="orange", 
                       annotation_text="Caution Zone (2.4)", annotation_position="top right")
    fig_mvrv.add_hline(y=3.7, line_dash="dash", line_color="red", 
                       annotation_text="Historical Top (3.7)", annotation_position="top right")
    
    # Color zones
    fig_mvrv.add_hrect(y0=0, y1=1.0, fillcolor="lightblue", opacity=0.2, 
                       annotation_text="Accumulation Zone", annotation_position="inside top")
    fig_mvrv.add_hrect(y0=1.0, y1=2.4, fillcolor="lightgreen", opacity=0.2,
                       annotation_text="Normal Zone", annotation_position="inside top")
    fig_mvrv.add_hrect(y0=2.4, y1=3.7, fillcolor="lightyellow", opacity=0.2,
                       annotation_text="Caution Zone", annotation_position="inside top")
    fig_mvrv.add_hrect(y0=3.7, y1=10, fillcolor="lightcoral", opacity=0.2,
                       annotation_text="Danger Zone", annotation_position="inside top")
    
    fig_mvrv.update_layout(
        title=f"Bitcoin MVRV Ratio - {timeframe} Data",
        xaxis_title="Date",
        yaxis_title="MVRV Ratio",
        height=500,
        showlegend=True,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_mvrv, use_container_width=True)
    
    # Secondary charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Market Cap vs Realized Cap
        fig_caps = go.Figure()
        
        fig_caps.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['market_cap']/1e9,
            mode='lines',
            name='Market Cap',
            line=dict(color='#FF6B35', width=2)
        ))
        
        fig_caps.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['realized_cap']/1e9,
            mode='lines',
            name='Realized Cap',
            line=dict(color='#4ECDC4', width=2)
        ))
        
        fig_caps.update_layout(
            title="Market Cap vs Realized Cap",
            xaxis_title="Date",
            yaxis_title="Billions USD",
            height=400
        )
        
        st.plotly_chart(fig_caps, use_container_width=True)
    
    with col2:
        # MVRV distribution
        fig_dist = px.histogram(
            df, 
            x='ratio', 
            nbins=30,
            title="MVRV Ratio Distribution",
            color_discrete_sequence=['#FF6B35']
        )
        
        fig_dist.update_layout(
            xaxis_title="MVRV Ratio",
            yaxis_title="Frequency",
            height=400
        )
        
        st.plotly_chart(fig_dist, use_container_width=True)

# Data table
st.subheader("📋 Recent Data")

if historical_data:
    # Show last 10 records
    recent_df = df.tail(10).copy()
    recent_df['timestamp'] = recent_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
    recent_df['market_cap'] = recent_df['market_cap'].apply(lambda x: f"${x/1e9:.1f}B")
    recent_df['realized_cap'] = recent_df['realized_cap'].apply(lambda x: f"${x/1e9:.1f}B")
    recent_df['ratio'] = recent_df['ratio'].apply(lambda x: f"{x:.4f}")
    
    recent_df = recent_df.rename(columns={
        'timestamp': 'Date/Time',
        'market_cap': 'Market Cap',
        'realized_cap': 'Realized Cap',
        'ratio': 'MVRV Ratio'
    })
    
    st.dataframe(recent_df, use_container_width=True)

# System status
st.sidebar.subheader("🔧 System Status")

scheduler_status = scheduler.get_scheduler_status()
if scheduler_status['running']:
    st.sidebar.success("✅ Scheduler Running")
else:
    st.sidebar.error("❌ Scheduler Stopped")

st.sidebar.info(f"📊 Active Jobs: {scheduler_status['job_count']}")

# MVRV explanation
with st.expander("📚 Understanding MVRV"):
    st.markdown("""
    ### What is MVRV?
    
    **Market Value to Realized Value (MVRV)** is a fundamental Bitcoin metric that compares:
    
    - **Market Value**: Current price × Total supply
    - **Realized Value**: Sum of all coins valued at their last transaction price
    
    ### Interpretation Guide:
    
    🔵 **MVRV < 1.0**: Market trading below "fair value" - potential accumulation zone
    
    🟢 **MVRV 1.0-2.4**: Normal/healthy market conditions
    
    🟡 **MVRV 2.4-3.7**: Elevated levels - exercise caution
    
    🔴 **MVRV > 3.7**: Historically overvalued - potential distribution zone
    
    ### Why It Matters:
    
    - Helps identify market tops and bottoms
    - Shows overall market profitability
    - Useful for long-term investment decisions
    - Based on actual on-chain transaction data
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🚀 Bitcoin MVRV Dashboard | Real-time On-chain Analysis</p>
    <p>Data updates hourly | Built with Streamlit & SQLite</p>
</div>
""", unsafe_allow_html=True)