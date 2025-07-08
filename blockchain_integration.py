import requests
import time
from datetime import datetime, timedelta
import json

class BlockchainIntegration:
    def __init__(self):
        self.mempool_base = "https://mempool.space/api"
        self.blockstream_base = "https://blockstream.info/api"
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'MVRV-Calculator/1.0'})
    
    def get_recent_blocks(self, count=10):
        """Get recent Bitcoin blocks"""
        try:
            url = f"{self.mempool_base}/blocks"
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            blocks = response.json()
            return blocks[:count]
        except Exception as e:
            print(f"Error fetching blocks: {e}")
            return []
    
    def get_block_transactions(self, block_hash, limit=25):
        """Get transactions from a specific block"""
        try:
            url = f"{self.mempool_base}/block/{block_hash}/txs"
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            txs = response.json()
            return [tx['txid'] for tx in txs[:limit]]
        except Exception as e:
            print(f"Error fetching block transactions: {e}")
            return []
    
    def get_transaction_details(self, txid):
        """Get detailed transaction information"""
        try:
            url = f"{self.blockstream_base}/tx/{txid}"
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching transaction {txid}: {e}")
            return None
    
    def extract_utxos_from_transaction(self, tx_data, block_timestamp):
        """Extract UTXO data from transaction"""
        if not tx_data:
            return []
        
        utxos = []
        for i, output in enumerate(tx_data.get('vout', [])):
            # Only include unspent outputs (we'll assume recent ones are unspent)
            utxos.append({
                'txid': tx_data['txid'],
                'vout': i,
                'value_btc': output['value'] / 100000000,  # Satoshi to BTC
                'timestamp': block_timestamp,
                'address': output.get('scriptpubkey_address', ''),
                'script_type': output.get('scriptpubkey_type', 'unknown')
            })
        
        return utxos
    
    def fetch_real_utxo_sample(self, target_count=2000):
        """Fetch real UTXO sample from Bitcoin blockchain"""
        print("🔗 Fetching real UTXO data from Bitcoin blockchain...")
        
        utxos = []
        blocks = self.get_recent_blocks(20)  # Get last 20 blocks
        
        for block in blocks:
            if len(utxos) >= target_count:
                break
            
            print(f"📦 Processing block {block['height']} ({block['id'][:8]}...)")
            
            # Get transactions from this block
            tx_ids = self.get_block_transactions(block['id'], 15)
            
            for tx_id in tx_ids:
                if len(utxos) >= target_count:
                    break
                
                # Get transaction details
                tx_data = self.get_transaction_details(tx_id)
                if tx_data:
                    # Extract UTXOs from this transaction
                    tx_utxos = self.extract_utxos_from_transaction(tx_data, block['timestamp'])
                    utxos.extend(tx_utxos)
                
                # Rate limiting
                time.sleep(0.1)
        
        print(f"✅ Collected {len(utxos)} real UTXOs from blockchain")
        return utxos
    
    def get_utxo_statistics(self, utxos):
        """Calculate statistics about UTXO set"""
        if not utxos:
            return {}
        
        values = [utxo['value_btc'] for utxo in utxos]
        timestamps = [utxo['timestamp'] for utxo in utxos]
        
        return {
            'total_utxos': len(utxos),
            'total_value_btc': sum(values),
            'avg_value_btc': sum(values) / len(values),
            'min_value_btc': min(values),
            'max_value_btc': max(values),
            'oldest_timestamp': min(timestamps),
            'newest_timestamp': max(timestamps),
            'unique_addresses': len(set(utxo['address'] for utxo in utxos if utxo['address']))
        }
    
    def validate_blockchain_connection(self):
        """Test blockchain API connectivity"""
        try:
            # Test Mempool.space
            response = self.session.get(f"{self.mempool_base}/blocks/tip/height", timeout=10)
            mempool_status = response.status_code == 200
            
            # Test Blockstream
            response = self.session.get(f"{self.blockstream_base}/blocks/tip/height", timeout=10)
            blockstream_status = response.status_code == 200
            
            return {
                'mempool_space': mempool_status,
                'blockstream': blockstream_status,
                'overall': mempool_status or blockstream_status
            }
        except Exception as e:
            print(f"Blockchain connection test failed: {e}")
            return {
                'mempool_space': False,
                'blockstream': False,
                'overall': False
            }
    
    def get_network_stats(self):
        """Get Bitcoin network statistics"""
        try:
            url = f"{self.mempool_base}/v1/statistics"
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching network stats: {e}")
            return {}
    
    def estimate_total_utxo_count(self):
        """Estimate total UTXO count in Bitcoin network"""
        # Based on historical data, Bitcoin has approximately 80-100 million UTXOs
        # This is a reasonable estimate for scaling calculations
        return 85_000_000
    
    def calculate_scaling_factor(self, sample_size):
        """Calculate scaling factor to estimate full UTXO set value"""
        total_estimated_utxos = self.estimate_total_utxo_count()
        if sample_size == 0:
            return 1
        return total_estimated_utxos / sample_size