#!/usr/bin/env python3
"""
Setup script for Mermaid Chart Generator
Packages the tool for distribution via pip
"""

from setuptools import setup, find_packages
import os

# Read the contents of README.md
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# Read the contents of requirements.txt
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="mermaid-chart-generator",
    version="1.0.0",
    description="A Python tool for converting Markdown files with Mermaid diagrams to DOCX documents and PNG images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jimmy Wong",
    author_email="support@jimmywongiot.com",
    url="https://jimmywongiot.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'mermaid-export=export_document.py:main',
            'mermaid-charts=export_flowcharts_only.py:main',
            'mermaid-gui=gui_tool.py:main',
            'mermaid-setup=setup_env.py:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Documentation",
        "Topic :: Text Processing :: Markup",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    keywords="mermaid, markdown, documentation, diagrams, flowcharts, docx, png",
    project_urls={
        "Source": "https://github.com/jimmywong2003/pyDocumentGeneratorFlowChart",
        "Bug Reports": "https://github.com/jimmywong2003/pyDocumentGeneratorFlowChart/issues",
    },
)
