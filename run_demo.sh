#!/bin/bash
# Cross-platform Demo Launcher for Unix/Linux/macOS
# Usage: ./run_demo.sh [option]

set -e

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_menu() {
    echo -e "${GREEN}=== Demo Chatbot - Script Launcher ===${NC}"
    echo "1. Run Demo Agent (Interactive)"
    echo "2. Run MCP Server"
    echo "3. Test Demo Agent"
    echo "4. Test MCP Server"
    echo "5. Run Master Menu"
    echo "6. Exit"
    echo "============================="
}

run_script() {
    local script_name=$1
    local description=$2
    echo -e "${YELLOW}${description}...${NC}"
    cd "$SCRIPT_DIR"
    python3 "$script_name"
}

run_python() {
    local script_path=$1
    local description=$2
    echo -e "${YELLOW}${description}...${NC}"
    python3 "$script_path"
}

main() {
    # Check if Python is available
    if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
        echo -e "${RED}Error: Python is not installed or not in PATH${NC}"
        exit 1
    fi

    # Use python3 if available, otherwise python
    if command -v python3 &> /dev/null; then
        alias python=python3
    fi

    if [[ $# -eq 0 ]]; then
        # Interactive mode
        while true; do
            print_menu
            read -p "Select option (1-6): " choice
            
            case $choice in
                1)
                    run_script "demo_agent.py" "Starting Demo Agent"
                    break
                    ;;
                2)
                    run_script "mcp_server.py" "Starting MCP Server"
                    break
                    ;;
                3)
                    run_script "test_agent.py" "Testing Demo Agent"
                    break
                    ;;
                4)
                    run_script "test_mcp.py" "Testing MCP Server"
                    break
                    ;;
                5)
                    run_script "run_demo.py" "Starting Master Menu"
                    break
                    ;;
                6)
                    echo "Goodbye!"
                    exit 0
                    ;;
                *)
                    echo -e "${RED}Invalid choice. Please select 1-6.${NC}"
                    ;;
            esac
        done
    else
        # Command line mode
        case $1 in
            1|agent)
                run_script "demo_agent.py" "Starting Demo Agent"
                ;;
            2|mcp)
                run_script "mcp_server.py" "Starting MCP Server"
                ;;
            3|test-agent)
                run_script "test_agent.py" "Testing Demo Agent"
                ;;
            4|test-mcp)
                run_script "test_mcp.py" "Testing MCP Server"
                ;;
            5|menu)
                run_script "run_demo.py" "Starting Master Menu"
                ;;
            help|-h|--help)
                echo "Usage: $0 [option]"
                echo "Options:"
                echo "  1, agent      - Run Demo Agent"
                echo "  2, mcp       - Run MCP Server"
                echo "  3, test-agent - Test Demo Agent"
                echo "  4, test-mcp   - Test MCP Server"
                echo "  5, menu      - Run Master Menu"
                echo "  help         - Show this help"
                ;;
            *)
                echo -e "${RED}Invalid option: $1${NC}"
                echo "Use '$0 help' for usage information"
                exit 1
                ;;
        esac
    fi
}

# Make script executable
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi