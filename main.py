#!/usr/bin/env python3
"""
Bitcoin MVRV Analysis System
Complete application for calculating and visualizing MVRV ratios
"""

import sys
import subprocess
import threading
import time
from scheduler import MVRVScheduler

def run_dashboard():
    """Run Streamlit dashboard"""
    subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py"])

def run_scheduler():
    """Run background scheduler"""
    scheduler = MVRVScheduler()
    try:
        scheduler.start_scheduler()
        print("🎯 Background scheduler started")
        
        # Keep scheduler running
        while True:
            time.sleep(60)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping scheduler...")
        scheduler.stop_scheduler()

def main():
    """Main application entry point"""
    print("🚀 Starting Bitcoin MVRV Analysis System")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        if mode == "dashboard":
            print("🎨 Starting dashboard only...")
            run_dashboard()
            
        elif mode == "scheduler":
            print("⏰ Starting scheduler only...")
            run_scheduler()
            
        elif mode == "setup":
            print("🔧 Running initial setup...")
            scheduler = MVRVScheduler()
            scheduler.initial_setup()
            print("✅ Setup completed!")
            
        else:
            print("❌ Invalid mode. Use: dashboard, scheduler, or setup")
            sys.exit(1)
    
    else:
        # Run both dashboard and scheduler
        print("🎯 Starting full system (dashboard + scheduler)...")
        
        # Start scheduler in background thread
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        
        # Give scheduler time to initialize
        time.sleep(3)
        
        # Start dashboard (blocking)
        print("🎨 Starting dashboard...")
        run_dashboard()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)