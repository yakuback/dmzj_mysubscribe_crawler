import json
import requests
from bs4 import BeautifulSoup
from dmzjmc_customerr import ResponseStatusError

class MySubscribe:
    def __init__(self, session):
        self.session = session
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36 Edg/80.0.361.62", 
            "Referer": "https://m.dmzj.com/login.html"
            }
        self._logprinter("Crawler", "Loading", True)

    @staticmethod
    def _response_status_check(response):
        if response.status_code == requests.codes.ok:
            return 0
        else:
            raise ResponseStatusError(str(response.status_code))

    @staticmethod
    def _logprinter(act, target, status):
        sta = "\033[32m[*Succeed!]\033[0m" if status else "\033[31;47m[*Failed!]\033[0m"
        print("\033[33m[%.10s]\033[0m %.20s... %s" % (act, target, sta))

    def _get_mymanga(self):
    # 弃用的方法
        prejson = self.session.get("https://m.dmzj.com/mysubscribe")
        self._response_status_check(prejson)  # 检查相应状态
        jsonstr = prejson.text
        if jsonstr == "":
            self._logprinter("Manga JSON", jsonstr, False)
        mysubscribe = json.loads(jsonstr)
        with open("mangasubscribes.txt", "w", encoding="utf-8") as sfile:
            for item in mysubscribe:
                sub_id = item['sub_id']
                print("%d" % sub_id, file=sfile)
            self._logprinter("JSON Write", sfile.name, True)

    def get_lnovel(self):
        payload = {"page": 1, "type_id": 4, "letter_id": 0, "read_id": 1}
        pre_novel_page = self.session.post("https://i.dmzj.com/ajax/my/subscribe", data=payload)
        self._response_status_check(pre_novel_page)

        soup = BeautifulSoup(pre_novel_page.text, features="lxml")
        pre_list = soup.find_all("h3")
        novels = []
        for item in pre_list:
            novels.append(item.a.string)
        
        with open("novelsubscribes.txt", "w", encoding="utf-8") as sfile:
            for novel in novels:
                print("%s" % novel, file=sfile)
            self._logprinter("HTML Write", sfile.name, True)
    
    def get_manga(self):
        payload = {"page": 1, "type_id": 1, "letter_id": 0, "read_id": 1}
        pre_manga_page = self.session.post("https://i.dmzj.com/ajax/my/subscribe", data=payload)
        self._response_status_check(pre_manga_page)

        soup = BeautifulSoup(pre_manga_page.text, features="lxml")
        pre_list = soup.find_all("h3")
        mangas = []
        for item in pre_list:
            mangas.append(item.a.string)
        
        with open("mangasubscribes.txt", "w", encoding="utf-8") as sfile:
            for manga in mangas:
                print("%s" % manga, file=sfile)
            self._logprinter("HTML Write", sfile.name, True)