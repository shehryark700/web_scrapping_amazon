import json
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create a new instance of the chrome driver
driver = webdriver.Chrome()

# Navigate to the Amazon UK homepage
driver.get("https://www.amazon.co.uk/ref=ap_frn_logo")

# Accept cookies if required
try:
    accept_cookies_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "sp-cc-accept")))
    accept_cookies_button.click()
except:
    pass

# Sign in
sign_in_button = driver.find_element(By.XPATH, "//span[contains(text(),'Account & Lists')]")
sign_in_button.click()

driver.implicitly_wait(10)

enter_email = driver.find_element(By.ID, "ap_email")
enter_email.send_keys("your_email")

continue_button = driver.find_element(By.ID, "continue")
continue_button.click()

enter_password = driver.find_element(By.ID, "ap_password")
enter_password.send_keys("1234567")

pass_signin_button = driver.find_element(By.ID, "signInSubmit")
pass_signin_button.click()

# Select UK as delivery location
select_delivery_option = driver.find_element(By.ID, "glow-ingress-line2")
select_delivery_option.click()
driver.implicitly_wait(10)

enter_uk_postcode = driver.find_element(By.XPATH, "//*[@id='GLUXZipUpdateInput']")
enter_uk_postcode.clear()
enter_uk_postcode.send_keys("wf13pp")
driver.implicitly_wait(10)

apply_button = driver.find_element(By.ID, "GLUXZipUpdate")
apply_button.click()
driver.implicitly_wait(10)

# Navigate to the kitchen and home appliances page
driver.get("https://www.amazon.co.uk/s?bbn=391784011&rh=n%3A391784011%2Cp_85%3A20930949031&dc&qid=1683639353&rnid=20930948031&ref=lp_391784011_nr_p_85_1")
driver.implicitly_wait(random.randint(5,10))

starting_page = 2
ending_page = 6

# Loop through the pages and extract the links
all_links = []
for i in range(starting_page, ending_page):
    try:
        # Find all products on the page
        all_products = driver.find_elements(By.CSS_SELECTOR, "div[data-component-type='s-search-result'] h2 a")

        # Extract the URLs from the links
        page_links = [link.get_attribute("href") for link in all_products]
        all_links.extend(page_links)

        # Navigate to the next page
        next_page = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//a[@aria-label='Go to page {i+1}']")))
        next_page.click()

        # Wait for the page to load
        driver.implicitly_wait(random.randint(5,10))
    except:
        print("Failed to navigate to page {}".format(i))

# Write the URLs to a JSON file
with open("product_urls.json", "w") as f:
    json.dump({'url':all_links}, f, indent=4)

# Close the browser
time.sleep(random.randint(10,20))
driver.quit()
