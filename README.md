# Youtube Scraper and Sentiment Analysis using Airflow in Docker 
Is a project for scraping youtube trending video and its comments, then doing simple sentiment analyisis with using airflow and docker environment.
The result of those is presented in Looker Studio Dashboard

# Project Scheme
![image](https://github.com/arifalse/final_assignment/assets/61183492/a65a3fdf-06e6-4ef6-94df-70def9210230)

# Requirements
- Docker (to build required application)
- Credential googlesheet (to write data to googlesheet using python api) 
- Docker_compose.yaml file (contains all applications configuration)
- Makefile (a makefile to ease building all required apps and its config to docker)

# How to run
- Install docker
- Using makefile with command 'make makefila all' to build all apps

# Final result
- Dashboard in Looker Studio
- Link https://lookerstudio.google.com/reporting/26f41445-6e7c-4738-b4a3-70a3b10cff46
- Example of dashboard :
- ![image](https://github.com/arifalse/final_assignment/assets/61183492/910a6a57-c6ad-4879-a62c-793d508b4b5e)


