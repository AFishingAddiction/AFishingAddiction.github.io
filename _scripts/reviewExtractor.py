import logging
import os
import sys
import time
import yaml

from typing import Tuple

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO").upper())
logger = logging.getLogger()


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
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        # Set up the Edge driver (replace with the path to your msedgedriver)
        edgedriver_path = "msedgedriver.exe"
        service = Service(edgedriver_path)

        # Create a new instance of the Chrome driver
        self.driver = webdriver.Edge(service=service, options=options)

    def wait_for_element_on_page(
        self, selector: Tuple, max_time: int = 10
    ) -> WebElement:
        logger.info(f"Waiting {max_time}s for element to appear: {str(selector)}")
        return WebDriverWait(self.driver, max_time).until(
            EC.visibility_of_element_located(selector)
        )

    def gracefully_wait_for_element_on_page(
        self, selector: Tuple, max_time: int = 10
    ) -> WebElement:
        try:
            return self.wait_for_element_on_page(selector, max_time)
        except TimeoutException:
            logger.info(f"Timed out waiting for element to appear: {str(selector)}")

    def wait_for_element_to_disappear(
        self, selector: Tuple, max_time: int = 10
    ) -> WebElement:
        logger.info(f"Waiting {max_time}s for element to disappear: {str(selector)}")
        return WebDriverWait(self.driver, max_time).until(
            EC.invisibility_of_element_located(selector)
        )

    def wait_for_element_to_be_stale(self, element, max_time):
        WebDriverWait(self.driver, max_time).until(EC.staleness_of(element))


class CabelasReviewExtractor(ReviewExtractor):
    REVIEWS_BUTTON_XPATH = '//*[@id="BPS_rating_summary"]/div/button/div[3]/div'
    REVIEWS_SELECTOR = "#BVRRContainer > div > div > div > div > ol > li > div > div.bv-content-container > div > div.bv-content-details-offset-off > div > div > div.bv-content-summary-body-text > p"
    LOAD_MORE_BUTTON_SELECTOR = "#BVRRContainer > div > div > div > div > div.bv-content-pagination > div > ul > li.bv-content-pagination-buttons-item.bv-content-pagination-buttons-item-next > a"

    def extract_reviews(self, url, min_reviews):
        # Visit the URL
        self.driver.get(url)
        reviews_button = self.driver.find_element(By.XPATH, self.REVIEWS_BUTTON_XPATH)
        WebDriverWait(self.driver, 10).until(EC.visibility_of(reviews_button))
        if reviews_button.is_displayed():
            reviews_button.click()
            logger.info("Review button clicked")

        self.popup_closed = False

        # Extract the reviews
        while len(self.reviews) < min_reviews:

            review_elements = self.driver.find_elements(
                By.CSS_SELECTOR, self.REVIEWS_SELECTOR
            )
            # print(review_elements)
            self.reviews.extend(
                [
                    review.text.replace("\n", " ").strip()
                    for review in review_elements
                    if review.text.strip()
                ]
            )
            logger.info(f"Gathered a total of {len(self.reviews)} reviews")

            self.check_and_clear_popup()

            # Check if there is a "Load More" button
            load_more_button = self.gracefully_wait_for_element_on_page(
                (By.CSS_SELECTOR, self.LOAD_MORE_BUTTON_SELECTOR), 10
            )
            if not load_more_button:
                break
            self.check_and_clear_popup()
            # Click the "Load More" button
            load_more_button.click()

            # Wait for the new reviews to load
            self.wait_for_element_to_be_stale(load_more_button, 10)

            # Wait for a short interval to ensure all reviews are loaded
            time.sleep(5)

        # Close the Chrome driver
        self.driver.quit()
        return self.reviews

    def check_and_clear_popup(self):
        if not self.popup_closed:
            popup_close_button_selector = (
                By.CSS_SELECTOR,
                "#bluecoreActionScreen > div.close_button-152678-position.close_button-152678-position-d0.bcTextShadow > button",
            )
            popup_close_button = self.gracefully_wait_for_element_on_page(
                popup_close_button_selector, 5
            )
            if popup_close_button:
                popup_close_button.click()
                self.wait_for_element_to_disappear(popup_close_button_selector, 5)
                self.popup_closed = True

    def run(self, url, min_reviews):
        return self.extract_reviews(url, min_reviews)


class YAMLHelper:
    @staticmethod
    def print(var):
        logger.info("Printing a var formatted as YAML")
        print(yaml.dump(var, allow_unicode=True, width=1024))


if __name__ == "__main__":
    # Get the URL from the command line argument
    if len(sys.argv) < 2:
        print("Please provide a URL as a command line argument.")
        sys.exit(1)

    url = sys.argv[1]

    # Extract and print the reviews
    min_reviews = 50  # Minimum number of reviews to retrieve

    extractor = CabelasReviewExtractor()
    reviews = extractor.run(url, min_reviews)

    YAMLHelper.print(reviews)
