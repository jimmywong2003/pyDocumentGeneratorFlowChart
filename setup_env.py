#!/usr/bin/env python3
"""
Environment Setup Script for Mermaid Chart Generator
Automatically installs all required dependencies for the tool.
"""

import os
import sys
import subprocess
import platform
import argparse
from pathlib import Path

class EnvironmentSetup:
    def __init__(self):
        self.platform = platform.system().lower()
        self.is_windows = self.platform == 'windows'
        self.is_macos = self.platform == 'darwin'
        self.is_linux = self.platform.startswith('linux')
        
        # Color codes for terminal output
        self.COLORS = {
            'RED': '\033[91m',
            'GREEN': '\033[92m',
            'YELLOW': '\033[93m',
            'BLUE': '\033[94m',
            'MAGENTA': '\033[95m',
            'CYAN': '\033[96m',
            'WHITE': '\033[97m',
            'RESET': '\033[0m',
            'BOLD': '\033[1m'
        }
    
    def color_print(self, message, color='WHITE', bold=False):
        """Print colored output to terminal"""
        color_code = self.COLORS.get(color.upper(), self.COLORS['WHITE'])
        bold_code = self.COLORS['BOLD'] if bold else ''
        print(f"{bold_code}{color_code}{message}{self.COLORS['RESET']}")
    
    def run_command(self, command, description, timeout=120):
        """Run a command with error handling"""
        self.color_print(f"{description}...", 'BLUE')
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=timeout
            )
            
            if result.returncode == 0:
                self.color_print(f"✓ {description} completed successfully", 'GREEN')
                return True
            else:
                self.color_print(f"✗ {description} failed: {result.stderr}", 'RED')
                return False
                
        except subprocess.TimeoutExpired:
            self.color_print(f"✗ {description} timed out", 'RED')
            return False
        except Exception as e:
            self.color_print(f"✗ {description} error: {e}", 'RED')
            return False
    
    def check_tool_installed(self, tool_name, version_command):
        """Check if a tool is installed"""
        try:
            result = subprocess.run(
                version_command, 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            return False
    
    def install_python_dependencies(self):
        """Install Python dependencies from requirements.txt"""
        if not os.path.exists('requirements.txt'):
            self.color_print("requirements.txt not found, creating default...", 'YELLOW')
            self.create_default_requirements()
        
        return self.run_command(
            f'"{sys.executable}" -m pip install -r requirements.txt',
            "Installing Python dependencies"
        )
    
    def create_default_requirements(self):
        """Create default requirements.txt if it doesn't exist"""
        requirements = """# Mermaid Chart Generator Dependencies
# Python packages required for the tool

# Core functionality
pandas>=1.3.0
numpy>=1.21.0

# GUI dependencies (for gui_tool.py)
tkinter>=0.0.0  # Usually included with Python

# Optional: for enhanced functionality
# pillow>=8.0.0  # For image processing
# requests>=2.25.0  # For web functionality
"""
        with open('requirements.txt', 'w') as f:
            f.write(requirements)
        self.color_print("✓ Created default requirements.txt", 'GREEN')
    
    def install_nodejs(self):
        """Install Node.js if not present"""
        node_installed = self.check_tool_installed('node', ['node', '--version'])
        npm_installed = self.check_tool_installed('npm', ['npm', '--version'])
        
        if node_installed and npm_installed:
            self.color_print("✓ Node.js and npm are already installed", 'GREEN')
            return True
        
        self.color_print("Node.js installation required...", 'YELLOW')
        
        if self.is_windows:
            return self.run_command(
                "winget install OpenJS.NodeJS || choco install nodejs -y",
                "Installing Node.js via Winget/Chocolatey"
            )
        elif self.is_macos:
            return self.run_command(
                "brew install node",
                "Installing Node.js via Homebrew"
            )
        elif self.is_linux:
            return self.run_command(
                "curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - && sudo apt-get install -y nodejs",
                "Installing Node.js via NodeSource"
            )
        else:
            self.color_print("Please install Node.js manually from https://nodejs.org/", 'YELLOW')
            return False
    
    def install_mermaid_cli(self):
        """Install Mermaid CLI"""
        # Check if mmdc is already installed
        try:
            result = subprocess.run(
                ['mmdc', '--version'],
                capture_output=True, 
                text=True, 
                timeout=10
            )
            if result.returncode == 0:
                self.color_print("✓ Mermaid CLI is already installed", 'GREEN')
                return True
        except:
            pass
        
        return self.run_command(
            "npm install -g @mermaid-js/mermaid-cli",
            "Installing Mermaid CLI"
        )
    
    def install_pandoc(self):
        """Install Pandoc if not present"""
        pandoc_installed = self.check_tool_installed('pandoc', ['pandoc', '--version'])
        
        if pandoc_installed:
            self.color_print("✓ Pandoc is already installed", 'GREEN')
            return True
        
        self.color_print("Pandoc installation required...", 'YELLOW')
        
        if self.is_windows:
            return self.run_command(
                "winget install JohnMacFarlane.Pandoc || choco install pandoc -y",
                "Installing Pandoc via Winget/Chocolatey"
            )
        elif self.is_macos:
            return self.run_command(
                "brew install pandoc",
                "Installing Pandoc via Homebrew"
            )
        elif self.is_linux:
            return self.run_command(
                "sudo apt-get install -y pandoc || sudo dnf install -y pandoc",
                "Installing Pandoc via package manager"
            )
        else:
            self.color_print("Please install Pandoc manually from https://pandoc.org/installing.html", 'YELLOW')
            return False
    
    def setup_environment(self):
        """Main setup method"""
        self.color_print("=" * 60, 'CYAN', True)
        self.color_print("MERMAID CHART GENERATOR - ENVIRONMENT SETUP", 'CYAN', True)
        self.color_print("=" * 60, 'CYAN', True)
        
        success = True
        
        # Install Python dependencies
        success &= self.install_python_dependencies()
        
        # Install Node.js and npm
        success &= self.install_nodejs()
        
        # Install Mermaid CLI
        success &= self.install_mermaid_cli()
        
        # Install Pandoc
        success &= self.install_pandoc()
        
        # Summary
        self.color_print("\n" + "=" * 60, 'CYAN')
        if success:
            self.color_print("✓ Environment setup completed successfully!", 'GREEN', True)
            self.color_print("\nYou can now use the tool:", 'WHITE')
            self.color_print("  GUI: python gui_tool.py", 'CYAN')
            self.color_print("  CLI: python export_document.py your_file.md", 'CYAN')
        else:
            self.color_print("✗ Environment setup completed with errors", 'RED', True)
            self.color_print("\nPlease check the errors above and install missing components manually.", 'YELLOW')
        
        return success

def main():
    parser = argparse.ArgumentParser(description='Setup environment for Mermaid Chart Generator')
    parser.add_argument('--skip-python', action='store_true', help='Skip Python dependencies installation')
    parser.add_argument('--skip-node', action='store_true', help='Skip Node.js installation')
    parser.add_argument('--skip-mermaid', action='store_true', help='Skip Mermaid CLI installation')
    parser.add_argument('--skip-pandoc', action='store_true', help='Skip Pandoc installation')
    
    args = parser.parse_args()
    
    setup = EnvironmentSetup()
    
    # Override methods based on skip flags
    if args.skip_python:
        setup.install_python_dependencies = lambda: True
    if args.skip_node:
        setup.install_nodejs = lambda: True
    if args.skip_mermaid:
        setup.install_mermaid_cli = lambda: True
    if args.skip_pandoc:
        setup.install_pandoc = lambda: True
    
    success = setup.setup_environment()
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
