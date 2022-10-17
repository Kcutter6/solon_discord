from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


driver_path = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(driver_path)

def waitForElementLoad(bySelector, name):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((bySelector, name))
        )
        return element
    except:
        return

def waitForAllElementsToLoad(bySelector, name):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((bySelector, name))
        )
        return element
    except:
        return

def findTeachers(teacherName):
    # Open staff directory page
    driver.get("https://www.solonschools.org/Page/1818")

    # Click the submit button on the 'select school' page to see list of teachers
    btn = waitForElementLoad(By.ID, "minibaseSubmit2967")
    btn.click()

    # Wait for next page to load by waiting for a sample element
    waitForElementLoad(By.XPATH, f'//td[contains(., "Caiola, Theresa")]')

    # Look for all instances of td (html tag) that contain the given teacher's name
    rows = waitForAllElementsToLoad(By.XPATH, f'//td[contains(.,"{teacherName}")]/..')

    # If no rows are found with given xpath, return with no teachers found
    if (not rows):
        return
    

    # Create an empty array to return each result into a non WebElement format
    # This is so we have to deal with selenium (selenium is a library) crap only in this file
    returnArr = []

    for row in rows:

        # This is an array of information stored in the selected row (but this is in WebElem format)
        allInfo = row.find_elements(By.TAG_NAME, "td") 

        # If teacher doesn't have a website, redirect to 'page not found' page
        weblink = None
        try:
            weblink = allInfo[4].find_elements(By.TAG_NAME, "a")[1].get_attribute("href")
        except:
            weblink = "https://www.solonschools.org/site/default.aspx?PageType=19"
        
        # Check if each attribute is there, otherwise replace with a default output
        Building = None
        try:
            Building = allInfo[1].text
        except:
            Building = "No Building"

        Position = None
        try:
            Position = allInfo[2].text
        except:
            Position = "No Position"
        
        VoiceMail = None
        try:
            VoiceMail = allInfo[3].text
        except:
            VoiceMail = "No Voicemail"

        # Convert the web element into a dictionary of strings (readable from other scripts without importing selenium library)
        returnArr.append({
                "name" : allInfo[0].text,
                "building" : Building,
                "position" : Position,
                "voice-mail" : VoiceMail,
                "website-link" : weblink # I am getting the redirect of the website
            })
    return returnArr

def getHeadline():
    # Open up district home page
    driver.get("https://www.solonschools.org/Domain/4")

    # Search for the most recent headline
    article = waitForAllElementsToLoad(By.XPATH, '//div[@id="sw-app-headlines-13"]/ul/li/div')[0]

    # Get all the attributes of the article, ex: (Link, thumbnail, header, description)
    HeaderElem = article.find_element(By.XPATH, "//h1/a")

    # Store attributes in a dictionary
    articleAtt = {
        "link" : HeaderElem.get_attribute("href"),
        "header" : HeaderElem.find_element(By.TAG_NAME, "span").text,
        "thumbnail" : article.find_element(By.XPATH, "//span/span/img").get_attribute("src"),
        "desc" : article.find_element(By.TAG_NAME, "p").text
    }

    return articleAtt

