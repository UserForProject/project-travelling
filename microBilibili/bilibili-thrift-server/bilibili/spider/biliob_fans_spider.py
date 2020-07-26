import os
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import json
import requests

# 定义请求头，将会多次使用
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
}


def get_up_info():
    url = 'https://www.biliob.com/authorlist'
    # 设置无头浏览器进行爬取
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    # browser = webdriver.Chrome()
    browser.get(url)
    time.sleep(1)

    # 定义一个信息 list 作为函数的返回值
    up_info_list = []

    # 消除进入页面时的弹出框
    i_got_it = browser.find_element_by_css_selector(
        'button.v-btn.v-btn--flat.v-btn--text.theme--light.v-size--default.primary--text')
    i_got_it.click()

    # 点击“加载更多”，在网页信息达到一定数量后再进行整体爬取
    click_time = 29
    for i in range(click_time):
        load_more = browser.find_element_by_css_selector(
            'button.v-btn.v-btn--block.v-btn--depressed.v-btn--flat.v-btn--outlined.v-btn--tile.theme--light.v-size--default.primary--text')
        # browser.execute_script("arguments[0].scrollIntoView();", load_more)
        load_more.click()
        time.sleep(2)

    info_elements = browser.find_elements_by_xpath(
        '/html/body/div/div/div/div/main/div/div/div/div[2]/div/div[2]/div[2]/span/div')
    for info_element in info_elements:
        # ActionChains(browser).move_to_element(info_element).perform()
        time.sleep(0.2)
        uid_fans_dict = {}
        uid_info = info_element.find_element_by_css_selector('div.row.no-gutters').text
        # 获取排行榜 up主 的 uid
        uid = uid_info.split()[2]
        # print(uid)
        # 获取排行榜 up主 的粉丝数
        general_info = info_element.find_element_by_css_selector('div.row.mt-2.no-gutters').text
        fans_num = general_info.split()[1].replace(',', '')
        # print(fans_num)
        # print(face_url)
        uid_fans_dict['uid'] = int(uid)
        uid_fans_dict['fans'] = int(fans_num)
        up_info_list.append(uid_fans_dict)

    browser.quit()
    return up_info_list


# 供数据库更新使用的快速返回粉丝数的爬虫
def get_fans_num(uid):
    api_url = 'http://api.bilibili.com/x/web-interface/card?mid={}'.format(uid)
    r = requests.get(api_url, headers=headers)
    try:
        r.raise_for_status()
    except:
        print("您查询的用户不存在或访问过于频繁，请稍后再试.")
    r.encoding = r.apparent_encoding
    json_str = r.text
    user_dict = json.loads(json_str)
    fans_num = user_dict['data']['card']['fans']
    return fans_num


# 获取粉丝数目排行榜的 top50 up主的信息（用于使用在排行榜中）
def get_top50_up_info(uid_list):
    api_url = 'http://api.bilibili.com/x/space/acc/info?mid={}'
    # 定义一个列表用于返回 up 主信息
    user_show_list = []
    for uid in uid_list:
        info_dict = {}
        r = requests.get(api_url.format(uid), headers=headers)
        try:
            r.raise_for_status()
        except:
            print("您查询的用户不存在或访问过于频繁，请稍后再试.")
        r.encoding = r.apparent_encoding
        # 解析 json
        json_str = r.text
        user_dict = json.loads(json_str)
        name = user_dict['data']['name']
        face_url = user_dict['data']['face']
        info_dict['uid'] = uid
        info_dict['name'] = name
        info_dict['face'] = face_url
        user_show_list.append(info_dict)
    print(user_show_list)
    return user_show_list


# 查询详细信息的爬虫
def get_detailed_info(uid):
    url = 'https://space.bilibili.com/{}'.format(uid)
    # 设置无头浏览器进行爬取
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    #browser = webdriver.Chrome()
    browser.get(url)

    # 定义 dict 作为详细信息的返回值
    detailed_info_dict = {}

    # 空间主页上的投稿按钮
    contribute_element = browser.find_element_by_css_selector("a.n-btn.n-video.n-audio.n-article.n-album")
    contribute_element.click()
    # 获取up主头像图片url
    faca_url = browser.find_element_by_id('h-avatar').get_attribute('src')
    detailed_info_dict['face'] = faca_url
    # 获取up主用户名
    username = browser.find_element_by_id('h-name').text
    detailed_info_dict['name'] = username
    # 获取up主的等级信息
    level = browser.find_element_by_css_selector('a.h-level.m-level').get_attribute('lvl')
    detailed_info_dict['level'] = int(level)
    # 获取up主的关注人数
    follow_num = browser.find_element_by_id('n-gz').text
    detailed_info_dict['follow'] = int(follow_num)
    # 获取up主的粉丝数
    fans_num = browser.find_element_by_css_selector('a.n-data.n-fs').get_attribute('title').replace(",", "")
    detailed_info_dict['follower'] = int(fans_num)

    # 获得up主的获赞数、播放数、阅读数
    data_elements = browser.find_elements_by_css_selector('div.n-data.n-bf')
    # 获赞数
    likes = data_elements[0].get_attribute('title').split('赞')[1].replace(",", "")
    detailed_info_dict['likes'] = int(likes)
    # 播放数
    play_amount = data_elements[1].get_attribute('title').split('为')[1].replace(",", "")
    detailed_info_dict['playAmount'] = play_amount
    # 阅读数
    # 由于存在某些up主从未发过专栏的情况，因此有可能阅读数标签不存在，需要添加判断条件
    if len(data_elements) == 6:
        reading_amount = data_elements[2].get_attribute('title').split('为')[1].replace(",", "")
        detailed_info_dict['readingAmount'] = int(reading_amount)
    else:
        detailed_info_dict['readingAmount'] = 0

    # 获取最多播放的视频信息
    video_info_list = []
    # 定位并点击最多播放按钮
    most_popular_videos_element = \
    browser.find_element_by_css_selector('ul.be-tab-inner.clearfix').find_elements_by_tag_name('li')[1]
    most_popular_videos_element.click()
    time.sleep(0.5)
    video_elements = browser.find_elements_by_css_selector('a.cover')
    for i in range(3):
        video_info_dict = {}
        # 获取视频链接
        video_info_dict['video_url'] = video_elements[i].get_attribute('href')
        img_element = video_elements[i].find_element_by_tag_name('img')
        # 获取视频封面
        video_info_dict['video_cover'] = img_element.get_attribute('src')
        # 获取视频标题
        video_info_dict['video_title'] = img_element.get_attribute('alt')
        video_info_list.append(video_info_dict)
    detailed_info_dict['video'] = video_info_list

    time.sleep(5)
    browser.quit()
    return detailed_info_dict


