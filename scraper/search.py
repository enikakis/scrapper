
# That class help us to find page urls for the items we are searching
from time import sleep
from webbrowser import Chrome
from bs4 import BeautifulSoup
from scraper.scraper import Scraper
from selenium.webdriver.common.by import By


class Search(Scraper):

    location_btn_text = "Locations"
    current_page = 0
    results_url_array = []

    def __init__(self, driver: Chrome, search_value: str, search_type: str, location=None, pages_limit=3):
        super().__init__(driver)
        self.search_value = search_value
        self.search_type = search_type
        self.location = location
        self.pages_limit = pages_limit

    # Makes search url for navigation
    def __make_search_url(self):
        search_linkedin_url = "https://www.linkedin.com/search/results"
        location_param = self._get_location_param(self.location)
        if location_param != None:
            search_linkedin_url = search_linkedin_url + "/" + self.search_type + \
                "/" + location_param + "keywords=" + self.search_value
        else:
            search_linkedin_url = search_linkedin_url + "/" + \
                self.search_type + "/keywords=" + self.search_value
        return search_linkedin_url

    # Search and find items urls for given pages
    def search(self):
        if self.is_signed_in():
            search_url = self.__make_search_url()
            print("navigate to url: ", search_url)
            self.driver.get(search_url)
            self.current_page = 0
            page_limit = self.pages_limit if self.pages_limit else 100
            while self.current_page < page_limit:
                sleep(2)
                self.current_page += 1
                self.results_url_array.extend(
                    self.get_page_urls())
                self._scroll_page_down()
                sleep(2)
                next_button_xpath = '//button[@aria-label="Next"]'
                if self.__find_enabled_element_by_xpath__(next_button_xpath) == False:
                    print("next button is disabled")
                    break
                next_button = self.driver.find_element(
                    By.XPATH, next_button_xpath)
                next_button.click()
        else:
            print("you are not logged in!")

    # Gives items urls for a given page
    def get_page_urls(self):
        page_source = BeautifulSoup(self.driver.page_source)
        items = page_source.find_all('a', class_='app-aware-link')
        items_url = []
        for item in items:
            url = item.get('href')
            if url not in items_url and len(item.find_all('span')) != 0:
                items_url.append(url)
        print(items_url)
        return items_url

    # returns location parameter
    def _get_location_param(self, location):
        if location == "Greece":
            return '''?geoUrn=%5B"104677530"%5D&'''
        elif location == "Attiki":
            return '''?geoUrn=%5B"106238681"%5D&'''
        elif location == "Usa":
            return '''?geoUrn=%5B"103644278"%5D&'''
        elif location == "Germany":
            return '''?geoUrn=%5B"101282230"%5D&'''
        else:
            return None
