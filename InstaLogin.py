import os
from selenium.webdriver.common.action_chains import ActionChains
import time

def login(driver, username, password):
    
    ## Go to Instagram:
    driver.get("http://instagram.com")

    ## Find the Log In button and click on it:
    login_link = driver.find_element_by_link_text('Log in')
    ActionChains(driver).move_to_element(login_link).click().perform()
    
    ## Enter your username:
    input_username = driver.find_elements_by_xpath("//input[@name='username']")
    ActionChains(driver).move_to_element(input_username[0]).click().send_keys(username).perform()
    
    time.sleep(1)
    
    ## Enter your password:
    input_password = driver.find_elements_by_xpath("//input[@name='password']")
    ActionChains(driver).move_to_element(input_password[0]).click().send_keys(password).send_keys(u'\ue007').perform()  
    ## Note send_keys(u'\ue007') simulates pressing ENTER
       
    time.sleep(1)
    
def credentials(filename):
    cwd = os.getcwd()
    for r,d,f in os.walk(cwd):
        for files in f:
            if files == filename:
                path = os.path.join(r,files)
              
    with open(path, 'r') as f:
        content = f.readlines()
        content = [x.strip() for x in content]
    return(content)