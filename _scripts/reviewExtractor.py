import logging
import os
import sys
import time
import yaml

from math import floor, inf
from typing import Tuple

from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO").upper())
logger = logging.getLogger()


class Product:
    url: str
    __name: str
    __brand: str
    __rating: str
    reviews: list

    def __init__(self, url) -> None:
        self.url = url
        self.reviews = []

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name.strip()

    @property
    def brand(self) -> str:
        return self.__brand

    @brand.setter
    def brand(self, brand: str):
        self.__brand = brand.strip()

    @property
    def rating(self) -> float:
        return float(self.__rating) if self.__rating else ""

    @rating.setter
    def rating(self, rating: str):
        self.__rating = float(rating.strip()) if rating else None

    def add_reviews(self, reviews: list):
        self.reviews.extend(reviews)


class ReviewExtractor:
    product: Product = None

    def __init__(self, product):
        self.product = product
        self.setup_driver()

    def setup_driver(self):
        # Set up Selenium options
        options = Options()
        options.add_argument("--guest")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument(
            "user-data-dir={}".format(os.path.join(os.getcwd(), ".browser_profile"))
        )

        # Set up the Edge driver (replace with the path to your msedgedriver)
        edgedriver_path = "msedgedriver.exe"
        service = Service(edgedriver_path)

        # Create a new instance of the Chrome driver
        self.driver = webdriver.Edge(service=service, options=options)
        self.driver.set_page_load_timeout(600)

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

    def wait_for_element_to_be_clickable(self, selector: Tuple, max_time: int = 10):
        return WebDriverWait(self.driver, max_time).until(
            EC.element_to_be_clickable(selector)
        )

    def gracefully_wait_for_element_to_be_clickable(
        self, selector: Tuple, max_time: int = 10
    ) -> WebElement:
        try:
            return self.wait_for_element_to_be_clickable(selector, max_time)
        except TimeoutException:
            logger.info(
                f"Timed out waiting for element to be clickable: {str(selector)}"
            )


class CabelasReviewExtractor(ReviewExtractor):
    PRODUCT_NAME_SELECTOR = (
        By.CSS_SELECTOR,
        "div.namePartPriceContainer div h1.main_header",
    )
    PRODUCT_BRAND_SELECTOR = (
        By.CSS_SELECTOR,
        "input[name='tm_Prod_Brnd']",
    )
    PRODUCT_AVG_REVIEW_SELECTOR = (
        By.CSS_SELECTOR,
        "div.bv_avgRating_component_container",
    )
    REVIEWS_BUTTON_XPATH = '//*[@id="BPS_rating_summary"]/div/button/div[3]/div'
    REVIEWS_SELECTOR = "#BVRRContainer > div > div > div > div > ol > li > div > div.bv-content-container > div > div.bv-content-details-offset-off > div > div > div.bv-content-summary-body-text > p"
    LOAD_MORE_BUTTON_SELECTOR = "#BVRRContainer > div > div > div > div > div.bv-content-pagination > div > ul > li.bv-content-pagination-buttons-item.bv-content-pagination-buttons-item-next > a"

    def find_product_name(self):
        while True:
            product_name_elem = self.gracefully_wait_for_element_on_page(
                self.PRODUCT_NAME_SELECTOR, 15
            )
            if product_name_elem:
                self.product.name = product_name_elem.text
                logger.info(f"Found product name: '{self.product.name}'")
                break
            else:
                self.check_and_clear_popup()

    def find_product_brand(self):
        while True:
            brand = self.driver.execute_script(
                f'return document.querySelector("{self.PRODUCT_BRAND_SELECTOR[1]}").value'
            )
            if brand:
                self.product.brand = brand
                logger.info(f"Found product brand: '{self.product.brand}'")
                break
            else:
                self.check_and_clear_popup()

    def find_product_rating(self):
        while True:
            product_rating_elem = self.gracefully_wait_for_element_on_page(
                self.PRODUCT_AVG_REVIEW_SELECTOR, 15
            )
            if product_rating_elem:
                self.product.rating = product_rating_elem.text
                logger.info(f"Found product rating: '{self.product.rating}'")
                break
            else:
                self.check_and_clear_popup()

    def extract_reviews(self, min_reviews):
        while True:
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, self.REVIEWS_BUTTON_XPATH)
                    )
                )
                reviews_button = self.wait_for_element_to_be_clickable(
                    (By.XPATH, self.REVIEWS_BUTTON_XPATH), 5
                )
                # Click the "Load More" button
                reviews_button.click()
                logger.info("Review button clicked")
                self.check_and_clear_popup()
                break
            except:
                continue

        # Extract the reviews
        while len(self.product.reviews) < min_reviews:

            review_elements = self.driver.find_elements(
                By.CSS_SELECTOR, self.REVIEWS_SELECTOR
            )
            self.product.add_reviews(
                [
                    review.text.replace("\n", " ").strip()
                    for review in review_elements
                    if review.text.strip()
                ]
            )
            logger.info(f"Gathered a total of {len(self.product.reviews)} reviews")

            self.check_and_clear_popup()

            # WebDriverWait(self.driver, 5).until(
            #     EC.presence_of_element_located((By.CSS_SELECTOR, self.LOAD_MORE_BUTTON_SELECTOR))
            # )
            # Check if there is a "Load More" button
            load_more_button = self.gracefully_wait_for_element_to_be_clickable(
                (By.CSS_SELECTOR, self.LOAD_MORE_BUTTON_SELECTOR), 5
            )
            if not load_more_button:
                break
            self.check_and_clear_popup()
            # WebDriverWait(self.driver, 5).until(
            #     EC.presence_of_element_located((By.CSS_SELECTOR, self.LOAD_MORE_BUTTON_SELECTOR))
            # )
            load_more_button = self.gracefully_wait_for_element_to_be_clickable(
                (By.CSS_SELECTOR, self.LOAD_MORE_BUTTON_SELECTOR), 5
            )
            # Click the "Load More" button
            if load_more_button:
                try:
                    load_more_button.click()

                    # Wait for the new reviews to load
                    self.wait_for_element_to_be_stale(load_more_button, 10)
                except ElementClickInterceptedException:
                    continue

            # Wait for a short interval to ensure all reviews are loaded
            time.sleep(5)

        # Close the Chrome driver
        self.driver.quit()

    def check_and_clear_popup(self):
        if not self.popup_closed:
            popup_close_button_selector = (
                By.CSS_SELECTOR,
                "#bluecoreActionScreen > div.close_button-152678-position.close_button-152678-position-d0.bcTextShadow > button",
            )
            popup_close_button = self.gracefully_wait_for_element_to_be_clickable(
                popup_close_button_selector, 15
            )
            if popup_close_button:
                popup_close_button.click()
                self.wait_for_element_to_disappear(popup_close_button_selector, 5)
                self.popup_closed = True

    def run(self, min_reviews):
        # Visit the URL
        self.driver.get(url)
        self.popup_closed = False
        self.find_product_name()
        self.find_product_brand()
        self.find_product_rating()

        # self.check_and_clear_popup()
        # self.extract_reviews(min_reviews)


