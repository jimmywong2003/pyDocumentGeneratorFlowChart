# Packaging Guide for Mermaid Chart Generator

This guide covers how to package and distribute the Mermaid Chart Generator tool for different platforms and distribution methods.

## Distribution Options

### 1. Windows Executable (.exe)
**Target Audience**: Non-technical users who want a simple double-click installation

**Build Command**:
```bash
python build_windows.py
```

**Output**: Creates `MermaidChartGenerator_Windows/` directory containing:
- `Mermaid Chart Generator.exe` - GUI application
- `mermaid-export.exe` - CLI document export tool
- `mermaid-charts.exe` - CLI chart export tool  
- `mermaid-setup.exe` - Environment setup tool
- Documentation files (LICENSE, README.md, user_guideline.md)

**Dependencies Included**: None - users must install Node.js, Mermaid CLI, and Pandoc separately or use the setup tool

### 2. Python Package (pip installable)
**Target Audience**: Developers and technical users

**Build Command**:
```bash
# Build source distribution
python setup.py sdist

# Build wheel distribution  
python setup.py bdist_wheel
```

**Installation**:
```bash
# Install from local source
pip install .

# Install from distribution files
pip install dist/mermaid-chart-generator-1.0.0.tar.gz
```

**Entry Points** (available after installation):
- `mermaid-gui` - GUI application
- `mermaid-export` - CLI document export
- `mermaid-charts` - CLI chart export
- `mermaid-setup` - Environment setup

### 3. Source Code Distribution
**Target Audience**: Developers who want to modify or extend the tool

**Files to Include**:
- All Python source files (`*.py`)
- Documentation (`README.md`, `user_guideline.md`, `LICENSE`)
- Requirements file (`requirements.txt`)
- Build scripts (`setup.py`, `build_windows.py`)
- This packaging guide

## External Dependencies Management

### Required External Tools
The tool requires these external dependencies that are NOT bundled:

1. **Node.js** - JavaScript runtime
2. **Mermaid CLI** - Diagram rendering (`npm install -g @mermaid-js/mermaid-cli`)
3. **Pandoc** - Document conversion

### Handling Dependencies

#### For Windows Executable:
- Include `mermaid-setup.exe` that guides users through installation
- Provide clear documentation on manual installation
- Consider bundling installers for these tools (advanced)

#### For Python Package:
- Document requirements in README.md
- Use `setup_env.py` for automated setup
- Provide troubleshooting guide for dependency issues

## Build Process

### Windows Executable Build
```bash
# Clean previous builds
python build_windows.py

# Or build manually with PyInstaller
pyinstaller --name="Mermaid Chart Generator" --windowed gui_tool.py
pyinstaller --name="mermaid-export" --console export_document.py
pyinstaller --name="mermaid-charts" --console export_flowcharts_only.py
pyinstaller --name="mermaid-setup" --console setup_env.py
```

### Python Package Build
```bash
# Build source distribution
python setup.py sdist

# Build wheel distribution
python setup.py bdist_wheel

# Upload to PyPI (if configured)
twine upload dist/*
```

## Testing Packages

### Test Windows Executable
1. Copy to clean Windows machine
2. Test GUI application functionality
3. Test CLI tools from command prompt
4. Verify dependency installation guidance works

### Test Python Package
1. Create fresh virtual environment
2. Install package: `pip install .`
3. Test all entry points work correctly
4. Verify documentation is accessible

## Version Management

### Version Bumping
Update version in:
- `setup.py` (version parameter)
- Documentation files
- Any other version references

### Changelog
Maintain a `CHANGELOG.md` file with:
- Version numbers and release dates
- New features added
- Bug fixes
- Breaking changes
- Known issues

## Distribution Platforms

### Recommended Platforms
1. **GitHub Releases** - For source code and Windows executables
2. **PyPI** - For Python package distribution  
3. **Standalone Website** - For direct downloads
4. **Package Managers** - Consider Chocolatey (Windows), Homebrew (macOS), apt (Linux)

### File Naming Conventions
- Windows: `MermaidChartGenerator_v1.0.0_Windows.zip`
- Source: `mermaid-chart-generator-1.0.0.tar.gz`
- Wheel: `mermaid_chart_generator-1.0.0-py3-none-any.whl`

## Security Considerations

### Code Signing (Recommended for Windows)
- Sign executables with digital certificate
- Provides authenticity and security verification
- Required for some corporate environments

### Dependency Security
- Regularly update Python dependencies
- Monitor for security vulnerabilities
- Use dependabot or similar tools

## Performance Optimization

### Executable Size
- Use UPX compression with PyInstaller
- Remove unnecessary files from distribution
- Consider splitting GUI and CLI tools

### Startup Time
- Test cold and warm startup times
- Optimize imports and initialization
- Consider lazy loading for less used features

## Troubleshooting Packaging Issues

### Common Issues
1. **Missing dependencies** - Ensure all required files are included
2. **Path issues** - Use relative paths and proper data file handling
3. **Anti-virus false positives** - Common with PyInstaller, may require whitelisting
4. **Permission issues** - Ensure proper file permissions in packages

### Debugging
- Use `--debug` flag with PyInstaller
- Check build logs for missing modules
- Test on clean environments

## Continuous Integration

### GitHub Actions Example
```yaml
name: Build and Release
on:
  push:
    tags: v*

jobs:
  build:
    runs-on: windows-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
    - name: Install dependencies
      run: pip install pyinstaller
    - name: Build Windows executable
      run: python build_windows.py
    - name: Upload artifacts
      uses: actions/upload-artifact@v2
      with:
        name: windows-executable
        path: MermaidChartGenerator_Windows/
```

## Legal Considerations

### Licensing
- Include LICENSE file in all distributions
- Ensure compliance with all dependency licenses
- Provide proper attribution

### Privacy
- Don't collect user data without consent
- Be transparent about any analytics
- Follow privacy regulations (GDPR, CCPA, etc.)

---

*Last updated: September 2025*
