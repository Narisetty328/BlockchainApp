"""
BTC Brain - My Personal Bitcoin MVRV Analysis Engine
Created with love for understanding Bitcoin's true value
"""

import requests
import time
from datetime import datetime, timedelta
import random
import json

class BitcoinBrain:
    def __init__(self):
        # My personal API endpoints - chosen for reliability
        self.my_apis = {
            'mempool': "https://mempool.space/api",
            'explorer': "https://blockstream.info/api", 
            'prices': "https://api.coingecko.com/api/v3"
        }
        
        # My custom session with personality
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'PersonalMVRVAnalyzer/2024 (Educational)',
            'Accept': 'application/json'
        })
        
        # My understanding of Bitcoin network (approximate values I researched)
        self.btc_knowledge = {
            'total_utxos_estimate': 87_500_000,  # My research-based estimate
            'avg_block_time_minutes': 10,
            'satoshis_per_btc': 100_000_000
        }
    
    def check_my_connection(self):
        """My way of testing if I can reach Bitcoin data"""
        print("🧠 BTC Brain checking connection to Bitcoin world...")
        
        connection_health = {}
        
        # Test my chosen APIs
        for name, url in self.my_apis.items():
            try:
                if name == 'mempool':
                    test_url = f"{url}/blocks/tip/height"
                elif name == 'explorer':
                    test_url = f"{url}/blocks/tip/height"
                else:  # prices
                    test_url = f"{url}/ping"
                
                response = self.session.get(test_url, timeout=8)
                connection_health[name] = response.status_code == 200
                
                if connection_health[name]:
                    print(f"   ✨ {name.title()} API: Connected & Ready")
                else:
                    print(f"   😞 {name.title()} API: Not responding")
                    
            except Exception as e:
                connection_health[name] = False
                print(f"   💔 {name.title()} API: Connection failed")
        
        overall_health = any(connection_health.values())
        
        if overall_health:
            print("🎉 BTC Brain is connected to Bitcoin network!")
        else:
            print("😔 BTC Brain cannot reach Bitcoin network right now")
            
        return {**connection_health, 'brain_online': overall_health}
    
    def fetch_recent_bitcoin_blocks(self, how_many=15):
        """My method to get fresh Bitcoin blocks"""
        print(f"🔍 Fetching last {how_many} Bitcoin blocks...")
        
        try:
            response = self.session.get(f"{self.my_apis['mempool']}/blocks", timeout=15)
            response.raise_for_status()
            
            all_blocks = response.json()
            recent_blocks = all_blocks[:how_many]
            
            print(f"📦 Got {len(recent_blocks)} fresh blocks from Bitcoin network")
            return recent_blocks
            
        except Exception as error:
            print(f"😓 Couldn't fetch blocks: {error}")
            return []
    
    def extract_transactions_from_block(self, block_id, tx_limit=20):
        """My way of getting transactions from a specific block"""
        try:
            url = f"{self.my_apis['mempool']}/block/{block_id}/txs"
            response = self.session.get(url, timeout=12)
            response.raise_for_status()
            
            transactions = response.json()
            
            # My selection logic - get diverse transaction types
            selected_txs = []
            for i, tx in enumerate(transactions[:tx_limit]):
                selected_txs.append(tx['txid'])
                
            return selected_txs
            
        except Exception as error:
            print(f"🤔 Block {block_id[:8]}... gave me trouble: {error}")
            return []
    
    def analyze_transaction_deeply(self, tx_id):
        """My deep dive into a Bitcoin transaction"""
        try:
            url = f"{self.my_apis['explorer']}/tx/{tx_id}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            tx_data = response.json()
            return tx_data
            
        except Exception as error:
            print(f"🔬 Transaction {tx_id[:8]}... analysis failed: {error}")
            return None
    
    def discover_utxos_from_transaction(self, tx_info, block_time):
        """My unique way of finding UTXOs in transactions"""
        if not tx_info:
            return []
        
        my_utxos = []
        
        # My logic for identifying valuable UTXOs
        for output_index, output in enumerate(tx_info.get('vout', [])):
            
            # My criteria for interesting UTXOs
            btc_value = output['value'] / self.btc_knowledge['satoshis_per_btc']
            
            # Skip dust (my personal threshold)
            if btc_value < 0.00001:  # Less than 1000 sats
                continue
            
            utxo_info = {
                'tx_hash': tx_info['txid'],
                'output_position': output_index,
                'btc_amount': btc_value,
                'creation_time': block_time,
                'recipient_address': output.get('scriptpubkey_address', 'unknown'),
                'script_pattern': output.get('scriptpubkey_type', 'mystery'),
                'my_confidence': self.calculate_my_confidence(btc_value, output)
            }
            
            my_utxos.append(utxo_info)
        
        return my_utxos
    
    def calculate_my_confidence(self, btc_value, output_data):
        """Calculate confidence score for UTXO data quality"""
        confidence = 0.5
        
        if btc_value > 1.0:
            confidence += 0.3
        elif btc_value > 0.1:
            confidence += 0.2
        elif btc_value > 0.01:
            confidence += 0.1
        
        script_type = output_data.get('scriptpubkey_type', '')
        if script_type in ['p2pkh', 'p2sh', 'v0_p2wpkh']:
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def hunt_for_real_utxos(self, target_utxos=2500):
        """Collect real UTXO data from Bitcoin blockchain"""
        print(f"🎯 Collecting {target_utxos} real Bitcoin UTXOs...")
        
        my_utxo_collection = []
        blocks_processed = 0
        
        # Get fresh blocks to hunt in
        hunting_blocks = self.fetch_recent_bitcoin_blocks(25)
        
        for block in hunting_blocks:
            if len(my_utxo_collection) >= target_utxos:
                break
                
            print(f"🔎 Hunting in block {block['height']} ({block['id'][:8]}...)")
            blocks_processed += 1
            
            # Get transactions from this block
            tx_list = self.extract_transactions_from_block(block['id'], 12)
            
            for tx_id in tx_list:
                if len(my_utxo_collection) >= target_utxos:
                    break
                
                # Analyze this transaction
                tx_details = self.analyze_transaction_deeply(tx_id)
                
                if tx_details:
                    # Find UTXOs in this transaction
                    found_utxos = self.discover_utxos_from_transaction(tx_details, block['timestamp'])
                    my_utxo_collection.extend(found_utxos)
                
                # My polite delay to not overwhelm APIs
                time.sleep(0.15)
        
        print(f"🏆 Hunt complete! Found {len(my_utxo_collection)} real UTXOs from {blocks_processed} blocks")
        return my_utxo_collection
    
    def calculate_utxo_insights(self, my_utxos):
        """My personal analysis of the UTXO collection"""
        if not my_utxos:
            return {}
        
        btc_values = [utxo['btc_amount'] for utxo in my_utxos]
        timestamps = [utxo['creation_time'] for utxo in my_utxos]
        confidences = [utxo['my_confidence'] for utxo in my_utxos]
        
        my_insights = {
            'total_utxos_found': len(my_utxos),
            'total_btc_value': sum(btc_values),
            'average_utxo_size': sum(btc_values) / len(btc_values),
            'largest_utxo': max(btc_values),
            'smallest_utxo': min(btc_values),
            'oldest_utxo_time': min(timestamps),
            'newest_utxo_time': max(timestamps),
            'average_confidence': sum(confidences) / len(confidences),
            'unique_addresses': len(set(utxo['recipient_address'] for utxo in my_utxos if utxo['recipient_address'] != 'unknown')),
            'my_quality_score': self.calculate_my_quality_score(my_utxos)
        }
        
        return my_insights
    
    def calculate_my_quality_score(self, utxos):
        """Calculate overall quality score for UTXO dataset"""
        if not utxos:
            return 0
        
        size_score = sum(min(utxo['btc_amount'] * 10, 5) for utxo in utxos) / len(utxos)
        confidence_score = sum(utxo['my_confidence'] for utxo in utxos) / len(utxos) * 5
        diversity_score = len(set(utxo['script_pattern'] for utxo in utxos)) * 0.5
        
        total_score = (size_score + confidence_score + diversity_score) / 3
        return min(total_score, 10.0)
    
    def estimate_full_network_scaling(self, sample_size):
        """Scale UTXO sample to estimate full Bitcoin network"""
        if sample_size == 0:
            return 1
        
        estimated_total = self.btc_knowledge['total_utxos_estimate']
        base_factor = estimated_total / sample_size
        
        if sample_size < 1000:
            adjustment = 0.8
        elif sample_size < 2000:
            adjustment = 0.9
        else:
            adjustment = 1.0
        
        final_factor = base_factor * adjustment
        
        print(f"🧮 Scaling: {sample_size} UTXOs → Full network (factor: {final_factor:.0f})")
        return final_factor