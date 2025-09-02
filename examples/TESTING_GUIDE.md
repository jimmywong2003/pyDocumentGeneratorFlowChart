# Testing Guide for Mermaid Chart Generator

This guide provides comprehensive testing instructions for the Mermaid Chart Generator tool.

## Test Files Overview

### 1. Basic Flowchart Example (`basic_flowchart.md`)
- **Purpose**: Test basic flowchart functionality
- **Diagrams**: 3 flowcharts with different structures
- **Expected Output**: 3 PNG files
- **Features Tested**: Basic nodes, conditional logic, subgraphs

### 2. Advanced Diagrams Example (`advanced_diagrams.md`)
- **Purpose**: Test various Mermaid diagram types
- **Diagrams**: 5 different diagram types
- **Expected Output**: 5 PNG files
- **Features Tested**: Sequence, class, state, gantt, pie charts

## Testing Procedures

### Prerequisites
Ensure these dependencies are installed:
- Python 3.7+
- Node.js and Mermaid CLI (`npm install -g @mermaid-js/mermaid-cli`)
- Pandoc (for DOCX conversion)

### Automated Setup
```bash
# Install all dependencies automatically
python setup_env.py
```

### Manual Testing Steps

#### Test 1: Basic Flowchart Export
```bash
# Export to DOCX with embedded diagrams
python export_document.py examples/basic_flowchart.md

# Export only diagrams to PNG
python export_flowcharts_only.py examples/basic_flowchart.md
```

**Expected Results**:
- `basic_flowchart.docx` file created
- `flowchats/` directory with 3 PNG files:
  - `flowchart_1.png` - Simple Process Flow
  - `flowchart_2.png` - User Registration Process
  - `flowchart_3.png` - System Architecture

#### Test 2: Advanced Diagrams Export
```bash
# Export to DOCX with embedded diagrams
python export_document.py examples/advanced_diagrams.md

# Export only diagrams to PNG
python export_flowcharts_only.py examples/advanced_diagrams.md
```

**Expected Results**:
- `advanced_diagrams.docx` file created
- `flowchats/` directory with 5 PNG files:
  - `flowchart_1.png` - Sequence Diagram
  - `flowchart_2.png` - Class Diagram
  - `flowchart_3.png` - State Diagram
  - `flowchart_4.png` - Gantt Chart
  - `flowchart_5.png` - Pie Chart

#### Test 3: GUI Application Testing
```bash
# Launch the graphical interface
python gui_tool.py
```

**GUI Test Steps**:
1. Click "Browse..." and select `examples/basic_flowchart.md`
2. Choose output directory
3. Click "Generate DOCX + Charts"
4. Verify progress bar and status messages
5. Check output files are created correctly

### Automated Testing Script

Create a test script (`run_tests.py`) for automated testing:

```python
#!/usr/bin/env python3
"""
Automated test script for Mermaid Chart Generator
"""

import os
import subprocess
import sys

def run_test(command, description):
    """Run a test command and report results"""
    print(f"🧪 Testing: {description}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ PASS: {description}")
            return True
        else:
            print(f"❌ FAIL: {description}")
            print(f"   Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ ERROR: {description} - {e}")
        return False

def main():
    print("🚀 Starting Mermaid Chart Generator Tests")
    print("="*50)
    
    success = True
    
    # Test basic flowchart export
    success &= run_test(
        'python export_flowcharts_only.py examples/basic_flowchart.md',
        'Basic flowchart PNG export'
    )
    
    # Test advanced diagrams export
    success &= run_test(
        'python export_flowcharts_only.py examples/advanced_diagrams.md',
        'Advanced diagrams PNG export'
    )
    
    # Test DOCX generation
    success &= run_test(
        'python export_document.py examples/basic_flowchart.md',
        'DOCX document generation'
    )
    
    # Verify output files
    if os.path.exists('flowchats') and os.listdir('flowchats'):
        print("✅ PASS: PNG files created successfully")
    else:
        print("❌ FAIL: No PNG files found")
        success = False
    
    if os.path.exists('basic_flowchart.docx'):
        print("✅ PASS: DOCX file created successfully")
    else:
        print("❌ FAIL: DOCX file not found")
        success = False
    
    # Summary
    print("\n" + "="*50)
    if success:
        print("🎉 ALL TESTS PASSED!")
        print("The Mermaid Chart Generator is working correctly.")
    else:
        print("💥 SOME TESTS FAILED!")
        print("Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

## Expected Test Results

### Successful Test Indicators
- PNG files created in `flowchats/` directory
- DOCX files created in current directory
- No error messages in console output
- All diagrams properly rendered

### Common Issues and Solutions

1. **"Mermaid CLI not found"**
   - Solution: Run `npm install -g @mermaid-js/mermaid-cli`

2. **"Pandoc not found"**
   - Solution: Install Pandoc from https://pandoc.org/installing.html

3. **Permission errors**
   - Solution: Run with administrator privileges if needed

4. **Diagrams not detected**
   - Verify Markdown syntax: use ```` ```mermaid ```` code blocks

## Performance Testing

### Large Document Testing
Create a test file with many diagrams to test performance:

```bash
# Generate stress test (creates file with 50 diagrams)
python -c "
for i in range(50):
    print(f'```mermaid\\nflowchart TD\\n    Start{i} --> Process{i}\\n```\\n')
" > examples/stress_test.md

# Test performance
time python export_flowcharts_only.py examples/stress_test.md
```

### Memory Usage Monitoring
Monitor resource usage during conversion to ensure the tool handles large documents efficiently.

## Cross-Platform Testing

Test on different platforms:
- Windows 10/11
- macOS
- Linux (Ubuntu, CentOS)

Verify that:
- All functionality works consistently
- Path handling is platform-agnostic
- Dependencies are properly detected

## Version Compatibility

Test with:
- Different Python versions (3.7+)
- Different Node.js versions
- Various Mermaid CLI versions

---

*Last updated: September 2025*
