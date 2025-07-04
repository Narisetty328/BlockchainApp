# 🪙 Bitcoin MVRV Analysis System

A complete Python application that calculates and visualizes the MVRV (Market Value to Realized Value) ratio for Bitcoin with real-time data collection, SQLite storage, and an interactive Streamlit dashboard.

## 🎯 Features

### 📊 Core Functionality
- **Real-time Data Collection**: Live Bitcoin price and market data from CoinGecko API
- **MVRV Calculation**: Accurate Market Cap / Realized Cap ratio computation
- **Automated Scheduling**: Hourly data updates and daily aggregations
- **SQLite Database**: Structured storage with optimized queries
- **Interactive Dashboard**: Colorful Streamlit interface with real-time charts

### 🎨 Dashboard Features
- **Live Metrics**: Current MVRV ratio, market cap, realized cap
- **Market Signals**: Color-coded buy/sell/hold/caution indicators
- **Historical Charts**: Interactive Plotly visualizations with reference zones
- **Time Range Selection**: Hourly or daily data views
- **Auto-refresh**: Real-time dashboard updates
- **Distribution Analysis**: MVRV ratio frequency charts

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Data Sources   │───▶│   Processing    │───▶│  Presentation   │
│                 │    │                 │    │                 │
│ • CoinGecko API │    │ • MVRV Engine   │    │ • Streamlit UI  │
│ • Blockchair    │    │ • SQLite DB     │    │ • Plotly Charts │
│ • Mock UTXOs    │    │ • Scheduler     │    │ • Market Signals│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
BlockchainApp/
├── main.py              # Application entry point
├── dashboard.py         # Streamlit dashboard
├── database.py          # SQLite database layer
├── data_collector.py    # API data collection
├── mvrv_calculator.py   # MVRV computation engine
├── scheduler.py         # Automated job scheduling
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.8+
pip (Python package manager)
```

### Installation
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run initial setup (creates database and collects initial data)
python main.py setup

# 3. Start the complete system
python main.py
```

### Alternative Run Modes
```bash
# Dashboard only
python main.py dashboard

# Scheduler only (background data collection)
python main.py scheduler

# Full system (recommended)
python main.py
```

## 📊 Database Schema

### Tables Structure
```sql
-- Current price and supply data
price_data(timestamp, price_usd, supply)

-- UTXO transaction data
utxo_data(txid, value_btc, moved_timestamp, value_usd)

-- Historical price lookups
historical_prices(timestamp, price_usd)

-- MVRV calculation results
mvrv_ratios(timestamp, market_cap, realized_cap, ratio, timeframe)
```

### Key Features
- **Foreign Keys**: Proper relational structure
- **Indexes**: Optimized for time-series queries
- **UNIQUE Constraints**: Prevent duplicate data
- **Flexible Timeframes**: Hourly and daily aggregations

## 🔄 Processing Pipeline

### Hourly Jobs
1. **Data Collection**: Fetch current Bitcoin price and supply
2. **Historical Prices**: Get price data for UTXO timestamps
3. **UTXO Processing**: Calculate USD values at movement time
4. **MVRV Calculation**: Compute Market Cap / Realized Cap
5. **Storage**: Save results to SQLite database

### Daily Jobs
1. **Aggregation**: Summarize hourly data into daily averages
2. **Statistics**: Calculate min, max, standard deviation
3. **Trend Analysis**: Identify market direction changes

## 🎨 Dashboard Components

### 📈 Real-time Metrics
- Current MVRV ratio with 7-day comparison
- Market cap and realized cap in billions
- 7-day average with min/max range

### 🚦 Market Signals
- **🔵 BUY**: MVRV < 1.0 (Undervalued)
- **🟢 HOLD**: MVRV 1.0-2.4 (Normal)
- **🟡 CAUTION**: MVRV 2.4-3.7 (Elevated)
- **🔴 SELL**: MVRV > 3.7 (Overvalued)

