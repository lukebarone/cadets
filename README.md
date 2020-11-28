### Cadets Repo

![Python Lint Checker](https://github.com/lukebarone/cadets/workflows/Python%20Lint%20Checker/badge.svg?branch=master)

This is my personal repo for scripts I need for Cadets.

## Contents

1. [Roll Call Export Fixer](./roll_call_export_fixer.py)

### Roll Call Export Fixer

This Python3 script takes in a .CSV file in the same folder, and corrects it to work with GSuite. It removes the "Cost Centre" column (Column V), which GSuite does not support; it makes the Recovery Phone number appear in E164 format (or use the Work number if provided); creates the email address (and validates the result), sets the correct OU (in progress) and creates the password. The `results.csv` file that is generated can then be uploaded to GSuite.

## Contributing

- All pull requests must be to a "dev" branch - not directly to "master"
- All `*.py` files must pass the automated PyLinter check
- Changes to `requirements.txt` require an explanation
- Commit messages must make good sense. Not everyone here reads perfect Python code.