#!/usr/bin/env python3
"""
Simple test script to verify package structure and build readiness
"""

import os
import sys
import subprocess

def test_package_structure():
    """Test if package structure is correct"""
    print("🔍 Testing package structure...")
    
    # Check required files
    required_files = [
        'setup.py',
        'pyproject.toml', 
        'MANIFEST.in',
        'README.md',
        'requirements.txt',
        'auto_blogger/__init__.py',
        'auto_blogger/gui_blogger.py',
        'auto_blogger/automation_engine.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"  ✅ {file}")
    
    if missing_files:
        print(f"  ❌ Missing files: {missing_files}")
        return False
    
    return True

def test_package_import():
    """Test if package can be imported"""
    print("\n🐍 Testing package import...")
    
    try:
        # Add current directory to path
        sys.path.insert(0, '.')
        
        # Try to import the package
        import auto_blogger
        print(f"  ✅ Package imported successfully")
        print(f"  ✅ Version: {auto_blogger.__version__}")
        print(f"  ✅ Author: {auto_blogger.__author__}")
        
        return True
    except Exception as e:
        print(f"  ❌ Import failed: {e}")
        return False

def test_setup_py():
    """Test if setup.py is valid"""
    print("\n📦 Testing setup.py...")
    
    try:
        # Test setup.py syntax
        result = subprocess.run(
            [sys.executable, 'setup.py', '--help-commands'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("  ✅ setup.py is valid")
            return True
        else:
            print(f"  ❌ setup.py error: {result.stderr}")
            return False
    except Exception as e:
        print(f"  ❌ setup.py test failed: {e}")
        return False

def test_pyproject_toml():
    """Test if pyproject.toml is valid"""
    print("\n⚙️ Testing pyproject.toml...")
    
    try:
        import tomllib
    except ImportError:
        try:
            import tomli as tomllib
        except ImportError:
            print("  ⚠️ Cannot test pyproject.toml (tomllib/tomli not available)")
            return True
    
    try:
        with open('pyproject.toml', 'rb') as f:
            data = tomllib.load(f)
        
        # Check required sections
        required_sections = ['build-system', 'project']
        for section in required_sections:
            if section in data:
                print(f"  ✅ {section} section found")
            else:
                print(f"  ❌ {section} section missing")
                return False
        
        return True
    except Exception as e:
        print(f"  ❌ pyproject.toml error: {e}")
        return False

def create_build_instructions():
    """Create build instructions"""
    print("\n📋 Build Instructions:")
    print("=" * 50)
    
    instructions = """
1. Install build tools:
   pip install --upgrade pip setuptools wheel build twine

2. Clean previous builds:
   rm -rf build/ dist/ *.egg-info/

3. Build package:
   python -m build
   # OR
   python setup.py sdist bdist_wheel

4. Check package:
   twine check dist/*

5. Test install (optional):
   pip install dist/auto_blogger-1.0.0-py3-none-any.whl

6. Upload to Test PyPI:
   twine upload --repository testpypi dist/*

7. Test from Test PyPI:
   pip install --index-url https://test.pypi.org/simple/ auto-blogger

8. Upload to PyPI:
   twine upload dist/*

9. Install from PyPI:
   pip install auto-blogger

10. Test installation:
    autoblog --help
    auto-blogger --help
    python -c "import auto_blogger; auto_blogger.main()"
"""
    
    print(instructions)

def main():
    """Main test function"""
    print("🚀 AUTO-blogger Package Test")
    print("=" * 40)
    
    tests = [
        test_package_structure,
        test_package_import,
        test_setup_py,
        test_pyproject_toml
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("\n✅ All tests passed! Package is ready for PyPI.")
        create_build_instructions()
        return True
    else:
        print("\n❌ Some tests failed. Please fix issues before publishing.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)