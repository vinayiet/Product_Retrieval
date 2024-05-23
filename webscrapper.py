import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Set up the Selenium WebDriver for Firefox
driver = webdriver.Firefox()

try:
    # Navigate to the main shirts page
    url = 'https://allensolly.abfrl.in/c/men-shirts'
    driver.get(url)

    # Wait for the page to load completely
    time.sleep(5)  # Adjust the sleep time if needed

    # Function to click the "LOAD MORE" button if present
    def click_load_more():
        try:
            load_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "LOAD MORE")]'))
            )
            driver.execute_script("arguments[0].scrollIntoView();", load_more_button)
            load_more_button.click()
            print("Clicked 'LOAD MORE' button.")
            return True
        except Exception as e:
            print("No 'LOAD MORE' button found or unable to click:", str(e))
            return False

    # Ensure we have at least 30 shirts by clicking the "LOAD MORE" button if needed
    product_info = []
    while len(product_info) < 100:
        # Scroll down to load more products
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)  # Wait for new products to load

            # Check for the "LOAD MORE" button and click it if present
            if not click_load_more():
                break  # Exit the loop if no "LOAD MORE" button is found

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Get the updated page source
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find all elements with the product title class and add to the list
        products = soup.find_all('div', class_='ProductCard_productInfo__uZhFN')
        for product in products:
            title_element = product.find('div', class_='ProductCard_title__9M6wy')
            detail_element = product.find('div', class_='ProductCard_description__BQzle')  # Assuming this class holds details
            if title_element and detail_element:
                title = title_element.text.strip()
                detail = detail_element.text.strip()
                product_info.append((title, detail))

        # If we have reached 30 unique products, break the loop
        if len(product_info) >= 100:
            break

    # Print the number of unique products found
    print(f"Number of unique products found: {len(product_info)}")

    # Click on each product detail to open it in a new tab
    data = []  # List to store scraped data
    for idx, (title, detail) in enumerate(product_info[:100], start=1):
        print(f"{idx}. Title: {title}\n   Product: {detail}\n")
        try:
            # Find the product description element using the product title
            description_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f'//div[contains(@class, "ProductCard_title__9M6wy") and contains(text(), "{title}")]/ancestor::div[contains(@class, "ProductCard_productInfo__uZhFN")]'))
            )

            # Open the product detail by clicking on the element
            description_element.click()
            print("Opened product description.")

            # Wait for the new tab to open
            time.sleep(2)

            # Switch to the new tab
            driver.switch_to.window(driver.window_handles[-1])
            print("Switched to new tab.")

            # Scraping the product description from the new tab using CSS selector
            product_description_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#__next > main > div > div:nth-child(1) > div > div.col-sm-5.col-md-5.col-lg-5 > div > div.PDPDetails_prodDescDetails__D7ddV > div.ProductDetails_container__0vRlj.ProductDetails_AS__WcrW_ > p.MuiTypography-root.MuiTypography-body1.ProductDetails_description__7hqm9.css-12a9y8i'))
            )
            product_description = product_description_element.text.strip()

            # Append scraped data to the list
            data.append(('Allen Solly', 'Men', title, detail, product_description))

            # Close the new tab
            driver.close()
            print("Closed new tab.")

            # Switch back to the original tab
            driver.switch_to.window(driver.window_handles[0])
            print("Switched back to the original tab.")

            # Wait for the page to reload
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f'//div[contains(@class, "ProductCard_title__9M6wy") and contains(text(), "{title}")]'))
            )
        except Exception as e:
            print(f"Error occurred while processing product detail: {str(e)}")

    # Convert the scraped data into a pandas DataFrame
    df = pd.DataFrame(data, columns=['Brand', 'Category', 'Title', 'Product Detail', 'Product Description'])

    # Export the DataFrame to an Excel file
    df.to_excel('scraped_data.xlsx', index=False)

finally:
    driver.quit()
