import json
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options


def get_map_data():
    urls = ["https://you.ctrip.com/searchsite/district/?query=%e4%b8%ad%e5%9b%bd&isAnswered=&isRecommended" \
            "=&publishDate=&PageNo={}".format(str(i)) for i in range(1, 4)]
    # 设置无头浏览器进行爬取
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    # browser = webdriver.Chrome()

    # 定义字典变量存储爬取到的数据
    # 存储城市名称与城市具体信息的映射
    cityName_cityInfo = {}
    # 存储信息名称和信息值的映射
    infoName_infoValue = {}

    for url in urls:
        # 访问页面
        browser.get(url)

        # 获取城市详细页面的url
        a_elements = browser.find_elements_by_css_selector("body > div.content.cf > div.main > div.search-content.cf "
                                                           "> div > div.result > ul > li > a")
        city_urls = []
        for a_element in a_elements:
            city_urls.append(a_element.get_attribute("href"))
        # print(city_urls)

        # 访问到城市的详情页面以进一步获取数据
        for city_url in city_urls:
            browser.get(city_url)

            # 设置一些条件筛选掉非中国省份
            weather_element = element_filter(browser, "WeaTher", "id")
            if weather_element is None:
                # 获取当前省份|直辖市|特别行政区名称
                city_name = browser.find_element_by_css_selector("div.f_left").find_element_by_tag_name("a").text
                if len(city_name) == 0 or len(city_name) > 3:
                    continue
                # print(city_name)
                # 获取“游记分享“篇数、“精彩照片”张数、“实用问答”个数
                data_element = element_filter(browser, "dl.datacount", "css")
                if data_element is not None:
                    # 对应非省份的情况
                    data_count_elements = data_element.find_elements_by_tag_name("dd")
                    # print(city_name)
                    infoName_infoValue["url"] = city_url
                else:
                    # 第一热门旅游城市
                    hot_city = browser.find_element_by_css_selector("div.hot_destlist.cf").find_element_by_tag_name(
                        "li")
                    # 跳转到最热门城市的详情页面
                    hot_city_url = hot_city.find_element_by_tag_name("a").get_attribute("href")
                    browser.get(hot_city_url)
                    data_count_elements = browser.find_element_by_css_selector(
                        "dl.datacount").find_elements_by_tag_name("dd")
                    city_name = browser.find_element_by_css_selector("div.f_left").find_element_by_tag_name("a").text
                    # print(city_name)
                    infoName_infoValue["url"] = hot_city_url
                data_count_list = []
                for data_count_element in data_count_elements:
                    data_count = int(data_count_element.find_element_by_tag_name("span").text)
                    data_count_list.append(data_count)
                infoName_infoValue["travelling_notes"] = data_count_list[0]
                infoName_infoValue["pictures"] = data_count_list[1]
                infoName_infoValue["question_answer"] = data_count_list[2]
                # print(infoName_infoInfo)
                # 获取“想去”人数
                want_number = int(browser.find_element_by_id("emWantValueID").text)
                infoName_infoValue["wanting"] = want_number
                # 获取“去过”人数
                been_number = int(browser.find_element_by_id("emWentValueID").text)
                infoName_infoValue["been_to"] = been_number
                # print(infoName_infoValue)
                # 建立字典映射关系
                cityName_cityInfo[city_name] = infoName_infoValue
                infoName_infoValue = {}
    browser.quit()
    return cityName_cityInfo


def element_filter(driver, locator, way):
    if way == "css":
        try:
            target_element = driver.find_element_by_css_selector(locator)
            return target_element
        except NoSuchElementException as error:
            return None
    elif way == "id":
        try:
            target_element = driver.find_element_by_id(locator)
            return target_element
        except NoSuchElementException as error:
            return None


