from dmzjmc_login_manager import LoginManager
from dmzjmc_crawler import MySubscribe
try:
    # initialize
    dmzj = LoginManager("username", "password")
    dmzj.login()
    # crawler
    sub = MySubscribe(dmzj.session)
    sub.get_manga()
    sub.get_lnovel()
except:
    dmzj.session.close()
else:
    dmzj.session.close()