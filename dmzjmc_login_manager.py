from dmzjmc_customerr import GetInvalidToken, LoginError, ResponseStatusError
import requests
import json
from bs4 import BeautifulSoup


class LoginManager:
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
        self._logprinter("LoginMan", "Loading", True)
        
    def _get_login_page_res(self):
        # 获取self.login_url的Response对象
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.login_page_res = self.session.get(self.login_url)
        # 检查响应状态
        if self._response_status_check(self.login_page_res) == 0:
            self._logprinter("Get Page", self.login_url, True)

    def _get_login_token(self):
        soup = BeautifulSoup(self.login_page_res.text, features="lxml")
        self.login_token = soup.find("form").input['value']
        # 检查Token有效性
        if self.login_token == "":
            raise GetInvalidToken("InvalidToken")
        self._logprinter("Get Token", self.login_token, True)

    def login(self):
        self._get_login_page_res()
        self._get_login_token()
        login_payload = {
            "callback":"success", "nickname": self.username, "password": self.password, 
            "type": "0", "token": self.login_token
            }
        i_respons = self.session.get(self.i_url, params=login_payload)
        self._response_status_check(i_respons)

        # 检查登录状态
        code, msg = self._check_login_status(i_respons.text)
        if code == 1000:
            self._logprinter("Login Msg", msg, True)
        else:
            self._logprinter("Login Msg", msg, False)
            raise LoginError(code)

    @staticmethod
    def _check_login_status(raw_respons):
        prejson = raw_respons[8:-1]  # 格式化JSON
        respons = json.loads(prejson)
        code = respons['code']
        msg = respons['msg']
        return code, msg
    
    @staticmethod
    def _logprinter(act, target, status):
        sta = "\033[32m[*Succeed!]\033[0m" if status else "\033[31;47m[*Failed!]\033[0m"
        print("\033[33m[%.10s]\033[0m %.20s... %s" % (act, target, sta))

    @staticmethod
    def _response_status_check(response):
        if response.status_code == requests.codes.ok:
            return 0
        else:
            raise ResponseStatusError(str(response.status_code))

    def close(self):
        self.session.close()