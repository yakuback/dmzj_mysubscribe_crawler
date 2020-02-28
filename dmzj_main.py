from dmzj_customerr import GetInvalidToken, LoginErr
import requests
import json
from bs4 import BeautifulSoup


class GetMySubscribe:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.login_url = "https://m.dmzj.com/login.html"
        self.i_url = "https://i.dmzj.com/api/login"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36 Edg/80.0.361.62", 
            "Referer": "https://m.dmzj.com/login.html"
            }
        print("dmzj_subscribe" + "[Loaded!]")

    def _get_login_page_res(self):
        # 获取self.login_url的Response对象
        self.session = requests.Session()
        self.login_page_res = self.session.get(self.login_url, headers=self.headers)
        self.login_page_res.raise_for_status()  # 检查状态码

    def _get_login_token(self):
        soup = BeautifulSoup(self.login_page_res.text)
        self.login_token = soup.find("form").input['value']
        if self.login_token == "":
            raise GetInvalidToken("InvalidToken")

    @staticmethod
    def _check_login_status(raw_respons):
        prejson = raw_respons[8:-1]  # 格式化JSON
        respons = json.loads(prejson)
        code = respons['code']
        msg = respons['msg']
        return code, msg

    def login(self):
        self._get_login_page_res()
        print("get page: " + self.login_url + "[Succeed!]")
        self._get_login_token()
        print("get token: " + self.login_token + "[Succeed!]")
        login_payload = {
            "callback":"success", "nickname": self.username, "password": self.password, 
            "type": "0", "token": self.login_token
            }
        i_respons = self.session.get(self.i_url, params=login_payload, headers=self.headers)
        i_respons.raise_for_status()  # 检查状态码

        # 检查登录状态
        code, msg = self._check_login_status(i_respons.text)
        if code == 1000:
            print("login msg:" + msg + "[Succeed!]")
        else:
            print("login msg:" + msg + "[failed]")
            raise LoginErr(code)

    def get_mysubscribe(self):
        prejson = self.session.get("https://m.dmzj.com/mysubscribe", headers=self.headers)
        prejson.raise_for_status()  # 检查状态码
        jsonstr = prejson.text
        if jsonstr == "":
            print("mysubscribe json:" + jsonstr + "[failed]")
        mysubscribe = json.loads(jsonstr)
        with open(mysubscribe.txt, "w") as file:
            for item in mysubscribe:
                file.write(item)
            print("mysubscribe write:" + file.name + "[Succeed!]")