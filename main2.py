import requests
import os
import yaml
import time
import threading
import concurrent.futures
from contextlib import closing
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging
import traceback

logging.basicConfig(level=logging.ERROR, filename='error.log', format='%(asctime)s - %(levelname)s - %(message)s')


class Main:
    def __init__(self):
        print('contextlib')
        if not os.path.exists('record.yaml'):
            open('record.yaml', 'w').write('')
            record = ''
        else:
            record = open('record.yaml', 'r').read()

        with open('菲律宾开通vb 3.csv', 'r', encoding='utf-8') as f:
            data = f.read()
        self.plt = os.environ['SERVICEMACHINE'] if 'SERVICEMACHINE' in os.environ else '1'

        self.max_threads = 200

        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        self.driver.get('file://' + os.getcwd() + '\\index.html')

        self.proxies = []

        self.data = data.split('\n')
        self.record = yaml.load(record, Loader=yaml.FullLoader) if record != '' else {}

        threading.Thread(target=self.get_proxy, args=()).start()

        self.start()

    def start(self):
        data = ['']
        while len(data) > 0:
            data = [d.strip() for d in self.data if d not in self.record and d != '']
            
            print('Done: ' + str(len(self.record.keys())))
            print('Undone: ' + str(len(data)))
            print('All data: ' + str(len(self.data)))
    
            with concurrent.futures.ThreadPoolExecutor(self.max_threads) as executor:
                futures = [executor.submit(self.scan, number) for number in data]
            concurrent.futures.wait(futures)

        print('All data is done.')

    def start0(self):
        self.get_proxy()
        keys = list(self.record.keys())
        data = [d.strip() for d in self.data if d not in keys]
        proxy = None

        for data in tqdm(data):
            number = data.strip()
            if number == '' or number in keys:
                continue

            proxy = self.scan(number, proxy)

    # Scan and get the result of number.
    def scan(self, number, proxy=None):

        if proxy is None:
            proxy = self.proxies.pop(0)

        url = f"https://www.klook.cn/v3/userserv/user/register_service/account_is_exist_only?user_type=6&login_id=63-{number}"

        headers = {'Host': 'www.klook.cn', 'Connection': 'keep-alive',
                   'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
                   'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'Upgrade-Insecure-Requests': '1',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
                   'Sec-Purpose': 'prefetch;prerender', 'Purpose': 'prefetch',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                   'Sec-Fetch-Site': 'none', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-User': '?1',
                   'Sec-Fetch-Dest': 'document', 'Accept-Encoding': 'gzip, deflate, br',
                   'Accept-Language': 'zh-CN,zh;q=0.9'}

        query_response, proxy = self.get(url, headers, proxy)

        if query_response is False:
            return False

        if 'arg1' in query_response.text:
            arg1 = query_response.text.split('arg1=\'')[1].split('\'')[0]
            acw_tc = self.get_cookie(arg1)
            cookie = 'acw_sc__v2=' + acw_tc + '; acw_tc=' + query_response.cookies.get('acw_tc')
            headers['cookie'] = cookie
            response, proxy = self.get(url, headers, proxy)
            if response is False:
                return False
        else:
            response = query_response

        response.encoding = response.apparent_encoding

        if response.text[0] == '{':
            response_json = response.json()
            if response_json['success']:
                if response_json['result']['exist']:
                    self.save(number, 1)
                else:
                    self.save(number, 0)
        if response.status_code == 405 or '滑动验证页面' in response.text:
            return False

    # Save data.
    def save(self, number, result):
        self.record[number] = result
        open('record.yaml', 'a').write(f"'{number}': {result}\n")
        return True

    # Get cookie.
    def get_cookie(self, arg1):
        return self.driver.execute_script(
            f'return "{arg1}".unsbox().hexXor("3000176000856006061501533003690027800375");')

    # Send get request.
    def get(self, url, headers, proxy=None):
        if proxy is None:
            proxy = self.proxies.pop()

        try:
            with closing(requests.get(url, headers=headers, proxies={'https': 'http://' + proxy, 'http': 'http://' + proxy}, timeout=10)) as response:
                return response, proxy
        except Exception as e:
            type_e = type(e)
            if type_e == requests.exceptions.ReadTimeout:
                return False, False

        return False, False

    # Get the proxy.
    def get_proxy(self):
        while True:  # 用 while True 替换 while 1
            try:  # 加入异常处理
                if len(self.proxies) < 200:
                    response = requests.get('https://api.smartproxy.cn/web_v1/ip/get-ip-v3?app_key=c5b60a6380cda12c5d73b52b924bd506&pt=9&num=200&ep=&cc=&state=&city=&life=1&protocol=1&format=txt&lb=%5Cr%5Cn')
                    #response = requests.get('http://api.proxy.ipidea.io/getBalanceProxyIp?big_num=900&return_type=txt&lb=1&sb=0&flow=1&regions=&protocol=http')
                    self.proxies += [d for d in response.text.split('\r\n') if d != '']

                    if '白名单' in response.text:
                        print('Please add whitelist ' + response.text.split('IP')[1].split('到')[0])

                time.sleep(5)
            except requests.RequestException as e:  # 捕获请求异常
                logging.error(f"Request error occurred: {str(e)}")
                logging.error(traceback.format_exc())
            except Exception as e:  # 捕获其他可能的异常
                logging.error(f"An unexpected error occurred: {str(e)}")
                logging.error(traceback.format_exc())

if __name__ == '__main__':
    Main().get_proxy()