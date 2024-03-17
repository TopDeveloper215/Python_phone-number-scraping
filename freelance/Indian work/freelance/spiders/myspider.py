# import scrapy
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service

# class MySpider(scrapy.Spider):
#     name = 'my_spider'
#     start_urls = ['https://www.storia.ro/ro/rezultate/vanzare/apartament/toata-romania?market=ALL&ownerTypeSingleSelect=ALL&by=DEFAULT&direction=DESC&viewType=listing']

#     def __init__(self):
#        service = Service(executable_path='./chromedriver.exe')
#        options = webdriver.ChromeOptions()
#        chrome_options = Options()
#        chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
#        chrome_options.add_argument("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")  # Add your user agent here
#        self.driver = webdriver.Chrome(service=service, options=options)

#     def parse(self, response):
#         # Extract the URLs of the description pages
#         apartment = response.xpath(".//li[@data-cy='listing-item']/a/@href").extract()

#         # Follow each URL to scrape data from the description page
#         for url in apartment:
#             yield response.follow(url, callback=self.parse_description_page)

#     def parse_description_page(self, response):
#         # Click the button to reveal full content
#         button = self.driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/aside/div/div[2]/div[3]/div/button')
#         button.click()

#         # Wait for the full content to load
#         WebDriverWait(self.driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/aside/div/div[2]/div[3]/div/a'))
#         )

#         # Extract full content
#         full_content = self.driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/aside/div/div[2]/div[3]/div/a').text

#         yield {
#             'Number': full_content
#         }

#     def closed(self, reason):
#         self.driver.quit()



# import scrapy
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from urllib.parse import urljoin


# class MySpider(scrapy.Spider):
#     name = 'my_spider'
#     # allowed_domains = ['www.storia.ro']

#     def start_requests(self):
#         # Set a user agent for the requests
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
#         }
        
#         # Start the request with the proper user agent
#         yield scrapy.Request(url='https://www.storia.ro/ro/rezultate/vanzare/apartament/toata-romania?market=ALL&ownerTypeSingleSelect=ALL&by=DEFAULT&direction=DESC&viewType=listing', headers=headers, callback=self.parse)

#     def parse(self, response):
#         # Extract the URLs of the description pages
#         apartments = response.xpath(".//li[@data-cy='listing-item']/a/@href").extract()

        

#         with webdriver.Chrome(service=Service(executable_path='./chromedriver.exe')) as driver:
#             for url in apartments:
#                 full_url = urljoin(response.url, url)  # Create a full URL
#                 driver.get(full_url)

#                 # Click the button to reveal full content
#                 button = WebDriverWait(driver, 10).until(
#                     EC.presence_of_element_located((By.XPATH, '//button[@data-cy="phone-number.show-full-number-button"]'))
#                 )
#                 button.click()

#                 # Wait for the full content to load
#                 full_content = WebDriverWait(driver, 10).until(
#                     EC.presence_of_element_located((By.XPATH, '//a[@data-cy="phone-number.full-phone-number"]'))
#                 ).text

#                 yield {
#                     'Number': full_content
#                 }


# import scrapy
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from urllib.parse import urljoin
# import csv

# class MySpider(scrapy.Spider):
#     name = 'my_spider'

#     def start_requests(self):
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
#         }
        
#         yield scrapy.Request(url='https://www.storia.ro/ro/rezultate/vanzare/apartament/toata-romania?market=ALL&ownerTypeSingleSelect=ALL&by=DEFAULT&direction=DESC&viewType=listing', headers=headers, callback=self.parse)

#     def parse(self, response):
#         apartments = response.xpath(".//li[@data-cy='listing-item']/a/@href").extract()

        

#         data = []

#         with webdriver.Chrome(service=Service(executable_path='./chromedriver.exe')) as driver:
#             for url in apartments:
#                 full_url = urljoin(response.url, url)
#                 driver.get(full_url)

#                 button = WebDriverWait(driver, 10).until(
#                     EC.presence_of_element_located((By.XPATH, '//button[@data-cy="phone-number.show-full-number-button"]'))
#                 )
#                 button.click()

#                 full_content = WebDriverWait(driver, 10).until(
#                     EC.presence_of_element_located((By.XPATH, '//a[@data-cy="phone-number.full-phone-number"]'))
#                 ).text

#                 data.append({'Number': full_content})

#         # Write to CSV
#         with open('output.csv', 'w', newline='') as csvfile:
#             fieldnames = ['Number']
#             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#             writer.writeheader()
#             for item in data:
#                 writer.writerow(item)


import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin
import csv
import time
from selenium.common.exceptions import TimeoutException

class MySpider(scrapy.Spider):
    name = 'my_spider'
    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
        }
        
        yield scrapy.Request(url='https://www.storia.ro/ro/rezultate/vanzare/apartament/toata-romania?market=ALL&ownerTypeSingleSelect=ALL&by=DEFAULT&direction=DESC&viewType=listing', headers=headers, callback=self.parse)

    def parse(self, response):
        data = []

        # Configure the WebDriver
        with webdriver.Chrome(service=Service(executable_path='./chromedriver.exe')) as driver:
            driver.get(response.url)

            while True:
                try:
                    # Extract data from the current page
                    apartments = response.xpath(".//li[@data-cy='listing-item']/a/@href").extract()
                    for url in apartments:
                        full_url = urljoin(response.url, url)
                        driver.get(full_url)

                        button = WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.XPATH, '//button[@data-cy="phone-number.show-full-number-button"]'))
                        )
                        button.click()

                        full_content = WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.XPATH, '//a[@data-cy="phone-number.full-phone-number"]'))
                        ).text

                        data.append({'Number': full_content})

                except TimeoutException:
                    print("TimeoutException: Skipping the current item.")
                    continue

                # Check if there's a next page
                next_button = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, './/button[@data-cy="pagination.next-page"]'))
                )
                if not next_button.is_enabled():
                    break

                # Click the "Next" button to go to the next page
                next_button.click()

                time.sleep(5)

        # Write to CSV
        with open('output.csv', 'w', newline='') as csvfile:
            fieldnames = ['Number']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for item in data:
                writer.writerow(item)

