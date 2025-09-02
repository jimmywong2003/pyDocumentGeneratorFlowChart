#!/usr/bin/env python3
"""
Document Export Script
Exports Markdown files to DOCX format and converts Mermaid flowcharts to PNG images.
"""

import os
import re
import sys
import subprocess
import platform
import argparse
from pathlib import Path

class DocumentExporter:
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
    
    def check_tool_installed(self, tool_name):
        """Check if a tool is installed and available in PATH"""
        try:
            if tool_name == 'pandoc':
                result = subprocess.run(['pandoc', '--version'], 
                                      capture_output=True, text=True, timeout=10)
                return result.returncode == 0
            elif tool_name == 'mermaid':
                # Check if mmdc is available in PATH
                result = subprocess.run(['mmdc', '--version'], 
                                      capture_output=True, text=True, timeout=10)
                return result.returncode == 0
            elif tool_name == 'npm':
                result = subprocess.run(['npm', '--version'], 
                                      capture_output=True, text=True, timeout=10)
                return result.returncode == 0
            elif tool_name == 'choco':
                result = subprocess.run(['choco', '--version'], 
                                      capture_output=True, text=True, timeout=10)
                return result.returncode == 0
            elif tool_name == 'winget':
                result = subprocess.run(['winget', '--version'], 
                                      capture_output=True, text=True, timeout=10)
                return result.returncode == 0
            elif tool_name == 'brew':
                result = subprocess.run(['brew', '--version'], 
                                      capture_output=True, text=True, timeout=10)
                return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            return False
        return False
    
    def get_installation_options(self, tool_name):
        """Get platform-specific installation options with executable commands"""
        options = []
        
        if tool_name == 'pandoc':
            if self.is_windows:
                options.extend([
                    {"name": "Chocolatey", "command": "choco install pandoc -y", "available": self.check_tool_installed('choco')},
                    {"name": "Winget", "command": "winget install JohnMacFarlane.Pandoc", "available": self.check_tool_installed('winget')},
                    {"name": "Manual download", "command": None, "instructions": "Visit: https://pandoc.org/installing.html#windows"}
                ])
            elif self.is_macos:
                options.extend([
                    {"name": "Homebrew", "command": "brew install pandoc", "available": self.check_tool_installed('brew')},
                    {"name": "Manual download", "command": None, "instructions": "Visit: https://pandoc.org/installing.html#macos"}
                ])
            elif self.is_linux:
                options.extend([
                    {"name": "APT (Ubuntu/Debian)", "command": "sudo apt-get install -y pandoc", "available": True},
                    {"name": "DNF (Fedora/RHEL)", "command": "sudo dnf install -y pandoc", "available": True},
                    {"name": "Manual download", "command": None, "instructions": "Visit: https://pandoc.org/installing.html#linux"}
                ])
        
        elif tool_name == 'mermaid':
            if self.is_windows:
                options.extend([
                    {"name": "npm install (requires Node.js)", "command": "npm install -g @mermaid-js/mermaid-cli", "available": self.check_tool_installed('npm')},
                    {"name": "Chocolatey", "command": "choco install mermaid -y", "available": self.check_tool_installed('choco')},
                    {"name": "Manual installation", "command": None, "instructions": "1. Install Node.js from https://nodejs.org/\n2. Run: npm install -g @mermaid-js/mermaid-cli"}
                ])
            else:
                options.extend([
                    {"name": "npm install", "command": "npm install -g @mermaid-js/mermaid-cli", "available": self.check_tool_installed('npm')},
                    {"name": "Manual installation", "command": None, "instructions": "1. Install Node.js from https://nodejs.org/\n2. Run: npm install -g @mermaid-js/mermaid-cli"}
                ])
        
        return options
    
    def prompt_yes_no(self, question):
        """Prompt user with a yes/no question"""
        while True:
            response = input(f"{question} (y/n): ").strip().lower()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            print("Please answer 'y' or 'n'")
    
    def prompt_option_selection(self, question, options):
        """Prompt user to select from numbered options"""
        print(f"\n{question}")
        for i, option in enumerate(options, 1):
            status = "✓" if option.get('available', True) else "✗ (not available)"
            print(f"{i}. {option['name']} {status}")
        
        while True:
            try:
                choice = input(f"\nEnter choice [1-{len(options)}]: ").strip()
                if not choice:
                    continue
                choice_num = int(choice)
                if 1 <= choice_num <= len(options):
                    return choice_num - 1  # Return index
                print(f"Please enter a number between 1 and {len(options)}")
            except ValueError:
                print("Please enter a valid number")
    
    def install_tool_interactive(self, tool_name):
        """Interactive tool installation with multiple options"""
        self.color_print(f"\n{tool_name.upper()} is not installed.", 'YELLOW', True)
        
        options = self.get_installation_options(tool_name)
        
        # Add skip option
        options.append({"name": "Skip installation", "command": None, "instructions": None})
        
        selected_index = self.prompt_option_selection(
            f"Choose installation method for {tool_name}:", options
        )
        
        selected_option = options[selected_index]
        
        if selected_option['name'] == "Skip installation":
            self.color_print(f"Skipping {tool_name} installation.", 'YELLOW')
            return True  # Continue without the tool
        
        if selected_option['command']:
            # Try to execute the command
            self.color_print(f"Attempting to install using: {selected_option['command']}", 'BLUE')
            try:
                result = subprocess.run(
                    selected_option['command'], 
                    shell=True, 
                    capture_output=True, 
                    text=True, 
                    timeout=120
                )
                
                if result.returncode == 0:
                    self.color_print(f"✓ Successfully installed {tool_name}", 'GREEN')
                    return True  # Installation successful
                else:
                    self.color_print(f"✗ Installation failed: {result.stderr}", 'RED')
                    self.color_print("Please try another installation method.", 'YELLOW')
                    return self.install_tool_interactive(tool_name)  # Retry
                    
            except subprocess.TimeoutExpired:
                self.color_print("✗ Installation timed out", 'RED')
                return False
            except Exception as e:
                self.color_print(f"✗ Installation error: {e}", 'RED')
                return False
        else:
            # Show manual instructions
            self.color_print("Manual installation instructions:", 'CYAN')
            self.color_print(selected_option['instructions'], 'WHITE')
            
            if self.prompt_yes_no("Would you like to try another installation method?"):
                return self.install_tool_interactive(tool_name)  # Retry
            else:
                self.color_print(f"Please install {tool_name} manually and run this script again.", 'YELLOW')
                return False
    
    def extract_mermaid_blocks(self, markdown_content):
        """Extract all Mermaid code blocks from Markdown content"""
        pattern = r'```mermaid\s*(.*?)```'
        matches = re.findall(pattern, markdown_content, re.DOTALL)
        return matches
    
    def export_to_docx(self, input_file, output_file=None):
        """Convert Markdown file to DOCX using pandoc"""
        if output_file is None:
            output_file = input_file.replace('.md', '.docx')
        
        try:
            self.color_print(f"Converting {input_file} to DOCX...", 'BLUE')
            result = subprocess.run([
                'pandoc', input_file, '-o', output_file
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                self.color_print(f"✓ Successfully created: {output_file}", 'GREEN')
                return True
            else:
                self.color_print(f"✗ Failed to convert: {result.stderr}", 'RED')
                return False
                
        except subprocess.TimeoutExpired:
            self.color_print("✗ Conversion timed out", 'RED')
            return False
        except Exception as e:
            self.color_print(f"✗ Error during conversion: {e}", 'RED')
            return False
    
    def export_flowcharts_to_images(self, input_file, output_dir='flowchats'):
        """Export Mermaid flowcharts to PNG images"""
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Read the Markdown file
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.color_print(f"✗ Error reading file: {e}", 'RED')
            return False
        
        # Extract Mermaid blocks
        mermaid_blocks = self.extract_mermaid_blocks(content)
        
        if not mermaid_blocks:
            self.color_print("No Mermaid flowcharts found in the document.", 'YELLOW')
            return True
        
        self.color_print(f"Found {len(mermaid_blocks)} Mermaid flowchart(s)", 'BLUE')
        
        success_count = 0
        for i, mermaid_code in enumerate(mermaid_blocks, 1):
            output_file = os.path.join(output_dir, f'flowchart_{i}.png')
            
            # Create temporary .mmd file
            temp_file = f'temp_flowchart_{i}.mmd'
            try:
                with open(temp_file, 'w', encoding='utf-8') as f:
                    f.write(mermaid_code.strip())
                
                # Convert to PNG using mmdc
                self.color_print(f"Converting flowchart {i} to PNG...", 'BLUE')
                result = subprocess.run([
                    'mmdc', '-i', temp_file, '-o', output_file,
                    '-w', '1200', '-H', '800', '--backgroundColor', 'white'
                ], capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    self.color_print(f"✓ Created: {output_file}", 'GREEN')
                    success_count += 1
                else:
                    self.color_print(f"✗ Failed to convert flowchart {i}: {result.stderr}", 'RED')
                
                # Clean up temporary file
                os.remove(temp_file)
                
            except Exception as e:
                self.color_print(f"✗ Error processing flowchart {i}: {e}", 'RED')
                if os.path.exists(temp_file):
                    os.remove(temp_file)
        
        self.color_print(f"Successfully converted {success_count}/{len(mermaid_blocks)} flowcharts", 
                         'GREEN' if success_count == len(mermaid_blocks) else 'YELLOW')
        return success_count > 0
    
    def run(self, input_file):
        """Main execution method"""
        self.color_print("=" * 60, 'CYAN', True)
        self.color_print("DOCUMENT EXPORT SCRIPT", 'CYAN', True)
        self.color_print("=" * 60, 'CYAN', True)
        
        # Check if input file exists
        if not os.path.exists(input_file):
            self.color_print(f"✗ Input file not found: {input_file}", 'RED')
            return False
        
        # Check dependencies
        self.color_print("\nChecking dependencies...", 'BLUE', True)
        
        pandoc_installed = self.check_tool_installed('pandoc')
        mermaid_installed = self.check_tool_installed('mermaid')
        
        self.color_print(f"Pandoc: {'✓ Installed' if pandoc_installed else '✗ Not installed'}", 
                        'GREEN' if pandoc_installed else 'RED')
        self.color_print(f"Mermaid CLI: {'✓ Installed' if mermaid_installed else '✗ Not installed'}", 
                        'GREEN' if mermaid_installed else 'RED')
        
        # Handle missing dependencies
        if not pandoc_installed:
            if not self.install_tool_interactive('pandoc'):
                return False
            # Re-check after potential installation
            pandoc_installed = self.check_tool_installed('pandoc')
        
        if not mermaid_installed:
            if not self.install_tool_interactive('mermaid'):
                self.color_print("Mermaid CLI is required for flowchart export.", 'YELLOW')
        
        # Perform conversions
        success = True
        
        if pandoc_installed:
            success &= self.export_to_docx(input_file)
        else:
            self.color_print("Skipping DOCX conversion (pandoc not available)", 'YELLOW')
        
        if mermaid_installed:
            success &= self.export_flowcharts_to_images(input_file)
        else:
            self.color_print("Skipping flowchart export (mermaid-cli not available)", 'YELLOW')
        
        # Summary
        self.color_print("\n" + "=" * 60, 'CYAN')
        if success:
            self.color_print("✓ Export completed successfully!", 'GREEN', True)
        else:
            self.color_print("✗ Export completed with errors", 'RED', True)
        
        return success

def main():
    parser = argparse.ArgumentParser(description='Export Markdown to DOCX and flowcharts to PNG')
    parser.add_argument('input_file', help='Input Markdown file (.md)')
    parser.add_argument('--output-dir', default='flowchats', help='Output directory for flowcharts')
    
    args = parser.parse_args()
    
    exporter = DocumentExporter()
    success = exporter.run(args.input_file)
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
