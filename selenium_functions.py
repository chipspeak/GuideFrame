from selenium import webdriver  # Importing the webdriver module from selenium and other modules
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

'''
For GUIDEFRAME-15 selenium functionality has been broken out into a separate script
This will aid legibility and also lend itself to the SDK-lite id where we provide a simple
library of functions that are clear to a user but deeper on this side in terms of error-handling etc
Additional functions will be added as they are required before a doc is prepared to outline them
'''

# Function to setup the driver and return it for initialization in main scripts
def driver_setup(driver_location):
    # Setting up with Chrome options and the ChromeDriver service
    options = Options()
    options.add_argument("usr/bin/google-chrome")

    # Disable the "Chrome is being controlled by automated test software" banner
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # Specify the path to ChromeDriver
    service = Service(driver_location) 

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    return driver


# Function to open a URL
def open_url(driver, target):
    driver.get(target)


# Function to set window size
def set_window_size(driver):
    driver.maximize_window()


# Function to find an element by its id
def find_element(driver, id):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, id))
        )
        return element
    except Exception as e:
        print(f"Error finding element with ID '{id}': {e}")
        return None


# Function to scroll to an element using a href
def scroll_to_element(driver, href):
    try:
        # Use WebDriverWait to ensure the element is present
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//a[@href='{href}']"))
        )
        driver.execute_script("arguments[0].scrollIntoView()", element)


    except Exception as e:
        print(f"Error in scroll_to_element for href '{href}': {e}")


# Function to hover over a href element and click it (ideal for link buttons)
def hover_and_click(driver, href):
    try:
        # Use WebDriverWait to ensure the element is present
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//a[@href='{href}']"))
        )
        # Use ActionChains to hover over the element
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()

        # Click the element
        element.click()
    except Exception as e:
        print(f"Error in hover_and_click for href '{href}': {e}")


# Function to hover over an href element (ideal for link buttons)
def hover_over_element(driver, href):
    try:
        # Use WebDriverWait to ensure the element is present
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//a[@href='{href}']"))
        )
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()

    except Exception as e:
        print(f"Error in hover_and_click for href '{href}': {e}")


# Function to click an element using a CSS selector with error handling
def click_element(driver, css_selector):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        element.click()
    except Exception as e:
        print(f"Error clicking element with selector '{css_selector}': {e}")


# Function to type into an input field using an ID with error handling
def type_into_field(driver, element_id, text):
    try:
        input_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, element_id))
        )
        input_field.send_keys(text)
    except Exception as e:
        print(f"Error typing into field with ID '{element_id}': {e}")