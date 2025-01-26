# OP Analyzer Service

## Overview
A flexible data analysis script that extracts and processes data from different sources like StackOverflow and GitHub.

## Features
- Fetch data from StackOverflow and GitHub APIs
- Apply configurable analysis flows
- Command-line interface for easy execution


## Installation
```bash
# Clone the repository
git clone https://github.com/nathanielsade/op_analyzer.git

# Install required library
pip install requests
```

## Usage
```bash
# Basic execution
python app.py "Github" "1"

# Analyze StackOverflow data
python app.py "Stackoverflow"
```

## Command-Line Arguments
- First argument: Data source ("Github" or "Stackoverflow")
- Second argument (optional): Analysis flow ID

## Error Handling
- Validates data source and analysis flow
- Provides informative error messages
- Handles API request exceptions
