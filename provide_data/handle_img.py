from threading import Thread
from re import search
from requests import get, post
from requests.packages.urllib3 import disable_warnings
from requests.exceptions import RequestException
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from PIL.Image import open as op
from io import BytesIO
from sqlite3 import connect
from os.path import dirname
from abc import ABCMeta, abstractmethod
# import asyncio
# import aiohttp


class Spyder:
    def __init__(self, url):
        self.url = url
        self.catalog = ""
        self.a = []
        self.encoding = 'utf-8'

    def get_url(self, url, headers=None, method='GET'):
        disable_warnings(InsecureRequestWarning)
        if headers is None:
            headers = {
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"}
        if method == "GET":
            response = get(url=url, headers=headers, verify=False)
        elif method == "POST":
            response = post(url=url, headers=headers, verify=False)
        else:
            return RequestException
        response.encoding = self.encoding
        return response

    def write_content(self):
        p = self.catalog.split('/')
        coon = connect(f"{dirname(__file__)}/../static/content.db")
        cur = coon.cursor()
        text1 = f"CREATE TABLE IF not exists {p[-3]} (url TEXT,name TEXT);"
        cur.execute(text1)
        url = self.url
        name = p[-1]
        t = f"insert into [{p[-3]}]([url], [name]) select '{url}', '{name}' where not exists (select * from [{p[-3]}] where [name]='{name}')"
        cur.execute(t)
        coon.commit()
        cur.close()
        coon.close()

    def dl(self, TF=True, headers=None):
        self.write_content()
        for i, image in enumerate(self.a):
            filename = self.catalog + (len(str(len(self.a))) - len(str(i + 1))) * "0" + str(i + 1) + ".webp"
            p = Thread(target=self.download, args=(image, filename, TF, headers))
            self.a[i] = search("([^<>/\\\|:""\*\?]+\.\w+$)", filename).group()
            p.start()

    def download(self, image_url, filename, TF, headers=None):
        content = None
        if TF:
            while True:
                try:
                    content = self.get_url(image_url, headers=headers).content
                except Exception as e:
                    print(e, 'DownloadError', filename)
                    continue
                break
        else:
            content = image_url
        try:
            op(BytesIO(content)).save(filename)
        except:
            with open(filename, "wb+") as f:
                f.write(content)

    # def dl_2(self, TF=True, headers=None,number:int=30):
    #     self.write_content()
    #     loop = asyncio.get_event_loop()
    #     loop.run_until_complete(self.run(TF,headers,number))
    #     loop.close()
    #
    # async def run(self, TF, headers, number:int):
    #     sem = asyncio.Semaphore(number)
    #     task_list = []
    #     for i, image in enumerate(self.a):
    #         filename = self.catalog + (len(str(len(self.a))) - len(str(i + 1))) * "0" + str(i + 1) + ".webp"
    #         c = self.down_load(filename, image, sem, TF, headers)
    #         task = asyncio.ensure_future(c)
    #         task_list.append(task)
    #     await asyncio.wait(task_list)
    #
    # async def down_load(self, filename, image_url, sem, TF, headers):
    #     async with sem:
    #         async with aiohttp.ClientSession() as sess:
    #             if TF:
    #                 while True:
    #                     try:
    #                         async with await sess.get(url=image_url, headers=headers) as response:
    #                             content = await response.read()
    #                     except Exception as e:
    #                         print(e, 'DownloadError', filename)
    #                         continue
    #                     break
    #             else:
    #                 content = image_url
    #                 del image_url
    #             try:
    #                 await op(BytesIO(content)).save(filename)
    #             except:
    #                 with open(filename, "wb+") as f:
    #                     f.write(content)


class Basic(metaclass=ABCMeta):
    def __init__(self, url):
        self.sp = Spyder(url)
        self.encoding = "utf-8"

    @abstractmethod
    def main(self):
        pass
