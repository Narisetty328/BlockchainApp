import requests
import time
from datetime import datetime, timedelta
import json
from database import MVRVDatabase

class DataCollector:
    def __init__(self):
        self.db = MVRVDatabase()
        self.coingecko_base = "https://api.coingecko.com/api/v3"
        self.blockchair_base = "https://api.blockchair.com/bitcoin"
        
    def fetch_current_price_data(self):
        """Fetch current Bitcoin price and supply from CoinGecko"""
        try:
            url = f"{self.coingecko_base}/coins/bitcoin"
            response = requests.get(url, timeout=30)
            data = response.json()
            
            price_usd = data['market_data']['current_price']['usd']
            supply = data['market_data']['circulating_supply']
            timestamp = datetime.utcnow().isoformat()
            
            self.db.insert_price_data(timestamp, price_usd, supply)
            
            return {
                'timestamp': timestamp,
                'price_usd': price_usd,
                'supply': supply
            }
            
        except Exception as e:
            print(f"Error fetching price data: {e}")
            return None
    
    def fetch_utxo_sample_data(self, limit=1000):
        """Fetch sample UTXO data from Blockchair API"""
        try:
            # Get recent transactions for UTXO analysis
            url = f"{self.blockchair_base}/transactions?limit={limit}"
            response = requests.get(url, timeout=30)
            data = response.json()
            
            utxo_list = []
            
            for tx in data.get('data', []):
                # Simulate UTXO data structure
                utxo_list.append((
                    tx.get('hash', ''),
                    tx.get('output_total', 0) / 100000000,  # Convert satoshi to BTC
                    tx.get('time', datetime.utcnow().isoformat()),
                    0  # Will be calculated with historical price
                ))
            
            # Get historical prices for UTXO timestamps and calculate USD values
            processed_utxos = []
            for txid, value_btc, moved_timestamp, _ in utxo_list:
                historical_price = self.get_historical_price(moved_timestamp)
                if historical_price:
                    value_usd = value_btc * historical_price
                    processed_utxos.append((txid, value_btc, moved_timestamp, value_usd))
            
            if processed_utxos:
                self.db.insert_utxo_data(processed_utxos)
            
            return len(processed_utxos)
            
        except Exception as e:
            print(f"Error fetching UTXO data: {e}")
            return 0
    
    def get_historical_price(self, timestamp_str):
        """Get historical Bitcoin price for given timestamp"""
        try:
            # First check if we have it in database
            price = self.db.get_price_at_timestamp(timestamp_str)
            if price:
                return price
            
            # Convert timestamp to date for API call
            dt = datetime.fromisoformat(timestamp_str.replace('Z', ''))
            date_str = dt.strftime('%d-%m-%Y')
            
            url = f"{self.coingecko_base}/coins/bitcoin/history"
            params = {'date': date_str}
            
            response = requests.get(url, params=params, timeout=30)
            data = response.json()
            
            if 'market_data' in data:
                price = data['market_data']['current_price']['usd']
                self.db.insert_historical_price(timestamp_str, price)
                return price
            
            return None
            
        except Exception as e:
            print(f"Error fetching historical price: {e}")
            return None
    
    def fetch_historical_price_range(self, days=30):
        """Fetch historical prices for the last N days"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Convert to timestamps
            start_ts = int(start_date.timestamp())
            end_ts = int(end_date.timestamp())
            
            url = f"{self.coingecko_base}/coins/bitcoin/market_chart/range"
            params = {
                'vs_currency': 'usd',
                'from': start_ts,
                'to': end_ts
            }
            
            response = requests.get(url, params=params, timeout=30)
            data = response.json()
            
            prices_inserted = 0
            for price_point in data.get('prices', []):
                timestamp = datetime.fromtimestamp(price_point[0] / 1000).isoformat()
                price = price_point[1]
                
                self.db.insert_historical_price(timestamp, price)
                prices_inserted += 1
            
            return prices_inserted
            
        except Exception as e:
            print(f"Error fetching historical price range: {e}")
            return 0
    
    def generate_mock_utxo_data(self, count=10000):
        """Generate mock UTXO data for demonstration"""
        import random
        
        utxo_list = []
        base_time = datetime.now() - timedelta(days=365)  # 1 year ago
        
        for i in range(count):
            # Generate random UTXO
            txid = f"mock_tx_{i:06d}"
            value_btc = random.uniform(0.001, 10.0)  # Random BTC amount
            
            # Random timestamp in the past year
            days_ago = random.randint(1, 365)
            moved_timestamp = (base_time + timedelta(days=days_ago)).isoformat()
            
            # Get historical price (or use mock price)
            historical_price = random.uniform(20000, 70000)  # Mock price range
            value_usd = value_btc * historical_price
            
            utxo_list.append((txid, value_btc, moved_timestamp, value_usd))
        
        self.db.insert_utxo_data(utxo_list)
        return count
    
    def collect_all_data(self):
        """Collect all required data for MVRV calculation"""
        print("🔄 Starting data collection...")
        
        # 1. Fetch current price data
        price_data = self.fetch_current_price_data()
        if price_data:
            print(f"✅ Current price: ${price_data['price_usd']:,.2f}")
        
        # 2. Fetch historical prices
        historical_count = self.fetch_historical_price_range(30)
        print(f"✅ Historical prices: {historical_count} records")
        
        # 3. Generate mock UTXO data (since real UTXO data requires full node)
        utxo_count = self.generate_mock_utxo_data(5000)
        print(f"✅ UTXO data: {utxo_count} records")
        
        return price_data is not None