class YAMLProductHelper:
    CHAT_GPT_REVIEW_SUMMARY_PROMPT = """I want you to act like a fishing expert. I will provide you with a list of reviews for a single fishing product. It is your job to create a summary of the reviews to provide to your bass angler followers. I want you to take only the product reviews I provide in this prompt and not consider any reviews from any previous prompts. You will aggregate the reviews and highlight the product's distinct strengths and weaknesses in 2 bullet lists. Each bullet in the list will contain a title, followed by a hyphen, followed by a brief description of that point. The bullet list will be formatted as a markdown list.
For example:
"- Title - Description
- Title 2 - Description 2"

I also want you to write a summarized review as if it were my own personalized review with personal experience. The summary should be 2 paragraphs with 3 sentences each. In the summary, do not introduce me or address the audience. Only focus on the product. When referring to the people that have provided the reviews, refer to them as "anglers" and not "users" or "reviewers".

Here are the reviews for the "{product_name}":"""

    @staticmethod
    def print(var):
        print(yaml.dump(var, allow_unicode=True, width=1024))

    @staticmethod
    def print_product_markdown(product: Product):
        print(
            yaml.dump(
                {
                    "products": {
                        "category": [
                            {
                                "banner": "",
                                "banner_class": "",
                                "product": product.name,
                                "brand": product.brand,
                                "rating": product.rating,
                            }
                        ]
                    }
                },
                allow_unicode=True,
            )
        )

    @staticmethod
    def print_product_review_prompt(product: Product):
        print(
            YAMLProductHelper.CHAT_GPT_REVIEW_SUMMARY_PROMPT.format(
                product_name=product.name
            )
        )
        YAMLProductHelper.print(product.reviews)


if __name__ == "__main__":
    # Get the URL from the command line argument
    if len(sys.argv) < 2:
        print("Please provide a URL as a command line argument.")
        sys.exit(1)

    url = sys.argv[1]

    # Extract and print the reviews
    min_reviews = 50  # Minimum number of reviews to retrieve

    product = Product(url)

    extractor = CabelasReviewExtractor(product)
    extractor.run(min_reviews)

    YAMLProductHelper.print_product_markdown(product)
    YAMLProductHelper.print_product_review_prompt(product)
