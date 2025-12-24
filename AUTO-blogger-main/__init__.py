#!/usr/bin/env python3
"""
AUTO-blogger - AI-Powered WordPress Automation Tool

A comprehensive WordPress automation tool that combines AI content generation,
Getty Images integration, and comprehensive SEO optimization.

Copyright © 2025 AryanVBW
GitHub: https://github.com/AryanVBW/AUTO-blogger
"""

__version__ = "1.0.0"
__author__ = "AryanVBW"
__email__ = "AryanVBW@gmail.com"
__description__ = "Automated WordPress Blog Posting Tool with AI Integration"
__url__ = "https://github.com/AryanVBW/AUTO-blogger"

# Import main components for easy access
try:
    from .gui_blogger import BlogAutomationGUI, main
    from .automation_engine import BlogAutomationEngine
except ImportError:
    # Handle relative imports when package is not installed
    pass

# Package metadata
__all__ = [
    "BlogAutomationGUI",
    "BlogAutomationEngine", 
    "main",
    "__version__",
    "__author__",
    "__email__",
    "__description__",
    "__url__"
]