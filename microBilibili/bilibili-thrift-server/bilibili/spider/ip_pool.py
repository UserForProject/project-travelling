import time
import requests
from bs4 import BeautifulSoup
import json


def check_ip(proxies_list):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/84.0.4147.89 Safari/537.36 '
    }

    # 定义能用的 ip 列表
    can_use = []

    # 通过访问百度来检测 代理ip 可用性
    for proxy in proxies_list:
        proxy_dict = {}
        fields = proxy.split("'")
        proxy_dict[fields[1]] = fields[3]
        try:
            response = requests.get('https://www.baidu.com', headers=headers, proxies=proxy_dict, timeout=0.1)
            if response.status_code == 200:
                can_use.append(proxy_dict)
        except Exception as e:
            print(e)

    print("可用的ip数量为： " + str(len(can_use)))
    print("===================================================")
    return can_use


def get_all_ip():
    urls = ["https://www.kuaidaili.com/free/inha/{}/".format(i) for i in range(1, 6)]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/84.0.4147.89 Safari/537.36 '
    }

    for url in urls:
        data = requests.get(url, headers=headers)
        soup = BeautifulSoup(data.text, 'lxml')

        proxies_list = []

        all_info_list = soup.find('tbody').find_all('tr')
        for all_info in all_info_list:
            proxies_dict = {}
            # 查找 ip 信息
            ip = all_info.find('td', attrs={'data-title': 'IP'}).text
            # 查找端口信息
            port = all_info.find('td', attrs={'data-title': 'PORT'}).text
            # 查找类型信息 -- HTTP | HTTPS
            http_type = all_info.find('td', attrs={'data-title': '类型'}).text

            # 构建 代理ip 字典，加入到代理列表中
            proxies_dict[http_type] = ip + ":" + port
            # print(proxies_dict)
            proxies_list.append(proxies_dict)

        time.sleep(1)
    return proxies_list


def get_all_ip2():
    proxies_list = get_all_ip()
    urls = ["http://www.ip3366.net/?stype=1&page={}".format(i) for i in range(1, 11)]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/84.0.4147.89 Safari/537.36 '
    }

    for url in urls:
        data = requests.get(url, headers=headers)
        soup = BeautifulSoup(data.text, 'lxml')

        all_info_list = soup.find('tbody').find_all('tr')
        for all_info in all_info_list:
            proxies_dict = {}
            info_elements = all_info.find_all('td')
            # 查找 ip 信息
            ip = info_elements[0].text
            # 查找端口信息
            port = info_elements[1].text
            # 查找类型信息 -- HTTP | HTTPS
            http_type = info_elements[3].text

            # 构建 代理ip 字典，加入到代理列表中
            proxies_dict[http_type] = ip + ":" + port
            # print(proxies_dict)
            proxies_list.append(proxies_dict)

        time.sleep(1)
    format_list = list(set([str(li) for li in proxies_list]))
    return format_list


if __name__ == '__main__':
    can_use = check_ip(get_all_ip2())
