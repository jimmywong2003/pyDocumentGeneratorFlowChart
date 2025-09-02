#!/usr/bin/env python3
"""
Windows Executable Build Script
Builds standalone Windows executable using PyInstaller
"""

import os
import subprocess
import sys
import shutil
from pathlib import Path

def run_command(cmd, description):
    """Run a command with error handling"""
    print(f"⏳ {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} error: {e}")
        return False

def clean_build_dirs():
    """Clean up build directories"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🧹 Cleaned {dir_name}/")

def build_gui_executable():
    """Build GUI executable"""
    print("\n" + "="*60)
    print("BUILDING GUI EXECUTABLE")
    print("="*60)
    
    # Build GUI executable
    cmd = (
        'python -m PyInstaller '
        '--name="Mermaid Chart Generator" '
        '--windowed '
        '--icon=NONE '
        '--add-data="LICENSE;." '
        '--add-data="README.md;." '
        '--add-data="user_guideline.md;." '
        '--add-data="requirements.txt;." '
        'gui_tool.py'
    )
    
    return run_command(cmd, "Building GUI executable")

def build_cli_executables():
    """Build CLI executables"""
    print("\n" + "="*60)
    print("BUILDING CLI EXECUTABLES")
    print("="*60)
    
    # Build export_document.py executable
    cmd1 = (
        'python -m PyInstaller '
        '--name="mermaid-export" '
        '--console '
        '--add-data="LICENSE;." '
        'export_document.py'
    )
    
    # Build export_flowcharts_only.py executable
    cmd2 = (
        'python -m PyInstaller '
        '--name="mermaid-charts" '
        '--console '
        '--add-data="LICENSE;." '
        'export_flowcharts_only.py'
    )
    
    # Build setup_env.py executable
    cmd3 = (
        'python -m PyInstaller '
        '--name="mermaid-setup" '
        '--console '
        '--add-data="LICENSE;." '
        'setup_env.py'
    )
    
    success = True
    success &= run_command(cmd1, "Building mermaid-export executable")
    success &= run_command(cmd2, "Building mermaid-charts executable") 
    success &= run_command(cmd3, "Building mermaid-setup executable")
    
    return success

def create_installer_package():
    """Create installer package with all executables"""
    print("\n" + "="*60)
    print("CREATING INSTALLER PACKAGE")
    print("="*60)
    
    # Create package directory
    package_dir = "MermaidChartGenerator_Windows"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    os.makedirs(package_dir)
    
    # Copy executables
    files_to_copy = [
        ("dist/Mermaid Chart Generator/Mermaid Chart Generator.exe", "Mermaid Chart Generator.exe"),
        ("dist/mermaid-export/mermaid-export.exe", "mermaid-export.exe"),
        ("dist/mermaid-charts/mermaid-charts.exe", "mermaid-charts.exe"),
        ("dist/mermaid-setup/mermaid-setup.exe", "mermaid-setup.exe"),
    ]
    
    for src, dst in files_to_copy:
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(package_dir, dst))
            print(f"📦 Copied {dst}")
        else:
            print(f"⚠️  File not found: {src}")
    
    # Copy documentation
    docs_to_copy = ["LICENSE", "README.md", "user_guideline.md"]
    for doc in docs_to_copy:
        if os.path.exists(doc):
            shutil.copy2(doc, os.path.join(package_dir, doc))
            print(f"📄 Copied {doc}")
    
    print(f"\n✅ Package created in: {package_dir}/")
    return True

def main():
    """Main build function"""
    print("Mermaid Chart Generator - Windows Build Script")
    print("="*50)
    
    # Clean previous builds
    clean_build_dirs()
    
    # Build executables
    success = True
    success &= build_gui_executable()
    success &= build_cli_executables()
    
    if success:
        # Create installer package
        create_installer_package()
        
        print("\n" + "="*60)
        print("🎉 BUILD COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("Files created:")
        print("- Mermaid Chart Generator.exe (GUI application)")
        print("- mermaid-export.exe (CLI document export)")
        print("- mermaid-charts.exe (CLI chart export)")
        print("- mermaid-setup.exe (Environment setup)")
        print("\nThe packaged files are in: MermaidChartGenerator_Windows/")
    else:
        print("\n" + "="*60)
        print("❌ BUILD FAILED!")
        print("="*60)
        print("Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
