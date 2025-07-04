import sqlite3
from datetime import datetime
import json

class MVRVDatabase:
    def __init__(self, db_path="mvrv_bitcoin.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Price data table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS price_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                price_usd REAL NOT NULL,
                supply REAL NOT NULL,
                UNIQUE(timestamp)
            )
        """)
        
        # UTXO data table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS utxo_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                txid TEXT NOT NULL,
                value_btc REAL NOT NULL,
                moved_timestamp TEXT NOT NULL,
                value_usd REAL NOT NULL,
                UNIQUE(txid)
            )
        """)
        
        # Historical prices table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS historical_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                price_usd REAL NOT NULL,
                UNIQUE(timestamp)
            )
        """)
        
        # MVRV ratios table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mvrv_ratios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                market_cap REAL NOT NULL,
                realized_cap REAL NOT NULL,
                ratio REAL NOT NULL,
                timeframe TEXT DEFAULT 'hourly',
                UNIQUE(timestamp, timeframe)
            )
        """)
        
        # Create indexes for performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_price_timestamp ON price_data(timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_mvrv_timestamp ON mvrv_ratios(timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_utxo_moved ON utxo_data(moved_timestamp)")
        
        conn.commit()
        conn.close()
    
    def insert_price_data(self, timestamp, price_usd, supply):
        """Insert current price data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO price_data (timestamp, price_usd, supply)
            VALUES (?, ?, ?)
        """, (timestamp, price_usd, supply))
        
        conn.commit()
        conn.close()
    
    def insert_utxo_data(self, utxo_list):
        """Insert UTXO data in batch"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.executemany("""
            INSERT OR REPLACE INTO utxo_data (txid, value_btc, moved_timestamp, value_usd)
            VALUES (?, ?, ?, ?)
        """, utxo_list)
        
        conn.commit()
        conn.close()
    
    def insert_historical_price(self, timestamp, price_usd):
        """Insert historical price data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO historical_prices (timestamp, price_usd)
            VALUES (?, ?)
        """, (timestamp, price_usd))
        
        conn.commit()
        conn.close()
    
    def insert_mvrv_ratio(self, timestamp, market_cap, realized_cap, ratio, timeframe='hourly'):
        """Insert MVRV calculation result"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO mvrv_ratios (timestamp, market_cap, realized_cap, ratio, timeframe)
            VALUES (?, ?, ?, ?, ?)
        """, (timestamp, market_cap, realized_cap, ratio, timeframe))
        
        conn.commit()
        conn.close()
    
    def get_latest_mvrv(self):
        """Get latest MVRV calculation"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT timestamp, market_cap, realized_cap, ratio
            FROM mvrv_ratios
            WHERE timeframe = 'hourly'
            ORDER BY timestamp DESC
            LIMIT 1
        """)
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'timestamp': result[0],
                'market_cap': result[1],
                'realized_cap': result[2],
                'ratio': result[3]
            }
        return None
    
    def get_mvrv_history(self, timeframe='hourly', limit=168):  # 7 days of hourly data
        """Get MVRV historical data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT timestamp, market_cap, realized_cap, ratio
            FROM mvrv_ratios
            WHERE timeframe = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (timeframe, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        return [{
            'timestamp': row[0],
            'market_cap': row[1],
            'realized_cap': row[2],
            'ratio': row[3]
        } for row in reversed(results)]
    
    def get_price_at_timestamp(self, timestamp):
        """Get historical price at specific timestamp"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT price_usd FROM historical_prices
            WHERE timestamp <= ?
            ORDER BY timestamp DESC
            LIMIT 1
        """, (timestamp,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None