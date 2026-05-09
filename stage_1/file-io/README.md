# File I/O — Reading JSON Configs and Writing AWS Reports

Scripts for reading JSON configuration files and generating EC2 instance reports.

## Files

- `ec2_reporter.py` — main script: loads config, filters instances, generates reports
- `aws_config.json` — AWS environment configuration (project, region, tags)
- `ec2_instances.json` — EC2 instance data input file

## What it does

1. Reads AWS environment config from `aws_config.json`
2. Loads EC2 instance list from `ec2_instances.json`
3. Filters instances by state (running / stopped)
4. Generates `ec2_report.txt` — human-readable report
5. Generates `ec2_report.json` — structured report for system ingestion or S3 storage

## Usage

Run from the file-io directory:

    py ec2_reporter.py

## Output example

    Config loaded: converge / dev / us-east-1
    Instances loaded: 4 total
      Running: 2 | Stopped: 2
    TXT report generated: ec2_report.txt
    JSON report generated: ec2_report.json

## Concepts covered

- open() with context manager (with statement)
- json.load() and json.dump() for JSON file handling
- List comprehensions for filtering AWS resource data
- datetime for report timestamps
