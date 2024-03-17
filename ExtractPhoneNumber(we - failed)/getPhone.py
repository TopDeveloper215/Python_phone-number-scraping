import pandas as pd
import os
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from getExistingCSV import getExistingCSV
import time
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.134 Safari/537.36'
}


urls = [
    "https://www.storia.ro/ro/rezultate/vanzare/apartament/toata-romania?market=ALL&ownerTypeSingleSelect=ALL&by=DEFAULT&direction=DESC&viewType=listing",
    "https://www.storia.ro/ro/rezultate/vanzare/garsoniere/toata-romania?market=ALL&ownerTypeSingleSelect=ALL&by=DEFAULT&direction=DESC&viewType=listing",
    "https://www.storia.ro/ro/rezultate/vanzare/casa/toata-romania?market=ALL&ownerTypeSingleSelect=ALL&by=DEFAULT&direction=DESC&viewType=listing",
    "https://www.storia.ro/ro/rezultate/vanzare/investitii/toata-romania?market=PRIMARY&by=DEFAULT&direction=DESC&viewType=listing",
    "https://www.storia.ro/ro/rezultate/inchiriere/camera/toata-romania?market=ALL&by=DEFAULT&direction=DESC&viewType=listing",
    "https://www.storia.ro/ro/rezultate/vanzare/teren/toata-romania?market=ALL&by=DEFAULT&direction=DESC&viewType=listing",
    "https://www.storia.ro/ro/rezultate/vanzare/spatiu-comercial/toata-romania?market=ALL&ownerTypeSingleSelect=ALL&by=DEFAULT&direction=DESC&viewType=listing",
    "https://www.storia.ro/ro/rezultate/vanzare/depozite-hale/toata-romania?market=ALL&ownerTypeSingleSelect=ALL&by=DEFAULT&direction=DESC&viewType=listing",
    "https://www.storia.ro/ro/rezultate/vanzare/garaj/toata-romania?market=ALL&ownerTypeSingleSelect=ALL&by=DEFAULT&direction=DESC&viewType=listing",

    "https://www.storia.ro/ro/rezultate/inchiriere/apartament/toata-romania?market=ALL&by=DEFAULT&direction=DESC&viewType=listing",
    "https://www.storia.ro/ro/rezultate/inchiriere/garsoniere/toata-romania?market=ALL&by=DEFAULT&direction=DESC&viewType=listing",
    "https://www.storia.ro/ro/rezultate/inchiriere/casa/toata-romania?market=ALL&by=DEFAULT&direction=DESC&viewType=listing",
    "https://www.storia.ro/ro/rezultate/inchiriere/teren/toata-romania?market=ALL&by=DEFAULT&direction=DESC&viewType=listing",
    "https://www.storia.ro/ro/rezultate/inchiriere/spatiu-comercial/toata-romania?market=ALL&by=DEFAULT&direction=DESC&viewType=listing",
    "https://www.storia.ro/ro/rezultate/inchiriere/depozite-hale/toata-romania?market=ALL&by=DEFAULT&direction=DESC&viewType=listing",
    "https://www.storia.ro/ro/rezultate/inchiriere/garaj/toata-romania?market=ALL&by=DEFAULT&direction=DESC&viewType=listing",

]


