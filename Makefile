include .env
export

CURRENT_DATE := $(shell powershell -Command "Get-Date -Format 'yyyy-MM-dd'")
JDBC_URL := "jdbc:postgresql://${POSTGRES_HOST}/${POSTGRES_DB}"
JDBC_PROPERTIES := '{"user": "${POSTGRES_ACCOUNT}", "password": "${POSTGRES_PASSWORD}"}'

help:
	@echo ## postgres			- Run a Postgres container, including its inter-container network.

all: postgres airflow selenium copy_credential

postgres: postgres-create

postgres-create:
	@docker-compose -f ./docker/docker-compose.yaml --env-file .env up -d
	@echo '__________________________________________________________'
	@echo 'Postgres container created at port ${POSTGRES_PORT}...'
	@echo '__________________________________________________________'
	@echo 'Postgres Docker Host    : ${POSTGRES_HOST}' &&\
		echo 'Postgres Account        : ${POSTGRES_ACCOUNT}' &&\
		echo 'Postgres password       : ${POSTGRES_PASSWORD}' &&\
		echo 'Postgres Db             : ${POSTGRES_DB}'
	@echo '==========================================================='

airflow: airflow-create

airflow-create:
	@docker-compose -f ./docker/docker-compose.yaml --env-file .env up -d
	
selenium :
	@docker exec -it airflow_scheduler_tgs bash -c "pip install selenium"
	@docker exec -it airflow_scheduler_tgs bash -c "pip install bs4"
	@docker exec -it airflow_scheduler_tgs bash -c "pip install lxml"
	@docker exec -it airflow_scheduler_tgs bash -c "pip install gspread"
	@docker exec -it airflow_scheduler_tgs bash -c "pip install oauth2client"
	@docker exec -it airflow_scheduler_tgs bash -c "pip install selenium-stealth"
	@docker exec -it airflow_scheduler_tgs bash -c "pip install deep_translator"
	@docker exec -it airflow_scheduler_tgs bash -c "pip install textblob"
	@docker exec -it airflow_scheduler_tgs bash -c "pip install gspread-dataframe"

copy_credential :
	@docker cp python_gsheet_credential.json airflow_scheduler_tgs:/opt/airflow/python_gsheet_credential.json

clean:
	@powershell -Command "& .\helper\goodnight.ps1"