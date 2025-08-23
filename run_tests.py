#!/usr/bin/env python3
"""
Enhanced test runner for the demo chatbot project.

This script provides easy test execution with options for different test suites.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_tests(test_type="all", verbose=False, coverage=False):
    """Run the specified test suite."""
    
    # Ensure we're in the project root
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Base pytest command
    cmd = ["python", "-m", "pytest"]
    
    if verbose:
        cmd.append("-v")
    
    if coverage:
        cmd.extend(["--cov=src/demo_chatbot", "--cov-report=html", "--cov-report=term"])
    
    # Add test selection based on type
    if test_type == "agents":
        cmd.append("tests/test_enhanced_agents.py")
    elif test_type == "config":
        cmd.append("tests/test_enhanced_config.py")
    elif test_type == "servers":
        cmd.append("tests/test_enhanced_servers.py")
    elif test_type == "original":
        cmd.extend(["tests/test_agents.py", "tests/test_config.py", "tests/test_servers.py"])
    elif test_type == "enhanced":
        cmd.extend([
            "tests/test_enhanced_agents.py",
            "tests/test_enhanced_config.py", 
            "tests/test_enhanced_servers.py"
        ])
    else:  # all
        cmd.append("tests/")
    
    print(f"Running command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n✅ Tests completed successfully!")
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Tests failed with return code: {e.returncode}")
        return e.returncode
    except FileNotFoundError:
        print("❌ pytest not found. Please install it with: pip install pytest")
        return 1


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Run tests for demo chatbot")
    parser.add_argument(
        "test_type",
        nargs="?",
        default="all",
        choices=["all", "agents", "config", "servers", "original", "enhanced"],
        help="Type of tests to run"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Run tests in verbose mode"
    )
    parser.add_argument(
        "--coverage", "-c",
        action="store_true",
        help="Run tests with coverage reporting"
    )
    
    args = parser.parse_args()
    
    print("🧪 Demo Chatbot Test Runner")
    print("=" * 40)
    print(f"Test type: {args.test_type}")
    print(f"Verbose: {args.verbose}")
    print(f"Coverage: {args.coverage}")
    print("=" * 40)
    
    return run_tests(args.test_type, args.verbose, args.coverage)


if __name__ == "__main__":
    sys.exit(main())