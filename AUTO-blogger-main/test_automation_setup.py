#!/usr/bin/env python3
"""
Comprehensive Automation Setup Test
Tests all components of the AUTO-blogger automation system

Copyright © 2025 AryanVBW
GitHub: https://github.com/AryanVBW
"""

import sys
import os
import platform
import subprocess
import importlib
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_status(message, status="INFO"):
    """Print a status message with color coding"""
    colors = {
        "PASS": "\033[92m✅",
        "FAIL": "\033[91m❌",
        "WARN": "\033[93m⚠️",
        "INFO": "\033[94mℹ️"
    }
    reset = "\033[0m"
    print(f"{colors.get(status, '')} {message}{reset}")

def test_system_info():
    """Test and display system information"""
    print_header("SYSTEM INFORMATION")
    
    print_status(f"Operating System: {platform.system()} {platform.release()}", "INFO")
    print_status(f"Python Version: {platform.python_version()}", "INFO")
    print_status(f"Architecture: {platform.machine()}", "INFO")
    print_status(f"Platform: {platform.platform()}", "INFO")
    
    # Check if running in virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print_status("Running in virtual environment", "PASS")
    else:
        print_status("Running in system Python", "WARN")

def test_core_dependencies():
    """Test core Python dependencies"""
    print_header("CORE DEPENDENCIES")
    
    dependencies = [
        ('requests', 'HTTP requests'),
        ('bs4', 'BeautifulSoup web scraping'),
        ('selenium', 'Web automation'),
        ('tkinter', 'GUI framework'),
        ('json', 'JSON handling'),
        ('logging', 'Logging system'),
        ('threading', 'Multi-threading'),
        ('queue', 'Thread-safe queues')
    ]
    
    for module, description in dependencies:
        try:
            importlib.import_module(module)
            print_status(f"{module}: {description}", "PASS")
        except ImportError:
            print_status(f"{module}: {description} - NOT AVAILABLE", "FAIL")

def test_optional_dependencies():
    """Test optional dependencies"""
    print_header("OPTIONAL DEPENDENCIES")
    
    optional_deps = [
        ('openai', 'OpenAI API integration'),
        ('google.generativeai', 'Google Gemini AI'),
        ('PIL', 'Image processing (Pillow)'),
        ('webdriver_manager', 'WebDriver management'),
        ('colorama', 'Terminal colors'),
        ('tqdm', 'Progress bars'),
        ('validators', 'Data validation')
    ]
    
    for module, description in optional_deps:
        try:
            importlib.import_module(module)
            print_status(f"{module}: {description}", "PASS")
        except ImportError:
            print_status(f"{module}: {description} - NOT AVAILABLE", "WARN")

def test_project_structure():
    """Test project file structure"""
    print_header("PROJECT STRUCTURE")
    
    project_root = Path(__file__).parent
    
    required_files = [
        'gui_blogger.py',
        'automation_engine.py',
        'autoblog_launcher.py',
        'requirements.txt',
        'install.sh',
        'AUTO Blogger.command'
    ]
    
    required_dirs = [
        'configs',
        'scripts',
        'scripts/installation',
        'scripts/launchers',
        'docs',
        'website'
    ]
    
    # Check required files
    for file_path in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            print_status(f"File: {file_path}", "PASS")
        else:
            print_status(f"File: {file_path} - MISSING", "FAIL")
    
    # Check required directories
    for dir_path in required_dirs:
        full_path = project_root / dir_path
        if full_path.exists() and full_path.is_dir():
            print_status(f"Directory: {dir_path}", "PASS")
        else:
            print_status(f"Directory: {dir_path} - MISSING", "FAIL")

def test_configuration_files():
    """Test configuration files"""
    print_header("CONFIGURATION FILES")
    
    project_root = Path(__file__).parent
    configs_dir = project_root / 'configs'
    
    config_files = [
        'default.json',
        'category_keywords.json',
        'internal_links.json',
        'external_links.json',
        'static_clubs.json',
        'tag_synonyms.json',
        'stop_words.json',
        'do_follow_urls.json',
        'style_prompt.json',
        'gemini_prompts.json',
        'custom_seo_keywords.json'
    ]
    
    for config_file in config_files:
        config_path = configs_dir / config_file
        if config_path.exists():
            try:
                import json
                with open(config_path, 'r', encoding='utf-8') as f:
                    json.load(f)
                print_status(f"Config: {config_file}", "PASS")
            except json.JSONDecodeError:
                print_status(f"Config: {config_file} - INVALID JSON", "FAIL")
        else:
            print_status(f"Config: {config_file} - MISSING", "WARN")

