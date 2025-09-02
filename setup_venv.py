#!/usr/bin/env python3
"""
Virtual Environment Setup Script for Mermaid Chart Generator
Creates and configures a Python virtual environment for the project.
"""

import os
import sys
import subprocess
import platform
import venv
from pathlib import Path

class VenvSetup:
    def __init__(self):
        self.platform = platform.system().lower()
        self.venv_dir = "venv"
        self.venv_path = Path(self.venv_dir)
        
    def create_venv(self):
        """Create Python virtual environment"""
        print("Creating Python virtual environment...")
        
        if self.venv_path.exists():
            print(f"Virtual environment already exists at {self.venv_path}")
            return True
            
        try:
            # Create virtual environment
            venv.create(self.venv_dir, with_pip=True)
            print(f"✓ Virtual environment created at {self.venv_path}")
            return True
        except Exception as e:
            print(f"✗ Failed to create virtual environment: {e}")
            return False
            
    def get_venv_python(self):
        """Get path to virtual environment Python executable"""
        if self.platform == "windows":
            return self.venv_path / "Scripts" / "python.exe"
        else:
            return self.venv_path / "bin" / "python"
            
    def get_venv_pip(self):
        """Get path to virtual environment pip executable"""
        if self.platform == "windows":
            return self.venv_path / "Scripts" / "pip.exe"
        else:
            return self.venv_path / "bin" / "pip"
            
    def install_dependencies(self):
        """Install Python dependencies in virtual environment"""
        pip_path = self.get_venv_pip()
        
        if not pip_path.exists():
            print("✗ pip not found in virtual environment")
            return False
            
        print("Installing Python dependencies...")
        
        try:
            # Install requirements.txt if it exists
            if Path("requirements.txt").exists():
                result = subprocess.run(
                    [str(pip_path), "install", "-r", "requirements.txt"],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                if result.returncode == 0:
                    print("✓ Python dependencies installed successfully")
                    return True
                else:
                    print(f"✗ Failed to install dependencies: {result.stderr}")
                    return False
            else:
                print("ℹ No requirements.txt found, skipping Python dependency installation")
                return True
                
        except subprocess.TimeoutExpired:
            print("✗ Dependency installation timed out")
            return False
        except Exception as e:
            print(f"✗ Error during dependency installation: {e}")
            return False
            
    def create_activation_scripts(self):
        """Create activation scripts for convenience"""
        print("Creating activation scripts...")
        
        # Create activate.bat for Windows
        activate_bat = """@echo off
echo Activating virtual environment...
call venv\\Scripts\\activate.bat
echo Virtual environment activated!
echo.
echo To deactivate, run: deactivate
"""
        
        # Create activate.sh for Unix-like systems
        activate_sh = """#!/bin/bash
echo "Activating virtual environment..."
source venv/bin/activate
echo "Virtual environment activated!"
echo ""
echo "To deactivate, run: deactivate"
"""
        
        try:
            with open("activate.bat", "w") as f:
                f.write(activate_bat)
            print("✓ Created activate.bat for Windows")
            
            with open("activate.sh", "w") as f:
                f.write(activate_sh)
            # Make shell script executable
            os.chmod("activate.sh", 0o755)
            print("✓ Created activate.sh for Unix systems")
            
            return True
        except Exception as e:
            print(f"✗ Failed to create activation scripts: {e}")
            return False
            
    def create_venv_requirements(self):
        """Create basic requirements if none exists"""
        if not Path("requirements.txt").exists():
            print("Creating basic requirements.txt...")
            
            requirements = """# Mermaid Chart Generator - Python Dependencies
# Core dependencies for the project

# GUI dependencies (included with Python)
# tkinter

# Optional enhancements (uncomment if needed)
# pandas>=1.3.0
# numpy>=1.21.0
# pillow>=8.0.0
# requests>=2.25.0

# Development tools
# black>=22.0.0
# flake8>=4.0.0
# pytest>=7.0.0
"""
            
            try:
                with open("requirements.txt", "w") as f:
                    f.write(requirements)
                print("✓ Created requirements.txt")
                return True
            except Exception as e:
                print(f"✗ Failed to create requirements.txt: {e}")
                return False
        return True
        
    def setup_environment(self):
        """Main setup method"""
        print("=" * 60)
        print("VIRTUAL ENVIRONMENT SETUP")
        print("=" * 60)
        
        success = True
        
        # Create virtual environment
        success &= self.create_venv()
        
        # Create requirements if needed
        success &= self.create_venv_requirements()
        
        # Install dependencies
        success &= self.install_dependencies()
        
        # Create activation scripts
        success &= self.create_activation_scripts()
        
        # Summary
        print("\n" + "=" * 60)
        if success:
            print("✓ Virtual environment setup completed successfully!")
            print("\nNext steps:")
            print("1. Activate the virtual environment:")
            if self.platform == "windows":
                print("   activate.bat")
            else:
                print("   source activate.sh")
            print("2. Run the setup script to install other dependencies:")
            print("   python setup_env.py")
            print("3. Use the tool:")
            print("   python gui_tool.py")
        else:
            print("✗ Virtual environment setup completed with errors")
            
        return success

def main():
    """Main function"""
    setup = VenvSetup()
    success = setup.setup_environment()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
