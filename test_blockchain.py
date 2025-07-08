#!/usr/bin/env python3
"""
Test script to verify real blockchain integration
"""

from blockchain_integration import BlockchainIntegration
from mvrv_calculator import MVRVCalculator
from data_collector import DataCollector

def test_blockchain_connection():
    """Test blockchain API connectivity"""
    print("🔗 Testing Blockchain Integration...")
    print("=" * 50)
    
    blockchain = BlockchainIntegration()
    
    # Test API connectivity
    print("1. Testing API Connectivity:")
    status = blockchain.validate_blockchain_connection()
    
    if status['mempool_space']:
        print("   ✅ Mempool.space API: Connected")
    else:
        print("   ❌ Mempool.space API: Failed")
    
    if status['blockstream']:
        print("   ✅ Blockstream API: Connected")
    else:
        print("   ❌ Blockstream API: Failed")
    
    if not status['overall']:
        print("   ⚠️ No blockchain APIs available")
        return False
    
    # Test fetching real blocks
    print("\n2. Testing Real Block Data:")
    blocks = blockchain.get_recent_blocks(3)
    
    if blocks:
        print(f"   ✅ Fetched {len(blocks)} recent blocks")
        for i, block in enumerate(blocks[:2]):
            print(f"   📦 Block {i+1}: Height {block['height']}, Hash: {block['id'][:16]}...")
    else:
        print("   ❌ Failed to fetch block data")
        return False
    
    # Test fetching real UTXOs
    print("\n3. Testing Real UTXO Data:")
    try:
        utxos = blockchain.fetch_real_utxo_sample(100)  # Small sample for testing
        
        if utxos:
            print(f"   ✅ Fetched {len(utxos)} real UTXOs from blockchain")
            
            # Show sample UTXO
            sample_utxo = utxos[0]
            print(f"   📊 Sample UTXO:")
            print(f"      - TXID: {sample_utxo['txid'][:16]}...")
            print(f"      - Value: {sample_utxo['value_btc']:.8f} BTC")
            print(f"      - Timestamp: {sample_utxo['timestamp']}")
            
            # Calculate statistics
            stats = blockchain.get_utxo_statistics(utxos)
            print(f"   📈 UTXO Statistics:")
            print(f"      - Total UTXOs: {stats['total_utxos']}")
            print(f"      - Total Value: {stats['total_value_btc']:.2f} BTC")
            print(f"      - Average Value: {stats['avg_value_btc']:.8f} BTC")
            
        else:
            print("   ❌ Failed to fetch UTXO data")
            return False
            
    except Exception as e:
        print(f"   ❌ Error fetching UTXOs: {e}")
        return False
    
    print("\n✅ Blockchain integration test completed successfully!")
    return True

def test_mvrv_calculation():
    """Test MVRV calculation with real blockchain data"""
    print("\n🧮 Testing MVRV Calculation with Real Data...")
    print("=" * 50)
    
    try:
        # Initialize components
        collector = DataCollector()
        calculator = MVRVCalculator()
        
        # Collect current price data
        print("1. Collecting current Bitcoin price...")
        price_data = collector.fetch_current_price_data()
        
        if price_data:
            print(f"   ✅ Current BTC Price: ${price_data['price_usd']:,.2f}")
            print(f"   ✅ Circulating Supply: {price_data['supply']:,.0f} BTC")
        else:
            print("   ❌ Failed to fetch price data")
            return False
        
        # Calculate MVRV with real blockchain data
        print("\n2. Calculating MVRV with real blockchain UTXOs...")
        result = calculator.perform_hourly_calculation()
        
        if result:
            print(f"   ✅ MVRV Calculation Successful!")
            print(f"   📊 Results:")
            print(f"      - MVRV Ratio: {result['mvrv_ratio']:.4f}")
            print(f"      - Market Cap: ${result['market_cap']/1e9:.2f}B")
            print(f"      - Realized Cap: ${result['realized_cap']/1e9:.2f}B")
            print(f"      - Price: ${result['price_usd']:,.2f}")
            
            # Interpret result
            mvrv = result['mvrv_ratio']
            if mvrv > 3.7:
                signal = "🔴 SELL - Historically overvalued"
            elif mvrv > 2.4:
                signal = "🟡 CAUTION - Elevated levels"
            elif mvrv > 1.0:
                signal = "🟢 HOLD - Normal range"
            else:
                signal = "🔵 BUY - Potentially undervalued"
            
            print(f"   🚦 Market Signal: {signal}")
            
        else:
            print("   ❌ MVRV calculation failed")
            return False
        
        print("\n✅ MVRV calculation test completed successfully!")
        return True
        
    except Exception as e:
        print(f"   ❌ Error in MVRV calculation: {e}")
        return False

def main():
    """Run all blockchain integration tests"""
    print("🪙 Bitcoin MVRV System - Blockchain Integration Test")
    print("=" * 60)
    
    # Test blockchain connection
    blockchain_ok = test_blockchain_connection()
    
    if blockchain_ok:
        # Test MVRV calculation
        mvrv_ok = test_mvrv_calculation()
        
        if mvrv_ok:
            print("\n🎉 ALL TESTS PASSED!")
            print("✅ Real blockchain integration is working correctly")
            print("✅ UTXO data is being fetched from Bitcoin network")
            print("✅ MVRV calculations are using real on-chain data")
            print("\n🚀 System is ready for interview demonstration!")
        else:
            print("\n❌ MVRV calculation test failed")
    else:
        print("\n❌ Blockchain connection test failed")
        print("⚠️ Check internet connection and API availability")

if __name__ == "__main__":
    main()