# Data Validation Program

Validation program which checks GDPR Data with the Master AIMS Data.

## Introduction

This program takes files in a given folder (`personal-data-child`,`personal-data-adult`, `rishta-nata`,`waqfe-nau-adult`, `waqfe-nau-adult`,`wasiyat`) and finds `aims` and `name` which either match or do not match with the master AIMS Data and generates a file with the matches or mismatches as well as their location.

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

The `folder_name` can be one of the following: 
* `personal-data-child`
* `personal-data-adult`
* `rishta-nata`
* `waqfe-nau-adult`
* `waqfe-nau-adult`
* `wasiyat`

The `match_type` can be one of the following:

* `matches`
* `mismatches`
