import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from deep_translator import GoogleTranslator
from textblob import TextBlob
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe

#function to load to data to posgre using sqlalchemy
#def load_to_postgre(user,password,host,port,database,table_name,dataframe):
def write_to_postgre(dataframe,table_name):
    
    #credentials
    user = 'user'
    password = 'password'
    host = 'postgres_tgs'
    port = '5432'
    database = 'postgres_db'

    #define engine
    engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}')
    
    #dump it using to_sql
    dataframe.to_sql(table_name, engine, if_exists='replace',index=False)
    
    print(f'Dataframe succesfully write on {database}{table_name}')


#function to read all data from a table using sqlalchemy
def read_from_postgre(database,table_name) :

    #credentials
    user = 'user'
    password = 'password'
    host = 'postgres_tgs'
    port = '5432'
    database = 'postgres_db'

    #define engine
    engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}')
    
    #execute it and feth to pandas dataframe
    
    df = pd.read_sql_query(f'SELECT * FROM "{table_name}"',con=engine)
    #print(df.columns.tolist())
    #print(df.head(10).transpose())

    #add columns
    return df

#function to calculate sentiment score (based on polarity)
def sentiment_score(x) :
  
    #load traslator object
    try :
        translator = GoogleTranslator(source='auto', target='en')
    
        #do translation and calculate polairy and subjectuvty from translated string
        translated_string = translator.translate(x)

        text = TextBlob(translated_string)
        polarity=text.sentiment.polarity
    except :
        polarity='invalid'
    
    return polarity

#function to do transformation
def transfrom_dataframe(df) :
    
    print('---------- TRANSOFRMATION PROCESS IS STARTING ----------')

    #grouping data and calclute mean of sentimen score
    df=df[df.sentiment_score!='invalid']
    df=df\
    .groupby(['channel_video','title_video','url_video','detailed_total_views','detailed_video_rank'])\
    .aggregate(
    {'sentiment_score': 'mean'}
    ).reset_index()

    #column modify
    df['detailed_total_views']=[i.split(' ')[0].replace(',','') for i in df['detailed_total_views']]
    df['detailed_total_views']=[i.replace('.','') for i in df['detailed_total_views']]
    df['detailed_total_views']=df.detailed_total_views.astype(int)

    df = df.drop_duplicates(subset = ['channel_video', 'title_video'],keep = 'last').reset_index()

    return df

#function to do transformation
def offload_to_googlesheet(df) :
    
    print('---------- STARTING OFFLOAD TO GOOGLESHEET----------')
    #grouping data and calclute mean of sentimen score
    credential=ServiceAccountCredentials.from_json_keyfile_name('python_gsheet_credential.json')
    client=gspread.authorize(credential)

    worksheet1=client.open('dataset_for_GDS').sheet1
    worksheet1.clear()
   
    #column modift
    worksheet1.clear()
    set_with_dataframe(worksheet=worksheet1, dataframe=df, include_index=False,
    include_column_header=True, resize=True)
    
    print('---------- SUCCESFULLY OFFLOADED TO GOOGLESHEET----------')
