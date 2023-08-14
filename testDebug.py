from os import path
from selenium import webdriver
from scraper.constants import Constants as c
from scraper.account import Account
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from scraper.person import Person
from openpyxl import Workbook, load_workbook
import pandas as pd

crome_path = path.abspath("chrome_driver/chromedriver")
ser = Service(crome_path)
driver = webdriver.Chrome(service=ser)
account = Account(driver)
account.login(c.email, c.password)
url = c.testUrls[8]
my_person = Person(driver, url)
