#!/usr/bin/env python
# coding:utf-8
# python version 2.7
# https://fofa.so/ 搜索结果提取

import urllib
from bs4 import BeautifulSoup
import requests, sys, base64, time


def spider_href_info(key='', ucookie=''):
    # 网站新添了验证码，只能使用cookie登陆了
    header = {
        "Connection": "keep-alive",
        "Cookie": "_fofapro_ars_session=" + ucookie,
    }
    code = key.decode('gbk')
    code = urllib.quote(base64.b64encode(code))
    print("https://fofa.so/result?&qbase64=" + code)
    # 定位总数
    html = requests.get(url="https://fofa.so/result?&qbase64=" + code,
                        headers=header).content
    soup = BeautifulSoup(html)
    total_entries = soup.find(name="input", attrs={"id": "total_entries"}).attrs['value']
    print('total_entries :' + str(total_entries))
    page = (int(total_entries, 10) / 10) + 1
    if len(ucookie) < 32:  # 不登陆，只能提取前10条数据
        page = 1
    # 按页获取
    if total_entries > 0:
        for i in range(1, page + 1):
            time.sleep(2)  # 防封延时
            html = requests.get(
                url="https://fofa.so/result?full=true&page=" + str(i) + "&qbase64=" + code,
                headers=header).content
            soup = BeautifulSoup(html)
            # 提取每页信息
            hreflist = []
            divs = soup.find_all(name="div", attrs={"class": "list_mod"})
            for d in divs:
                url = d.find(name="div", attrs={"class": "list_mod_t"}).find('a').attrs['href']  # 单项的url
                info = ' '.join(d.find(name="ul", attrs={"class": "list_sx1"}).text.split())  # 单项的列表信息
                live = str(d.find(name="div", attrs={"class": "auto-wrap"}).text[:64])  # 存活状态
                if live.find('200') != -1:
                    hreflist.append([url, info])
            print i, hreflist.__len__()
            # 你的操作
            with open('hreffile.txt', 'ab') as f:
                for u in hreflist:
                    f.write(str(u[0] + '\n'))
            # 普通会员只能翻5页，若是正式会员请注释该代码
            if i == 5:
                break

    print('spider_href_info end:' + key)


if __name__ == '__main__':
    print('Example: xxx.py [key] [yourcookie]')
    # 编码设置
    reload(sys)
    sys.setdefaultencoding('utf8')

    print(sys.argv)
    if sys.argv.__len__() == 2:
        spider_href_info(sys.argv[1])
    elif sys.argv.__len__() == 3:
        spider_href_info(sys.argv[1], sys.argv[2])
