

#####################################################################################
#### Create class for the posts data:
class Post:
    def __init__(self, link, account, date, media_type, media_link, 
                 description = None, location = None, loc_link = None, likes = None):
        self.link = link
        self.account = account
        self.date = date
        
        self.media_type = media_type
        self.set_media_type(media_type)
        
        self.media_link = media_link
        self.description = description
        self.location = location
        self.loc_link = loc_link
        self.likes = likes
        
    def set_media_type(self, media_type):
        if media_type in ("Image", "Video", "Multi Image"):
            self.media_type = media_type
        else:
            self.media_type = 'Error'
            print("Incorrect media type. Please enter one of the following values: Image, Video, Multi Image")
            #raise ValueError("Incorrect media type. Please enter one of the following values: Image, Video, Multi Image")
    
    def to_dict(self):
        return {'Link': self.link, 
                 'Account': self.account, 
                 'Date': self.date, 
                 'Media Type': self.media_type, 
                 'Media Link': self.media_link,
                 'Description': self.description, 
                 'Location': self.location, 
                 'Location Link': self.loc_link, 
                 'Likes': self.likes}       
   

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time                             

#### Create function for scraping the posts:
# Note it requires the initial article element and the dictionary to be given as inputs:
def scrape(article_elem_init, list_data):      
    
    article_elem = driver.find_elements_by_xpath("//article") # using this to count the number of posts we are going to scrape    
    
    if len(article_elem) <= len(article_elem_init):
        n = 1
        n_end = 4
    else:
        n = 5
        n_end = 7
    
    while n <= n_end:
                
        """Get the LINK to the post"""  
        try:
            post_elem = driver.find_element_by_xpath("//article["+str(n)+"]/div[2]/section[2]/div/a") 
            link = post_elem.get_attribute('href')[:-9]
        except:
            link = 'n/a'
        
        """Get the account USERNAME"""
        user_elem = driver.find_element_by_xpath("//article["+str(n)+"]/header/div/div/div/h2/a") 
        account = user_elem.text
        
        
        """Get the DATE of the post"""    
        date_elem=driver.find_element_by_xpath("//article["+str(n)+"]/div/div/a/time").get_attribute('datetime')
        date = date_elem
        
        
        """Get the TYPE of the post (e.g. Image vs Video)"""  
        try:
            multi_elem = driver.find_element_by_xpath("//article["+str(n)+"]/div[1]/div/div/div/div[2]/div/div[1]/div/ul/li[1]/div/div/div/div[1]/img")      
            media_type = 'Multi Image'
            media_link = multi_elem.get_attribute('src')
                    
        except NoSuchElementException:
            try:
                vid_elem = driver.find_element_by_xpath("//article["+str(n)+"]/div[1]/div/div/div/div[1]/div/video") ## video link
                media_type = 'Video'
                media_link = vid_elem.get_attribute('src')
            except NoSuchElementException:
                try:
                    img_elem = driver.find_element_by_xpath("//article["+str(n)+"]/div[1]/div/div/div/img") ## image link
                    media_type = 'Image'
                    media_link = img_elem.get_attribute('src')
                except NoSuchElementException:
                    try:
                        img_elem = driver.find_element_by_xpath("//article["+str(n)+"]/div[1]/div/div/div/div/img") ## image link
                        media_type = 'Image'
                        media_link = img_elem.get_attribute('src')
                    except:
                        media_type = None
                        media_link = 'n/a'

                
        """Get the post DESCRIPTION"""             
        try:
            desc_elem=driver.find_element_by_xpath("//article["+str(n)+"]/div/div/ul/li/div/div/div/span")
            description = desc_elem.text
        except:
            description = None
            
            
        """Get the number of LIKES"""   
        try:        
            like_elem=driver.find_element_by_xpath("//article["+str(n)+"]/div[2]/section[2]/div")
            likes = re.sub('[^0-9]','',like_elem.text)
        except:    
            likes = 0
        
        
        """Get the LOCATION"""      
        try:    
            loc_elem = driver.find_element_by_xpath("//article["+str(n)+"]/header/div/div/a")
            location = loc_elem.text
            loc_link = loc_elem.get_attribute('href')
        except:
            location = 'No location'
            loc_link = None

        list_data.append(Post(link, account, date, media_type, media_link, description, location, loc_link, likes))
        
        n+=1     
    
    driver.execute_script("arguments[0].scrollIntoView();", article_elem[n_end-1])
    return(str(len(article_elem))+" posts scraped.")


#####################################################################################
#### Test the above:

#### Open ChromeDriver and log in to Instagram:
from Instagram.Admin.FileLocator import locate
from Instagram.InstaLogin import login, credentials
driver = webdriver.Chrome(locate("chromedriver.exe"))


#### Log into Instagram:
login_info = credentials('login.txt')
login(driver, login_info[0], login_info[1])
time.sleep(4)


#### Scrape data for each post 
driver.execute_script("window.scrollTo(0, 1)") # need to scroll a bit for the article element to appear
time.sleep(2)
article_elem_init = driver.find_elements_by_xpath("//article") # using this to base the scrape count
list_data = []
scrape(article_elem_init, list_data) # run this as many times as you want (maybe automate with a function)


