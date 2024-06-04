# Remote Job Scraper with DynamoDB Storage
This Python script scrapes job postings from Remotive.com and stores them in a DynamoDB table.

## Features
* Scrapes job titles, companies, locations, and description URLs.
* Handles potential CAPTCHAs using SeleniumBase.
* Stores data in a DynamoDB table (requires configuration).

## Requirements
* Python 3.x
* SeleniumBase (install with `pip install seleniumbase`)
* BeautifulSoup4 (install with `pip install beautifulsoup4`)
* boto3 (install with `pip install boto3`)
* AWS Account with DynamoDB enabled (for data storage)

## Usage
- Configure DynamoDB:
    * Replace table_name in the storeData function with your desired DynamoDB table name.
    * Ensure you have proper IAM permissions to access DynamoDB from your script's execution environment.

- Run the Script:
    * Execute the script using python remotive_job_scraper.py

## Output
The script prints the scraped job data to the console. It also stores the data in your DynamoDB table (if configured).

## Disclaimer
This script is for educational purposes only. Remotive.com may have terms of service regarding scraping their website. Be responsible and respectful when using this script.