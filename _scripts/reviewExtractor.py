import logging
import os
import sys
import time
import urllib.parse
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

IMPACT_AFA_ACCOUNT_ID = 4236519
IMPACT_AFA_MEDIA_PROPERTY_ID = 4301075
IMPACT_AFA_SECONDARY_ID = 132065
IMPACT_CABELAS_CAMPAIGN_ID = 2623
IMPACT_URL_INTEGRATION_SOURCE = "PUI2_895"


class Product:
    url: str
    __name: str
    __brand: str
    __buy_url: str
    __rating: str
    __sku: str
    reviews: set

    def __init__(self, url) -> None:
        self.url = url
        self.reviews = set()

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
    def buy_url(self) -> str:
        return self.__buy_url

    @buy_url.setter
    def buy_url(self, buy_url: str):
        self.__buy_url = buy_url.strip()

    @property
    def rating(self) -> float:
        return float(self.__rating) if self.__rating else ""

    @rating.setter
    def rating(self, rating: str):
        self.__rating = float(rating.strip()) if rating else None

    @property
    def sku(self) -> str:
        return self.__sku

    @sku.setter
    def sku(self, sku: str):
        self.__sku = sku.strip()

    def add_reviews(self, reviews: list):
        self.reviews.update(set(reviews))


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
    PRODUCT_SKU_SELECTOR = (
        By.CSS_SELECTOR,
        "input[name='tm_Sku_Id']",
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

    def find_product_sku(self):
        while True:
            sku = self.driver.execute_script(
                f'return document.querySelector("{self.PRODUCT_SKU_SELECTOR[1]}").value'
            )
            if sku:
                self.product.sku = sku
                logger.info(f"Found product sku: '{self.product.sku}'")
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

            # Check if there is a "Load More" button
            load_more_button = self.gracefully_wait_for_element_to_be_clickable(
                (By.CSS_SELECTOR, self.LOAD_MORE_BUTTON_SELECTOR), 5
            )
            if not load_more_button:
                break
            logger.info("Found load_more_button")
            self.check_and_clear_popup()
            load_more_button = self.gracefully_wait_for_element_to_be_clickable(
                (By.CSS_SELECTOR, self.LOAD_MORE_BUTTON_SELECTOR), 5
            )
            # Click the "Load More" button
            if load_more_button:
                logger.info("Getting ready to click load_more_button")
                try:
                    load_more_button.click()

                    # Wait for the new reviews to load
                    self.wait_for_element_to_be_stale(load_more_button, 10)
                except ElementClickInterceptedException:
                    continue
            else:
                break

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

    def find_product_buy_url(self):
        encoded_url_params = urllib.parse.urlencode(
            {
                "prodsku": self.product.sku,
                "u": self.product.url,
                "intsrc": IMPACT_URL_INTEGRATION_SOURCE,
                "subId1": "SHORTENED_PAGE_ID",
            }
        )
        self.product.buy_url = f"https://cabelas.xhuc.net/c/{IMPACT_AFA_ACCOUNT_ID}/{IMPACT_AFA_SECONDARY_ID}/{IMPACT_CABELAS_CAMPAIGN_ID}?{encoded_url_params}"

    def run(self, min_reviews):
        # Visit the URL
        self.driver.get(url)
        self.popup_closed = False
        self.find_product_name()
        self.find_product_brand()
        self.find_product_rating()
        self.find_product_sku()
        self.find_product_buy_url()

        self.check_and_clear_popup()
        self.extract_reviews(min_reviews)


class MyDumper(yaml.SafeDumper):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_representer(
            type(None),
            lambda dumper, value: dumper.represent_scalar("tag:yaml.org,2002:null", ""),
        )

    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)


class YAMLProductHelper:
    CHAT_GPT_REVIEW_SUMMARY_PROMPT = """PROMPT:
I want you to act like a fishing expert. I will provide you with a list of reviews for a single fishing product. It is your job to create a summary of the reviews to provide to your bass angler followers. I want you to take only the product reviews I provide in this prompt and not consider any reviews from any previous prompts. When referring to the people that have provided the reviews, refer to them as "anglers" and not "users" or "reviewers".

You will aggregate the reviews and highlight the product's distinct "pros" and "cons" in 2 lists. Please format the pros and cons in a YAML list so that I can copy and paste into my YAML file. The keys for the lists should be "pros" and "cons". For each of the items in the list, don't include a colon. Instead, replace the colon with a hyphen. Each of the items in the list should contain a short title, a hyphen, and a description of the pro or con.

Here are the reviews for the "{product_name}":
{yaml_reviews}

Don't forget about the formatting!

After you give me the list of the pros and cons, I also want you to write a summarized review as if it were my own personalized review with personal experience. The summary should be 2 paragraphs with 3 sentences each. Do not format the review in YAML. In the summary, do not introduce me or address the audience. Only focus on the product."""

    @staticmethod
    def print(var):
        print(yaml.dump(var, allow_unicode=True, width=1024))

    @staticmethod
    def star_rating(rating):
        empty_stars = half_stars = 0
        full_stars = floor(rating)
        remaining_stars = rating - full_stars
        if remaining_stars <= 0.32:
            empty_stars += 1
        elif remaining_stars >= 0.78:
            full_stars += 1
        else:
            half_stars += 1
        empty_stars += 5 - full_stars - empty_stars - half_stars
        return (
            ('<i class="fas fa-star">' * full_stars)
            + ('<i class="fas fa-star-half"></i>' * half_stars)
            # + ('<i class="fas fa-star-o">' * empty_stars)
        )

    @staticmethod
    def print_product_markdown(product: Product):
        print(
            yaml.dump(
                {
                    "products": {
                        "category": [YAMLProductHelper.markdown_mapper(product)]
                    }
                },
                Dumper=MyDumper,
                allow_unicode=True,
                sort_keys=False,
                width=inf,
            )
        )

    @staticmethod
    def markdown_mapper(product):
        return {
            "banner": None,
            "banner_class": "primary|secondary|tertiary|quaternary",
            "product": product.name,
            "url": product.url,
            "sku": product.sku,
            "brand": product.brand,
            "rating": product.rating,
            "rating_stars": YAMLProductHelper.star_rating(product.rating),
            "buy_url": product.buy_url,
            "image_link": None,
            # "prime": None,
            "length": None,
            "weight": None,
            "type": None,
            "hooks": None,
            "blade_type": None,
            "features": [None],
            "pieces": 1,
            "summarized_reviews": None,
            "pros": [None],
            "cons": [None],
            "personal_review": None,
        }

    @staticmethod
    def print_product_review_prompt(product: Product):
        if not product.reviews:
            return
        print(
            YAMLProductHelper.CHAT_GPT_REVIEW_SUMMARY_PROMPT.format(
                product_name=product.name,
                yaml_reviews=yaml.dump(list(product.reviews), allow_unicode=True, width=4096)
            )
        )


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
