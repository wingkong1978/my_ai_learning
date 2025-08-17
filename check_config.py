#!/usr/bin/env python3
"""
Configuration checker for demo-chatbot.
"""
import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from chatbot.config.settings import Config
    Config.validate()
    print("[INFO] API key validated successfully")
    exit(0)
except ValueError as e:
    print(f"[ERROR] {e}")
    exit(1)
except Exception as e:
    print(f"[ERROR] Configuration check failed: {e}")
    exit(1)