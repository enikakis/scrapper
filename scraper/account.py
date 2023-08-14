import getpass
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome

from scraper.scraper import Scraper


class Account(Scraper):

    def __init__(self, driver):
        super().__init__(driver)

    def __prompt_email_password():
        u = input("Email: ")
        p = getpass.getpass(prompt="Password: ")
        return (u, p)

    def _login_with_cookie(self, cookie):
        self.driver.get("https://www.linkedin.com/login")
        self.driver.add_cookie({
            "name": "li_at",
            "value": cookie})

    def logout(self):
        account_btn = self.driver.find_element_by_id("ember36")
        account_btn.click()
        sleep(2)
        WebDriverWait(self.driver, 1).until(
            EC.presence_of_element_located((By.XPATH, '//*[@href="/m/logout/"]')))
        signout_link_btn = self.driver.find_element_by_xpath(
            '//*[@href="/m/logout/"]')
        signout_link_btn.click()
        sleep(2)

    def login(self, email=None, password=None, cookie=None, timeout=10):
        # driver.maximize_window()
        if cookie is not None:
            return self._login_with_cookie(self.driver, cookie)

        if not email or not password:
            email, password = self.__prompt_email_password()

        self.driver.get("https://www.linkedin.com/login")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "username")))

        email_elem = self.driver.find_element_by_id("username")
        email_elem.send_keys(email)

        password_elem = self.driver.find_element_by_id("password")
        password_elem.send_keys(password)
        password_elem.submit()

        try:
            if self.driver.url == 'https://www.linkedin.com/checkpoint/lg/login-submit':
                remember = self.driver.find_element_by_id(self.REMEMBER_PROMPT)
                if remember:
                    remember.submit()

            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.ID, self.VERIFY_LOGIN_ID)))
        except:
            pass

    def is_signed_in(self, driver: Chrome):
        try:
            driver.find_element_by_id(self.VERIFY_LOGIN_ID)
            return True
        except:
            pass
        return False
