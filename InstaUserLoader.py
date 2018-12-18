####################################################################################
### Download influencers' posts

from Instagram.Admin.FileLocator import locate
from Instagram.InstaLogin import login, credentials
import os
import pandas
import pickle
import re
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time

                  
influencers=['barcelonafoodexperience']
driver = webdriver.Chrome(locate("chromedriver.exe"))

scroll_num=3

def last_post(user):

    ## Find the last scrape file
    scrape_files = [x for x in os.listdir('Instagram\\Data') if x.endswith(".pkl")]
    
    
    ## Unpickle the data
    with open('Instagram\\Data\\'+scrape_files[len(scrape_files)-1], 'rb') as pf:
        df = pickle.load(pf)
    
    
    ## Identify the last link for the selected Instagrammer:
    df_u = df[df.Account == user]
    return df_u['Post link'].iloc[0]
    
  
posts_dict = { 'Account':[],
               'Post link':[], 
               'Description':[], 
               'Medium':[], 
               'File link':[], 
               'Date':[], 
               'Location':[], 
               'Likes/Views':[]  }

links = []   
for i in influencers:
    
    driver.get("https://www.instagram.com/"+i)
    
    article_elem_init = driver.find_elements_by_xpath("//main/div/div[4]/article/div[1]/div/div") # using this to base the scrape count
    n=1
    while n<=len(article_elem_init):
        links.append(driver.find_element_by_xpath('//main/div/div[4]/article/div[1]/div/div['+str(n)+']/div[1]/a').get_attribute('href'))
        links.append(driver.find_element_by_xpath('//main/div/div[4]/article/div[1]/div/div['+str(n)+']/div[2]/a').get_attribute('href'))
        links.append(driver.find_element_by_xpath('//main/div/div[4]/article/div[1]/div/div['+str(n)+']/div[3]/a').get_attribute('href'))
        n+=1
       
    '''Old code starts here'''    
          
    ## Get all links to the lastest posts and their descriptions:
    post_elem = driver.find_elements_by_xpath("//main/article/div/div/div/div/a") 
    img_elem = driver.find_elements_by_xpath("//main/article/div/div/div/div/a/div/div/img")
    
   
    n=0
    while n < len(post_elem):
        
        if post_elem[n].get_attribute('href') != last_post(i):
            
            posts_dict['Account'].append(i)    
            posts_dict['Post link'].append(post_elem[n].get_attribute('href'))
            posts_dict['Description'].append(img_elem[n].get_attribute('alt'))
            posts_dict['File link'].append(img_elem[n].get_attribute('src'))
        
            try:
                if post_elem[n].text=='':
                    posts_dict['Medium'].append('Image')
                else:
                    posts_dict['Medium'].append(post_elem[n].text)
                        
            except IndexError:
                posts_dict['Medium'].append('Image')
        
            n+=1
        
        else:
            break
    
    
## Collect information about each link (need fix the below to treat videos differently from images):
n=0
while n < len(posts_dict['Post link']):
    try:
        driver.get(posts_dict['Post link'][n])
        
        date_elem=driver.find_elements_by_xpath("//time")[0].get_attribute('title')
        posts_dict['Date'].append(date_elem)
        
        like_elem=driver.find_elements_by_xpath("//article/div/section/div/span")[0].text
        posts_dict['Likes/Views'].append(re.sub('[^0-9]','',like_elem))
        
        loc_elem=driver.find_elements_by_xpath("//header/div/div/a")[0].get_attribute('title')
        posts_dict['Location'].append(loc_elem)
        
    except IndexError:
        posts_dict['Location'].append('No location')
    
    n+=1

df = pandas.DataFrame.from_dict(posts_dict)


## Check if the file exists and pickle the data:
nowDate = pandas.datetime.today()
count=0
for o in [x for x in os.listdir('Instagram\\Data') if x.endswith(".pkl")]:
    if nowDate.strftime("%y%m%d") in o:
        count+=1
if count==0:
    pickle.dump( df, open( 'Instagram\\Data\\'+nowDate.strftime("%y%m%d")+'.pkl', "wb" ) )
else:
    pickle.dump( df, open( 'Instagram\\Data\\'+nowDate.strftime("%y%m%d")+' ('+str(count)+').pkl', "wb" ) )


