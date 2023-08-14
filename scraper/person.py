import logging
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scraper.datamodels import Experience, Education, Accomplishment
from scraper.scraper import Scraper
from bs4 import BeautifulSoup


class Person(Scraper):

    # important values for scrapping
    top_card = "pv-top-card"
    wait_for_element_time_out = 5
    about_div_class = "pv-shared-text-with-see-more t-14 t-normal t-black display-flex align-items-center"
    location_div_class = "pb2 pv-text-details__left-panel"
    accomplishment_section_class = "pv-profile-section pv-accomplishments-section artdeco-card mv4 ember-view"
    accomplishment_block_class = "pv-accomplishments-block__content break-words"
    top_section_class = "artdeco-card ember-view pv-top-card"
    job_div_class = "text-body-medium break-words"
    connections_span_class = "t-bold"
    experience_div_id = "experience"
    education_div_id = "education"
    accomplishment_div_id = "publications"

    def __init__(
            self,
            driver: Chrome,
            name=None,
            about=None,
            experiences=None,
            educations=None,
            accomplishments=None,
            person_url: str = None,
            job_title=None,
            profile_description=None,
            connections=None):
        super().__init__(driver)
        self.person_url = person_url,
        self.name = name
        self.about = about or []
        self.experiences = experiences or []
        self.educations = educations or []
        self.accomplishments = accomplishments or []
        self.job_title = job_title
        self.profile_decription = profile_description or []
        self.connections = connections

        if person_url != None:
            self.driver.get(person_url)
            self.scrape()

    def add_about(self, about):
        self.about.append(about)

    def add_experience(self, experience):
        self.experiences.append(experience)

    def add_education(self, education):
        self.educations.append(education)

    def add_accomplishment(self, accomplishment):
        self.accomplishments.append(accomplishment)

    def add_location(self, location):
        self.location = location

    def add_profile_description(self, item):
        self.profile_decription.append(item)

    def scrape(self):
        if self.is_signed_in():
            self.scrape_logged_in()
        else:
            print("you are not logged in!")

    def scrape_logged_in(self):
        driver = self.driver
        duration = None
        # Starting page source
        page_source = BeautifulSoup(driver.page_source, features="html.parser")

        root = WebDriverWait(driver, self.wait_for_element_time_out).until(
            EC.presence_of_element_located(
                (
                    By.CLASS_NAME,
                    self.top_card,
                )
            )
        )

        # Get profile details

        # 1) name
        try:
            self.name = root.find_element(
                By.CLASS_NAME, self.NAME).text.strip()
        except:
            logging.warning("Name not found")
            self.name = None

        # 2) location
        try:
            location_div = page_source.find(
                "div", {"class": self.location_div_class})
            location = location_div.span.getText().strip()
        except:
            logging.warning("Location not found")
            location = None
        if location:
            self.location = location

        # 3) job title
        try:
            top_section = page_source.find(
                "section", {"class": self.top_section_class})
            job = top_section.find(
                "div", {"class": self.job_div_class}).get_text().strip()
            self.job_title = job
        except:
            logging.warning("Job not found")
            self.job_title = None

        # 4) connections
        try:
            connections = top_section.find(
                "span", {"class": self.connections_span_class}).get_text().strip()
            self.connections = connections
        except:
            logging.warning("Connections not found")
            self.connections = None

        # 5) profile desc
        try:
            for item in top_section.find_all("h2"):
                if item != None:
                    self.add_profile_description(item.div.get_text().strip())
        except:
            logging.warning("Profile desc error")

        # get about
        try:
            about_div = page_source.find(
                'div', {'class': self.about_div_class})
            about = " ".join(about_div.div.text.split())
            # remove "... see more"
            about = about.replace("… see more", "")
        except:
            logging.warning("About text not found")
            about = None
        if about:
            logging.info("About text found")
            self.add_about(about)

        # get experience
        try:
            self.__scroll_and_find_element_by_id(
                self.education_div_id)
            exp_section = driver.find_element(
                By.XPATH, "//section[.//div[@id='{experience}']]".format(experience=self.experience_div_id))
            self._click_section_buttton_by_element(exp_section)
            exp = driver.find_element(
                By.XPATH, "//section[.//div[@id='{experience}']]".format(experience=self.experience_div_id))
        except:
            logging.warning("Experiance section not found")
            exp = None

        if exp is not None:
            for position in exp.find_elements(By.CLASS_NAME, "pv-position-entity"):

                position_title = position.find_element(By.TAG_NAME,
                                                       "h3").text.strip()
                try:
                    company = position.find_elements(By.TAG_NAME, "p")[
                        1].text.strip()
                    times = str(
                        position.find_elements(By.TAG_NAME, "h4")[0]
                        .find_elements(By.TAG_NAME, "span")[1]
                        .text.strip()
                    )
                    from_date = " ".join(times.split(" ")[:2])
                    to_date = " ".join(times.split(" ")[3:])
                    duration = (
                        position.find_elements(By.TAG_NAME, "h4")[1]
                        .find_elements(By.TAG_NAME, "span")[1]
                        .text.strip()
                    )
                    location = (
                        position.find_elements(By.TAG_NAME, "h4")[2]
                        .find_elements(By.TAG_NAME, "span")[1]
                        .text.strip()
                    )
                except:
                    company = None
                    from_date, to_date, duration, location = (
                        None, None, None, None)

                experience = Experience(
                    position_title=position_title,
                    from_date=from_date,
                    to_date=to_date,
                    duration=duration,
                    location=location,
                )
                experience.institution_name = company
                self.add_experience(experience)

        # get education
        try:
            self.__scroll_and_find_element_by_id(self.education_div_id)
            edu = driver.find_element(
                By.XPATH, "//section[.//div[@id='{edu}']]".format(edu=self.education_div_id))
            self._click_section_buttton_by_element(edu)
            edu = driver.find_element(
                By.XPATH, "//section[.//div[@id='{edu}']]".format(edu=self.education_div_id))
        except:
            logging.warning("Education section not found")
            edu = None

        if edu:
            for school in edu.find_elements(By.CLASS_NAME, "pv-profile-section__list-item"):
                university = school.find_element(
                    By.CLASS_NAME, "pv-entity__school-name").text.strip()

                try:
                    degree = (
                        school.find_element(
                            By.CLASS_NAME, "pv-entity__degree-name")
                        .find_elements(By.TAG_NAME, "span")[1]
                        .text.strip()
                    )
                except:
                    logging.warning("Education degree not found")
                    degree = None

                try:
                    times = (
                        school.find_element(By.CLASS_NAME, "pv-entity__dates")
                        .find_elements(By.TAG_NAME, "span")[1]
                        .text.strip()
                    )
                    from_date, to_date = (times.split(
                        " ")[0], times.split(" ")[2])
                except:
                    logging.warning("Education degree time not found")
                    from_date, to_date = (None, None)

                education = Education(
                    from_date=from_date, to_date=to_date, degree=degree
                )
                education.institution_name = university
                self.add_education(education)

        # get accomplishment
        try:
            self.__scroll_and_find_element_by_class(
                self.accomplishment_section_class)
            page_source = BeautifulSoup(
                driver.page_source, features="html.parser")
            acc_section = page_source.find(
                'section', {"class": self.accomplishment_section_class})
            blocks = acc_section.find_all(
                "div", {"class": self.accomplishment_block_class})
            for block in blocks:
                title = block.h3.get_text().strip()
                item_value = []
                for item in block.find_all("li"):
                    item_value.append(item.get_text().strip())
                accomplishment = Accomplishment()
                accomplishment.title = title
                accomplishment.descriptions = item_value
                self.add_accomplishment(accomplishment)
        except:
            logging.warning("Accomplisment not found")
            pass

    def __scroll_and_find_element_by_id(self, id, number_of_scrolls=5):
        self._scroll_page_up()
        sleep(2)
        for scroll in range((number_of_scrolls)):
            self.driver.execute_script(
                "window.scrollTo(0, Math.ceil(document.body.scrollHeight * {scr}/{number}));".format(
                    scr=scroll, number=number_of_scrolls)
            )
            sleep(1)
            try:
                element = self.driver.find_element(By.ID, id)
                if element:
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView(true);", element)
                    return element
            except:
                logging.warning("scroll not found {id}".format(id=id))
                pass
        return None

    def __scroll_and_find_element_by_class(self, class_name, number_of_scrolls=5):
        self._scroll_page_up()
        sleep(2)
        for scroll in range((number_of_scrolls)):
            self.driver.execute_script(
                "window.scrollTo(0, Math.ceil(document.body.scrollHeight * {scr}/{number}));".format(
                    scr=scroll, number=number_of_scrolls)
            )
            sleep(1)
            try:
                element = self.driver.find_element(By.CLASS_NAME, class_name)
                if element:
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView(true);", element)
                    return element
            except:
                pass
        return None

    def _click_section_buttton_by_id(self, section_id):
        try:
            education_section = self.driver.find_element(By.ID, section_id)
            see_more = education_section.find_element(By.TAG_NAME, "button")
            see_more.click()
            sleep(2)
        except Exception as e:
            logging.warning("Button not located in section: %s ", section_id)

    def _click_div_buttton_by_id(self, section_class):
        try:
            education_section = self.driver.find_element(
                By.CLASS_NAME, section_class)
            see_more = education_section.find_element(By.TAG_NAME, "button")
            see_more.click()
            sleep(2)
        except Exception as e:
            logging.warning(
                "Button not located in div with class: %s ", section_class)

    def _click_section_buttton_by_element(self, section_element):
        try:
            education_section = section_element
            see_more = education_section.find_element(By.TAG_NAME, "button")
            see_more.click()
            sleep(2)
        except Exception as e:
            logging.warning(
                "Button not located in section : %s ", section_element)
