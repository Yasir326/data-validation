# Data Validation Program

Validation program which checks gdpr data with the master aims data.

## Introduction

This program takes all files in a given folder (`personal-data`, `wasiyat`, `rishta-nata`,`waqfe-nau`) and finds `aims` and `name` which do not match the master Aims Data and generates a file with the mismatches as well as their location.

## Getting Started

### Pre-requisites

1. You will need to have [Python](https://www.python.org/).
2. Download the project dependencies with the following commands:

```bash
# Create a virtual environment
python3 -m venv venv

# Activate it
source ./venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running locally

You can run the program with:

```bash
python main.py ${folder_name} ${match_type}
```
