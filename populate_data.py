#!/usr/bin/env python3
"""
Data Population Script
Quickly populate database with historical MVRV data for chart visualization
"""

import requests
import numpy as np
from datetime import datetime, timedelta
from my_database import MyPersonalDatabase
from my_mvrv_engine import MyMVRVEngine

def populate_historical_data():
    """Populate database with realistic historical MVRV data"""
    print("🚀 Populating database with historical MVRV data...")
    
    db = MyPersonalDatabase()
    engine = MyMVRVEngine()
    
    # Get current Bitcoin price
    try:
        print("📡 Fetching current Bitcoin price...")
        url = "https://api.coingecko.com/api/v3/coins/bitcoin"
        response = requests.get(url, timeout=30)
        data = response.json()
        
        current_price = data["market_data"]["current_price"]["usd"]
        supply = data["market_data"]["circulating_supply"]
        
        print(f"✅ Current BTC: ${current_price:,.2f}")
        print(f"✅ Supply: {supply:,.0f} BTC")
        
    except Exception as e:
        print(f"⚠️ Using fallback price data: {e}")
        current_price = 45000
        supply = 19_500_000
    
    # Generate 30 days of hourly data
    print("📊 Generating 30 days of hourly MVRV data...")
    
    base_date = datetime.now() - timedelta(days=30)
    data_points = []
    
    for hour in range(30 * 24):  # 30 days * 24 hours
        timestamp = base_date + timedelta(hours=hour)
        
        # Generate realistic price variation
        days_ago = (datetime.now() - timestamp).days
        price_factor = 1.0 + (np.random.normal(0, 0.02) * (1 + days_ago * 0.01))
        price = current_price * price_factor
        
        # Generate realistic MVRV (typically 0.8 to 3.5)
        base_mvrv = 1.4 + 0.6 * np.sin(hour * 0.01) + 0.3 * np.sin(hour * 0.05)
        noise = np.random.normal(0, 0.1)
        mvrv_ratio = max(0.6, min(4.0, base_mvrv + noise))
        
        # Calculate market and realized caps
        market_cap = price * supply
        realized_cap = market_cap / mvrv_ratio
        
        data_points.append({
            'timestamp': timestamp.isoformat(),
            'price': price,
            'supply': supply,
            'market_cap': market_cap,
            'realized_cap': realized_cap,
            'mvrv_ratio': mvrv_ratio
        })
    
    print(f"💾 Storing {len(data_points)} data points...")
    
    # Store price data
    for point in data_points[::6]:  # Every 6 hours for price data
        db.store_my_price_discovery(
            point['timestamp'], 
            point['price'], 
            point['supply']
        )
    
    # Store MVRV analysis results
    for point in data_points:
        db.store_my_mvrv_analysis(
            timestamp=point['timestamp'],
            market_cap=point['market_cap'],
            realized_cap=point['realized_cap'],
            ratio=point['mvrv_ratio'],
            signal=get_signal_for_mvrv(point['mvrv_ratio']),
            confidence=0.85,
            timeframe='hourly'
        )
    
    # Generate some historical prices
    print("📈 Adding historical price data...")
    for i in range(0, len(data_points), 24):  # Daily prices
        point = data_points[i]
        db.remember_historical_price(point['timestamp'], point['price'])
    
    # Generate some UTXO data
    print("🔗 Adding sample UTXO data...")
    utxo_batch = []
    for i in range(100):  # 100 sample UTXOs
        point = data_points[i * 7]  # Every week
        utxo_batch.append((
            f"sample_tx_{i:04d}",
            np.random.uniform(0.01, 5.0),  # BTC amount
            point['timestamp'],
            np.random.uniform(500, 50000),  # USD value
            0.8  # Confidence
        ))
    
    db.store_my_utxo_discoveries(utxo_batch)
    
    print("✅ Database populated successfully!")
    
    # Show statistics
    stats = db.get_my_database_stats()
    print("\n📊 Database Statistics:")
    print(f"   Price Records: {stats.get('my_price_tracking', 0)}")
    print(f"   UTXO Records: {stats.get('my_utxo_discoveries', 0)}")
    print(f"   MVRV Records: {stats.get('my_mvrv_analysis', 0)}")
    print(f"   Historical Prices: {stats.get('my_price_memory', 0)}")
    
    return True

def get_signal_for_mvrv(mvrv_ratio):
    """Get market signal for MVRV ratio"""
    if mvrv_ratio > 3.7:
        return "🔴 SELL ZONE"
    elif mvrv_ratio > 2.4:
        return "🟡 CAUTION ZONE"
    elif mvrv_ratio > 1.0:
        return "🟢 NORMAL RANGE"
    else:
        return "🔵 BUY ZONE"

if __name__ == "__main__":
    try:
        success = populate_historical_data()
        if success:
            print("\n🎉 Data population complete!")
            print("🚀 You can now run the dashboard:")
            print("   streamlit run dashboard.py")
        else:
            print("\n❌ Data population failed")
    except Exception as e:
        print(f"\n💥 Error: {e}")
        print("Make sure all dependencies are installed and APIs are accessible")