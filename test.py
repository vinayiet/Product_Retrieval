from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

# Set up the Selenium WebDriver for Firefox
driver = webdriver.Firefox()

try:
    # Navigate to the main shirts page
    url = 'https://allensolly.abfrl.in/c/men-shirts'
    driver.get(url)

    # Close the ad if it's present
    try:
        close_button = driver.find_element(by=By.XPATH, value='//*[local-name()="path" and @fill-rule="evenodd"]')
        close_button.click()
        print("Ad closed successfully.")
    except Exception as e:
        print("No ad found or unable to close ad:", str(e))

    # Wait for the page to load completely
    time.sleep(5)  # Adjust the sleep time if needed

    # Scroll down to load more products
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for new products to load
        time.sleep(1)  # Adjust the sleep time if needed

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Get the page source
    page_source = driver.page_source

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all elements with the product title class
    product_titles = soup.find_all('div', class_='ProductCard_title__9M6wy')

    # Print the product titles
    for title in product_titles:
        print(title.text.strip())

finally:
    driver.quit()
