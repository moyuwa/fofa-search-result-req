#!/usr/bin/env python
# coding:utf-8
# python version 2.7
# https://fofa.so/ 搜索结果提取

import urllib
from bs4 import BeautifulSoup
import requests, sys, base64, time


def writefile(datalist=[]):
    with open('hreffile.txt', 'ab') as f:
        for u in datalist:
            f.write(str(u[0] + '\n'))


# 提取每页信息
def spider_page_1(html):
    soup = BeautifulSoup(html, 'html.parser')
    hreflist = []
    divs = soup.find_all(name="div", attrs={"class": "list_mod"})
    for d in divs:
        url = d.find(name="div", attrs={"class": "list_mod_t"}).find('a').attrs['href']  # 单项的url
        info = ' '.join(d.find(name="ul", attrs={"class": "list_sx1"}).text.split())  # 单项的列表信息
        live = str(d.find(name="div", attrs={"class": "auto-wrap"}).text[:64])  # 存活状态
        # uls = d.find(name="ul", attrs={"class": "list_sx1"})  # 详细提取单项的列表信息
        # for ul in uls:
        #     if ul.name == 'li':
        #         print(ul.text.replace('\n', ''))
        if live.find('200') != -1:
            hreflist.append([url, info])
    return hreflist


# 定位总数
def spider_total_entries(header, code):
    html = requests.get(url="https://fofa.so/result?full=true&qbase64=" + code,
                        headers=header).content
    soup = BeautifulSoup(html, 'html.parser')
    total_entries = soup.find(name="input", attrs={"id": "total_entries"}).attrs['value']
    return total_entries


# 按页获取
def spider_page_all(header, code, page):
    for i in range(1, page + 1):
        time.sleep(2)  # 防封延时
        html = requests.get(
            url="https://fofa.so/result?full=true&page=" + str(i) + "&qbase64=" + code,
            headers=header).content
        # 你的操作
        datalist = spider_page_1(html)
        writefile(datalist)
        print(i, datalist.__len__())
        # 普通会员只能翻5页，若是正式会员请注释该代码
        if i == 5:
            break


# 枚举中国城市获取更多
def spider_CN_city(key='', ucookie=''):
    header = {"Connection": "keep-alive", "Cookie": "_fofapro_ars_session=" + ucookie}
    citylist = [['Zhejiang', '浙江'], ['Unknown', '未知'], ['Beijing', '北京'], ['Guangdong', '广东'], ['Shandong', '山东'],
                ['Jilin', '吉林'], ['Shanghai', '上海'], ['Jiangsu', '江苏'], ['Henan', '河南'], ['Shanxi', '山西'],
                ['Liaoning', '辽宁'], ['Fujian', '福建'], ['Sichuan', '四川'], ['Guangxi', '广西'], ['Hubei', '湖北'],
                ['Heilongjiang', '黑龙江'], ['Hunan', '湖南'], ['Shaanxi', '陕西'], ['Tianjin', '天津'], ['Hebei', '河北'],
                ['Jiangxi', '江西'], ['Chongqing', '重庆'], ['Yunnan', '云南'], ['Anhui', '安徽'], ['Gansu', '甘肃'],
                ['Inner Mongolia Autonomous Region', '内蒙古自治区'], ['Guizhou', '贵州'],
                ['Ningsia Hui Autonomous Region', '宁陕回族自治区'],
                ['Ningxia Hui Autonomous Region', '宁夏回族自治区'], ['Hainan', '海南'], ['Xinjiang', '新疆'], ['Qinghai', '青海'],
                ['Tibet', '西藏']]
    for c in citylist:
        code = key.decode('gbk') + ' && country=\"CN\" && region=\"' + c[0] + '\"'  # 解码？
        code = urllib.quote(base64.b64encode(code))
        # 获取总数，确定页数
        total_entries = spider_total_entries(header, code)
        page = (int(total_entries, 10) / 10) + 1
        if len(ucookie) < 32:  # 不登陆，只能提取前10条数据
            page = 1
        print('total_entries :' + str(total_entries), 'page :' + str(page))
        # 搜索结果获取
        if total_entries > 0:
            spider_page_all(header, code, page)
    print('spider_CN_city end:' + key)


def spider_fofa_info(key='', ucookie=''):
    # 网站新添了验证码，只能使用cookie登陆了
    header = {"Connection": "keep-alive", "Cookie": "_fofapro_ars_session=" + ucookie}
    code = key.decode('gbk')
    code = urllib.quote(base64.b64encode(code))
    print("https://fofa.so/result?full=true&qbase64=" + code)
    # 获取总数，确定页数
    total_entries = spider_total_entries(header, code)
    page = (int(total_entries, 10) / 10) + 1
    if len(ucookie) < 32:  # 不登陆，只能提取前10条数据
        page = 1
    print('total_entries :' + str(total_entries), 'page :' + str(page))
    # 搜索结果获取
    if total_entries > 0:
        spider_page_all(header, code, page)
    print('spider_href_info end:' + key)


if __name__ == '__main__':
    print('Example: xxx.py "port=\\"80\\"" [cookie]')
    # 编码设置
    reload(sys)
    sys.setdefaultencoding('utf8')

    print(sys.argv)
    if sys.argv.__len__() == 2:
        spider_fofa_info(sys.argv[1])
        # spider_CN_city(sys.argv[1])
    elif sys.argv.__len__() == 3:
        spider_fofa_info(sys.argv[1], sys.argv[2])
        # spider_CN_city(sys.argv[1], sys.argv[2])
