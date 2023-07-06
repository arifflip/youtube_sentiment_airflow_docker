# Youtube Scraper and Sentiment Analysis using Airflow in Docker 
is a project for scraping youtube trending video and its comments, then doing simple sentiment analyisis with using airflow and docker environment.
The result of those is presented in Looker Studio Dashboard

# Project Scheme
![image](https://github.com/arifalse/final_assignment/assets/61183492/a65a3fdf-06e6-4ef6-94df-70def9210230)

# Requirement
- Docker (to build required application)
- credential googlesheet (to write data to googlesheet using python api) 
- docker_compose.yaml file (contains all applications configuration)
- makefile (a makefile to ease building all required apps and its config to docker)

# How to run
- install docker
- using makefile with comman 'make makefila all

# final result
- Dashboard in Looker Studio
- link https://lookerstudio.google.com/reporting/26f41445-6e7c-4738-b4a3-70a3b10cff46
- Example of dashboard :
- ![image](https://github.com/arifalse/final_assignment/assets/61183492/dfd9a80b-e931-431f-ac2b-6983c28138b9)


