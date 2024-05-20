# Building Data Pipeline Project from Current-Weather-API

## Requirements
Data source: 1. OpenWeather API

## Tools
1. AWS EC2 Instance: Platform where the programming happens, linked to VS-Code
2. VS-Code: Where the actually programming happens
3. Python: To help with Extraction-Transformation-Loading, from API to S3 bucket
4. AWS S3 Bucket: Storage where the extracted data from API gets dumped/stored
5. Tableau : Weather Dashboard
6. Apache Airflow: Automate and Orchestrate the data pipeline; where I scheduled a daily requests pull of data from API >>> ETL>>> S3 >>> Tableau
