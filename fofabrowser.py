#!/usr/bin/env python
# coding:utf-8
# python version 2.7
# https://fofa.so/ 搜索结果提取 (浏览器版本) by 6time

import os, sys
import json, base64, time, datetime
import urllib, requests
from bs4 import BeautifulSoup

# 编码设置
reload(sys)
sys.setdefaultencoding('utf8')


class fofabrower():
    def __init__(self):
        self._ucookie = ""
        self._header = ""
        self._code = ""
        pass

    # 定位总数
    def spider_total_entries(self):
        while 1:
            try:
                html = requests.get(url="https://fofa.so/result?qbase64=" + self._code,
                                    headers=self._header).content  # full=true
                if "Retry later" in html:
                    time.sleep(10)  # 请求频繁就等一等
                else:
                    break
            except requests.exceptions.ConnectionError:
                time.sleep(10)
        soup = BeautifulSoup(html, 'html.parser')
        total_entries = soup.find(name="span", attrs={"class": "pSpanColor"}).text#.attrs['value']
        total_entries=total_entries.replace(',','')
        page = (int(total_entries, 10) / 10) + 1
        print('total_entries :' + str(total_entries), 'page :' + str(page))
        if total_entries == 0:
            return
        self.spider_page_all(1, page)

    # 按页获取
    def spider_page_all(self, page1, page2):
        for i in range(page1, page2 + 1):
            time.sleep(2)
            urls = "https://fofa.so/result?page=" + str(i) + "&qbase64=" + self._code  # full=true
            print(urls)
            while 1:
                try:
                    html = requests.get(url=urls, headers=self._header).content
                    if "Retry later" in html:
                        time.sleep(10)  # 请求频繁就等一等
                    else:
                        break
                except requests.exceptions.ConnectionError:
                    time.sleep(10)
            if "出错了!</div>" in html:
                break
            # 你的操作
            datalist = self.spider_page_1(html)
            self.writefile(datalist)
            print("%d/%d:%d" % (i, page2, datalist.__len__()))
            # 注册会员只能翻5页
            if i == 5 and self._fofajson["fofabrowser"]["isvip"] == "False":
                break
            if len(self._ucookie) < 32:  # 不登陆，只能提取前10条数据
                break

    # 提取每页信息
    def spider_page_1(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        hreflist = []
        divs = soup.find_all(name="div", attrs={"class": "list_mod"})
        for d in divs:
            top1 = d.find(name="div", attrs={"class": "list_mod_t"}).find_all('a')
            host = top1[0].text.rstrip()  # 开始提取信息
            port = top1[1].text
            if len(top1) > 2:
                protocol = top1[2].text
            else:
                protocol = ""
            top2 = d.find(name="ul", attrs={"class": "list_sx1"}).find_all(name="li")  # 详细提取单项的列表信息
            try:
                title = top2[0].text.replace('\n', '').replace(' ', '')
            except:
                title = ""
            for li in top2:
                if li.find(name="i", attrs={"class": "fa-cog"}) is not None:
                    system = li.text
                if li.find(name="i", attrs={"class": "fa-map-marker"}) is not None:
                    ip = li.text.replace('\r', '').replace('\n', '').replace(' ', '')
            headertext = str(d.find(name="div", attrs={"class": "auto-wrap"}).text[:256])  # 右边响应头
            if headertext.find('Server:') == -1:
                server = ""
            else:
                s = headertext[headertext.find('Server:'):]  # Server: nginx
                s2 = s[:s.find('\n')].replace('\r', '').split(':')
                if len(s2) > 1:
                    server = s2[1]
                else:
                    server = ""
            l1 = [host, ip, port, server, protocol, title]
            hreflist.append(l1)
        return hreflist

    # 枚举中国城市获取更多
    def spider_CN_city(self, key):
        citylist = [['Zhejiang', '浙江'], ['Unknown', '未知'], ['Beijing', '北京'], ['Guangdong', '广东'], ['Shandong', '山东'],
                    ['Jilin', '吉林'], ['Shanghai', '上海'], ['Jiangsu', '江苏'], ['Henan', '河南'], ['Shanxi', '山西'],
                    ['Liaoning', '辽宁'], ['Fujian', '福建'], ['Sichuan', '四川'], ['Guangxi', '广西'], ['Hubei', '湖北'],
                    ['Heilongjiang', '黑龙江'], ['Hunan', '湖南'], ['Shaanxi', '陕西'], ['Tianjin', '天津'], ['Hebei', '河北'],
                    ['Jiangxi', '江西'], ['Chongqing', '重庆'], ['Yunnan', '云南'], ['Anhui', '安徽'], ['Gansu', '甘肃'],
                    ['Inner Mongolia Autonomous Region', '内蒙古自治区'], ['Guizhou', '贵州'],
                    ['Ningsia Hui Autonomous Region', '宁陕回族自治区'],
                    ['Ningxia Hui Autonomous Region', '宁夏回族自治区'], ['Hainan', '海南'], ['Xinjiang', '新疆'],
                    ['Qinghai', '青海'],
                    ['Tibet', '西藏']]
        for c in citylist:
            query_str = key + ' && country=\"CN\" && region=\"' + c[0] + '\"'  # 解码？l
            self.spider_page_all(query_str)

    def writefile(self, datalist=[]):
        with open(self.filename, 'ab') as f:
            for r in datalist:
                # f.write(str(r[0] + '\n'))
                w = "%s,%s:%s,%s,%s,%s\n" % (r[0], r[1], r[2], r[3], r[4], r[5].encode('utf-8'))
                f.write(w)

    def run(self):
        jsonpath = os.getcwd() + "\\fofa.json"
        print(jsonpath)
        with open(jsonpath, 'r') as f:
            self._fofajson = json.load(f)
        self._ucookie = self._fofajson["fofabrowser"]["_fofapro_ars_session"]
        for q in self._fofajson["query_list"]:
            dt = datetime.datetime.now()
            self.filename = "%d%02d%02d-%02d%02d%02d.csv" % (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
            print('query_str:%s' % q)
            self._header = {"Connection": "keep-alive", "Cookie": "_fofapro_ars_session=" + self._ucookie}
            self._code = urllib.quote(base64.b64encode(q))
            if self._fofajson["fofabrowser"]["CN_city"] == "False":
                self.spider_total_entries()
                # self.spider_page_all(326, 962)
            else:
                self.spider_CN_city(q)


if __name__ == '__main__':
    _fb = fofabrower()
    _fb.run()
