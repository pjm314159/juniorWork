from os import makedirs, getcwd, rename, remove, listdir
from os.path import exists, dirname
from shutil import move
from threading import Thread
from re import split
import selenium.common.exceptions
from .handle_img import Basic
from random import randint
from time import sleep
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random import sample
from urllib.parse import urlparse


class A(Basic):
    def __init__(self, url):
        Basic.__init__(self, url)
        self.sp.encoding = "utf-8"
        self.flag_3 = True

    def main(self):
        option = ChromeOptions()
        # option.add_argument('--headless')
        local = ''.join(sample(list("abcdefghijklmnopqrstuvwxyz"), 5))
        makedirs(f"{dirname(__file__)}/../static/image/goddess/{local}")
        prefs = {"profile.managed_default_content_settings.images": 2,
                 "download.default_directory": f"{getcwd()}\\static\\image\\goddess\\{local}",
                 "profile.content_settings.exceptions.automatic_downloads": {
                     f'http://{urlparse(self.sp.url).netloc}:80,*': {'expiration': '0',
                                                                     'last_modified': '13289714118886977', 'model': 0,
                                                                     'setting': 1}}}
        option.add_experimental_option("prefs", prefs)
        driver = Chrome(options=option)
        driver.get(self.sp.url)
        sleep(5)
        WebDriverWait(driver, 20, 0.5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="book-detail-layout"]/div[2]/div[1]/div/div[2]/p[1]')))
        b = driver.find_element_by_xpath('//*[@id="book-detail-layout"]/div[2]/div[1]/div/div[2]/p[1]').text
        b = b.replace(".", '')

        n = f"{dirname(__file__)}/../static/image/goddess/{b}"

        self.sp.catalog = f"{n}/{b}"
        if not exists(n):
            makedirs(n)
        else:
            remove(f"{dirname(__file__)}/../static/image/goddess/{local}")
        locator = '//*[@id="book-detail-layout"]/div[2]/ul'
        WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located((By.XPATH, locator)))
        urls = []
        pay = 0
        mn = (driver.find_element_by_xpath(locator)).find_elements(By.TAG_NAME, "a")
        for aasd in range(len(mn)):
            urls.append(mn[aasd].get_attribute("href"))
            asd = mn[aasd].find_element_by_xpath("div[2]/span[2]").get_attribute("style")
            if not asd and pay == 0:
                pay = aasd

        if pay == 0:
            pay = len(urls) + 1
        next = driver.find_element_by_xpath('//*[@id="book-detail-layout"]/div[2]/div[4]/div[2]')
        if next.get_attribute("class") == "active":
            next.click()
            sleep(0.75)
            for aasd in (driver.find_element_by_xpath(locator)).find_elements(
                    By.TAG_NAME, "a"):
                urls.append(aasd.get_attribute("href"))
        money = 0
        r = 0
        for j, i in enumerate(urls):
            if money < 60 and pay <= j:
                if j != pay:
                    driver.execute_script("localStorage.clear();")
                self.register(driver)
                money = 150
            money -= 60
            driver.get(i)
            WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, "img-box")))
            for n in range(5):
                sleep(0.5)
            imgs = driver.find_elements(By.CLASS_NAME, "img-box")
            for img_asd in range(len(imgs)):
                while True:
                    try:
                        img = imgs[img_asd].find_element_by_tag_name("img")
                    except selenium.common.exceptions.StaleElementReferenceException as e:
                        imgs = driver.find_elements(By.CLASS_NAME, "img-box")
                        sleep(1)
                        print(e)
                        continue
                    except selenium.common.exceptions.NoSuchElementException as e:
                        imgs = driver.find_elements(By.CLASS_NAME, "img-box")
                        print(e)
                        continue
                    if img.get_attribute("src")[:5] == "data:":
                        r+=1
                        js = f'var a=document.createElement("a"); a.href="{img.get_attribute("src")}";a.download="{f"{b}{r:0>4d}.webp"}";a.click();'
                        driver.execute_script(js)
                        break
                    else:
                        print(2)
        for i in range(r):
            i = i + 1
            while not exists(f'{dirname(__file__)}/../static/image/goddess/{local}/{b}{i:0>4d}.webp'):
                print(exists(f'{dirname(__file__)}/../static/image/goddess/{local}/{b}{i:0>4d}.webp'))
            move(f'{dirname(__file__)}/../static/image/goddess/{local}/{b}{i:0>4d}.webp', f'{n}/{b}{i:0>4d}.webp')
        driver.quit()

        self.flag_3 = False

    def dl(self):
        p = Thread(target=self.main, args=())
        p.start()

    def register(self, driver):
        foo = split("/", self.sp.url)
        driver.get(foo[0] + "//" + foo[2] + "/register")
        WebDriverWait(driver, 20, 1).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="signup-layout"]/div[2]/div[1]/div/input')))
        sleep(1.5)
        driver.find_element_by_xpath('//*[@id="signup-layout"]/div[2]/div[1]/div/input').send_keys(
            "13" + str(randint(100000000, 999999999)))
        password = "qwer" + str(randint(100000000, 999999999))
        driver.find_element_by_xpath('//*[@id="signup-layout"]/div[2]/div[2]/div/input').send_keys(password)
        driver.find_element_by_xpath('//*[@id="signup-layout"]/div[2]/div[3]/div/input').send_keys(password)
        driver.find_element_by_xpath('//*[@id="signup-layout"]/div[2]/div[4]').click()
        WebDriverWait(driver, 20, 0.5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'mint-msgbox-btns')))
        driver.find_element_by_class_name('mint-msgbox-btns').click()
        sleep(1)


if __name__ == '__main__':
    urls = ["1461", "2968"]
    h = "http://vq7nlr.nicegiving.com/directory/"
    url = h + "2139"
    a = A(url)
    a.dl()
