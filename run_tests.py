#!/usr/bin/env python3
"""
Automated test script for Mermaid Chart Generator
Runs comprehensive tests to verify the tool works correctly
"""

import os
import subprocess
import sys
import time
from pathlib import Path

def run_test(command, description, timeout=60):
    """Run a test command and report results"""
    print(f"🧪 Testing: {description}")
    print(f"   Command: {command}")
    
    start_time = time.time()
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout)
        end_time = time.time()
        elapsed = end_time - start_time
        
        if result.returncode == 0:
            print(f"✅ PASS: {description} ({elapsed:.2f}s)")
            return True, elapsed
        else:
            print(f"❌ FAIL: {description}")
            print(f"   Error: {result.stderr}")
            return False, elapsed
    except subprocess.TimeoutExpired:
        print(f"⏰ TIMEOUT: {description} (exceeded {timeout}s)")
        return False, timeout
    except Exception as e:
        print(f"❌ ERROR: {description} - {e}")
        return False, 0

def cleanup_test_files():
    """Clean up test output files"""
    files_to_remove = [
        'basic_flowchart.docx',
        'advanced_diagrams.docx',
        'stress_test.md'
    ]
    
    directories_to_remove = [
        'flowchats',
        'test_output'
    ]
    
    print("\n🧹 Cleaning up test files...")
    
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print(f"   Removed: {file}")
    
    for directory in directories_to_remove:
        if os.path.exists(directory):
            import shutil
            shutil.rmtree(directory)
            print(f"   Removed: {directory}/")

def verify_file_exists(filepath, description):
    """Verify that a file exists and has content"""
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        print(f"✅ VERIFIED: {description} - {filepath}")
        return True
    else:
        print(f"❌ MISSING: {description} - {filepath}")
        return False

def verify_directory_files(directory, expected_count, description):
    """Verify a directory exists and has expected number of files"""
    if os.path.exists(directory) and os.path.isdir(directory):
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        if len(files) >= expected_count:
            print(f"✅ VERIFIED: {description} - {len(files)} files in {directory}/")
            return True
        else:
            print(f"❌ INCOMPLETE: {description} - Expected {expected_count}, found {len(files)} files in {directory}/")
            return False
    else:
        print(f"❌ MISSING: {description} - Directory {directory}/ not found")
        return False

def main():
    print("🚀 Starting Mermaid Chart Generator Comprehensive Tests")
    print("="*60)
    
    success = True
    test_results = []
    
    # Clean up any previous test files
    cleanup_test_files()
    
    # Test 1: Basic flowchart PNG export
    test1_success, test1_time = run_test(
        'python export_flowcharts_only.py examples/basic_flowchart.md',
        'Basic flowchart PNG export'
    )
    test_results.append(('Basic PNG Export', test1_success, test1_time))
    success &= test1_success
    
    # Verify basic test output
    if test1_success:
        success &= verify_directory_files('flowchats', 3, 'Basic flowchart PNG files')
    
    # Test 2: Advanced diagrams PNG export
    test2_success, test2_time = run_test(
        'python export_flowcharts_only.py examples/advanced_diagrams.md',
        'Advanced diagrams PNG export'
    )
    test_results.append(('Advanced PNG Export', test2_success, test2_time))
    success &= test2_success
    
    # Verify advanced test output
    if test2_success:
        success &= verify_directory_files('flowchats', 8, 'All PNG files')  # 3 basic + 5 advanced
    
    # Test 3: DOCX generation with basic flowcharts
    test3_success, test3_time = run_test(
        'python export_document.py examples/basic_flowchart.md',
        'DOCX document generation (basic)'
    )
    test_results.append(('DOCX Basic Export', test3_success, test3_time))
    success &= test3_success
    
    # Verify DOCX file
    if test3_success:
        success &= verify_file_exists('basic_flowchart.docx', 'Basic flowchart DOCX file')
    
    # Test 4: DOCX generation with advanced diagrams
    test4_success, test4_time = run_test(
        'python export_document.py examples/advanced_diagrams.md',
        'DOCX document generation (advanced)'
    )
    test_results.append(('DOCX Advanced Export', test4_success, test4_time))
    success &= test4_success
    
    # Verify DOCX file
    if test4_success:
        success &= verify_file_exists('advanced_diagrams.docx', 'Advanced diagrams DOCX file')
    
    # Test 5: Create and test with stress test file
    print("\n📊 Creating stress test file...")
    stress_content = ""
    for i in range(10):  # Reduced from 50 to 10 for faster testing
        stress_content += f"""```mermaid
flowchart TD
    Start{i} --> Process{i}
    Process{i} --> Decision{i}{{Check}}
    Decision{i} -->|Yes| EndSuccess{i}
    Decision{i} -->|No| EndFail{i}
```

"""
    
    with open('examples/stress_test.md', 'w') as f:
        f.write("# Stress Test\\n\\n" + stress_content)
    
    test5_success, test5_time = run_test(
        'python export_flowcharts_only.py examples/stress_test.md',
        'Stress test PNG export (10 diagrams)',
        timeout=120
    )
    test_results.append(('Stress Test Export', test5_success, test5_time))
    success &= test5_success
    
    # Verify stress test output
    if test5_success:
        success &= verify_directory_files('flowchats', 18, 'All PNG files including stress test')  # 3 + 5 + 10
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    total_time = 0
    for test_name, test_success, test_time in test_results:
        status = "✅ PASS" if test_success else "❌ FAIL"
        print(f"{status}: {test_name} ({test_time:.2f}s)")
        total_time += test_time
    
    print(f"⏱️  Total test time: {total_time:.2f}s")
    
    if success:
        print("\n🎉 ALL TESTS PASSED!")
        print("The Mermaid Chart Generator is working correctly.")
        print("\n📁 Generated files:")
        print("- basic_flowchart.docx")
        print("- advanced_diagrams.docx") 
        print("- flowchats/ directory with PNG files")
    else:
        print("\n💥 SOME TESTS FAILED!")
        print("Please check the error messages above.")
        sys.exit(1)
    
    # Clean up test files
    cleanup_test_files()

if __name__ == "__main__":
    main()