def get_scenery_info(url):
    # 设置无头浏览器进行爬取
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    # browser = webdriver.Chrome()

    # 定义要返回的对象列表
    scenery_info_list = []

    # sight：必游  restaurant：必吃   shopping：必逛
    tag_list = ["sight", "restaurant", "shopping"]
    for i in range(3):
        browser.get(url)
        ActionChains(browser).move_to_element(
            browser.find_element_by_css_selector("a.{}".format(tag_list[i]))).perform()
        # 获取某标签下的 6 个景点信息
        if i == 0:
            spot_elements = browser.find_elements_by_css_selector("#poi_{} > ul > li > a".format(str(i)))
        else:
            spot_elements = browser.find_elements_by_css_selector("#poi_{} > ul > li > a".format(str(i + 1)))
        # 获取景点 url 列表
        scenery_url_list = []
        for spot_element in spot_elements:
            scenery_url_list.append(spot_element.get_attribute("href"))
        for scenery_url in scenery_url_list:
            browser.get(scenery_url)
            # 构造 SceneryInfo 对象
            scenery_info = {}
            # 设置景点标签
            scenery_info["tag"] = tag_list[i]
            # 定义评论字典供使用
            comments_dict = {}
            if i == 0:
                # 对应“必游”标签情形，其页面解析方法不同
                # 获取景点名称
                scenery_info["name"] = browser.find_element_by_css_selector(
                    '#__next > div.poiDetailPageWrap > div > div.baseInfoModule > div.baseInfoMain > div.title > h1').text
                # print(scenery_info["name"])
                # 获取评论详情
                comments_elements = browser.find_elements_by_css_selector("span.hotTag")
                # 根据标签内容筛选除去无用评论标签分类
                useless_element_flag = True
                for comments_element in comments_elements:
                    if useless_element_flag:
                        if comments_element.text.find("来自旅拍") != -1:
                            useless_element_flag = False
                        continue
                    comments_tag = comments_element.text.split("(")[0]
                    comments_num = int(comments_element.text.split("(")[1].split(")")[0])
                    comments_dict[comments_tag] = comments_num
                # print(comments_dict)
            else:
                # 获取景点名称
                scenery_info["name"] = browser.find_element_by_css_selector("div.f_left").find_element_by_tag_name(
                    "h1").text
                # print(scenery_info["name"])
                # 获取评论详情
                comments_elements = browser.find_element_by_css_selector("ul.tablist").find_elements_by_tag_name("li")
                # 筛除第 1 个评论标签
                first_element_flag = True
                for comments_element in comments_elements:
                    if first_element_flag:
                        first_element_flag = False
                        continue
                    comments_tag = comments_element.text.split("(")[0]
                    comments_num = comments_element.text.split("(")[1].split(")")[0]
                    comments_dict[comments_tag] = comments_num
                # print(comments_dict)
            scenery_info["comments"] = comments_dict
            scenery_info_list.append(scenery_info)
            # 清空元素内容以便下一循环使用
            comments_dict = {}
            scenery_info = {}

    browser.quit()
    return scenery_info_list


# def get_latitude_longitude():
#     city_names = get_map_data().keys()
#     # 设置无头浏览器进行爬取
#     # chrome_options = Options()
#     # chrome_options.add_argument('--headless')
#     # browser = webdriver.Chrome(chrome_options=chrome_options)
#     browser = webdriver.Chrome()
#     # 定义存储城市：经纬度的字典
#     city_la_lo_dict = {}
#     # 获取每个城市的经纬度坐标
#     browser.get("http://map.jiqrxx.com/jingweidu/")
#     input_element = browser.find_element_by_id("address")
#     submit_button = browser.find_element_by_css_selector("div.nav").find_element_by_tag_name("button")
#     # 找到对应省份的经纬度信息
#     for name in city_names:
#         input_element.click()
#         input_element.clear()
#         input_element.click()
#         time.sleep(2)
#         input_element.send_keys(name)
#         submit_button.click()
#         time.sleep(1)
#         la_lo_info = browser.find_element_by_id("centerDiv").text
#         info_dict = {}
#         info_dict["latitude"] = float(la_lo_info.split('  ')[0].split(', ')[0])
#         info_dict["longitude"] = float(la_lo_info.split('  ')[0].split(', ')[1])
#         city_la_lo_dict[name] = info_dict
#         print(name + ": " + str(info_dict))
#
#     browser.quit()
#     with open("map_data.json", "w") as f:
#         f.write(json.dumps(city_la_lo_dict, ensure_ascii=False, indent=4, separators=(',', ':')))


# if __name__ == "__main__":
#     get_latitude_longitude()
#     scenery_info_list = get_scenery_info("https://you.ctrip.com/place/dengfeng1014.html")
#     for scenery_info in scenery_info_list:
        # print(str(scenery_info))
    # start = time.time()
    # get_map_data()
    # end = time.time()
    #
    # print(end - start)


