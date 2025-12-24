#!/bin/bash

# AUTO-blogger PyPI Build Script
# Copyright © 2025 AryanVBW

set -e  # Exit on any error

echo "🚀 AUTO-blogger PyPI Build Script"
echo "==================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [[ ! -f "setup.py" ]] || [[ ! -f "pyproject.toml" ]]; then
    print_error "setup.py or pyproject.toml not found!"
    print_error "Please run this script from the AUTO-blogger root directory."
    exit 1
fi

print_status "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed or not in PATH"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
print_success "Python $PYTHON_VERSION found"

# Function to install build tools
install_build_tools() {
    print_status "Installing build tools..."
    
    if python3 -m pip install --upgrade pip setuptools wheel build twine; then
        print_success "Build tools installed successfully"
    else
        print_warning "Failed to install build tools with python3 -m pip"
        print_status "Trying with pip3..."
        
        if pip3 install --upgrade pip setuptools wheel build twine; then
            print_success "Build tools installed successfully with pip3"
        else
            print_error "Failed to install build tools"
            print_error "Please install manually: pip3 install --upgrade pip setuptools wheel build twine"
            exit 1
        fi
    fi
}

# Function to clean previous builds
clean_build() {
    print_status "Cleaning previous build artifacts..."
    
    # Remove build directories
    rm -rf build/ dist/ *.egg-info/ auto_blogger.egg-info/
    
    # Remove __pycache__ directories
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    
    # Remove .pyc files
    find . -name "*.pyc" -delete 2>/dev/null || true
    
    print_success "Build artifacts cleaned"
}

# Function to test package structure
test_package() {
    print_status "Testing package structure..."
    
    if python3 test_package.py; then
        print_success "Package structure test passed"
    else
        print_warning "Package structure test had some issues, but continuing..."
    fi
}

# Function to build package
build_package() {
    print_status "Building package..."
    
    # Try modern build method first
    if python3 -m build; then
        print_success "Package built successfully with 'python -m build'"
    else
        print_warning "Modern build failed, trying legacy method..."
        
        # Fallback to setup.py
        if python3 setup.py sdist bdist_wheel; then
            print_success "Package built successfully with setup.py"
        else
            print_error "Both build methods failed"
            exit 1
        fi
    fi
    
    # List built files
    if [[ -d "dist" ]]; then
        print_status "Built files:"
        ls -la dist/
    fi
}

# Function to check package
check_package() {
    print_status "Checking package with twine..."
    
    if twine check dist/*; then
        print_success "Package check passed"
    else
        print_error "Package check failed"
        exit 1
    fi
}

# Function to show upload instructions
show_upload_instructions() {
    echo ""
    print_success "Package built successfully!"
    echo ""
    print_status "Next steps:"
    echo ""
    echo "1. Test upload to Test PyPI:"
    echo "   twine upload --repository testpypi dist/*"
    echo ""
    echo "2. Test installation from Test PyPI:"
    echo "   pip install --index-url https://test.pypi.org/simple/ auto-blogger"
    echo ""
    echo "3. Upload to production PyPI:"
    echo "   twine upload dist/*"
    echo ""
    echo "4. Test final installation:"
    echo "   pip install auto-blogger"
    echo "   autoblog --help"
    echo ""
    print_status "Make sure you have configured your PyPI credentials in ~/.pypirc"
    echo ""
}

# Main execution
main() {
    case "${1:-build}" in
        "clean")
            clean_build
            ;;
        "install-tools")
            install_build_tools
            ;;
        "test")
            test_package
            ;;
        "build")
            install_build_tools
            clean_build
            test_package
            build_package
            check_package
            show_upload_instructions
            ;;
        "upload-test")
            print_status "Uploading to Test PyPI..."
            twine upload --repository testpypi dist/*
            ;;
        "upload")
            print_status "Uploading to PyPI..."
            read -p "Are you sure you want to upload to PyPI? (yes/no): " confirm
            if [[ $confirm == "yes" ]]; then
                twine upload dist/*
                print_success "Package uploaded to PyPI!"
                echo "Install with: pip install auto-blogger"
            else
                print_status "Upload cancelled"
            fi
            ;;
        "help")
            echo "Usage: $0 [command]"
            echo ""
            echo "Commands:"
            echo "  build         - Full build process (default)"
            echo "  clean         - Clean build artifacts"
            echo "  install-tools - Install build tools"
            echo "  test          - Test package structure"
            echo "  upload-test   - Upload to Test PyPI"
            echo "  upload        - Upload to PyPI"
            echo "  help          - Show this help"
            echo ""
            ;;
        *)
            print_error "Unknown command: $1"
            echo "Use '$0 help' for usage information"
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"