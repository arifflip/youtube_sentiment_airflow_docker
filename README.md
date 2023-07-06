# Youtube Scraper and Sentiment Analysis using Airflow in Docker 
Is a project for scraping youtube trending video and its comments, then doing simple sentiment analyisis with using airflow and docker environment.
The result of those is presented in Looker Studio Dashboard

# Project Scheme
![image](https://github.com/arifalse/final_assignment/assets/61183492/c1ce4630-8669-4612-904c-8ba8aaab3135)

# Requirements
- Docker (to build required application)
- Credential googlesheet (an json filte which contain credential to write data to googlesheet using python api) 
- Docker_compose.yaml file (contains all applications configuration)
- Makefile (a makefile to ease building all required apps and its config to docker) 

# How to run
1. make sure docker is already installed
2. its more comfortable if your dir tree is same as this :

![image](https://github.com/arifalse/final_assignment/assets/61183492/db539535-37fe-45e0-bcb3-9fec0c66a2e5)

3. if all file is already set, you can run this command to build container in docker :
   - 'make all' its command using makefile to build postgres airflow and selenium
   - if all three container is already running, you can type 'make packages' to install all required pacakge
   - then type 'make copy_credential' to copy your google spreadsheet credential inside container direcotry
4. if all step is done, you can add all dag file and py file based on this tree
   ![image](https://github.com/arifalse/final_assignment/assets/61183492/df989775-511e-4cf4-a878-a705320f3999)
5. dependencies of scraping, sentiment, and offloading dags can be seen in airflow webserver :

   ![image](https://github.com/arifalse/final_assignment/assets/61183492/df499704-1d8e-41c8-8791-c0f987acdfca)

7. Tips if any error happen :
   -if theres an error at 'selenium' after all containers succesfully builded, restart the container will fix it
   
# Final result
- Dashboard in Looker Studio
- Link https://lookerstudio.google.com/reporting/26f41445-6e7c-4738-b4a3-70a3b10cff46
- Example of dashboard :
- ![image](https://github.com/arifalse/final_assignment/assets/61183492/8fefd509-f033-4a2f-a9a6-039818667741)