#### Create a dataframe and remove duplicates:
import pandas as pd
import datetime
df = pd.DataFrame([s.to_dict() for s in list_data]).drop_duplicates().reset_index()
df['Date of scrape'] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M')

       
        
#####################################################################################
#### Clean up the location data:

#### Create a class for location data:        
class Location:
    def __init__(self, location, loc_link, lat, lon, city, country, street, website, phone, desc_posts):
        self.location = location
        self.loc_link = loc_link
        self.lat = lat
        self.lon = lon
        self.street = street
        self.city = city
        self.country = country
        self.website = website
        self.phone = phone
        self.desc_posts = desc_posts
    
    def to_dict(self):
        return {'Location': self.location, 
                 'Location Link': self.loc_link, 
                 'Lat': self.lat,
                 'Lon': self.lon,
                 'City': self.city,
                 'Country': self.country,
                 'Street': self.street,
                 'Website': self.website,
                 'Phone': self.phone,
                 'Posts Descriptions': self.desc_posts
                 } 
                                
#### Remove posts without location:
df_loc = df[df.Location!='No location'].reset_index(drop=True)
print(df_loc.head(5))


#### Remove posts without specific locations:
loc_distinct = df_loc[['Location','Location Link']].drop_duplicates().reset_index()


#### Download info about each unique location and identify the ones that are just cities:
from user_agent import generate_user_agent
import requests
from bs4 import BeautifulSoup
import re
import json

loc_data = []
for position,link in enumerate(loc_distinct['Location Link']): 
    
    # Generate random user agents to not look suspicious:
    headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))}
   
    url = link 
    html = requests.get(url, timeout=5, headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')
    script_tag = soup.find('script', text=re.compile('window\._sharedData'))
    shared_data = script_tag.string.partition('=')[-1].strip(' ;')
    try:
        j = json.loads(shared_data)
        city = json.loads(j['entry_data']['LocationsPage'][0]['graphql']['location']['address_json'])['city_name']
        if city == loc_distinct['Location'][position]:
            lat = None
            lon = None
            street = 'Location is too general'
            country = json.loads(j['entry_data']['LocationsPage'][0]['graphql']['location']['address_json'])['country_code']
            website = j['entry_data']['LocationsPage'][0]['graphql']['location']['website']
            phone = j['entry_data']['LocationsPage'][0]['graphql']['location']['phone']
            posts = j['entry_data']['LocationsPage'][0]['graphql']['location']['edge_location_to_media']['edges']
            n = 0
            desc_posts = []
            while n < len(posts):
                try:
                    desc_posts.append(j['entry_data']['LocationsPage'][0]['graphql']['location']['edge_location_to_media']['edges'][n]['node']['edge_media_to_caption']['edges'][0]['node']['text']) 
                except:
                    pass
                n+=1
        else:
            lat = j['entry_data']['LocationsPage'][0]['graphql']['location']['lat']
            lon = j['entry_data']['LocationsPage'][0]['graphql']['location']['lng']
            street = json.loads(j['entry_data']['LocationsPage'][0]['graphql']['location']['address_json'])['street_address']
            country = json.loads(j['entry_data']['LocationsPage'][0]['graphql']['location']['address_json'])['country_code']
            website = j['entry_data']['LocationsPage'][0]['graphql']['location']['website']
            phone = j['entry_data']['LocationsPage'][0]['graphql']['location']['phone']
            posts = j['entry_data']['LocationsPage'][0]['graphql']['location']['edge_location_to_media']['edges']
            n = 0
            desc_posts = []
            while n < len(posts):
                try:
                    desc_posts.append(j['entry_data']['LocationsPage'][0]['graphql']['location']['edge_location_to_media']['edges'][n]['node']['edge_media_to_caption']['edges'][0]['node']['text']) 
                except:
                    pass
                n+=1
        loc_data.append(Location(loc_distinct['Location'][position], link, lat, lon, city, country, street, website, phone, desc_posts))
    
    except:
        print('Error with ',link)


#### Create a dataframe:
df_loc_detail = pd.DataFrame([s.to_dict() for s in loc_data])
df_loc_detail = df_loc_detail[ df_loc_detail.Street != 'Location is too general' ]
df_loc_detail['Date of scrape'] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M')


#### Append to existing data and pickle again:
import pickle
import os
for o in [x for x in os.listdir('Instagram\\Data') if x.endswith(".pkl")]:
    if 'insta_locations' in o:
        df_loc_detail_old = pickle.load(open('Instagram\\Data\\'+o,'rb')).drop(['Date of scrape'], axis=1)        
        df_loc_detail_new = df_loc_detail_old.append(df_loc_detail)
        df_loc_detail_new = df_loc_detail_new.drop_duplicates(subset=df_loc_detail_new.columns.difference(['Date of scrape'])).reset_index()       
        pickle.dump(df_loc_detail_new, open('Instagram\\Data\\insta_locations.pkl', 'wb'))
    else:
        pickle.dump(df_loc_detail, open('Instagram\\Data\\insta_locations.pkl', 'wb'))


#### Flag the locations that are not related to food:

# Separate file for testng/building model   
 
import re
import os
import pickle

