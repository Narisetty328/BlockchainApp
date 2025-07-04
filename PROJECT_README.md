# 🪙 Bitcoin MVRV Analysis System

## 🎯 Overview
Complete Python application for calculating and visualizing Bitcoin's MVRV (Market Value to Realized Value) ratio with real-time data collection and interactive dashboard.

## ⚡ Quick Start

### 1. Install Dependencies
```bash
pip install streamlit pandas numpy plotly requests schedule python-dateutil
```

### 2. Run the System
```bash
# Option 1: Setup first (recommended)
python main.py setup
python main.py

# Option 2: Direct run
python main.py
```

### 3. Access Dashboard
- Open browser to: `http://localhost:8501`
- Dashboard updates automatically every 30 seconds

## 📊 Features

### Core Functionality
- ✅ **Real-time Data**: Live Bitcoin price from CoinGecko API
- ✅ **MVRV Calculation**: Market Cap / Realized Cap ratio
- ✅ **SQLite Database**: Structured data storage
- ✅ **Automated Updates**: Hourly data collection
- ✅ **Daily Aggregation**: Summary statistics

### Dashboard Features
- 🎨 **Colorful Interface**: Gradient backgrounds and themed cards
- 📈 **Live Metrics**: Current MVRV, market cap, realized cap
- 🚦 **Market Signals**: BUY/SELL/HOLD/CAUTION indicators
- 📊 **Interactive Charts**: Historical trends with reference zones
- ⏰ **Auto-refresh**: Real-time updates

## 🏗️ System Architecture

```
Data Collection → MVRV Calculation → SQLite Storage → Streamlit Dashboard
     ↓                  ↓                ↓               ↓
CoinGecko API    Market/Realized Cap   Time-series    Interactive UI
Mock UTXOs       Hourly Updates        Indexing       Real-time Charts
```

## 📁 File Structure

```
BlockchainApp/
├── main.py              # Application entry point
├── dashboard.py         # Streamlit dashboard
├── database.py          # SQLite database layer
├── data_collector.py    # API data collection
├── mvrv_calculator.py   # MVRV computation
├── scheduler.py         # Automated scheduling
├── requirements.txt     # Dependencies
└── PROJECT_README.md    # This file
```

## 🔧 Run Modes

```bash
# Full system (dashboard + background scheduler)
python main.py

# Dashboard only
python main.py dashboard

# Background scheduler only
python main.py scheduler

# Initial setup (create database, collect data)
python main.py setup
```

## 📊 MVRV Interpretation

| MVRV Range | Signal | Color | Meaning |
|------------|--------|-------|---------|
| < 1.0 | 🔵 BUY | Blue | Undervalued, accumulation zone |
| 1.0-2.4 | 🟢 HOLD | Green | Normal market conditions |
| 2.4-3.7 | 🟡 CAUTION | Yellow | Elevated levels, monitor |
| > 3.7 | 🔴 SELL | Red | Overvalued, historical tops |

## 🛠️ Troubleshooting

### Common Issues

**1. Module Not Found Error**
```bash
pip install -r requirements.txt
```

**2. Database Error**
```bash
python main.py setup
```

**3. API Rate Limit**
- System handles rate limits automatically
- Uses free tier limits (50 calls/minute)

**4. Dashboard Not Loading**
- Check if port 8501 is available
- Try: `streamlit run dashboard.py --server.port 8502`

## 🎨 Dashboard Components

### Main Metrics
- **MVRV Ratio**: Current value with 7-day comparison
- **Market Cap**: Bitcoin's total market value
- **Realized Cap**: On-chain value at last transaction
- **Market Signal**: Color-coded buy/sell indicator

### Charts
- **MVRV Trend**: Historical ratio with colored zones
- **Market vs Realized Cap**: Dual-line comparison
- **Distribution**: MVRV frequency histogram

### Controls
- **Auto-refresh**: 30-second updates
- **Manual Update**: Force data refresh
- **Time Range**: 1-30 days selection
- **Timeframe**: Hourly or daily view

## 🔄 Data Pipeline

### Hourly Process
1. Fetch Bitcoin price from CoinGecko
2. Get circulating supply data
3. Calculate market capitalization
4. Estimate realized cap from UTXO data
5. Compute MVRV ratio
6. Store in SQLite database

### Daily Process
1. Aggregate hourly MVRV data
2. Calculate daily averages
3. Store summary statistics
4. Update trend indicators

## 🚀 Performance

- **Database**: SQLite with optimized indexes
- **API Calls**: Rate-limited with retry logic
- **Memory**: ~50MB typical usage
- **Response Time**: <2 seconds for dashboard updates

## 📈 Technical Details

### Database Schema
```sql
price_data(timestamp, price_usd, supply)
utxo_data(txid, value_btc, moved_timestamp, value_usd)
mvrv_ratios(timestamp, market_cap, realized_cap, ratio, timeframe)
```

### API Integration
- **CoinGecko**: Free tier, 50 calls/minute
- **Timeout**: 30 seconds per request
- **Retry Logic**: 3 attempts with backoff

### Calculations
```
Market Cap = Current Price × Circulating Supply
Realized Cap = Σ(UTXO_value × Price_when_last_moved)
MVRV Ratio = Market Cap / Realized Cap
```

## 🎯 Use Cases

- **Investment Analysis**: Market timing decisions
- **Risk Assessment**: Portfolio allocation
- **Research**: On-chain analysis studies
- **Education**: Understanding Bitcoin fundamentals

## 🔮 Future Enhancements

- Multi-cryptocurrency support
- Email/SMS alerts
- REST API endpoints
- Machine learning predictions
- Mobile app integration

---

**🚀 Ready to analyze Bitcoin's MVRV ratio in real-time!**

*Built with Python, Streamlit, and SQLite*