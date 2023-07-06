#|----------------------------------------------------------------------------------|  
#  Dependecies 
#|----------------------------------------------------------------------------------| 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import pandas as pd
import os
import time


#|----------------------------------------------------------------------------------|  
#  Class youtube scraper
#|----------------------------------------------------------------------------------| 

#class for scraping youtube 
class youtube_trending_video_scrapper() :
    def __init__(self,url) :
        self.url=url

        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')  
        remote_webdriver = 'remote_chromedriver'
        self.driver=webdriver.Remote(f'{remote_webdriver}:4444/wd/hub',options=chrome_options)
        #self.driver=driver
        
    #method to scroll down the page 
    def scroll_down(self) :
        body = self.driver.find_element(By.CSS_SELECTOR,'body')
        body.send_keys(Keys.END)

    #method to get all video element after visiting list of trending youtube video    
    def get_all_video_element(self):
        self.driver.get(self.url)
        list_result=[]
        list_name=[]
        time.sleep(2)
        self.scroll_down()
        try :
            list_element=self.driver.find_elements(By.ID,"dismissible")
            for i in list_element :
                if self.get_title_video(i) not in list_name :
                    list_name.append(self.get_title_video(i))
                    list_result.append(i)            
        except :
            list_result=None
        return list_result

    #method to extract url from video element
    def get_url_video(self,webelement) :
        try :
            value=webelement.find_element(By.ID,'video-title').get_attribute('href')
        except:
            value=None
        return value

    #method to extract video's title from video element
    def get_title_video(self,webelement) :
        try :
            value=webelement.find_element(By.ID,"video-title").text
        except:
            value=None
        return value
    
    #method to extract channel name from video element
    def get_channel_name(self,webelement) :
        try :
            value=webelement.find_element(By.ID,"channel-name").text
        except:
            value=None
        return value

    #method to extract number of total views from video element
    def get_total_views(self,webelement) :
        try :
            value=webelement.find_element(By.ID,'metadata-line').text
            value=value.split('\n')[0]
        except:
            value=None
        return value

    #method to extract upload information from video element
    def get_upload_date(self,webelement) :
        try :
            value=webelement.find_element(By.ID,'metadata-line').text
            value=value.split('\n')[1]
        except:
            value=None
        return value
    
    #method to extract detailed total views from youtube video page
    def get_detailed_views(self) :
        try :
            self.driver.find_element(By.ID,'expand').click()
            value=self.driver.find_element(By.CSS_SELECTOR,'.bold.yt-formatted-string').text
        except :
            value=None
        return value

    #method to extract video's ranking  from youtube video page
    def get_detailed_trending_rank(self) :
        try :
            value=self.driver.find_elements(By.CSS_SELECTOR,'a.yt-simple-endpoint.yt-formatted-string')
            value=[i.text for i in value if i.text.__contains__('di Trending')][0]
        except :
           value=None
        return value

    
    #method to extract data from video element then store it in dict
    def extract_data(self,elem) :
        data={
            'channel_video' : self.get_channel_name(elem),
            'url_video' : self.get_url_video(elem),
            'title_video': self.get_title_video(elem),
            'total_views_video': self.get_total_views(elem),
            'upload_date':self.get_upload_date(elem)
             }
        return data
    
    #method to extract all listed videos from youtube trending video page 
    def extract_trending_video(self) :
        list_video=self.get_all_video_element()
        data=[]
        for i in list_video :
            data.append(self.extract_data(i))
        df=pd.DataFrame.from_dict(data)
        df=df[~df.url_video.isnull()]
        return df

    #method to extract all comment from video page (only scrap comment in 1 minute not all comment)
    def extract_comment_video(self,df) :
        
        #create base df for hold all new df
        columnbase=['channel_video', 'url_video', 'title_video','total_views_video', 'upload_date','detailed_total_views','detailed_video_rank','comment']
        df_result=pd.DataFrame(columns=columnbase)
        
        #loop to scrape comment (only for 1 minute)
        for index, row in df.iterrows() :
            print(f"---------- runing at index : {index}, on title : {row['title_video']}) ---------- ")
            self.driver.get(row['url_video'])
            time.sleep(2)
            
            #pause video
            self.driver.find_element(By.CSS_SELECTOR,'ytd-player, #container.ytd-player').click()
            
            #get detail view and trending rank
            time.sleep(1)
            ls_komen=[]
            val_detail_views=self.get_detailed_views()
            val_rank_video=self.get_detailed_trending_rank()
            
            #loop to extract comment
            length_comment=0
            for i in range(10) :    
                self.scroll_down()
                time.sleep(1)
                for i in self.driver.find_elements(By.ID,'content-text') :
                    if i.text not in ls_komen :
                        ls_komen.append(i.text)
                current_length=len(self.driver.find_elements(By.ID,'content-text'))
                if current_length == length_comment :
                    break
                length_comment=current_length
            
            #build dataframe result
            df_comment=pd.DataFrame(ls_komen,columns=['comment'])
            
            df_comment['channel_video']=row['channel_video']
            df_comment['detailed_total_views']=val_detail_views
            df_comment['detailed_video_rank']=val_rank_video
            
            df_comment=df_comment.merge(df,on=['channel_video'],how='left')
            df_comment=df_comment[columnbase]
            df_result=pd.concat([df_result,df_comment])
        return df_result

    #method to run all scraping stage (all trendings video & comment in it)         
    def run_scrapper(self) :
        
        print('---------- SCRAPING PROCESS IS STARTING ----------')

        #scrape ternding video
        print('---------- starting to scrap trending video ----------')
        df_trending=self.extract_trending_video()
        #print(df_trending.head(10))
        
        df_trending=df_trending[~df_trending.title_video.str.contains('#shorts')]
        
        print(df_trending.head(10))

        df_trending=df_trending[df_trending.title_video!=''].head(19).reset_index()

        #scrape comment each video
        print('---------- starting to scrap comment from each trending video ----------')
        df_result=self.extract_comment_video(df_trending)
        
        #quit driver
        self.driver.quit()
        print('---------- SCRAPING PROCESS HAS COMPLETE ----------')
        
        return df_result