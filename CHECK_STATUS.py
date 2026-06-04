#!/usr/bin/env python3
"""
Banking App Status Checker
Verifies that all components are properly configured and accessible
"""

import sys
import subprocess
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError
import json
from dotenv import load_dotenv
import os

# Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header():
    print(f"\n{BOLD}{BLUE}🏦 Banking Management System - Status Checker{RESET}\n")
    print("=" * 50)

def print_section(title):
    print(f"\n{BOLD}{BLUE}{title}{RESET}")
    print("-" * 50)

def check_success(message):
    print(f"{GREEN}✓ {message}{RESET}")

def check_error(message):
    print(f"{RED}✗ {message}{RESET}")

def check_warning(message):
    print(f"{YELLOW}⚠ {message}{RESET}")

def check_file_exists(path, name):
    if Path(path).exists():
        check_success(f"{name} found")
        return True
    else:
        check_error(f"{name} NOT found at {path}")
        return False

def check_http_endpoint(url, name):
    try:
        response = urlopen(url, timeout=5)
        check_success(f"{name} is accessible ({response.status})")
        return True
    except URLError as e:
        check_error(f"{name} is NOT accessible: {str(e)}")
        return False
    except Exception as e:
        check_error(f"{name} check failed: {str(e)}")
        return False

def check_mongodb_connection():
    """Check MongoDB connection"""
    try:
        from pymongo import MongoClient
        load_dotenv("BankAPI/.env")
        mongodb_uri = os.getenv("MONGODB_URI")
        
        if not mongodb_uri:
            check_error("MONGODB_URI not found in .env")
            return False
        
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
        # Trigger connection
        client.admin.command('ping')
        check_success("MongoDB Atlas connection OK")
        client.close()
        return True
    except Exception as e:
        check_error(f"MongoDB connection failed: {str(e)}")
        return False

def check_python_packages():
    """Check if required Python packages are installed"""
    required_packages = {
        'flask': 'Flask',
        'pymongo': 'pymongo',
        'flask_cors': 'Flask-CORS',
        'flasgger': 'Flasgger',
        'dotenv': 'python-dotenv'
    }
    
    all_installed = True
    for import_name, display_name in required_packages.items():
        try:
            __import__(import_name)
            check_success(f"{display_name} installed")
        except ImportError:
            check_error(f"{display_name} NOT installed")
            all_installed = False
    
    return all_installed

def check_node_packages():
    """Check if Node packages are installed"""
    frontend_path = Path("frontend/node_modules")
    if frontend_path.exists():
        check_success("Node packages installed (node_modules exists)")
        return True
    else:
        check_warning("Node packages NOT installed (run: npm install in frontend/)")
        return False

def print_startup_instructions():
    print(f"\n{BOLD}{BLUE}📋 Next Steps:{RESET}")
    print("\n1. Start Backend (Flask):")
    print(f"   {YELLOW}cd BankAPI{RESET}")
    print(f"   {YELLOW}python app.py{RESET}")
    
    print("\n2. In another terminal, start Frontend (React):")
    print(f"   {YELLOW}cd frontend{RESET}")
    print(f"   {YELLOW}npm install  (if not done yet){RESET}")
    print(f"   {YELLOW}npm run dev{RESET}")
    
    print("\n3. Open in browser:")
    print(f"   {GREEN}http://localhost:3000{RESET}")
    
    print("\n4. Or use the quick start script:")
    print(f"   {YELLOW}.\\START_ALL.ps1{RESET}")

def main():
    print_header()
    
    all_good = True
    
    # Check Backend Files
    print_section("Backend Configuration")
    backend_files = {
        "BankAPI/app.py": "Flask app",
        "BankAPI/data_store.py": "Data store",
        "BankAPI/requirements.txt": "Requirements",
        "BankAPI/.env": "Environment config",
        "BankAPI/routes/customers.py": "Customer routes",
        "BankAPI/routes/accounts.py": "Account routes",
    }
    
    for path, name in backend_files.items():
        if not check_file_exists(path, name):
            all_good = False
    
    # Check Python packages
    print_section("Python Packages")
    if not check_python_packages():
        all_good = False
        check_warning("Run: pip install -r BankAPI/requirements.txt")
    
    # Check MongoDB
    print_section("MongoDB Atlas Connection")
    if not check_mongodb_connection():
        all_good = False
    
    # Check Frontend Files
    print_section("Frontend Configuration")
    frontend_files = {
        "frontend/package.json": "package.json",
        "frontend/vite.config.js": "Vite config",
        "frontend/index.html": "HTML template",
        "frontend/src/App.jsx": "React App",
    }
    
    for path, name in frontend_files.items():
        if not check_file_exists(path, name):
            all_good = False
    
    # Check Node packages
    print_section("Node Packages")
    check_node_packages()
    
    # Check if services are running
    print_section("Running Services (Optional)")
    print("Checking if servers are already running...")
    backend_running = check_http_endpoint("http://localhost:5000", "Backend")
    frontend_running = check_http_endpoint("http://localhost:3000", "Frontend")
    
    if backend_running:
        print(f"   {BLUE}Backend API Docs: http://localhost:5000/apidocs{RESET}")
    if frontend_running:
        print(f"   {BLUE}Frontend App: http://localhost:3000{RESET}")
    
    # Summary
    print_section("Summary")
    if all_good:
        if backend_running and frontend_running:
            check_success("Everything is ready and running!")
            print(f"\n{BOLD}Access the app at: {GREEN}http://localhost:3000{RESET}")
        else:
            check_success("Everything is configured correctly!")
            print_startup_instructions()
    else:
        check_error("Some checks failed. Please review the issues above.")
        print_startup_instructions()
    
    print("\n" + "=" * 50)
    print(f"{BLUE}Happy Banking! 🏦{RESET}\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n{RED}Error: {str(e)}{RESET}\n")
        sys.exit(1)
