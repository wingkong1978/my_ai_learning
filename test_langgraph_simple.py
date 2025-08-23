#!/usr/bin/env python3
"""
Simple structure test for LangGraph integration
Tests basic structure without Unicode issues
"""

import os
import sys
from pathlib import Path

def test_structure():
    """Test project structure"""
    print("Testing LangGraph Integration Structure...")
    
    # Check directory structure
    langgraph_dir = Path("chatbot/api/langgraph")
    examples_dir = Path("chatbot/examples")
    tests_dir = Path("chatbot/tests")
    
    print(f"LangGraph directory exists: {langgraph_dir.exists()}")
    print(f"Examples directory exists: {examples_dir.exists()}")
    print(f"Tests directory exists: {tests_dir.exists()}")
    
    # Check files
    files_to_check = [
        "chatbot/api/langgraph/__init__.py",
        "chatbot/api/langgraph/langgraph_client.py",
        "chatbot/api/langgraph/langgraph_workflows.py",
        "chatbot/examples/langgraph_examples.py",
        "chatbot/tests/test_langgraph_integration.py",
        "run_langgraph_demo.py",
        "LANGGRAPH_INTEGRATION.md"
    ]
    
    all_exist = True
    for file_path in files_to_check:
        exists = Path(file_path).exists()
        status = "OK" if exists else "MISSING"
        print(f"{status} {file_path}: {'exists' if exists else 'missing'}")
        if not exists:
            all_exist = False
    
    return all_exist

def test_documentation():
    """Test documentation"""
    print("\nTesting Documentation...")
    
    doc_file = Path("LANGGRAPH_INTEGRATION.md")
    if doc_file.exists():
        content = doc_file.read_text(encoding='utf-8', errors='replace')
        print(f"Documentation file exists ({len(content)} bytes)")
        
        # Check key sections
        sections = [
            "Overview",
            "Quick Start", 
            "Available Workflows",
            "Features",
            "Examples"
        ]
        
        for section in sections:
            if section in content:
                print(f"OK Contains '{section}' section")
            else:
                print(f"MISSING '{section}' section")
    else:
        print("Documentation file missing")
        return False
    
    return True

def main():
    """Run all tests"""
    print("LangGraph Integration Structure Test")
    print("=" * 50)
    
    tests = [
        ("Structure", test_structure),
        ("Documentation", test_documentation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
                print(f"OK {test_name} test passed")
            else:
                print(f"FAILED {test_name} test failed")
        except Exception as e:
            print(f"ERROR {test_name} test error: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("SUCCESS All structure tests passed!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install langchain langchain-community langgraph")
        print("2. Set API key in .env file")
        print("3. Run: python run_langgraph_demo.py")
    else:
        print("WARNING Some tests failed - check structure")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)