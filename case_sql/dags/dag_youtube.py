#|----------------------------------------------------------------------------------|  
#  Dependecies 
#|----------------------------------------------------------------------------------| 

from lib2to3.pgen2 import driver
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.mysql_operator import MySqlOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook

from datetime import datetime
import pandas as pd
import requests
import os
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from function_youtubescraper import *
from function_tools import *

#|----------------------------------------------------------------------------------|  
#  arg
#|----------------------------------------------------------------------------------| 

### defaulr args
args = {
    'owner': 'arif',
    'depends_on_past': False,
}

#|----------------------------------------------------------------------------------|  
#  Task
#|----------------------------------------------------------------------------------| 

#task to config driver and define youtube scraper object
def scrape() :  

    #create scrapper object
    scrapper=youtube_trending_video_scrapper('https://www.youtube.com/feed/trending')
    result=scrapper.run_scrapper()
    return result

#task to do scraping and write it to postgre
def scrape_and_load() :
     
    #run scrapper
    df_result=scrape()

    #write to postgre
    table_name = 'scraping_raw_result'
    write_to_postgre(df_result,table_name)

#tasl to read from postgre then do sentiment and write it again to postgre
def read_do_sentiment_load() :

    print('---------- SCORING FOR SENTIMENT ANALYSIS IS STARTING ----------')

    #read from tabel
    database = 'postgres_db'
    table_name = 'scraping_raw_result'
    df=read_from_postgre(database,table_name)

    #do sentiment
    df['sentiment_score']=df.comment.apply(lambda x: sentiment_score(x))

    #transfrom
    df=transfrom_dataframe(df)

    #write to postgre
    table_name = 'sentiment_youtube_trending_video'
    write_to_postgre(df,table_name)

#tasl to read from postgre then do sentiment and write it again to postgre
def offload() :
    
    #read from tabel
    database = 'postgres_db'
    table_name = 'sentiment_youtube_trending_video'
    df=read_from_postgre(database,table_name)

    offload_to_googlesheet(df)
    
#|----------------------------------------------------------------------------------|  
#  DAG
#|----------------------------------------------------------------------------------|

###dag tasks
with DAG(dag_id="test_scraper_youtube",
         start_date=datetime(2023,7,3),
         catchup=False) as dag:
                
        #task to
        task1 = PythonOperator(
        task_id="Scrape",
        python_callable=scrape_and_load)

        #task to  
        task2 = PythonOperator(
        task_id="Sentiment",
        python_callable=read_do_sentiment_load)

        #task to  
        task3 = PythonOperator(
        task_id="Offload",
        python_callable=offload)


#task dependencies
task1 >> task2 >> task3