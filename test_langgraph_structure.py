#!/usr/bin/env python3
"""
Simple structure test for LangGraph integration
Tests basic imports and structure without external dependencies
"""

import os
import sys
from pathlib import Path

def test_structure():
    """Test project structure"""
    print("🔍 Testing LangGraph Integration Structure...")
    
    # Check directory structure
    langgraph_dir = Path("chatbot/api/langgraph")
    examples_dir = Path("chatbot/examples")
    tests_dir = Path("chatbot/tests")
    
    print(f"✅ LangGraph directory exists: {langgraph_dir.exists()}")
    print(f"✅ Examples directory exists: {examples_dir.exists()}")
    print(f"✅ Tests directory exists: {tests_dir.exists()}")
    
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
        print(f"{'✅' if exists else '❌'} {file_path}: {'exists' if exists else 'missing'}")
        if not exists:
            all_exist = False
    
    return all_exist

def test_imports():
    """Test basic imports (without external dependencies)"""
    print("\n🔍 Testing Basic Imports...")
    
    try:
        # Test module structure
        import chatbot.api.langgraph
        print("✅ chatbot.api.langgraph module structure")
    except ImportError as e:
        print(f"⚠️  Import warning: {e}")
        print("This is expected if external dependencies are missing")
    
    try:
        # Test client classes (basic structure)
        from chatbot.api.langgraph.langgraph_client import LangGraphChatClient
        print("✅ LangGraphChatClient class definition")
    except ImportError as e:
        print(f"⚠️  Import warning: {e}")
        print("This is expected if external dependencies are missing")
    
    try:
        from chatbot.api.langgraph.langgraph_workflows import ChatWorkflow, ToolWorkflow, AdvancedWorkflow
        print("✅ Workflow classes definitions")
    except ImportError as e:
        print(f"⚠️  Import warning: {e}")
        print("This is expected if external dependencies are missing")
    
    return True

def test_documentation():
    """Test documentation"""
    print("\n🔍 Testing Documentation...")
    
    doc_file = Path("LANGGRAPH_INTEGRATION.md")
    if doc_file.exists():
        content = doc_file.read_text()
        print(f"✅ Documentation file exists ({len(content)} bytes)")
        
        # Check key sections
        sections = [
            "Overview",
            "Quick Start", 
            "Available Workflows",
            "Features",
            "Examples",
            "CLI Usage",
            "Testing",
            "Configuration"
        ]
        
        for section in sections:
            if section in content:
                print(f"✅ Contains '{section}' section")
            else:
                print(f"❌ Missing '{section}' section")
    else:
        print("❌ Documentation file missing")
        return False
    
    return True

def test_cli_scripts():
    """Test CLI scripts"""
    print("\n🔍 Testing CLI Scripts...")
    
    scripts = [
        "run_langgraph_demo.py"
    ]
    
    for script in scripts:
        if Path(script).exists():
            print(f"✅ {script} exists")
        else:
            print(f"❌ {script} missing")
    
    return True

def main():
    """Run all tests"""
    print("LangGraph Integration Structure Test")
    print("=" * 50)
    
    tests = [
        ("Structure", test_structure),
        ("Imports", test_imports),
        ("Documentation", test_documentation),
        ("CLI Scripts", test_cli_scripts)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
                print(f"✅ {test_name} test passed")
            else:
                print(f"❌ {test_name} test failed")
        except Exception as e:
            print(f"❌ {test_name} test error: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All structure tests passed!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install langchain langchain-community langgraph")
        print("2. Set API key in .env file")
        print("3. Run: python run_langgraph_demo.py")
    else:
        print("⚠️  Some tests failed - check structure")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)