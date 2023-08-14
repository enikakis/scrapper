from time import sleep
from webbrowser import Chrome
from selenium.webdriver.common.by import By


class Scraper(object):
    VERIFY_LOGIN_ID = "global-nav-search"
    REMEMBER_PROMPT = 'remember-me-prompt__form-primary'
    NAME = 'text-heading-xlarge'

    def __init__(self, driver: Chrome):
        self.driver = driver

    def is_signed_in(self):
        try:
            self.driver.find_element(By.ID, self.VERIFY_LOGIN_ID)
            return True
        except:
            pass
        return False

    def __find_element_by_class_name__(self, class_name):
        try:
            self.driver.find_element(By.CLASS_NAME, class_name)
            return True
        except:
            pass
        return False

    def __find_element_by_xpath__(self, tag_name):
        try:
            self.driver.find_element(By.XPATH, tag_name)
            return True
        except:
            pass
        return False

    def __find_enabled_element_by_xpath__(self, tag_name):
        try:
            elem = self.driver.find_element(By.XPATH, tag_name)
            return elem.is_enabled()
        except:
            pass
        return False

    def _find_element_contains_text(self, text):
        try:
            elem = self.driver.find_element(
                By.XPATH, "//*[contains(text(), " + text + ")]")
            return elem.is_enabled()
        except:
            pass
        return False

    def _scroll_page_down(self):
        self.driver.execute_script(
            'window.scrollTo(0, document.body.scrollHeight);')

    def _scroll_page_up(self):
        self.driver.execute_script(
            'window.scrollTo(0, -document.body.scrollHeight);')