# 定义一个判断元素是否存在的函数
def element_exists(element, tag_name):
    try:
        element.find_element_by_tag_name(tag_name)
        return True
    except NoSuchElementException:
        return False


# 获取各分区视频下的标签和综合评分的数据
def get_tags_and_weight(output_path):
    url = 'https://www.bilibili.com/ranking'
    # 设置无头浏览器进行爬取
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    # browser = webdriver.Chrome()
    browser.get(url)

    url_pts_dict = {}
    # 找到各个分区的点击按钮，逐个点击获取排行榜上所有分区标签，获得榜上所有视频的 url 链接 -- 1200
    subarea_tags = browser.find_element_by_css_selector('ul.rank-tab').find_elements_by_tag_name('li')
    for i in range(1, 13):
        subarea_tags[i].click()
        time.sleep(0.6)
        video_elements = browser.find_elements_by_css_selector('li.rank-item')
        for video_element in video_elements:
            video_url = video_element.find_element_by_css_selector('div.img').find_element_by_tag_name('a').get_attribute('href')
            pts = video_element.find_element_by_css_selector('div.pts').find_element_by_tag_name('div').text
            url_pts_dict[video_url] = int(pts)

    # 每次调用函数写入之前清空文件内容
    with open(output_path, 'w') as f:
        f.truncate()

    # 访问各个视频详细页面，获取播放量、标签数据
    # 设置标签的权重
    weight = 0.8
    for video_url in list(url_pts_dict.keys()):
        browser.get(video_url)
        time.sleep(0.5)
        # 获取标签
        try:
            tag_elements = browser.find_elements_by_css_selector('a.tag-link')
        except NoSuchElementException:
            # 对应视频链接里没有标签数据的情况（动画番剧）
            continue
        for tag_element in tag_elements:
            tag_name = tag_element.text
            # 判断该标签是否标蓝（蓝色代表该标签更重要，所占权重更大）
            if element_exists(tag_element, 'img'):
                tag_weight = round(url_pts_dict[video_url] * weight, 1)
            else:
                tag_weight = round(url_pts_dict[video_url] * (1 - weight), 1)
            # print(tag_name + ': ' + str(tag_weight))
            # 将得到的数据写入文件
            with open(output_path, 'a', encoding='UTF-8') as f:
                f.write(tag_name)
                f.write('\t')
                f.write(str(tag_weight))
                f.write(os.linesep)

    browser.quit()


# 获取各分区视频的综合评分之和
def get_subarea_heat():
    url = 'https://www.bilibili.com/ranking'
    # 设置无头浏览器进行爬取
    # chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # browser = webdriver.Chrome(chrome_options=chrome_options)
    browser = webdriver.Chrome()
    browser.get(url)

    subarea_pts_dict = {}
    # 找到各个分区的点击按钮，逐个点击获取排行榜上所有分区标签，获得榜上所有视频的 url 链接 -- 1200
    subarea_tags = browser.find_element_by_css_selector('ul.rank-tab').find_elements_by_tag_name('li')
    for i in range(1, 13):
        subarea_tags[i].click()
        subarea_name = subarea_tags[i].text
        time.sleep(0.6)
        video_elements = browser.find_elements_by_css_selector('li.rank-item')
        pts_sum = 0
        for video_element in video_elements:
            pts = video_element.find_element_by_css_selector('div.pts').find_element_by_tag_name('div').text
            pts_sum = pts_sum + int(pts)
        subarea_pts_dict[subarea_name] = pts_sum
        print(subarea_name + ": " + str(pts_sum))
    return subarea_pts_dict


# if __name__ == '__main__':
    # info_list = get_up_info()
    # for info in info_list:
    #     print(info)
    # get_top50_up_info([1, 2, 3])
    # print(get_subarea_heat())
    # get_tags_and_weight('D://comment.txt')
    # get_subarea_heat()
