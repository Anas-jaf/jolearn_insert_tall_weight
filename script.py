from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time  



driver=webdriver.Firefox()

def login_to_microsoft (username, password, url ,driver):
    EMAILFIELD = (By.ID, "i0116")
    PASSWORDFIELD = (By.ID, "i0118")
    NEXTBUTTON = (By.ID, "idSIButton9")

    driver.get(url)

    # wait for email field and enter email
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(EMAILFIELD)).send_keys(username)

    # Click Next
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(NEXTBUTTON)).click()

    # wait for password field and enter password
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(PASSWORDFIELD)).send_keys(password)

    # Click Login - same id?
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(NEXTBUTTON)).click()

def wait_for_element(driver, locator , overlay_locator=False):
    try:
        if overlay_locator:
            # Wait for the overlay element to disappear
            WebDriverWait(driver, 10).until(EC.invisibility_of_element_located(locator))
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    except StaleElementReferenceException:
        return wait_for_element(driver, locator)
    return element

def click_element( element):
    element.click()
    # return element

if __name__ == "__main__":
        
    driver.get("https://jolearn.jo/") 
    login = wait_for_element(driver, (By.CSS_SELECTOR, ".btn.btn-lg"))
    login_url = login.get_attribute('href') 
    login_to_microsoft('9841033839@jolearn.jo' , 'Ahmad33839' , login_url , driver)
    
