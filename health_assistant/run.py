#!/usr/bin/env python3
import os
import sys
import subprocess

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import flask
        import twilio
        import requests
        import bs4
        import schedule
        import dotenv
        import gtts
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        return False

def install_dependencies():
    """Install dependencies from requirements.txt"""
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("Dependencies installed successfully!")

def setup_env_file():
    """Check if .env file exists, if not create from example"""
    if not os.path.exists(".env") and os.path.exists(".env.example"):
        print("\nNOTE: .env file not found. Creating from .env.example")
        print("Please update the .env file with your actual credentials before using messaging features.\n")
        
        with open(".env.example", "r") as example_file:
            example_content = example_file.read()
        
        with open(".env", "w") as env_file:
            env_file.write(example_content)

def create_data_directory():
    """Create data directory if it doesn't exist"""
    os.makedirs("data", exist_ok=True)
    
    # Create empty medications.json if it doesn't exist
    if not os.path.exists("data/medications.json"):
        with open("data/medications.json", "w") as f:
            f.write("[]")

def main():
    """Main function to run the application"""
    # Change to the script's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print("Starting Health Assistant...")
    
    # Check and install dependencies if needed
    if not check_dependencies():
        print("Installing missing dependencies...")
        install_dependencies()
    
    # Setup environment
    setup_env_file()
    create_data_directory()
    
    # Run the Flask application
    print("Starting web server...")
    from app import app
    app.run(host='0.0.0.0', port=12000, debug=True)

if __name__ == "__main__":
    main()