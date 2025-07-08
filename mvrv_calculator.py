import sqlite3
from datetime import datetime, timedelta
import numpy as np
from database import MVRVDatabase
from blockchain_integration import BlockchainIntegration

class MVRVCalculator:
    def __init__(self):
        self.db = MVRVDatabase()
        self.blockchain = BlockchainIntegration()
    
    def calculate_market_cap(self, price_usd, supply):
        """Calculate current market capitalization"""
        return price_usd * supply
    
    def calculate_realized_cap_from_blockchain(self):
        """Calculate realized cap using real blockchain UTXO data"""
        print("🔗 Calculating realized cap from real blockchain data...")
        
        # Fetch real UTXO sample from blockchain
        utxos = self.blockchain.fetch_real_utxo_sample(2000)
        
        if not utxos:
            print("❌ No UTXO data available, falling back to database")
            return self.calculate_realized_cap_from_db()
        
        realized_cap_sample = 0
        processed_utxos = []
        
        for utxo in utxos:
            # Get historical price when UTXO was created
            historical_price = self.get_historical_price_for_timestamp(utxo['timestamp'])
            
            if historical_price:
                utxo_value_usd = utxo['value_btc'] * historical_price
                realized_cap_sample += utxo_value_usd
                
                # Store processed UTXO for database
                processed_utxos.append((
                    utxo['txid'],
                    utxo['value_btc'],
                    datetime.fromtimestamp(utxo['timestamp']).isoformat(),
                    utxo_value_usd
                ))
        
        # Store real UTXO data in database
        if processed_utxos:
            self.db.insert_utxo_data(processed_utxos)
        
        # Scale sample to estimate full UTXO set
        scaling_factor = self.blockchain.calculate_scaling_factor(len(utxos))
        total_realized_cap = realized_cap_sample * scaling_factor
        
        print(f"📊 Sample: {len(utxos)} UTXOs = ${realized_cap_sample/1e9:.2f}B")
        print(f"📈 Scaled: ${total_realized_cap/1e9:.2f}B (factor: {scaling_factor:.0f})")
        
        return total_realized_cap
    
    def calculate_realized_cap_from_db(self):
        """Fallback: Calculate realized cap from database UTXO data"""
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT SUM(value_usd) as realized_cap
            FROM utxo_data
        """)
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result[0] else 0
    
    def calculate_realized_cap(self):
        """Calculate realized cap - try blockchain first, fallback to DB"""
        try:
            return self.calculate_realized_cap_from_blockchain()
        except Exception as e:
            print(f"Blockchain calculation failed: {e}")
            return self.calculate_realized_cap_from_db()
    
    def get_historical_price_for_timestamp(self, timestamp):
        """Get Bitcoin price for specific timestamp"""
        try:
            # Convert timestamp to datetime
            dt = datetime.fromtimestamp(timestamp)
            
            # Check database first
            price = self.db.get_price_at_timestamp(dt.isoformat())
            if price:
                return price
            
            # Use CoinGecko API for historical price
            import requests
            date_str = dt.strftime('%d-%m-%Y')
            url = "https://api.coingecko.com/api/v3/coins/bitcoin/history"
            params = {'date': date_str}
            
            response = requests.get(url, params=params, timeout=30)
            data = response.json()
            
            if 'market_data' in data:
                price = data['market_data']['current_price']['usd']
                self.db.insert_historical_price(dt.isoformat(), price)
                return price
            
            # Fallback to approximate price based on current price
            current_price = 45000  # Approximate current BTC price
            days_ago = (datetime.now() - dt).days
            
            # Simple price estimation (not accurate, but better than nothing)
            if days_ago < 30:
                return current_price * (0.95 + 0.1 * (30 - days_ago) / 30)
            else:
                return current_price * 0.8  # Rough historical average
                
        except Exception as e:
            print(f"Error getting historical price: {e}")
            return 45000  # Default fallback price
    
    def calculate_mvrv_ratio(self, market_cap, realized_cap):
        """Calculate MVRV ratio"""
        if realized_cap <= 0:
            return 0
        return market_cap / realized_cap
    
    def perform_hourly_calculation(self):
        """Perform hourly MVRV calculation"""
        try:
            # Get latest price data
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT price_usd, supply, timestamp
                FROM price_data
                ORDER BY timestamp DESC
                LIMIT 1
            """)
            
            price_result = cursor.fetchone()
            conn.close()
            
            if not price_result:
                print("❌ No price data available")
                return None
            
            price_usd, supply, timestamp = price_result
            
            # Calculate market cap
            market_cap = self.calculate_market_cap(price_usd, supply)
            
            # Calculate realized cap from real blockchain data
            realized_cap = self.calculate_realized_cap()
            
            # Calculate MVRV ratio
            mvrv_ratio = self.calculate_mvrv_ratio(market_cap, realized_cap)
            
            # Store result
            self.db.insert_mvrv_ratio(
                timestamp=datetime.utcnow().isoformat(),
                market_cap=market_cap,
                realized_cap=realized_cap,
                ratio=mvrv_ratio,
                timeframe='hourly'
            )
            
            result = {
                'timestamp': timestamp,
                'price_usd': price_usd,
                'market_cap': market_cap,
                'realized_cap': realized_cap,
                'mvrv_ratio': mvrv_ratio
            }
            
            print(f"✅ MVRV calculated: {mvrv_ratio:.4f}")
            return result
            
        except Exception as e:
            print(f"❌ Error calculating MVRV: {e}")
            return None
    
    def perform_daily_aggregation(self):
        """Aggregate hourly data into daily summaries"""
        try:
            # Get yesterday's date
            yesterday = (datetime.now() - timedelta(days=1)).date()
            start_time = f"{yesterday}T00:00:00"
            end_time = f"{yesterday}T23:59:59"
            
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            
            # Get all hourly data for yesterday
            cursor.execute("""
                SELECT market_cap, realized_cap, ratio
                FROM mvrv_ratios
                WHERE timeframe = 'hourly'
                AND timestamp BETWEEN ? AND ?
            """, (start_time, end_time))
            
            hourly_data = cursor.fetchall()
            conn.close()
            
            if not hourly_data:
                print(f"❌ No hourly data for {yesterday}")
                return None
            
            # Calculate daily aggregates
            market_caps = [row[0] for row in hourly_data]
            realized_caps = [row[1] for row in hourly_data]
            ratios = [row[2] for row in hourly_data]
            
            daily_market_cap = np.mean(market_caps)
            daily_realized_cap = np.mean(realized_caps)
            daily_ratio = np.mean(ratios)
            
            # Store daily aggregate
            daily_timestamp = f"{yesterday}T12:00:00"  # Noon as representative time
            
            self.db.insert_mvrv_ratio(
                timestamp=daily_timestamp,
                market_cap=daily_market_cap,
                realized_cap=daily_realized_cap,
                ratio=daily_ratio,
                timeframe='daily'
            )
            
            result = {
                'date': str(yesterday),
                'market_cap': daily_market_cap,
                'realized_cap': daily_realized_cap,
                'mvrv_ratio': daily_ratio,
                'data_points': len(hourly_data)
            }
            
            print(f"✅ Daily aggregate: {daily_ratio:.4f} ({len(hourly_data)} points)")
            return result
            
        except Exception as e:
            print(f"❌ Error in daily aggregation: {e}")
            return None
    
    def get_mvrv_statistics(self):
        """Get MVRV statistics and insights"""
        try:
            # Get recent MVRV data
            recent_data = self.db.get_mvrv_history('hourly', 168)  # Last 7 days
            
            if not recent_data:
                return None
            
            ratios = [item['ratio'] for item in recent_data]
            
            stats = {
                'current': ratios[-1] if ratios else 0,
                'avg_7d': np.mean(ratios),
                'min_7d': min(ratios),
                'max_7d': max(ratios),
                'std_7d': np.std(ratios),
                'trend': 'up' if len(ratios) > 1 and ratios[-1] > ratios[-2] else 'down'
            }
            
            # Market signal based on MVRV thresholds
            current_ratio = stats['current']
            if current_ratio > 3.7:
                stats['signal'] = 'SELL'
                stats['signal_color'] = 'red'
                stats['signal_desc'] = 'Historically overvalued'
            elif current_ratio > 2.4:
                stats['signal'] = 'CAUTION'
                stats['signal_color'] = 'orange'
                stats['signal_desc'] = 'Elevated levels'
            elif current_ratio > 1.0:
                stats['signal'] = 'HOLD'
                stats['signal_color'] = 'green'
                stats['signal_desc'] = 'Normal range'
            else:
                stats['signal'] = 'BUY'
                stats['signal_color'] = 'blue'
                stats['signal_desc'] = 'Potentially undervalued'
            
            return stats
            
        except Exception as e:
            print(f"❌ Error calculating statistics: {e}")
            return None