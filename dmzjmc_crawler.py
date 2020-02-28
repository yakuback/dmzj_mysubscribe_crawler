class MySubscribe:
    def get_mymanga(self):
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