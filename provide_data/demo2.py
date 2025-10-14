from os import makedirs
from os.path import exists, dirname
from re import search
from bs4 import BeautifulSoup as bs
from .handle_img import Basic


class A(Basic):
    def __init__(self, url):
        Basic.__init__(self,url)
        self.sp.encoding = "gb18030"

    def main(self):
        response = self.sp.get_url(self.sp.url)
        soup = bs(response.text, "lxml")
        b = soup.find(class_="ptitle fc1").text
        n = f"{dirname(__file__)}/../static/image/syjszpc/{b}"
        self.sp.catalog = f"{n}/{b}"
        if not exists(n):
            makedirs(n)
        pages = int(search("\d+", soup.find(class_="fanye1").find("a").text).group())
        self.sp.a = [""]*pages
        for i in range(pages):
            if i == 0:
                image = (soup.find(id="nr234img")).find("img").get("src")
            else:
                image = search("([^<>/\\\|:""\*\?]+\.\w+$)", self.sp.a[0])
                asd = search("\d+",image.group())
                image = self.sp.a[0][:image.span()[0]] + image.group()[:asd.span()[0]] +"0"*(len(asd.group())-len(str(i)))+ str(i) + ".zip"
            self.sp.a[i] = image
        self.sp.dl()


if __name__ == '__main__':
    url = "http://m.syjszpc.com/shaonv/2021/0604/8275.html"
    from time import time
    a = time()
    while True:
        # url = input("url:")
        A(url).main()
        break
    print(time()-a)