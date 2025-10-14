from os import makedirs
from os.path import exists
import requests.exceptions
from bs4 import BeautifulSoup as bs
from re import search
from .handle_img import Basic
from os.path import dirname

class A(Basic):
    def __init__(self, url):
        Basic.__init__(self, url)
        self.sp.encoding = "utf-8"

    def main(self):
        response = self.sp.get_url(self.sp.url)
        soup = bs(response.text, "lxml")
        b = soup.find(id="htilte").text
        n = f"{dirname(__file__)}/../static/image/realPeople/{b}"
        self.sp.catalog = f"{n}/{b}"
        if not exists(n):
            makedirs(n)
        pages = int(search("\d+", soup.find(id="dinfo").find("span").text).group())
        n = dirname((soup.find(id="hgallery")).find("img").get("src"))
        self.sp.a = [""]*pages
        self.sp.a[0] = n+"/0.jpg"
        for i in range(1,pages):
            self.sp.a[i] = f'{n}/{i:0>3d}.jpg'
        self.sp.dl(headers={'referer': 'https://www.fnvshen.com/'})


if __name__ == '__main__':
    url= "https://www.fnvshen.com/g/24128/10.html"
    while True:
        # url = input("url:")
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
