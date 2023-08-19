from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import random
import boto3
import json

class BotInstagram():
    ser = Service(r"D:\Projetos\instagram\chromedriver.exe")
    def __init__(self):
        self.desired_capabilities = DesiredCapabilities.CHROME
        self.desired_capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}
        self.options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=self.options, desired_capabilities=self.desired_capabilities, service=BotInstagram.ser)
        self.driver.maximize_window()

    def entrar_link(self, link):
        response = None
        try: 
            self.driver.get(link)
            perfLog = self.driver.get_log('performance')
            for logIndex in range(0, len(perfLog)):
                if 'message' not in perfLog[logIndex]["message"]:
                    break
                try:
                    logMessage = json.loads(perfLog[logIndex]["message"])["message"]
                except:
                    break
                if logMessage["method"] == "Network.responseReceived":
                    if logMessage["params"]["response"]["url"] == link:
                        response   = logMessage["params"]["response"]['status']
                        print(f'{link} - {response}')
            if response == 429:
                exit(429) 

        except Exception as err:
            print(f'erro = {err}')
            return None
    
    def pegar_link_das_fotos(self):
        os_links = self.driver.find_elements(By.TAG_NAME, 'a')
        urls = list()

        for i in os_links:
            url = i.get_attribute("href")
            if url.startswith('https://www.instagram.com/p/'):
                if url not in urls:
                    urls.append(url)
                    print(urls)
        return urls

    def dar_like(self,url):
        try:
            self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/div[1]/div[1]/span/div/div').click()
        except Exception as err:
            print('Erro')
            return None
        

    def scroll_down(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    
tags = ['dji', 'drone', 'landscapephotography', 'fimix8se', 'dronefpv', 'dronephotography', 'dronestagram', 'djiphantom', 'djispark', 'djimavic', 'sunset', 'pordosol', 'viagem', 'turismo', 'floripa', 'portoalegre', 'saopaulo', 'curitiba', 'brasil', 'praia', 'beach', 'sun', 'enjoylife', 'surf', 'crossfit', 'fitness', 'iphone', \
'landscapephotography', 'aproveitaravida', 'nascerdosol' ]


bot = BotInstagram()
bot.entrar_link('https://www.instagram.com')
time.sleep(15)


final_urls = list()
for tag in tags:
    bot.entrar_link(f'https://www.instagram.com/explore/tags/{tag}')
    time.sleep(2)
    scroll_count = 0 
    while scroll_count <= 8:
        bot.scroll_down()
        time.sleep(4)
        scroll_count += 1
    urls = bot.pegar_link_das_fotos()
    for u in urls:
        final_urls.append(u)

print(f'Quantidade de links {len(final_urls)}')

for count, u in enumerate(final_urls):
    print(count)
    bot.entrar_link(u)
    time.sleep(random.randint(10, 50))
    bot.dar_like(u)