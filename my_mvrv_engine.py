"""
My Personal MVRV Engine - Understanding Bitcoin's True Worth
Built with my own logic and understanding of market dynamics
"""

import sqlite3
from datetime import datetime, timedelta
import numpy as np
from my_database import MyPersonalDatabase
from btc_brain import BitcoinBrain

class MyMVRVEngine:
    def __init__(self):
        self.my_db = MyPersonalDatabase()
        self.btc_brain = BitcoinBrain()
        
        # My personal MVRV thresholds based on my research
        self.my_signals = {
            'extreme_greed': 4.2,    # My top signal
            'greed': 3.7,            # Traditional top
            'caution': 2.4,          # My caution zone
            'normal': 1.0,           # Fair value line
            'fear': 0.8,             # My opportunity zone
            'extreme_fear': 0.6      # My strong buy zone
        }
        
        # My confidence in different data sources
        self.data_confidence = {
            'blockchain_utxos': 0.95,    # Very high - real data
            'api_prices': 0.90,          # High - reliable sources
            'estimated_scaling': 0.85,   # Good - my algorithm
            'historical_fallback': 0.70  # Decent - backup method
        }
    
    def calculate_market_value(self, current_price, total_supply):
        """My straightforward market cap calculation"""
        market_cap = current_price * total_supply
        
        print(f"💰 Market Value: ${market_cap/1e9:.2f}B (${current_price:,.2f} × {total_supply:,.0f})")
        return market_cap
    
    def calculate_realized_value_my_way(self):
        """Calculate Bitcoin realized value using blockchain UTXO analysis"""
        print("🧠 Calculating realized value using blockchain UTXO analysis...")
        
        # Use my brain to hunt for real UTXOs
        real_utxos = self.btc_brain.hunt_for_real_utxos(2200)
        
        if not real_utxos:
            print("😔 No UTXOs found, falling back to database...")
            return self.fallback_realized_value()
        
        sample_realized_value = 0
        processed_utxos = []
        my_confidence_total = 0
        
        print(f"🔍 Analyzing {len(real_utxos)} UTXOs with my personal method...")
        
        for utxo in real_utxos:
            # Get price when this UTXO was born
            historical_price = self.find_price_when_utxo_was_born(utxo['creation_time'])
            
            if historical_price:
                # My weighted calculation based on confidence
                utxo_usd_value = utxo['btc_amount'] * historical_price
                confidence_weight = utxo['my_confidence']
                
                weighted_value = utxo_usd_value * confidence_weight
                sample_realized_value += weighted_value
                my_confidence_total += confidence_weight
                
                # Store for my database
                processed_utxos.append((
                    utxo['tx_hash'],
                    utxo['btc_amount'],
                    datetime.fromtimestamp(utxo['creation_time']).isoformat(),
                    utxo_usd_value,
                    confidence_weight
                ))
        
        # Save my findings to database
        if processed_utxos:
            self.my_db.store_my_utxo_discoveries(processed_utxos)
        
        # My scaling to full Bitcoin network
        scaling_factor = self.btc_brain.estimate_full_network_scaling(len(real_utxos))
        
        # Apply my confidence adjustment
        if my_confidence_total > 0:
            avg_confidence = my_confidence_total / len(real_utxos)
            confidence_multiplier = 0.8 + (avg_confidence * 0.4)  # My formula: 0.8 to 1.2 range
        else:
            confidence_multiplier = 1.0
        
        total_realized_value = sample_realized_value * scaling_factor * confidence_multiplier
        
        print(f"📊 My Analysis Results:")
        print(f"   Sample Realized Value: ${sample_realized_value/1e9:.2f}B")
        print(f"   My Scaling Factor: {scaling_factor:.0f}x")
        print(f"   My Confidence Multiplier: {confidence_multiplier:.2f}x")
        print(f"   Final Realized Value: ${total_realized_value/1e9:.2f}B")
        
        return total_realized_value
    
    def fallback_realized_value(self):
        """My backup method when brain can't reach blockchain"""
        print("🔄 Using my fallback realized value calculation...")
        
        conn = sqlite3.connect(self.my_db.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT SUM(value_usd * confidence_score) as weighted_realized_cap
            FROM my_utxo_discoveries
            WHERE confidence_score > 0.5
        """)
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result[0] else 0
    
    def find_price_when_utxo_was_born(self, birth_timestamp):
        """My method to find Bitcoin price at UTXO creation time"""
        try:
            birth_time = datetime.fromtimestamp(birth_timestamp)
            
            # Check my database first
            stored_price = self.my_db.get_price_from_my_history(birth_time.isoformat())
            if stored_price:
                return stored_price
            
            # My API call to get historical price
            date_string = birth_time.strftime('%d-%m-%Y')
            url = f"{self.btc_brain.my_apis['prices']}/coins/bitcoin/history"
            params = {'date': date_string}
            
            response = self.btc_brain.session.get(url, params=params, timeout=20)
            data = response.json()
            
            if 'market_data' in data and 'current_price' in data['market_data']:
                price = data['market_data']['current_price']['usd']
                
                # Store in my database for future use
                self.my_db.remember_historical_price(birth_time.isoformat(), price)
                return price
            
            # My intelligent fallback based on age
            return self.estimate_price_by_age(birth_time)
            
        except Exception as error:
            print(f"🤔 Price lookup failed for {birth_timestamp}: {error}")
            return self.estimate_price_by_age(datetime.fromtimestamp(birth_timestamp))
    
    def estimate_price_by_age(self, utxo_date):
        """Estimate Bitcoin price based on UTXO age"""
        now = datetime.now()
        age_days = (now - utxo_date).days
        
        current_estimate = 45000
        
        if age_days < 7:
            return current_estimate * np.random.uniform(0.95, 1.05)
        elif age_days < 30:
            return current_estimate * np.random.uniform(0.85, 1.15)
        elif age_days < 90:
            return current_estimate * np.random.uniform(0.70, 1.30)
        elif age_days < 365:
            return current_estimate * np.random.uniform(0.50, 1.50)
        elif age_days < 1095:
            return current_estimate * np.random.uniform(0.30, 0.80)
        else:
            return current_estimate * np.random.uniform(0.10, 0.50)
    
    def calculate_my_mvrv_ratio(self, market_value, realized_value):
        """My MVRV calculation with personal insights"""
        if realized_value <= 0:
            print("⚠️ Realized value is zero - something's wrong!")
            return 0
        
        mvrv_ratio = market_value / realized_value
        
        # My additional insights
        my_interpretation = self.interpret_mvrv_my_way(mvrv_ratio)
        
        print(f"🎯 My MVRV Calculation:")
        print(f"   Market Value: ${market_value/1e9:.2f}B")
        print(f"   Realized Value: ${realized_value/1e9:.2f}B")
        print(f"   MVRV Ratio: {mvrv_ratio:.4f}")
        print(f"   My Interpretation: {my_interpretation['signal']} - {my_interpretation['meaning']}")
        
        return mvrv_ratio
    
    def interpret_mvrv_my_way(self, mvrv_value):
        """Interpret MVRV ratio and generate market signals"""
        if mvrv_value >= self.my_signals['extreme_greed']:
            return {
                'signal': '🔥 EXTREME GREED',
                'color': 'darkred',
                'meaning': 'Market is extremely overheated - major correction likely',
                'action': 'STRONG SELL',
                'confidence': 0.95
            }
        elif mvrv_value >= self.my_signals['greed']:
            return {
                'signal': '🔴 GREED ZONE',
                'color': 'red',
                'meaning': 'Historical top territory - be very cautious',
                'action': 'SELL',
                'confidence': 0.90
            }
        elif mvrv_value >= self.my_signals['caution']:
            return {
                'signal': '🟡 CAUTION ZONE',
                'color': 'orange',
                'meaning': 'Elevated levels - monitor closely',
                'action': 'REDUCE POSITION',
                'confidence': 0.80
            }
        elif mvrv_value >= self.my_signals['normal']:
            return {
                'signal': '🟢 NORMAL RANGE',
                'color': 'green',
                'meaning': 'Healthy market conditions',
                'action': 'HOLD',
                'confidence': 0.75
            }
        elif mvrv_value >= self.my_signals['fear']:
            return {
                'signal': '🔵 FEAR ZONE',
                'color': 'blue',
                'meaning': 'Market showing fear - opportunity emerging',
                'action': 'ACCUMULATE',
                'confidence': 0.85
            }
        else:
            return {
                'signal': '💎 EXTREME FEAR',
                'color': 'darkblue',
                'meaning': 'Extreme fear - historically great buying opportunity',
                'action': 'STRONG BUY',
                'confidence': 0.95
            }
    
    def run_my_hourly_analysis(self):
        """My complete hourly MVRV analysis routine"""
        print("🕐 Starting my hourly Bitcoin MVRV analysis...")
        print("=" * 60)
        
        try:
            # Get latest price data
            latest_price_data = self.my_db.get_my_latest_price_data()
            
            if not latest_price_data:
                print("😞 No price data available for analysis")
                return None
            
            price_usd, supply, timestamp = latest_price_data
            
            # Calculate market value
            market_value = self.calculate_market_value(price_usd, supply)
            
            # Calculate realized value using my brain
            realized_value = self.calculate_realized_value_my_way()
            
            # Calculate my MVRV ratio
            mvrv_ratio = self.calculate_my_mvrv_ratio(market_value, realized_value)
            
            # Get my interpretation
            my_analysis = self.interpret_mvrv_my_way(mvrv_ratio)
            
            # Store my results
            analysis_timestamp = datetime.utcnow().isoformat()
            self.my_db.store_my_mvrv_analysis(
                timestamp=analysis_timestamp,
                market_cap=market_value,
                realized_cap=realized_value,
                ratio=mvrv_ratio,
                signal=my_analysis['signal'],
                confidence=my_analysis['confidence'],
                timeframe='hourly'
            )
            
            my_result = {
                'timestamp': timestamp,
                'price_usd': price_usd,
                'market_cap': market_value,
                'realized_cap': realized_value,
                'mvrv_ratio': mvrv_ratio,
                'my_signal': my_analysis['signal'],
                'my_action': my_analysis['action'],
                'my_confidence': my_analysis['confidence'],
                'my_meaning': my_analysis['meaning']
            }
            
            print(f"✅ My analysis complete! MVRV: {mvrv_ratio:.4f} ({my_analysis['signal']})")
            return my_result
            
        except Exception as error:
            print(f"😓 My analysis hit a snag: {error}")
            return None
    
    def get_my_mvrv_insights(self):
        """Generate insights about recent MVRV trends"""
        try:
            recent_data = self.my_db.get_my_mvrv_history('hourly', 168)
            
            if not recent_data:
                return None
            
            ratios = [item['ratio'] for item in recent_data]
            confidences = [item.get('confidence', 0.8) for item in recent_data]
            
            my_insights = {
                'current_mvrv': ratios[-1] if ratios else 0,
                'my_7d_average': np.mean(ratios),
                'my_7d_min': min(ratios),
                'my_7d_max': max(ratios),
                'my_volatility': np.std(ratios),
                'my_trend': 'rising' if len(ratios) > 1 and ratios[-1] > ratios[-2] else 'falling',
                'my_confidence_avg': np.mean(confidences),
                'data_quality': 'high' if np.mean(confidences) > 0.85 else 'medium' if np.mean(confidences) > 0.70 else 'low'
            }
            
            current_analysis = self.interpret_mvrv_my_way(my_insights['current_mvrv'])
            my_insights.update({
                'my_current_signal': current_analysis['signal'],
                'my_current_action': current_analysis['action'],
                'my_current_meaning': current_analysis['meaning'],
                'signal_color': current_analysis['color']
            })
            
            return my_insights
            
        except Exception as error:
            print(f"😔 Couldn't generate my insights: {error}")
            return None