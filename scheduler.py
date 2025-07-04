import schedule
import time
import threading
from datetime import datetime
from data_collector import DataCollector
from mvrv_calculator import MVRVCalculator

class MVRVScheduler:
    def __init__(self):
        self.collector = DataCollector()
        self.calculator = MVRVCalculator()
        self.running = False
        self.thread = None
    
    def hourly_job(self):
        """Job to run every hour"""
        print(f"\n🕐 Hourly job started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Collect fresh data
        success = self.collector.collect_all_data()
        
        if success:
            # Calculate MVRV
            result = self.calculator.perform_hourly_calculation()
            
            if result:
                print(f"📊 MVRV Ratio: {result['mvrv_ratio']:.4f}")
                print(f"💰 Market Cap: ${result['market_cap']/1e9:.1f}B")
                print(f"🔄 Realized Cap: ${result['realized_cap']/1e9:.1f}B")
            else:
                print("❌ MVRV calculation failed")
        else:
            print("❌ Data collection failed")
        
        print("✅ Hourly job completed\n")
    
    def daily_job(self):
        """Job to run daily for aggregation"""
        print(f"\n📅 Daily aggregation started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        result = self.calculator.perform_daily_aggregation()
        
        if result:
            print(f"📈 Daily MVRV: {result['mvrv_ratio']:.4f}")
            print(f"📊 Data Points: {result['data_points']}")
        else:
            print("❌ Daily aggregation failed")
        
        print("✅ Daily job completed\n")
    
    def initial_setup(self):
        """Run initial data collection and calculation"""
        print("🚀 Running initial setup...")
        
        # Initial data collection
        self.collector.collect_all_data()
        
        # Initial MVRV calculation
        self.calculator.perform_hourly_calculation()
        
        print("✅ Initial setup completed")
    
    def start_scheduler(self):
        """Start the scheduler in a separate thread"""
        if self.running:
            print("⚠️ Scheduler already running")
            return
        
        print("🔄 Starting MVRV scheduler...")
        
        # Run initial setup
        self.initial_setup()
        
        # Schedule jobs
        schedule.every().hour.do(self.hourly_job)
        schedule.every().day.at("00:30").do(self.daily_job)  # Run daily at 12:30 AM
        
        # For testing - run every 2 minutes instead of hourly
        # schedule.every(2).minutes.do(self.hourly_job)
        
        self.running = True
        
        def run_scheduler():
            while self.running:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        
        self.thread = threading.Thread(target=run_scheduler, daemon=True)
        self.thread.start()
        
        print("✅ Scheduler started successfully")
        print("📋 Schedule:")
        print("   - Hourly: Data collection + MVRV calculation")
        print("   - Daily: Aggregate hourly data")
    
    def stop_scheduler(self):
        """Stop the scheduler"""
        if not self.running:
            print("⚠️ Scheduler not running")
            return
        
        print("🛑 Stopping scheduler...")
        self.running = False
        
        if self.thread:
            self.thread.join(timeout=5)
        
        schedule.clear()
        print("✅ Scheduler stopped")
    
    def run_manual_update(self):
        """Manually trigger data update and calculation"""
        print("🔄 Manual update triggered...")
        self.hourly_job()
    
    def get_scheduler_status(self):
        """Get current scheduler status"""
        return {
            'running': self.running,
            'next_jobs': [str(job) for job in schedule.jobs],
            'job_count': len(schedule.jobs)
        }

# Standalone execution
if __name__ == "__main__":
    scheduler = MVRVScheduler()
    
    try:
        scheduler.start_scheduler()
        
        print("\n🎯 Scheduler is running. Press Ctrl+C to stop...")
        print("💡 The system will:")
        print("   - Collect Bitcoin data every hour")
        print("   - Calculate MVRV ratios")
        print("   - Aggregate daily summaries")
        
        # Keep the main thread alive
        while True:
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutdown requested...")
        scheduler.stop_scheduler()
        print("👋 Goodbye!")