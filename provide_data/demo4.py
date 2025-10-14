from re import search
from os import makedirs
from os.path import exists
import requests.exceptions
from bs4 import BeautifulSoup as bs
from .handle_img import Basic
from os.path import dirname

class A(Basic):
    def __init__(self, url):
        Basic.__init__(self, url)
        self.sp.encoding = "gb18030"

    def main(self):
        response = self.sp.get_url(self.sp.url)
        soup = bs(response.text, "lxml")
        b = soup.find(class_="wz-title").text
        n = f"{dirname(__file__)}/../static/image/realPeople/{b}"
        self.sp.catalog = f"{n}/{b}"
        if not exists(n):
            makedirs(n)
        pages = int(search("\d+", soup.find(class_="page11list").find("a").text).group())
        for i in range(pages):
            if i == 0:
                image = (soup.find(class_="pic")).find("img").get("src")
            else:
                image = search("([^<>/\\\|:""\*\?]+\.\w+$)", self.sp.a[0])
                asd = search("\d+", image.group()).group()

                image = self.sp.a[0][:image.span()[0]] + str(int(asd) + i) + ".zip"
            self.sp.a.append(image)

        self.sp.dl()

if __name__ == '__main__':
    # url = "" https://www.fnvshen.com/article/
    url = "http://m.moyunso.com/meinv/2021/0911/5095.html"
    while True:
        url = input("url:")
        try:
            a = A(url)
            a.main()
        except requests.exceptions.InvalidSchema:
            print("\nurl不正确\n")
            continue
        except requests.exceptions.MissingSchema:
            print("\nurl不正确\n")
            continue
        except requests.exceptions.InvalidURL:
            print("\nurl不正确\n")
            continue
        break
