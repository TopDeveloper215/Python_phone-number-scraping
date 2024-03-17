import requests
import pandas as pd
import re
import concurrent.futures
import cloudscraper
from scrapy.http import HtmlResponse

list1 = []
df = pd.read_csv('links.csv')


class STORIA():
    counter = 0
    def start_request(self,row):
        try:

            url = row['URL']
            scraper = cloudscraper.create_scraper(browser={'browser': 'firefox', 'platform': 'windows', 'mobile': False})
            req = scraper.get(url=url,verify=False)
            response = HtmlResponse(url="", body=req.content)
            try:
                try:
                    phone_number = re.findall('phones":..(.*?)".',str(response.text))[0]
                except:
                    phone_number = ""

                item = {}
                item['Phone Number'] = phone_number
                item['URL'] = url
                list1.append(item)
                counter = self.counter + 1
                print(f"Data Added :- {counter}")
            except:
                print("CHECK YOUR CODE")


        except Exception as e:
            df = pd.DataFrame(list1)
            df.to_csv(f"Temp_STORIA_Full_Data.csv", index=False, encoding='utf-8-sig')
            print("CSV Generated")

if __name__ == '__main__':
    temp = STORIA()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
        process = list((pool.map(temp.start_request,((row) for k,row in df.iterrows()))))

    df = pd.DataFrame(list1)
    df.to_csv(f"STORIA_Full_Data.csv", index=False, encoding='utf-8-sig')
    print("CSV Generated")


