import jmcomic

class A:
    def __init__(self,url):
        self.option = None
        self.url = url
        self.jmOption = ""
    def create(self):
        self.option = jmcomic.create_option(self.jmOption)
    def download(self):
        if self.url[-1] == "/":
            self.url = self.url[:-1]
        if self.url.find("album")!=-1:
            album_id = self.url.split("/")[-2]
            self.option.download_album(album_id)
            return 0
        elif self.url.find("photo")!=-1:
            photo_id = self.url.split("/")[-2]
            self.option.download_photo(photo_id)
            return 0
        try:
            id = int(self.url)
            self.option.download_album(id)
        except :
            pass

if __name__ == '__main__':
    a = A("https://www.fnvshen.com/album/1224371/56")
    a.download()