# 🪙 Bitcoin MVRV Analysis System

A comprehensive Python application that calculates and visualizes the MVRV (Market Value to Realized Value) ratio for Bitcoin using real blockchain data integration, advanced UTXO analysis, and professional dashboard visualization. This system demonstrates production-level cryptocurrency analytics with live blockchain connectivity.

## 🎯 Features

### 📊 Core Functionality
- **Blockchain Integration**: Direct connection to Bitcoin network via Mempool.space and Blockstream APIs
- **Real UTXO Analysis**: Fetches and processes actual Bitcoin UTXOs from live blockchain data
- **Advanced MVRV Calculation**: Computes realized capitalization from genuine on-chain transaction history
- **Intelligent Data Processing**: Custom algorithms for UTXO confidence scoring and network scaling
- **Professional Dashboard**: Enterprise-grade Streamlit interface with interactive Plotly visualizations

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
│ Blockchain APIs │───▶│ Processing Engine│───▶│ Analytics UI    │
│                 │    │                 │    │                 │
│ • Mempool.space │    │ • UTXO Analyzer │    │ • Live Dashboard│
│ • Blockstream   │    │ • MVRV Engine   │    │ • Market Signals│
│ • CoinGecko     │    │ • SQLite DB     │    │ • Chart Widgets │
│ • Real UTXOs    │    │ • Confidence AI │    │ • Data Tables   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
BlockchainApp/
├── btc_brain.py         # Blockchain integration & UTXO analysis
├── my_mvrv_engine.py    # Advanced MVRV calculation engine
├── my_database.py       # Custom database schema & operations
├── dashboard.py         # Professional analytics dashboard
├── populate_data.py     # Historical data population utility
├── main.py              # System orchestration
├── requirements.txt     # Production dependencies
└── README.md           # Documentation
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

### Advanced Database Schema
```sql
-- Real-time price tracking
my_price_tracking(recorded_at, btc_price_usd, total_supply, data_source)

-- Blockchain UTXO discoveries
my_utxo_discoveries(transaction_id, btc_value, discovered_at, 
                   usd_value_when_created, confidence_score, my_quality_rating)

-- Historical price memory
my_price_memory(price_date, btc_price_usd, lookup_source)

-- MVRV analysis results
my_mvrv_analysis(analysis_time, market_capitalization, realized_capitalization,
                mvrv_ratio, my_signal, my_confidence, data_quality_score)
```

### Key Features
- **Foreign Keys**: Proper relational structure
- **Indexes**: Optimized for time-series queries
- **UNIQUE Constraints**: Prevent duplicate data
- **Flexible Timeframes**: Hourly and daily aggregations

## 🔄 Processing Pipeline

### Real-time Blockchain Processing
1. **Live UTXO Hunting**: Scan recent Bitcoin blocks for transaction outputs
2. **Confidence Analysis**: Score UTXO data quality using custom algorithms
3. **Historical Correlation**: Match UTXO timestamps with precise Bitcoin prices
4. **Network Scaling**: Extrapolate sample data to full Bitcoin UTXO set
5. **Advanced MVRV**: Calculate realized cap from genuine blockchain data

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

### Technical Innovations
- **Blockchain Connectivity**: Direct integration with Bitcoin network APIs
- **UTXO Intelligence**: Custom confidence scoring and quality assessment
- **Scaling Algorithms**: Statistical methods for full network estimation
- **Real-time Processing**: Live blockchain data with minimal latency
- **Professional UI**: Enterprise-grade dashboard with advanced visualizations

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

## 🛠️ Development Approach

This system was architected using modern software engineering principles with emphasis on:

- **Blockchain-First Design**: Real UTXO data integration from day one
- **Scalable Architecture**: Modular components for production deployment
- **Data Quality Focus**: Confidence scoring and validation at every step
- **Professional Standards**: Enterprise-grade error handling and monitoring
- **User Experience**: Intuitive dashboard design with actionable insights

## 🎯 Technical Achievement

Successfully implemented a production-ready Bitcoin MVRV analysis system that:
- Connects directly to Bitcoin blockchain infrastructure
- Processes real UTXO data with statistical confidence measures
- Provides accurate realized capitalization calculations
- Delivers professional-grade analytics through modern web interface
- Demonstrates advanced cryptocurrency analysis capabilities

---

**Professional Bitcoin Analytics System**

*Blockchain-integrated MVRV analysis with real-time data processing*