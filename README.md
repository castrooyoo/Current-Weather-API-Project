# Building Data Pipeline Project from Open Weather Map API

## Description
- Following the current weather patterns, I took the initiative to create a data pipeline to give insights in terms of current weather conditions daily. As a learning curve, I explored several Platforms to better practice and experience their capabilities as listed in the [tools section](##Tools).
- **Summary:** Extraction of data was sourced from the Open AI platform, which was connected with my AWS EC2 Instance and VSCode, where Airflow was integrated to automate and schedule the process daily and operate with S3 Bucket as the depository/storage. After this, the data was visualized in the dashboard using Tableau.

![Project Data Flow & Tools.png](https://github.com/castrooyoo/Current-Weather-API-Project/blob/main/Project%20Data%20Flow%20%26%20Tools.png)
## Requirements
Data source: OpenWeather API

## Tools
1. AWS EC2 Instance: Platform where the programming happens, linked to VS-Code
2. VS-Code: Where the actual programming happens
3. Python: To help with Extraction-Transformation-Loading, from API to S3 bucket
4. AWS S3 Bucket: Storage where the extracted data from API gets dumped/stored
5. Tableau: Weather Dashboard
6. Apache Airflow: Automate and Orchestrate the data pipeline; where I scheduled a daily requests pull of data from API >>> ETL>>> S3 >>> Tableau
