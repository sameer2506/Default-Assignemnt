import random
import time

from selenium import webdriver

import constant as cons
from google_sheet_manager import GoogleSheetManager


class Bot:
    def __init__(self, delay=5):
        print("Starting driver")
        self.delay = delay
        driver_location = "/usr/bin/chromedriver"
        self.driver = webdriver.Chrome(executable_path=driver_location)

    def close_session(self):
        print("Closing session")
        self.driver.close()
        manager.close_session()

    def search_key(self, job):
        search_input = self.driver.find_element_by_xpath(cons.job_role_input_type)
        search_input.send_keys(job)
        time.sleep(random.randint(15, 20))
        button = self.driver.find_element_by_xpath(cons.btn_search)
        button.click()
        button.click()
        time.sleep(random.randint(15, 20))

    def get_position_data(self, data):
        company_name = data.find_element_by_css_selector("h3[class='company_info']").text
        website_link = data.find_element_by_class_name('website-link__item')
        website = website_link.get_attribute('href')
        location = data.find_element_by_class_name('locality').text

        company_details = data.text

        rating = company_details.split('\n')[1]
        reviews = company_details.split('\n')[2]
        hourly_rate = company_details.split('\n')[4]
        min_project_size = company_details.split('\n')[3]
        employee_size = company_details.split('\n')[5]
        print(company_name)
        result = [company_name, website, location, rating, reviews, hourly_rate, min_project_size, employee_size]
        return result

    def run(self, job):
        print("Opening website")
        self.driver.maximize_window()
        self.driver.get(cons.website_url)
        time.sleep(random.randint(15, 20))

        self.search_key(job)

        company_list_detail = []

        companies = self.driver.find_elements_by_class_name("provider-row")

        for company in companies:
            time.sleep(random.randint(15, 20))
            data = self.get_position_data(company)
            company_list_detail.append(data)

        manager.append_rows(company_list_detail)

        print("Done scraping")
        bot.close_session()


if __name__ == "__main__":
    manager = GoogleSheetManager(credentials_path=cons.credentials_path, sheet_id=cons.sheet_id)
    manager.start_session()

    bot = Bot()
    job_role = "Mobile App Development"
    bot.run(job_role)
