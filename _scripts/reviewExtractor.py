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
    def __init__(self):
        self.clear_reviews()
        self.setup_driver()

    def clear_reviews(self):
        self.reviews = []

    def setup_driver(self):
        # Set up Selenium options
        options = Options()
        options.add_argument("--guest")

        # Set up the Edge driver (replace with the path to your msedgedriver)
        edgedriver_path = "msedgedriver.exe"
        service = Service(edgedriver_path)

        # Create a new instance of the Chrome driver
        self.driver = webdriver.Edge(service=service, options=options)

class CabelasReviewExtractor(ReviewExtractor):
    REVIEWS_BUTTON_XPATH = '//*[@id="BPS_rating_summary"]/div/button/div[3]/div'
    REVIEWS_SELECTOR = '#BVRRContainer > div > div > div > div > ol > li > div > div.bv-content-container > div > div.bv-content-details-offset-off > div > div > div.bv-content-summary-body-text > p'
    LOAD_MORE_BUTTON_SELECTOR = "#BVRRContainer > div > div > div > div > div.bv-content-pagination > div > ul > li.bv-content-pagination-buttons-item.bv-content-pagination-buttons-item-next > a"


    def extract_reviews(self, url, min_reviews):
        # Visit the URL
        self.driver.get(url)
        reviews_button = self.driver.find_element(
            By.XPATH, self.REVIEWS_BUTTON_XPATH
        )
        WebDriverWait(self.driver, 10).until(EC.visibility_of(reviews_button))
        if reviews_button.is_displayed():
            reviews_button.click()
            print("Review button clicked")

        # Extract the reviews
        while len(self.reviews) < min_reviews:

            review_elements = self.driver.find_elements(By.CSS_SELECTOR, self.REVIEWS_SELECTOR)
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
            load_more_button = self.driver.find_element(
                By.CSS_SELECTOR, self.LOAD_MORE_BUTTON_SELECTOR
            )
            if load_more_button.is_displayed():
                # Click the "Load More" button
                load_more_button.click()

                # Wait for the new reviews to load
                WebDriverWait(self.driver, 10).until(EC.staleness_of(load_more_button))

                # Wait for a short interval to ensure all reviews are loaded
                time.sleep(5)

            else:
                # No more reviews to load, break the loop
                break

        time.sleep(60)
        # Close the Chrome driver
        self.driver.quit()

    def create_yaml_list(self, min_reviews):
        # Format reviews as a YAML bullet list
        return yaml.dump(self.reviews, allow_unicode=True, width=1024)

    def run(self, url, min_reviews):
        self.extract_reviews(url, min_reviews)
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

    extractor = CabelasReviewExtractor()
    extractor.run(url, min_reviews)