### 📊 Interactive Charts
- **MVRV Trend**: Historical ratio with colored zones
- **Market vs Realized Cap**: Dual-line comparison
- **Distribution**: MVRV frequency histogram
- **Reference Lines**: Key threshold indicators

## 🔧 Configuration

### API Settings
- **CoinGecko**: Free tier (50 calls/minute)
- **Blockchair**: Free tier (10 calls/minute)
- **Timeout**: 30 seconds per request
- **Retry Logic**: 3 attempts with exponential backoff

### Scheduling
- **Hourly Updates**: Every hour on the hour
- **Daily Aggregation**: 12:30 AM daily
- **Manual Triggers**: Available via dashboard
- **Background Processing**: Non-blocking execution

## 📚 MVRV Understanding

### What is MVRV?
**Market Value to Realized Value** compares Bitcoin's current market cap to its "realized" cap based on when coins last moved.

### Calculation
```
Market Cap = Current Price × Circulating Supply
Realized Cap = Σ(UTXO_value × Price_when_last_moved)
MVRV Ratio = Market Cap / Realized Cap
```

### Historical Significance
- **MVRV > 3.7**: Historical market tops (2017, 2021 peaks)
- **MVRV < 1.0**: Market bottoms (2018, 2020 crashes)
- **MVRV ~2.4**: Average cycle peaks
- **MVRV ~1.0**: Break-even point for holders

## 🛠️ Technical Details

### Performance Optimizations
- **Database Indexing**: Fast time-series queries
- **Batch Processing**: Efficient UTXO data handling
- **Caching**: Reduced API calls for historical prices
- **Async Operations**: Non-blocking data collection

### Error Handling
- **API Timeouts**: Graceful fallback mechanisms
- **Data Validation**: Input sanitization and bounds checking
- **Database Errors**: Transaction rollback and retry logic
- **Network Issues**: Exponential backoff retry strategy

### Monitoring
- **Health Checks**: System status indicators
- **Job Scheduling**: Next run time display
- **Data Freshness**: Last update timestamps
- **Error Logging**: Comprehensive error tracking

## 🎯 Use Cases

### Investment Analysis
- **Market Timing**: Identify potential tops and bottoms
- **Risk Assessment**: Gauge overall market sentiment
- **Portfolio Management**: Long-term allocation decisions

### Research & Education
- **On-chain Analysis**: Understanding Bitcoin fundamentals
- **Market Cycles**: Historical pattern recognition
- **Academic Study**: Cryptocurrency valuation models

### Trading Support
- **Signal Generation**: Automated buy/sell indicators
- **Risk Management**: Position sizing based on MVRV levels
- **Backtesting**: Historical strategy validation

## 🔮 Future Enhancements

### Planned Features
- **Multi-timeframe Analysis**: Weekly, monthly aggregations
- **Alert System**: Email/SMS notifications for threshold breaches
- **API Endpoints**: REST API for external integrations
- **Export Functions**: CSV/JSON data export capabilities

### Advanced Analytics
- **MVRV Z-Score**: Normalized MVRV for better comparison
- **Cohort Analysis**: UTXO age-based segmentation
- **Correlation Studies**: Price vs MVRV relationship analysis
- **Machine Learning**: Predictive MVRV modeling

## 🤝 Contributing

### Development Setup
```bash
# Clone and setup
git clone <repository>
cd BlockchainApp
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Start development server
python main.py dashboard
```

### Code Style
- **PEP 8**: Python style guidelines
- **Type Hints**: Function parameter and return types
- **Docstrings**: Comprehensive function documentation
- **Error Handling**: Explicit exception management

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **CoinGecko**: Free cryptocurrency API
- **Blockchair**: Blockchain explorer API
- **Streamlit**: Interactive dashboard framework
- **Plotly**: Advanced charting library

---

**Built with ❤️ for the Bitcoin community**

*Real-time MVRV analysis for better investment decisions*