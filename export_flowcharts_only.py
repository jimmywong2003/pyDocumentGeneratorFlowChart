#!/usr/bin/env python3
"""
Flowchart Export Script
Exports only Mermaid flowcharts from Markdown files to PNG images.
Use this when Mermaid CLI installation fails for the full document export.
"""

import os
import re
import sys
import subprocess
import platform
import argparse
from pathlib import Path

class FlowchartExporter:
    def __init__(self):
        self.platform = platform.system().lower()
        
        # Color codes for terminal output
        self.COLORS = {
            'RED': '\033[91m',
            'GREEN': '\033[92m',
            'YELLOW': '\033[93m',
            'BLUE': '\033[94m',
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
    
    def check_mermaid_installed(self):
        """Check if Mermaid CLI is installed"""
        try:
            # Check if mmdc is available in PATH
            result = subprocess.run(['mmdc', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            return False
    
    def extract_mermaid_blocks(self, markdown_content):
        """Extract all Mermaid code blocks from Markdown content"""
        pattern = r'```mermaid\s*(.*?)```'
        matches = re.findall(pattern, markdown_content, re.DOTALL)
        return matches
    
    def export_flowcharts(self, input_file, output_dir='flowchats'):
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
    
    def provide_manual_instructions(self, input_file):
        """Provide instructions for manual conversion"""
        self.color_print("\n" + "=" * 60, 'CYAN')
        self.color_print("MANUAL CONVERSION INSTRUCTIONS", 'CYAN', True)
        self.color_print("=" * 60, 'CYAN')
        
        # Read the Markdown file to extract Mermaid blocks
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            mermaid_blocks = self.extract_mermaid_blocks(content)
            
            if mermaid_blocks:
                self.color_print(f"\nFound {len(mermaid_blocks)} Mermaid flowchart(s) to convert manually:", 'BLUE')
                
                for i, mermaid_code in enumerate(mermaid_blocks, 1):
                    self.color_print(f"\nFlowchart {i}:", 'YELLOW', True)
                    print("1. Go to https://mermaid.live/")
                    print("2. Paste the following Mermaid code:")
                    print("-" * 40)
                    print(mermaid_code.strip())
                    print("-" * 40)
                    print("3. Click 'Download' and save as PNG")
                    print("4. Name the file: flowchart_{i}.png")
                    print("5. Place it in the 'flowchats/' directory")
            
        except Exception as e:
            self.color_print(f"Error reading file for manual instructions: {e}", 'RED')
    
    def provide_docx_insertion_guide(self):
        """Provide guide for inserting images into DOCX"""
        self.color_print("\n" + "=" * 60, 'CYAN')
        self.color_print("DOCX IMAGE INSERTION GUIDE", 'CYAN', True)
        self.color_print("=" * 60, 'CYAN')
        
        guide = """
1. Open your DOCX file in Microsoft Word
2. Navigate to the section where each flowchart should appear
3. For each flowchart:
   - Go to Insert > Pictures > This Device
   - Select the corresponding PNG file from flowchats/ folder
   - Adjust size and positioning as needed
   - Add captions if desired (References > Insert Caption)

4. Recommended placement:
   - Flowchart 1: After 'Visa on Arrival (VOA) with Biometric Enhancement' section
   - Flowchart 2: After 'Extended Stay and Visa Renewal Process' section  
   - Flowchart 3: After 'Border Control and Entry/Exit Management' section

5. Image sizing tips:
   - Maintain aspect ratio when resizing
   - Use 'Wrap Text' options for better layout
   - Consider center alignment for diagrams
"""
        print(guide)
    
    def run(self, input_file):
        """Main execution method"""
        self.color_print("=" * 60, 'CYAN', True)
        self.color_print("FLOWCHART EXPORT TOOL", 'CYAN', True)
        self.color_print("=" * 60, 'CYAN')
        
        # Check if input file exists
        if not os.path.exists(input_file):
            self.color_print(f"✗ Input file not found: {input_file}", 'RED')
            return False
        
        # Check if Mermaid CLI is installed
        self.color_print("Checking Mermaid CLI installation...", 'BLUE')
        mermaid_installed = self.check_mermaid_installed()
        
        if mermaid_installed:
            self.color_print("✓ Mermaid CLI is installed", 'GREEN')
            success = self.export_flowcharts(input_file)
            
            if success:
                self.color_print("\n✓ Flowchart export completed!", 'GREEN', True)
                self.provide_docx_insertion_guide()
            else:
                self.color_print("\n✗ Flowchart export failed", 'RED', True)
                self.provide_manual_instructions(input_file)
        else:
            self.color_print("✗ Mermaid CLI not installed", 'RED')
            self.color_print("\nPlease install Mermaid CLI using one of these methods:", 'YELLOW')
            print("1. npm: npm install -g @mermaid-js/mermaid-cli")
            print("2. Requires Node.js: https://nodejs.org/")
            print("3. Or use manual conversion method below")
            
            self.provide_manual_instructions(input_file)
            self.provide_docx_insertion_guide()
        
        return True

def main():
    parser = argparse.ArgumentParser(description='Export Mermaid flowcharts from Markdown to PNG images')
    parser.add_argument('input_file', help='Input Markdown file (.md)')
    parser.add_argument('--output-dir', default='flowchats', help='Output directory for flowcharts')
    
    args = parser.parse_args()
    
    exporter = FlowchartExporter()
    success = exporter.run(args.input_file)
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
