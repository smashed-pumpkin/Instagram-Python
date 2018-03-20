from Instagram.Admin.FileLocator import locate
from Instagram.InstaLogin import login, credentials
from selenium import webdriver

credentials = credentials("login.txt")

# Open ChromeDriver:
driver = webdriver.Chrome(locate("chromedriver.exe"))

# Log into Instagram:
login(driver, credentials[0], credentials[1])

# Go to the list of users you follow:
driver.get("https://www.instagram.com/"+credentials[0])
following_elem = driver.find_element_by_xpath('//a[@href="https://www.instagram.com/'+credentials[0]+'/following"]')