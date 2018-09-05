from Instagram.Admin.FileLocator import locate
from Instagram.InstaLogin import login, credentials
import pandas
import re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import datetime
import os
import pickle


# Open ChromeDriver and log in to Instagram:
driver = webdriver.Chrome(locate("chromedriver.exe"))

# Log into Instagram:
login_info = credentials('login.txt')
login(driver, login_info[0], login_info[1])
time.sleep(2)

article_elem_init = driver.find_elements_by_xpath("//article") # using this to base the scrape count

#### Create an empty dictionary to which we will save data
feed_dict = {'Account':[],
            'Date':[], 
            'Medium':[], 
            'File link':[], 
            'Post link':[], 
            'Description':[], 
            'Location':[], 
            'Location Link':[],
            'Likes/Views':[]
            }

#### Scrape data for each post 
#### Note it requires the initial article element and the ditionary to be given as inputs:
def scrape(article_elem_init, feed_dict):      
    article_elem = driver.find_elements_by_xpath("//article") # using this to count the number of posts we are going to scrape    
    
    if len(article_elem) <= len(article_elem_init):
        n = 1
        n_end = 4
    else:
        n = 5
        n_end = 7
    
    while n <= n_end:
        
        """Get the account USERNAME"""
        user_elem = driver.find_elements_by_xpath("//article["+str(n)+"]/header/div/div/div/a") 
        feed_dict['Account'].append(user_elem[0].text)
        
        
        """Get the DATE of the post"""    
        date_elem=driver.find_element_by_xpath("//article["+str(n)+"]/div/div/a/time").get_attribute('datetime')
        feed_dict['Date'].append(date_elem)
        
        
        """Get the TYPE of the post (e.g. Image vs Video)"""  
        try:
            table_elem = driver.find_element_by_xpath("//article["+str(n)+"]/div[1]/div/div/div[2]/table/tbody")
            feed_dict['Medium'].append('Multi Image')
            feed_dict['File link'].append('n/a')
                    
        except NoSuchElementException:
            try:
                vid_elem = driver.find_element_by_xpath("//article["+str(n)+"]/div[1]/div/div/div/div[1]/div/video") ## video link
                feed_dict['Medium'].append('Video')
                feed_dict['File link'].append(vid_elem.get_attribute('src')) 
            except NoSuchElementException:
                try:
                    img_elem = driver.find_element_by_xpath("//article["+str(n)+"]/div[1]/div/div/div/img") ## image link
                    feed_dict['Medium'].append('Image')
                    feed_dict['File link'].append(img_elem.get_attribute('src'))
                except NoSuchElementException:
                    try:
                        img_elem = driver.find_element_by_xpath("//article["+str(n)+"]/div[1]/div/div/div/div/img") ## image link
                        feed_dict['Medium'].append('Image')
                        feed_dict['File link'].append(img_elem.get_attribute('src'))
                    except:
                        feed_dict['Medium'].append('n/a')
                        feed_dict['File link'].append('n/a')
                            
                '''
                try:
                    img_elem = driver.find_elements_by_xpath("//article["+str(n)+"]/div[1]/div/div[1]/div/div/div[1]/div/img")
                    feed_dict['File link'].append(img_elem[0].get_attribute('src'))
                except IndexError:
                    img_elem = driver.find_elements_by_xpath("//article["+str(n)+"]/div[1]/div/div[1]/div/div/div[1]/div/div/img")
                    feed_dict['File link'].append(img_elem[0].get_attribute('src'))
                '''
                
                
        """Get the LINK to the post"""  
        try:
            post_elem = driver.find_element_by_xpath("//article["+str(n)+"]/div[2]/section[2]/div/a")
            feed_dict['Post link'].append(post_elem.get_attribute('href')[:-9])
        except:
            feed_dict['Post link'].append('n/a')
        
        
        """Get the post DESCRIPTION"""             
        try:
            desc_elem=driver.find_element_by_xpath("//article["+str(n)+"]/div/div/ul/li/div/div/div/span")
            feed_dict['Description'].append(desc_elem.text)
        except:
            feed_dict['Description'].append('')
            
            
        """Get the number of LIKES"""   
        try:        
            like_elem=driver.find_element_by_xpath("//article["+str(n)+"]/div[2]/section[2]/div")
            feed_dict['Likes/Views'].append(re.sub('[^0-9]','',like_elem.text))
        except:    
            feed_dict['Likes/Views'].append('0')
        
        
        """Get the LOCATION"""      
        try:    
            loc_elem = driver.find_element_by_xpath("//article["+str(n)+"]/header/div/div/a")
            feed_dict['Location'].append(loc_elem.text)
            feed_dict['Location Link'].append(loc_elem.get_attribute('href'))
        except:
            feed_dict['Location'].append('No location')
            feed_dict['Location Link'].append('')
    
        n+=1     
    
    driver.execute_script("arguments[0].scrollIntoView();", article_elem[n_end-1])
    return(str(len(article_elem))+" posts scraped.")


#### Create a dataframe and remove duplicates:
def CreateDf(feed_dict):
    feed_df = pandas.DataFrame(feed_dict).drop_duplicates().reset_index()
    feed_df['Date of scrape'] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M')
    return("Data frame created as feed_df.")

#### Remove posts without location
def FilterLocation(feed_df):
    feed_df_loc = feed_df[feed_df.Location!='No location'].reset_index(drop=True)
    return("Filtered location data saved as feed_df_loc.")
    return(feed_df_loc.head(5))


#### Check if the file exists and pickle the data:
def PickleData(feed_df):
    nowDate = pandas.datetime.today()
    count=0
    for o in [x for x in os.listdir('Instagram\\Data') if x.endswith(".pkl")]:
        if nowDate.strftime("%y%m%d") in o:
            count+=1
    if count==0:
        pickle.dump( feed_df, open( 'Instagram\\Data\\'+str(login_info[0])+nowDate.strftime("%y%m%d")+'.pkl', "wb" ) )
        return('Data has been pickled and saved as: '+'Instagram\\Data\\'+str(login_info[0])+nowDate.strftime("%y%m%d")+'.pkl')
    else:
        pickle.dump( feed_df, open( 'Instagram\\Data\\'+str(login_info[0])+nowDate.strftime("%y%m%d")+' ('+str(count)+').pkl', "wb" ) )
        return('Data has been pickled and saved as: '+'Instagram\\Data\\'+str(login_info[0])+nowDate.strftime("%y%m%d")+' ('+str(count)+').pkl')
