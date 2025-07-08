"""
My Personal Database - Where I Store My Bitcoin Discoveries
Custom schema designed by me for my MVRV analysis needs
"""

import sqlite3
from datetime import datetime
import json

class MyPersonalDatabase:
    def __init__(self, db_name="my_bitcoin_analysis.db"):
        self.db_path = db_name
        self.setup_my_database()
    
    def setup_my_database(self):
        """Setting up my personal database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # My price tracking table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS my_price_tracking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recorded_at TEXT NOT NULL,
                btc_price_usd REAL NOT NULL,
                total_supply REAL NOT NULL,
                data_source TEXT DEFAULT 'coingecko',
                my_notes TEXT,
                UNIQUE(recorded_at)
            )
        """)
        
        # My UTXO discoveries table (my unique approach)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS my_utxo_discoveries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id TEXT NOT NULL,
                btc_value REAL NOT NULL,
                discovered_at TEXT NOT NULL,
                usd_value_when_created REAL NOT NULL,
                confidence_score REAL DEFAULT 0.8,
                my_quality_rating INTEGER DEFAULT 5,
                blockchain_source TEXT DEFAULT 'mempool',
                my_notes TEXT,
                UNIQUE(transaction_id)
            )
        """)
        
        # My historical price memory
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS my_price_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                price_date TEXT NOT NULL,
                btc_price_usd REAL NOT NULL,
                lookup_source TEXT DEFAULT 'coingecko',
                remembered_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(price_date)
            )
        """)
        
        # My MVRV analysis results
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS my_mvrv_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                analysis_time TEXT NOT NULL,
                market_capitalization REAL NOT NULL,
                realized_capitalization REAL NOT NULL,
                mvrv_ratio REAL NOT NULL,
                my_signal TEXT,
                my_confidence REAL DEFAULT 0.8,
                analysis_period TEXT DEFAULT 'hourly',
                my_interpretation TEXT,
                data_quality_score REAL DEFAULT 0.8,
                UNIQUE(analysis_time, analysis_period)
            )
        """)
        
        # My personal insights and notes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS my_insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                insight_date TEXT NOT NULL,
                insight_type TEXT NOT NULL,
                insight_content TEXT NOT NULL,
                confidence_level REAL DEFAULT 0.7,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # My custom indexes for fast queries
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_my_price_time ON my_price_tracking(recorded_at)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_my_mvrv_time ON my_mvrv_analysis(analysis_time)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_my_utxo_discovered ON my_utxo_discoveries(discovered_at)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_my_price_memory ON my_price_memory(price_date)")
        
        conn.commit()
        conn.close()
    
    def store_my_price_discovery(self, timestamp, price_usd, supply, notes=None):
        """Store my latest Bitcoin price discovery"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO my_price_tracking 
            (recorded_at, btc_price_usd, total_supply, my_notes)
            VALUES (?, ?, ?, ?)
        """, (timestamp, price_usd, supply, notes))
        
        conn.commit()
        conn.close()
    
    def store_my_utxo_discoveries(self, utxo_batch):
        """Store my batch of UTXO discoveries"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # My custom UTXO storage with confidence scoring
        for utxo_data in utxo_batch:
            if len(utxo_data) >= 5:  # My extended format
                txid, btc_val, discovered_time, usd_val, confidence = utxo_data[:5]
                quality_rating = min(int(confidence * 10), 10)  # My 1-10 scale
                
                cursor.execute("""
                    INSERT OR REPLACE INTO my_utxo_discoveries 
                    (transaction_id, btc_value, discovered_at, usd_value_when_created, 
                     confidence_score, my_quality_rating)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (txid, btc_val, discovered_time, usd_val, confidence, quality_rating))
            else:  # Fallback to basic format
                txid, btc_val, discovered_time, usd_val = utxo_data
                cursor.execute("""
                    INSERT OR REPLACE INTO my_utxo_discoveries 
                    (transaction_id, btc_value, discovered_at, usd_value_when_created)
                    VALUES (?, ?, ?, ?)
                """, (txid, btc_val, discovered_time, usd_val))
        
        conn.commit()
        conn.close()
    
    def remember_historical_price(self, date_str, price_usd):
        """Remember a historical Bitcoin price for future reference"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO my_price_memory (price_date, btc_price_usd)
            VALUES (?, ?)
        """, (date_str, price_usd))
        
        conn.commit()
        conn.close()
    
    def store_my_mvrv_analysis(self, timestamp, market_cap, realized_cap, ratio, 
                              signal=None, confidence=0.8, timeframe='hourly'):
        """Store my complete MVRV analysis"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO my_mvrv_analysis 
            (analysis_time, market_capitalization, realized_capitalization, mvrv_ratio,
             my_signal, my_confidence, analysis_period)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (timestamp, market_cap, realized_cap, ratio, signal, confidence, timeframe))
        
        conn.commit()
        conn.close()
    
    def get_my_latest_price_data(self):
        """Get my most recent price data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT btc_price_usd, total_supply, recorded_at
            FROM my_price_tracking
            ORDER BY recorded_at DESC
            LIMIT 1
        """)
        
        result = cursor.fetchone()
        conn.close()
        
        return result
    
    def get_price_from_my_history(self, date_str):
        """Get price from my historical memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT btc_price_usd FROM my_price_memory
            WHERE price_date <= ?
            ORDER BY price_date DESC
            LIMIT 1
        """, (date_str,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
    
    def get_my_latest_mvrv(self):
        """Get my latest MVRV analysis"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT analysis_time, market_capitalization, realized_capitalization, 
                   mvrv_ratio, my_signal, my_confidence
            FROM my_mvrv_analysis
            WHERE analysis_period = 'hourly'
            ORDER BY analysis_time DESC
            LIMIT 1
        """)
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'timestamp': result[0],
                'market_cap': result[1],
                'realized_cap': result[2],
                'ratio': result[3],
                'signal': result[4],
                'confidence': result[5]
            }
        return None
    
    def get_my_mvrv_history(self, period='hourly', limit=168):
        """Get my MVRV analysis history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT analysis_time, market_capitalization, realized_capitalization, 
                   mvrv_ratio, my_signal, my_confidence
            FROM my_mvrv_analysis
            WHERE analysis_period = ?
            ORDER BY analysis_time DESC
            LIMIT ?
        """, (period, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        history = []
        for row in reversed(results):  # Chronological order
            history.append({
                'timestamp': row[0],
                'market_cap': row[1],
                'realized_cap': row[2],
                'ratio': row[3],
                'signal': row[4],
                'confidence': row[5]
            })
        
        return history
    
    def save_my_insight(self, insight_type, content, confidence=0.7):
        """Save my personal insights about the market"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO my_insights (insight_date, insight_type, insight_content, confidence_level)
            VALUES (?, ?, ?, ?)
        """, (datetime.utcnow().isoformat(), insight_type, content, confidence))
        
        conn.commit()
        conn.close()
    
    def get_my_database_stats(self):
        """Get statistics about my database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Count my records
        tables = ['my_price_tracking', 'my_utxo_discoveries', 'my_mvrv_analysis', 'my_insights']
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            stats[table] = count
        
        # My data quality metrics
        cursor.execute("SELECT AVG(confidence_score) FROM my_utxo_discoveries")
        avg_utxo_confidence = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT AVG(my_confidence) FROM my_mvrv_analysis")
        avg_mvrv_confidence = cursor.fetchone()[0] or 0
        
        stats['my_data_quality'] = {
            'utxo_confidence': avg_utxo_confidence,
            'mvrv_confidence': avg_mvrv_confidence,
            'overall_quality': (avg_utxo_confidence + avg_mvrv_confidence) / 2
        }
        
        conn.close()
        return stats