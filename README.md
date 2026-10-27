# Automated Data Quality Pipeline

## Project Overview

A Python-based data quality pipeline that checks company and contact datasets for common data issues. It validates fields, identifies duplicate records, and generates CSV reports to help users review and investigate problematic data.

## Objectives

- Assess data completeness.
- Validate email addresses, phone numbers, website URLs, and dates.
- Identify exact duplicate records.
- Detect repeated email addresses after normalization.
- Generate detailed reports for records that require review.
- Produce a summary of data quality metrics.

## Technologies Used

- Python
- Pandas
- Regular expressions
- URL parsing
- CSV data processing

## Dataset

The project uses a sample company and contact dataset containing 1,250 records and 12 columns, including company name, industry, website, contact details, country, source system, and last verified date.

## Data Quality Checks

- Missing-value analysis
- Email format validation
- Phone number validation
- Website URL validation
- Date format validation
- Exact duplicate detection
- Repeated email detection
- Identification of records requiring review

## Results

The pipeline processed 1,250 records and generated the following results:

| Metric | Result |
|---|---:|
| Records with missing values | 81 |
| Invalid emails | 50 |
| Invalid phone numbers | 26 |
| Invalid websites | 12 |
| Invalid dates | 11 |
| Rows involved in exact duplicates | 50 |
| Rows involved in repeated email addresses | 100 |
| Records requiring review | 99 |

*Note: These issue counts can overlap because a single record may contain multiple data quality issues.*

## Generated Reports

- `data_quality_summary.csv` — Overall data quality metrics.
- `invalid_records_report.csv` — Records requiring review and their validation errors.
- `exact_duplicate_report.csv` — Records involved in exact duplicate groups.
- `near_duplicate_emails_report.csv` — Records with repeated normalized email addresses.

## How to Run

1. Install Python.
2. Install the required dependency:

   ```bash
   pip install pandas
   ```

3. Place `companies.csv` in the project folder.
4. Run the pipeline:

   ```bash
   python main.py
   ```

5. Review the generated CSV reports.

## Future Improvements

- Add configurable validation rules.
- Improve near-duplicate detection.
- Add automated tests and structured logging.
- Support larger datasets and configurable input/output paths.
- Add a data quality dashboard.

## Disclaimer

This is a portfolio project using sample data. The reported metrics describe the dataset processed by the pipeline.