def test_launcher_scripts():
    """Test launcher scripts"""
    print_header("LAUNCHER SCRIPTS")
    
    project_root = Path(__file__).parent
    
    launchers = [
        ('install.sh', 'Main installation script'),
        ('scripts/installation/install_auto_blogger.sh', 'Unix installation'),
        ('scripts/installation/install_autoblog.ps1', 'Windows PowerShell installation'),
        ('scripts/launchers/launch_auto_blogger_mac.sh', 'macOS launcher'),
        ('scripts/launchers/start_blogger.sh', 'Unix launcher'),
        ('scripts/launchers/start_blogger.bat', 'Windows launcher'),
        ('AUTO Blogger.command', 'macOS command file')
    ]
    
    for script_path, description in launchers:
        full_path = project_root / script_path
        if full_path.exists():
            # Check if script is executable (Unix-like systems)
            if script_path.endswith(('.sh', '.command')):
                if os.access(full_path, os.X_OK):
                    print_status(f"{description}: {script_path}", "PASS")
                else:
                    print_status(f"{description}: {script_path} - NOT EXECUTABLE", "WARN")
            else:
                print_status(f"{description}: {script_path}", "PASS")
        else:
            print_status(f"{description}: {script_path} - MISSING", "FAIL")

def test_automation_modules():
    """Test automation modules can be imported"""
    print_header("AUTOMATION MODULES")
    
    modules = [
        ('gui_blogger', 'Main GUI application'),
        ('automation_engine', 'Core automation engine'),
        ('autoblog_launcher', 'Application launcher')
    ]
    
    for module_name, description in modules:
        try:
            module = importlib.import_module(module_name)
            print_status(f"{description}: {module_name}", "PASS")
            
            # Additional checks for specific modules
            if module_name == 'automation_engine':
                if hasattr(module, 'SELENIUM_AVAILABLE'):
                    selenium_status = "AVAILABLE" if module.SELENIUM_AVAILABLE else "NOT AVAILABLE"
                    status = "PASS" if module.SELENIUM_AVAILABLE else "WARN"
                    print_status(f"  Selenium WebDriver: {selenium_status}", status)
                    
        except ImportError as e:
            print_status(f"{description}: {module_name} - IMPORT ERROR: {e}", "FAIL")
        except Exception as e:
            print_status(f"{description}: {module_name} - ERROR: {e}", "FAIL")

def test_virtual_environment():
    """Test virtual environment setup"""
    print_header("VIRTUAL ENVIRONMENT")
    
    project_root = Path(__file__).parent
    
    # Look for virtual environment directories
    venv_patterns = ['auto_blogger_venv_*', 'venv', '.venv', 'env']
    found_venvs = []
    
    for pattern in venv_patterns:
        found_venvs.extend(project_root.glob(pattern))
    
    if found_venvs:
        for venv_path in found_venvs:
            if venv_path.is_dir():
                # Check for activation script
                activate_script = venv_path / 'bin' / 'activate'
                if not activate_script.exists():
                    activate_script = venv_path / 'Scripts' / 'activate.bat'  # Windows
                
                if activate_script.exists():
                    print_status(f"Virtual environment found: {venv_path.name}", "PASS")
                else:
                    print_status(f"Invalid virtual environment: {venv_path.name}", "WARN")
    else:
        print_status("No virtual environment found", "WARN")
        print_status("Consider running the installer to create one", "INFO")

def test_git_repository():
    """Test Git repository status"""
    print_header("GIT REPOSITORY")
    
    project_root = Path(__file__).parent
    git_dir = project_root / '.git'
    
    if git_dir.exists():
        print_status("Git repository detected", "PASS")
        
        # Check if git command is available
        try:
            result = subprocess.run(['git', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print_status(f"Git version: {result.stdout.strip()}", "PASS")
                
                # Check repository status
                try:
                    result = subprocess.run(['git', 'status', '--porcelain'], 
                                          capture_output=True, text=True, cwd=project_root)
                    if result.returncode == 0:
                        if result.stdout.strip():
                            print_status("Repository has uncommitted changes", "WARN")
                        else:
                            print_status("Repository is clean", "PASS")
                except subprocess.CalledProcessError:
                    print_status("Could not check repository status", "WARN")
            else:
                print_status("Git command failed", "FAIL")
        except FileNotFoundError:
            print_status("Git command not found", "FAIL")
    else:
        print_status("Not a Git repository", "WARN")

def run_comprehensive_test():
    """Run all tests"""
    print("\n" + "="*60)
    print("  AUTO-BLOGGER AUTOMATION SETUP TEST")
    print("  Copyright © 2025 AryanVBW")
    print("="*60)
    
    test_functions = [
        test_system_info,
        test_core_dependencies,
        test_optional_dependencies,
        test_project_structure,
        test_configuration_files,
        test_launcher_scripts,
        test_automation_modules,
        test_virtual_environment,
        test_git_repository
    ]
    
    for test_func in test_functions:
        try:
            test_func()
        except Exception as e:
            print_status(f"Test {test_func.__name__} failed: {e}", "FAIL")
    
    print_header("TEST SUMMARY")
    print_status("Comprehensive automation setup test completed", "INFO")
    print_status("Review the results above for any issues", "INFO")
    print_status("For support, visit: https://github.com/AryanVBW/AUTO-blogger", "INFO")

if __name__ == "__main__":
    run_comprehensive_test()