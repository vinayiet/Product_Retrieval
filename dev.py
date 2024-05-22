from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    while len(product_info) < 30:
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
        product_elements = driver.find_elements(By.CLASS_NAME, 'ProductCard_productInfo__uZhFN')
        for product_element in product_elements:
            title_element = product_element.find_element(By.CLASS_NAME, 'ProductCard_title__9M6wy')
            description_element = product_element.find_element(By.CLASS_NAME, 'ProductCard_description__BQzle')
            title = title_element.text.strip()
            description = description_element.text.strip()
            product_info.append((title, description))

        # If we have reached 30 unique products, break the loop
        if len(product_info) >= 30:
            break

    # Print the number of unique products found
    print(f"Number of unique products found: {len(product_info)}")

    # Click on each product description to open it in a new tab
    for idx, (title, description) in enumerate(product_info[:30], start=1):
        print(f"{idx}. Title: {title}\n   Description: {description}\n")
        try:
            # Find the product description element and open it in a new tab
            product_detail_xpath = f'//p[contains(text(), "{description}")]'
            product_detail_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, product_detail_xpath))
            )
            product_detail_element.click()
            print("Clicked on product description.")
            # Wait for 2 seconds
            time.sleep(2)
            # Close the new tab
            driver.switch_to.window(driver.window_handles[-1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            print("Closed the new tab.")
        except Exception as e:
            print(f"Error occurred while processing product description: {str(e)}")

finally:
    driver.quit()
