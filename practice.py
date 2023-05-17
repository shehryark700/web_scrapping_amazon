import json
import random
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create a new instance of the Chrome driver
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
# Read email and password from credentials file
with open('credentials.json') as personal:
    credentials = json.load(personal)

enter_email.send_keys(credentials['email'])

continue_button = driver.find_element(By.ID, "continue")
continue_button.click()

enter_password = driver.find_element(By.ID, "ap_password")
enter_password.send_keys(credentials['password'])

pass_signin_button = driver.find_element(By.ID, "signInSubmit")
pass_signin_button.click()

# Select UK as the delivery location
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
time.sleep(random.randint(5, 10))

# Navigate to the kitchen and home appliances page
driver.get("https://www.amazon.co.uk/s?bbn=391784011&rh=n%3A391784011%2Cp_85%3A20930949031&dc&qid=1683639353&rnid=20930948031&ref=lp_391784011_nr_p_85_1")
driver.implicitly_wait(random.randint(5, 10))

starting_page = 2
ending_page = 6

# Loop through the pages and extract the links
all_links = []
for i in range(starting_page, ending_page):
    try:
        # Find all products on the page
        all_products = driver.find_elements(By.CSS_SELECTOR, "div[data-component-type='s-search-result']")

        # Extract the title and URL of each product
        for product in all_products:
            title_element = product.find_element(By.CSS_SELECTOR, "h2 a")
            title = title_element.text
            url = title_element.get_attribute("href")

            # Add the title and URL to the list
            all_links.append({'url': url, 'title': title})

        # Navigate to the next page
        next_page = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[@aria-label='Go to page {i + 1}']")))
        next_page.click()

    except Exception as e:
        print(f"Error on page {i}: {e}")

# Save the links to a JSON file
with open('amazon_links.json', 'w') as output:
    json.dump(all_links, output, indent=4)

# Open the first link from the list
if all_links:
    first_link = all_links[0]['url']
    driver.get(first_link)

# Get the three images from the link
images = []
try:
    full_image_script = driver.find_element(By.XPATH, '//*[@id="imageBlock_feature_div"]/script')
    # using regex to find
    full_image_urls = re.findall(r'"hiRes":"(.*?)"', full_image_script.get_attribute('innerHTML'))
    if full_image_urls:
        images.extend(full_image_urls[:3])
    else:
        images.append("Image not available")
except:
    images = ["Image not available"]

all_links[0]['image'] = images
# dump images into json file
with open('amazon_links.json', 'w') as output:
    json.dump(all_links, output, indent=4)

# close the browser
time.sleep(random.randint(10, 20))
driver.quit()