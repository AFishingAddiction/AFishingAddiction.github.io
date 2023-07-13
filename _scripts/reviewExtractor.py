import sys
import time
import yaml

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ReviewExtractor:
    REVIEWS_BUTTON_XPATH = '//*[@id="BPS_rating_summary"]/div/button/div[3]/div'
    REVIEWS_SELECTOR = '#BVRRContainer > div > div > div > div > ol > li > div > div.bv-content-container > div > div.bv-content-details-offset-off > div > div > div.bv-content-summary-body-text > p'
    LOAD_MORE_BUTTON_SELECTOR = "#BVRRContainer > div > div > div > div > div.bv-content-pagination > div > ul > li.bv-content-pagination-buttons-item.bv-content-pagination-buttons-item-next > a"

    def __init__(self, url):
        self.url = url
        self.reviews = []

    def extract_reviews(self, min_reviews):
        # Set up Selenium options
        browser_options = Options()

        # Set up the Edge driver (replace with the path to your chromedriver)
        edgedriver_path = "C:\\Users\\dansc\\Downloads\\edgedriver_win64\\msedgedriver.exe"
        service = Service(edgedriver_path)

        # Create a new instance of the Chrome driver
        driver = webdriver.Edge(service=service, options=browser_options)

        # Visit the URL
        driver.get(self.url)
        reviews_button = driver.find_element(
            By.XPATH, self.REVIEWS_BUTTON_XPATH
        )
        WebDriverWait(driver, 10).until(EC.visibility_of(reviews_button))
        if reviews_button.is_displayed():
            reviews_button.click()
            print("Review button clicked")

        # Extract the reviews
        while len(self.reviews) < min_reviews:

            review_elements = driver.find_elements(By.CSS_SELECTOR, self.REVIEWS_SELECTOR)
            # print(review_elements)
            self.reviews.extend(
                [
                    review.text.replace("\n", " ").strip()
                    for review in review_elements
                    if review.text.strip()
                ]
            )
            print(f"Reviews length: {len(self.reviews)}")
            # Check if there is a "Load More" button
            load_more_button = driver.find_element(
                By.CSS_SELECTOR, self.LOAD_MORE_BUTTON_SELECTOR
            )
            if load_more_button.is_displayed():
                # Click the "Load More" button
                load_more_button.click()

                # Wait for the new reviews to load
                WebDriverWait(driver, 10).until(EC.staleness_of(load_more_button))

                # Wait for a short interval to ensure all reviews are loaded
                time.sleep(2)

            else:
                # No more reviews to load, break the loop
                break

        time.sleep(60)
        # Close the Chrome driver
        driver.quit()

    def create_yaml_list(self, min_reviews):
        # Format reviews as a YAML bullet list
        return yaml.dump(self.reviews, allow_unicode=True, width=1024)

    def run(self, min_reviews):
        self.extract_reviews(min_reviews)
        reviews_yaml = self.create_yaml_list(min_reviews)
        print(reviews_yaml)


if __name__ == "__main__":
    # Get the URL from the command line argument
    if len(sys.argv) < 2:
        print("Please provide a URL as a command line argument.")
        sys.exit(1)

    url = sys.argv[1]

    # Extract and print the reviews
    min_reviews = 50  # Minimum number of reviews to retrieve

    extractor = ReviewExtractor(url)
    extractor.run(min_reviews)
