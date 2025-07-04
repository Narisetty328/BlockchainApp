#!/usr/bin/env python3
"""
Simple launcher for Bitcoin MVRV System
"""

import subprocess
import sys
import os

def main():
    print("🪙 Bitcoin MVRV Analysis System")
    print("=" * 40)
    print("1. Setup Database")
    print("2. Run Dashboard")
    print("3. Run Full System")
    print("4. Exit")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == "1":
        print("🔧 Setting up database...")
        from scheduler import MVRVScheduler
        scheduler = MVRVScheduler()
        scheduler.initial_setup()
        print("✅ Setup complete!")
        
    elif choice == "2":
        print("🎨 Starting dashboard...")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py"])
        
    elif choice == "3":
        print("🚀 Starting full system...")
        subprocess.run([sys.executable, "main.py"])
        
    elif choice == "4":
        print("👋 Goodbye!")
        
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()