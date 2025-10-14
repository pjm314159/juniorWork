import asyncio
from json import loads
from json.decoder import JSONDecodeError
from os import makedirs
from os.path import exists
import aiohttp
from requests import get, Session, post
from requests.exceptions import ConnectionError
from .handle_img import Basic
from re import search, sub
from base64 import b64decode


class A(Basic):
    def __init__(self, url):
        Basic.__init__(self, url)
        self.sp.encoding = "utf-8"
        self.bookId = search("\d+$", url).group()
        p = url.split("/")

        self.DOMAIN = "/".join(p[:3])

    def get_token(self):
        while True:
            try:
                r = get(f"{self.DOMAIN}/user/detail?ticket=")
                r.encoding = 'utf-8'
                token = loads(r.text)['content']['token']
                post(url=f"{self.DOMAIN}/user/getBillingAccount/qiandao", cookies={"ticket": token})
            except JSONDecodeError:
                print('token')
                continue
            except TypeError as e:
                print(e)
                continue
            except ConnectionError as e:
                print(e)
                continue
            break
        return token

    def main(self):
        token = self.get_token()
        g = Session()
        g.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}
        b = loads(g.get(f'{self.DOMAIN}/home/query/book?id=' + self.bookId).text)['content']['name']
        self.sp.catalog = "../static/image/xxmh88/" + b + "/" + b
        if not exists("../static/image/xxmh88/" + b):
            makedirs("../static/image/xxmh88/" + b)
        chapterId = loads(g.get(f'{self.DOMAIN}/home/query/directory/?bookId={self.bookId}').text)[
            'content']
        self.sp.a = [b''] * len(chapterId) * 50
        np = 0
        for j, i in enumerate(chapterId):

            url = f"{self.DOMAIN}/home/query/chapter?bookId={self.bookId}&chapterId={i['id']}"
            while True:
                if i['freeFlag'] == "true":
                    if j == 0:
                        g.get(url)
                else:
                    token = self.get_token()
                    g.post(f'{self.DOMAIN}/user/order/submit?bookId={self.bookId}&chapterId={i["id"]}',
                           cookies={"ticket": token})
                response = g.post(url, cookies={"ticket": token}).text
                try:
                    t = loads(response)['content']['imageList']
                except ValueError:
                    print(response)
                    continue
                if len(t) < 10:
                    print("t<0 line72")
                    continue
                for p in t:
                    foo = b64decode(sub("^data:image/\w+;base64,", "", get(sub("\.\w+$", ".html", p["url"])).text))
                    self.sp.a[np] = foo
                    np += 1
                break
        del self.sp.a[np+1:]
        self.sp.dl(False)


if __name__ == '__main__':
    while True:
        url = input("url:")
        #    url = 'https://www.xxmh88.com/#!/book/cover/88121'
        A(url).main()


