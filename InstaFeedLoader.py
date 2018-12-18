from Instagram.Admin.FileLocator import locate
from Instagram.InstaLogin import login, credentials
import pandas
import re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import datetime


# Open ChromeDriver and log in to Instagram:
driver = webdriver.Chrome(locate("chromedriver.exe"))

# Log into Instagram:
login_info = credentials('login.txt')
login(driver, login_info[0], login_info[1])
time.sleep(2)




## Create an empty dictionary to which we will save data
feed_dict = { 'Account':[],
              'Date':[], 
              'Medium':[], 
              'File link':[], 
              'Post link':[], 
              'Description':[], 
              'Location':[], 
              'Location Link':[],
              'Likes/Views':[]
              }


## Scroll down the page to load our sample of posts
scroll_num=5

s=0
while s <= scroll_num: 
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    ## Scrape data for each post        
    article_elem = driver.find_elements_by_xpath("//article") # using this to count the number of posts we are going to scrape
    n=1
    while n <= len(article_elem):
        
        """Get the account username"""
        user_elem = driver.find_elements_by_xpath("//article["+str(n)+"]/header/div/div/div/a") 
        feed_dict['Account'].append(user_elem[0].text)
        
        
        """Get the date of the post"""    
        date_elem=driver.find_element_by_xpath("//article["+str(n)+"]/div/div/a/time").get_attribute('datetime')
        feed_dict['Date'].append(date_elem)
        
        
        """Get the type of the post (e.g. Image vs Video)"""  
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
                
                
        """Get the link to the post"""  
        try:
            post_elem = driver.find_element_by_xpath("//article["+str(n)+"]/div[2]/section[2]/div/a")
            feed_dict['Post link'].append(post_elem.get_attribute('href')[:-9])
        except:
            feed_dict['Post link'].append('n/a')
        
        
        """Get the post description"""             
        try:
            desc_elem=driver.find_element_by_xpath("//article["+str(n)+"]/div/div/ul/li/span")
            feed_dict['Description'].append(desc_elem.text)
        except:
            feed_dict['Description'].append('')
            
            
        """Get the number of likes"""   
        try:        
            like_elem=driver.find_element_by_xpath("//article["+str(n)+"]/div[2]/section[2]/div")
            feed_dict['Likes/Views'].append(re.sub('[^0-9]','',like_elem.text))
        except IndexError:    
            feed_dict['Likes/Views'].append('0')
        
        
        """Get the location"""      
        try:    
            loc_elem = driver.find_element_by_xpath("//article["+str(n)+"]/header/div/div/a")
            feed_dict['Location'].append(loc_elem.text)
            feed_dict['Location Link'].append(loc_elem.get_attribute('href'))
        except:
            feed_dict['Location'].append('No location')
            feed_dict['Location Link'].append('')
    
        n+=1        

    s+=1


# Create a dataframe and remove posts without location
feed_df = pandas.DataFrame(feed_dict)
feed_df = feed_df[feed_df.Location!='No location'].reset_index(drop=True)
feed_df['Date of scrape'] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M')

'''
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
'''