"""
Demo script for demo-chatbot package.
This provides a simple entry point for running demonstrations.
"""

import os
import sys

def main():
    """Main demo function."""
    print("🚀 Starting demo-chatbot demonstration...")
    
    # Ensure we're running from the correct directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    
    # Add project root to Python path
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    try:
        # Import and run the demo
        from demo_chatbot.examples import run_demo_sync
        run_demo_sync()
        print("✅ Demo completed successfully!")
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        print(traceback.format_exc())
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())