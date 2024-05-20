# Building Data Pipeline Project from Current-Weather-API

## Description
- Following the current weather patterns, I took the initiative to create a data pipeline to give insights in terms of current weather conditions daily. As a learning curve, I explored several Platforms to better practice and experience their capabilities as listed in the [tools section](##Tools).
- **Summary:** Extraction of data was sourced from the Open AI platform, which was connected with my AWS EC2 Instance and VSCode, where Airflow was integrated to automate and schedule the process daily, and working with a depository of S3 Bucket. After this, the data was visualized in the dashboard using Tableau.

## Requirements
Data source: 1. OpenWeather API

## Tools
1. AWS EC2 Instance: Platform where the programming happens, linked to VS-Code
2. VS-Code: Where the actually programming happens
3. Python: To help with Extraction-Transformation-Loading, from API to S3 bucket
4. AWS S3 Bucket: Storage where the extracted data from API gets dumped/stored
5. Tableau : Weather Dashboard
6. Apache Airflow: Automate and Orchestrate the data pipeline; where I scheduled a daily requests pull of data from API >>> ETL>>> S3 >>> Tableau