def get_data(urls):
    browser_options = ChromeOptions()
    browser_options.headless = False
    browser_options.add_argument("--start-maximized")

    driver = Chrome(options=browser_options)
    job_driver = Chrome(options=browser_options)

    data = []

    for url in urls:
        driver.get(url)
        driver.implicitly_wait(10)
        adLists = driver.find_elements(
            By.CLASS_NAME, "css-1tiwk2i")

        for adIndex in range(len(adLists)):
            if (adIndex < 3):
                continue
            adUrl = adLists[adIndex].get_attribute('href')
            job_driver.get(adUrl)
            print(adUrl)
            driver.implicitly_wait(1000)
            response = requests.get(adUrl, headers=headers)
            print(response.status_code)
            print(response.json())
            # displayShowButton = driver.find_elements(
            #     By.CLASS_NAME, "css-1yijy9r")[0]
            # print(displayShowButton)
            # displayShowButton.click()
            

            # phoneNumberElement = driver.find_elements(
            #     By.CLASS_NAME, "css-1g26sdq")[0]
            # print(phoneNumberElement.get_attribute('innerHTML'))

    # startID = getExistingCSV()["total_row_count"] + 1
    # existingCSVFileCount = getExistingCSV()["num_csv"]
    # print(startID, existingCSVFileCount)
    # profession_selection_dropdown_toggle = driver.find_element(
    #     By.ID, "option-yrkedropdown-toggle")
    # profession_selection_dropdown_toggle.click()
    # profession_categories = driver.find_elements(
    #     By.CLASS_NAME, "option-groups-list")[0].find_elements(By.TAG_NAME, "li")
    # profession_selection_dropdown_toggle.click()
    # job_categories = driver.find_elements(By.CLASS_NAME, "link-wrapper")

    # for category_index in range(len(profession_categories)):
    #     if category_index < existingCSVFileCount:
    #         continue
    #     profession_selection_dropdown_toggle = driver.find_element(
    #         By.ID, "option-yrkedropdown-toggle")
    #     profession_selection_dropdown_toggle.click()
    #     tmp_profession_categories = driver.find_elements(
    #         By.CLASS_NAME, "option-groups-list")[0].find_elements(By.TAG_NAME, "li")
    #     tmp_profession_categories[category_index].click()
    #     sub_categories = driver.find_elements(
    #         By.CLASS_NAME, "col-options")[0].find_elements(By.TAG_NAME, "label")
    #     profession_selection_dropdown_toggle.click()
    #     for index in range(len(sub_categories)):
    #         if index == 0:
    #             continue
    #         print(index, "th subcategory")
    #         profession_selection_dropdown_toggle = driver.find_element(
    #             By.ID, "option-yrkedropdown-toggle")
    #         profession_selection_dropdown_toggle.click()
    #         clear_button = driver.find_elements(
    #             By.CLASS_NAME, "clear-filter-btn")[0]
    #         clear_button.click()
    #         tmp_profession_categories = driver.find_elements(
    #             By.CLASS_NAME, "option-groups-list")[0].find_elements(By.TAG_NAME, "li")
    #         tmp_profession_categories[category_index].click()
    #         tmp_sub_categories = driver.find_elements(
    #             By.CLASS_NAME, "col-options")[0].find_elements(By.TAG_NAME, "label")
    #         tmp_sub_categories[index].click()
    #         profession_selection_dropdown_toggle.click()

    #         print("Get total pages for each category", index)
    #         try:
    #             total_pages = int(driver.find_elements(
    #                 By.CLASS_NAME, 'digi-navigation-pagination__page-button--last')[0].find_elements(By.CLASS_NAME, 'digi-navigation-pagination__page-text')[0].get_attribute('innerHTML'))
    #         except:
    #             total_pages = len(driver.find_elements(
    #                 By.CLASS_NAME, "digi-navigation-pagination__page-text"))
    #             print('less than 6', index)
    #             if total_pages == 0:
    #                 total_pages = 1

    #         print(total_pages, index, 'totalpages')

    #         for page in range(total_pages):
    #             print(page, 'page')
    #             try:
    #                 jobs_per_page = driver.find_elements(
    #                     By.CLASS_NAME, "header-container")
    #             except:
    #                 continue
    #             print(len(jobs_per_page))
    #             for job in jobs_per_page:
    #                 try:
    #                     job_url = job.find_elements(By.TAG_NAME, 'a')[
    #                         0].get_attribute('href')
    #                     job_driver.get(job_url)
    #                     job_driver.implicitly_wait(10)
    #                     column = {
    #                         "No": len(data) + startID,
    #                         "JobLink": job_url,
    #                         "Contact Info": ''
    #                     }
    #                 except:
    #                     continue
    #                 try:
    #                     contact_info = job_driver.find_elements(By.CLASS_NAME, 'dont-break-out')[
    #                         0].find_elements(By.TAG_NAME, 'a')[0].get_attribute('innerHTML')
    #                     if '<' in contact_info:
    #                         column['Contact Info'] = contact_info.split(
    #                             '<')[0] + contact_info.split('>')[1]
    #                     else:
    #                         column['Contact Info'] = contact_info
    #                 except:
    #                     try:
    #                         column['Contact Info'] = job_driver.find_elements(
    #                             By.CLASS_NAME, 'application-info')[0].find_elements(By.TAG_NAME, 'a')[0].get_attribute('href')
    #                     except:
    #                         try:
    #                             column['Contact Info'] = job_driver.find_elements(
    #                                 By.CLASS_NAME, 'application-info')[0].find_elements(
    #                                 By.CLASS_NAME, 'break-word')[0].get_attribute('innerHTML')
    #                         except:
    #                             continue
    #                 print(column)
    #                 data.append(column)
    #             if page < total_pages-1:
    #                 try:
    #                     current_url = driver.current_url
    #                     current_url = current_url.split("&page=")[0]
    #                     print(current_url)
    #                     driver.get(current_url + '&page=' + str(page+2))
    #                     driver.implicitly_wait(10)
    #                 except:
    #                     continue
    export_csv(data)
    # startID = startID + len(data)
    # data = []

    driver.quit()
    return data


def export_csv(data, index=1):
    df = pd.DataFrame(data)
    # Apply transformations if needed
    df.to_csv("contact_info"+str(index)+'.csv', index=False)
    print(df)  # DEBUG


def main():
    data = get_data(urls=urls)
    print('DONE')


if __name__ == '__main__':
    main()
