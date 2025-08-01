#!/usr/bin/env python3
"""
Test script to verify configuration
Run this to check if your API key and files are properly configured
"""

import os
from dotenv import load_dotenv
import pandas as pd

def test_configuration():
    print("🔍 Testing SAP Chatbot Configuration...")
    print("=" * 50)
    
    # Test 1: Check .env file
    print("1. Checking .env file...")
    if os.path.exists('.env'):
        print("   ✅ .env file exists")
        load_dotenv()
        
        # Check API key
        api_key = os.getenv("SERPAPI_KEY", "********")
        if api_key:
            print(f"   ✅ API key configured: {api_key[:8]}...")
        else:
            print("   ❌ API key not configured")
            print("   💡 Add SERPAPI_KEY=your_key_here to .env file")
    else:
        print("   ❌ .env file not found")
        print("   💡 Create .env file with your API key")
    
    # Test 2: Check knowledge base
    print("\n2. Checking knowledge base...")
    kb_path = os.getenv("KB_DATA_PATH", "kb_data/sap_kb.xlsx")
    
    if os.path.exists(kb_path):
        print(f"   ✅ Knowledge base file exists: {kb_path}")
        
        try:
            df = pd.read_excel(kb_path)
            print(f"   ✅ File readable, {len(df)} rows found")
            
            # Check required columns
            required_cols = ['Note Title', 'Description']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                print(f"   ❌ Missing columns: {missing_cols}")
                print(f"   📋 Available columns: {list(df.columns)}")
            else:
                print("   ✅ Required columns found")
                
            # Check for empty data
            empty_rows = df[required_cols].isnull().any(axis=1).sum()
            if empty_rows > 0:
                print(f"   ⚠️  {empty_rows} rows have empty required fields")
            else:
                print("   ✅ No empty required fields")
                
        except Exception as e:
            print(f"   ❌ Error reading file: {e}")
    else:
        print(f"   ❌ Knowledge base file not found: {kb_path}")
        print("   💡 Place your Excel file in kb_data/sap_kb.xlsx")
    
    # Test 3: Check directories
    print("\n3. Checking directories...")
    required_dirs = ['kb_data']
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"   ✅ {dir_name}/ directory exists")
        else:
            print(f"   ❌ {dir_name}/ directory missing")
            print(f"   💡 Create directory: mkdir {dir_name}")
    
    # Test 4: Test API connection
    print("\n4. Testing API connection...")
    api_key = os.getenv("SERPAPI_KEY", "")
    if api_key:
        try:
            import requests
            params = {
                "engine": "google",
                "q": "test query",
                "api_key": api_key,
                "num": 1
            }
            response = requests.get("https://serpapi.com/search", params=params, timeout=10)
            if response.status_code == 200:
                print("   ✅ API connection successful")
            else:
                print(f"   ❌ API returned status: {response.status_code}")
        except Exception as e:
            print(f"   ❌ API connection failed: {e}")
    else:
        print("   ⏭️  Skipping API test (no key configured)")
    
    print("\n" + "=" * 50)
    print("🎯 Configuration test complete!")
    print("💡 If you see any ❌, fix those issues before running the app.")

if __name__ == "__main__":
    test_configuration()