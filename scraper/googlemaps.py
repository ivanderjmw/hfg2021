# -*- coding: utf-8 -*-
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotInteractableException, ElementClickInterceptedException
from bs4 import BeautifulSoup
from datetime import datetime
import time
import re
import logging
import traceback

GM_WEBPAGE = 'https://www.google.com/maps/'
MAX_WAIT = 10
MAX_RETRY = 5
MAX_SCROLLS = 40


PLACE_TEMPLATE = {
    "Name": "",
    "Rating": 0,
    "Address": "",
    "Contact": ""
}

class GoogleMapsScraper:

    search_results = []

    def __init__(self, debug=False):
        self.debug = debug
        self.driver = self.__get_driver()
        self.logger = self.__get_logger()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)

        self.driver.close()
        self.driver.quit()

        return True

    def __parse_results(self, result):
        item = {}

        name = result.find('h3', class_="section-result-title").find('span').text
        try:
            rating = float(result.find('span', class_="section-result-rating")['aria-label'].strip().split(' ')[0])
        except Exception as e:
            rating = None
        details = result.find('span', class_="section-result-details").text
        address = result.find('span', class_="section-result-location").text
        phone_number = result.find('span', class_="section-result-phone-number").find('span').text

        item["name"] = name
        item["details"] = details
        item["rating"] = rating
        item["address"] = address
        item["contact"] = phone_number

        # print("\n".join("{}\t{}".format(k, v) for k, v in item.items()))

        return item

    def get_results_data(self, offset):

        # Implementation for HFG 2021
        response = BeautifulSoup(self.driver.page_source, 'html.parser')
        rblock = response.find_all('div', class_='section-result-text-content')
        parsed_results = []
        for index, result in enumerate(rblock):
            if index >= offset:
                parsed_results.append(self.__parse_results(result))
                print(self.__parse_results(result))

        return parsed_results

    def more_results(self):
        next_button = self.driver.find_element_by_id('n7lv7yjyC35__section-pagination-button-next')
        print(next_button.tag_name)
        try:
            next_button.click()
        except (ElementNotInteractableException, ElementClickInterceptedException):
            return -1
        time.sleep(5)
        return 0


    def get_reviews(self, offset):

        # scroll to load reviews

        # wait for other reviews to load (ajax)
        time.sleep(4)

        self.__scroll()


        # expand review text
        self.__expand_reviews()

        # parse reviews
        response = BeautifulSoup(self.driver.page_source, 'html.parser')
        rblock = response.find_all('div', class_='section-review-content')
        parsed_reviews = []
        for index, review in enumerate(rblock):
            if index >= offset:
                parsed_reviews.append(self.__parse(review))
                print(self.__parse(review))

        return parsed_reviews

    def get_search_page(self, url):

        self.driver.get(url)

        time.sleep(4)

        return

    def get_account(self, url):

        self.driver.get(url)

        # ajax call also for this section
        time.sleep(4)

        resp = BeautifulSoup(self.driver.page_source, 'html.parser')

        place_data = self.__parse_place(resp)

        return place_data


    def __parse(self, review):

        item = {}

        id_review = review.find('button', class_='section-review-action-menu')['data-review-id']
        username = review.find('div', class_='section-review-title').find('span').text

        try:
            review_text = self.__filter_string(review.find('span', class_='section-review-text').text)
        except Exception as e:
            review_text = None

        rating = float(review.find('span', class_='section-review-stars')['aria-label'].split(' ')[1])
        relative_date = review.find('span', class_='section-review-publish-date').text

        try:
            n_reviews_photos = review.find('div', class_='section-review-subtitle').find_all('span')[1].text
            metadata = n_reviews_photos.split('\xe3\x83\xbb')
            if len(metadata) == 3:
                n_photos = int(metadata[2].split(' ')[0].replace('.', ''))
            else:
                n_photos = 0

            idx = len(metadata)
            n_reviews = int(metadata[idx - 1].split(' ')[0].replace('.', ''))

        except Exception as e:
            n_reviews = 0
            n_photos = 0

        user_url = review.find('a')['href']

        item['id_review'] = id_review
        item['caption'] = review_text

        # depends on language, which depends on geolocation defined by Google Maps
        # custom mapping to transform into date shuold be implemented
        item['relative_date'] = relative_date

        # store datetime of scraping and apply further processing to calculate
        # correct date as retrieval_date - time(relative_date)
        item['retrieval_date'] = datetime.now()
        item['rating'] = rating
        item['username'] = username
        item['n_review_user'] = n_reviews
        item['n_photo_user'] = n_photos
        item['url_user'] = user_url

        return item


    def __parse_place(self, response):

        place = {}
        try:
            place['overall_rating'] = float(response.find('div', class_='gm2-display-2').text.replace(',', '.'))
        except:
            place['overall_rating'] = 'NOT FOUND'

        try:
            place['n_reviews'] = int(response.find('div', class_='gm2-caption').text.replace('.', '').replace(',','').split(' ')[0])
        except:
            place['n_reviews'] = 0

        return place

    # expand review description
    def __expand_reviews(self):
        # use XPath to load complete reviews
        links = self.driver.find_elements_by_xpath('//button[@class=\'section-expand-review blue-link\']')
        for l in links:
            l.click()
        time.sleep(2)

    # load more reviews
    def more_reviews(self):
        # use XPath to load complete reviews
        #allxGeDnJMl__text gm2-button-alt
        #<button ved="1i:1,t:18519,e:0,p:kPkcYIz-Dtql-QaL1YawDw:1969" jstcache="1202" jsaction="pane.reviewChart.moreReviews" class="gm2-button-alt jqnFjrOWMVU__button-blue" jsan="7.gm2-button-alt,7.jqnFjrOWMVU__button-blue,0.ved,22.jsaction">14 reviews</button>
        #<button aria-label="14 reviews" vet="3648" jsaction="pane.rating.moreReviews" jstcache="1010" class="widget-pane-link" jsan="7.widget-pane-link,0.aria-label,0.vet,0.jsaction">14 reviews</button>
        links = self.driver.find_elements_by_xpath('//button[@jsaction=\'pane.reviewChart.moreReviews\']')
        print('LINKS HERE', links)
        for l in links:
            l.click()
        time.sleep(2)


    def __scroll(self):
        scrollable_div = self.driver.find_element_by_css_selector('div.section-layout.section-scrollbox.scrollable-y.scrollable-show')
        self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
        #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


    def __get_logger(self):
        # create logger
        logger = logging.getLogger('googlemaps-scraper')
        logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        fh = logging.FileHandler('gm-scraper.log')
        fh.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # add formatter to ch
        fh.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(fh)

        return logger


    def __get_driver(self, debug=False):
        options = Options()

        if not self.debug:
            options.add_argument("--headless")
        else:
            options.add_argument("--window-size=1366,768")

        options.add_argument("--disable-notifications")
        options.add_argument("--lang=en-GB")
        input_driver = webdriver.Chrome(chrome_options=options)

        return input_driver


    # util function to clean special characters
    def __filter_string(self, str):
        strOut = str.replace('\r', ' ').replace('\n', ' ').replace('\t', ' ')
        return strOut