import time

import execjs
import requests
from bs4 import BeautifulSoup


# mysql数据库模型

class eastMoney:

    def __init__(self):
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
            "sec-ch-ua": '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            # "Cookie": "v=A6sIgqQ-SH0UzZQX6kKhQd26OsSXwLilOdSD5B0oh-pBvMW6pZBPkkmkE2Uu"
        }
        # 当前日期 2025-01-01
        self.date = time.strftime("%Y-%m-%d", time.localtime())

    def get_bk_list(self):
        url = "https://quote.eastmoney.com/center/api/sidemenu_new.json"

        response = requests.request("GET", url, headers=self.headers)

        bk_list = response.json().get("bklist", [])
        return bk_list

    def get_bk_detail(self, bk_code):
        url = "https://push2.eastmoney.com/api/qt/clist/get"
        result = []

        querystring = {
            "fid": "f62", "po": "1", "pz": "200", "pn": "1", "fs": f"b:{bk_code}",
            # "fields": "f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124,f1,f13",
            "fields": "f12,f14,f62"
        }

        response = requests.request("GET", url, headers=self.headers, params=querystring)
        res_json = response.json()
        data = res_json.get("data", {})
        total = data.get("total", 0)

        diff = data.get("diff", {})
        for key, value in diff.items():
            result.append((value.get("f12", ""), value.get("f14", "")))

        if total > 200:
            for i in range(2, int(total / 200) + 2):
                querystring["pn"] = str(i)
                response = requests.request("GET", url, headers=self.headers, params=querystring)
                res_json = response.json()
                data = res_json.get("data", {})
                diff = data.get("diff", {})
                for key, value in diff.items():
                    result.append((value.get("f12", ""), value.get("f14", "")))
                time.sleep(3)

        return result

    def run(self):
        bk_list = self.get_bk_list()
        for bk in bk_list:
            bk_code = bk.get("code")
            bk_name = bk.get("name")
            print(f"开始获取{bk_code}:{bk_name}的成分股数据...")
            for stock in self.get_bk_detail(bk_code):
                print({
                    "bk_code": bk_code,
                    "bk_time": self.date,
                    # "bk_name": bk_name,
                    "stock_code": stock[0],
                    "stock_name": stock[1]

                })
            time.sleep(3)


# 同花顺
class tongHuaShun:

    def __init__(self):
        self.headers = {
            "Accept": "text/html, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
            "X-Requested-With": "XMLHttpRequest",
            "hexin-v": "A1X2fF7Mnhwq5bpZtZBXp2eIZFoNUhVf0wXt89e8EJAYNnuEn6IZNGNW_dRk",
            "sec-ch-ua": '"Not(A: Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            # "Cookie": "spversion=20130314; log=; Hm_lvt_722143063e4892925903024537075d0d=1739715147; Hm_lpvt_722143063e4892925903024537075d0d=1739715147; HMACCOUNT=C71F5CCBA0626CB7; Hm_lvt_929f8b362150b1f77b477230541dbbc2=1739715147; Hm_lpvt_929f8b362150b1f77b477230541dbbc2=1739715147; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1739715147; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1739715147; v=A23OxHa09n1-iJIR7NzPbw-AfALiyqFLK_8FcK9yqddz_IN8dxqxbLtOFWI8"
        }

    def hexin(self):
        # 获取hexin-v
        with open("wen.js", "r", encoding="utf-8") as f:
            js = f.read()
        JS = execjs.compile(js)  # 读取时间拼接进入js代码中
        hexin = JS.call("rt.update")
        return hexin

    def update_headers(self):
        self.headers["hexin-v"] = self.hexin()
        # print(f"hexin-v: {self.headers['hexin-v']}")

    def get_bk_list(self):
        url = "https://q.10jqka.com.cn/gn/index/field/addtime/order/desc/page/1/ajax/1/"

        response = requests.request("GET", url, headers=self.headers)
        # 创建BeautifulSoup对象
        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找表格
        table = soup.find('table', class_='m-pager-table')

        # 查找所有行
        rows = table.find_all('tr')

        # 创建一个列表来存储解析后的数据
        data = []

        # 遍历每一行
        for row in rows[1:]:  # 跳过表头
            cols = row.find_all('td')
            if len(cols) > 4:
                bk_time = cols[0].text.strip()
                bk_name = cols[1].find('a').text.strip()
                bk_link = cols[1].find('a').get('href')
                bk_code = bk_link.split('/')[-2]
                # 成分股数量
                bk_num = int(cols[4].text.strip())

                data.append([bk_time, bk_name, bk_link, bk_code, bk_num])

        return data

    def get_bk_detail(self, bk_code, bk_num):
        if bk_num > 100:
            bk_num = 100
        total_pages = bk_num // 20
        if bk_num % 20 != 0:
            total_pages += 1

        data = []
        for i in range(total_pages):
            print(f"开始获取第{i + 1}页数据...")
            page = i + 1
            url = f"https://q.10jqka.com.cn/gn/detail/field/199112/order/desc/page/{page}/ajax/1/code/{bk_code}"
            response = requests.request("GET", url, headers=self.headers)
            # 创建BeautifulSoup对象
            soup = BeautifulSoup(response.text, 'html.parser')

            # 查找表格
            table = soup.find('table', class_='m-table m-pager-table')

            # 查找所有行
            rows = table.find_all('tr')

            # 遍历每一行
            for row in rows[1:]:  # 跳过表头
                cols = row.find_all('td')
                if len(cols) > 1:
                    data.append((cols[1].text.strip(), cols[2].text.strip()))

            time.sleep(4)
            self.update_headers()

        return data

    def run(self):
        self.update_headers()
        bk_list = self.get_bk_list()
        for bk in bk_list:
            self.update_headers()
            bk_time = bk[0]
            bk_name = bk[1]
            bk_code = bk[3]
            bk_num = bk[4]
            print(f"开始获取{bk_code}的成分股数据...")
            for stock in self.get_bk_detail(bk_code, bk_num):
                print({
                    "bk_time": bk_time,
                    "bk_name": bk_name,
                    "stock_code": stock[0],
                    "stock_name": stock[1]
                })
            time.sleep(3)


# tong_hua_shun = tongHuaShun()
# # tong_hua_shun.get_bk_detail()
# tong_hua_shun.run()

east_money = eastMoney()
east_money.run()
