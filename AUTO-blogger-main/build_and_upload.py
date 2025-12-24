#!/usr/bin/env python3
"""
Build and Upload Script for AUTO-blogger PyPI Package

This script handles building and uploading the AUTO-blogger package to PyPI.

Copyright © 2025 AryanVBW
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, check=True):
    """Run a command and handle errors"""
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {cmd}")
        print(f"Error output: {e.stderr}")
        if check:
            sys.exit(1)
        return e

def clean_build():
    """Clean previous build artifacts"""
    print("🧹 Cleaning previous build artifacts...")
    
    # Directories to clean
    clean_dirs = ['build', 'dist', 'auto_blogger.egg-info', '*.egg-info']
    
    for dir_pattern in clean_dirs:
        if '*' in dir_pattern:
            # Handle glob patterns
            import glob
            for path in glob.glob(dir_pattern):
                if os.path.exists(path):
                    shutil.rmtree(path)
                    print(f"  Removed: {path}")
        else:
            if os.path.exists(dir_pattern):
                shutil.rmtree(dir_pattern)
                print(f"  Removed: {dir_pattern}")
    
    # Clean __pycache__ directories
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            shutil.rmtree(pycache_path)
            print(f"  Removed: {pycache_path}")

def install_build_tools():
    """Install required build tools"""
    print("🔧 Installing build tools...")
    run_command("pip install --upgrade pip setuptools wheel build twine")

def build_package():
    """Build the package"""
    print("📦 Building package...")
    
    # Build using modern build tool
    run_command("python -m build")
    
    # Also build using setup.py for compatibility
    run_command("python setup.py sdist bdist_wheel")
    
    print("✅ Package built successfully!")
    
    # List built files
    if os.path.exists('dist'):
        print("\n📁 Built files:")
        for file in os.listdir('dist'):
            file_path = os.path.join('dist', file)
            size = os.path.getsize(file_path) / 1024  # KB
            print(f"  {file} ({size:.1f} KB)")

def check_package():
    """Check the built package"""
    print("🔍 Checking package...")
    
    # Check with twine
    run_command("twine check dist/*")
    
    print("✅ Package check passed!")

def test_install():
    """Test installation in a virtual environment"""
    print("🧪 Testing package installation...")
    
    # Create test virtual environment
    test_env = "test_env"
    if os.path.exists(test_env):
        shutil.rmtree(test_env)
    
    run_command(f"python -m venv {test_env}")
    
    # Activate and install
    if sys.platform == "win32":
        pip_cmd = f"{test_env}\\Scripts\\pip"
        python_cmd = f"{test_env}\\Scripts\\python"
    else:
        pip_cmd = f"{test_env}/bin/pip"
        python_cmd = f"{test_env}/bin/python"
    
    # Install the package
    wheel_file = None
    for file in os.listdir('dist'):
        if file.endswith('.whl'):
            wheel_file = os.path.join('dist', file)
            break
    
    if wheel_file:
        run_command(f"{pip_cmd} install {wheel_file}")
        
        # Test import
        test_result = run_command(f"{python_cmd} -c 'import auto_blogger; print(auto_blogger.__version__)'")
        if test_result.returncode == 0:
            print("✅ Package installation test passed!")
        else:
            print("❌ Package installation test failed!")
            return False
    
    # Cleanup
    shutil.rmtree(test_env)
    return True

def upload_to_pypi(test=True):
    """Upload package to PyPI"""
    if test:
        print("🚀 Uploading to Test PyPI...")
        run_command("twine upload --repository testpypi dist/*")
        print("\n📝 Test installation command:")
        print("pip install --index-url https://test.pypi.org/simple/ auto-blogger")
    else:
        print("🚀 Uploading to PyPI...")
        response = input("Are you sure you want to upload to PyPI? (yes/no): ")
        if response.lower() == 'yes':
            run_command("twine upload dist/*")
            print("\n📝 Installation command:")
            print("pip install auto-blogger")
        else:
            print("Upload cancelled.")

def main():
    """Main function"""
    print("🚀 AUTO-blogger PyPI Build and Upload Script")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('setup.py') or not os.path.exists('pyproject.toml'):
        print("❌ Error: setup.py or pyproject.toml not found!")
        print("Please run this script from the AUTO-blogger root directory.")
        sys.exit(1)
    
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description='Build and upload AUTO-blogger package')
    parser.add_argument('--clean', action='store_true', help='Clean build artifacts only')
    parser.add_argument('--build', action='store_true', help='Build package only')
    parser.add_argument('--test', action='store_true', help='Test package installation')
    parser.add_argument('--upload-test', action='store_true', help='Upload to Test PyPI')
    parser.add_argument('--upload', action='store_true', help='Upload to PyPI')
    parser.add_argument('--all', action='store_true', help='Run all steps (clean, build, test)')
    
    args = parser.parse_args()
    
    try:
        if args.clean or args.all:
            clean_build()
        
        if args.build or args.all or args.upload_test or args.upload:
            install_build_tools()
            build_package()
            check_package()
        
        if args.test or args.all:
            if not test_install():
                print("❌ Package test failed!")
                sys.exit(1)
        
        if args.upload_test:
            upload_to_pypi(test=True)
        
        if args.upload:
            upload_to_pypi(test=False)
        
        if not any([args.clean, args.build, args.test, args.upload_test, args.upload, args.all]):
            print("\n📋 Usage:")
            print("  python build_and_upload.py --all          # Clean, build, and test")
            print("  python build_and_upload.py --build        # Build only")
            print("  python build_and_upload.py --test         # Test installation")
            print("  python build_and_upload.py --upload-test  # Upload to Test PyPI")
            print("  python build_and_upload.py --upload       # Upload to PyPI")
            print("  python build_and_upload.py --clean        # Clean build artifacts")
        
        print("\n✅ Script completed successfully!")
        
    except KeyboardInterrupt:
        print("\n❌ Script interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Script failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()