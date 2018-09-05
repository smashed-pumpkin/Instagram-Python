from Instagram.Admin.FileLocator import locate
from selenium.webdriver.common.action_chains import ActionChains
import time


def credentials(filename):

    path = locate(filename)
              
    with open(path, 'r') as f:
        content = f.readlines()
        content = [x.strip() for x in content]
        
    return(content)



def login(driver, username, password):
    
    ## Go to Instagram:
    driver.get("https://www.instagram.com/accounts/login/")
    
    time.sleep(2)
    
    ## Enter your username:
    input_username = driver.find_elements_by_xpath("//input[@name='username']")
    ActionChains(driver).move_to_element(input_username[0]).click().send_keys(username).perform()
    
    time.sleep(1)
    
    ## Enter your password:
    input_password = driver.find_elements_by_xpath("//input[@name='password']")
    ActionChains(driver).move_to_element(input_password[0]).click().send_keys(password).send_keys(u'\ue007').perform()  
    ## Note send_keys(u'\ue007') simulates pressing ENTER
       
    time.sleep(1)
    
