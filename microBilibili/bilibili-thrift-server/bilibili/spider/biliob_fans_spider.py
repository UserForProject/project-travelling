import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


def get_up_info():
    url = 'https://www.biliob.com/authorlist'
    # 设置无头浏览器进行爬取
    # chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # browser = webdriver.Chrome(chrome_options=chrome_options)
    browser = webdriver.Chrome()
    browser.get(url)
    time.sleep(1)

    # 定义一个信息 list 作为函数的返回值
    up_info_list = []

    # 消除进入页面时的弹出框
    i_got_it = browser.find_element_by_css_selector('button.v-btn.v-btn--flat.v-btn--text.theme--light.v-size--default.primary--text')
    i_got_it.click()

    # 点击“加载更多”，在网页信息达到一定数量后再进行整体爬取
    click_time = 3
    for i in range(click_time):
        load_more = browser.find_element_by_css_selector(
            'button.v-btn.v-btn--block.v-btn--depressed.v-btn--flat.v-btn--outlined.v-btn--tile.theme--light.v-size--default.primary--text')
        # browser.execute_script("arguments[0].scrollIntoView();", load_more)
        load_more.click()
        time.sleep(2)

    info_elements = browser.find_elements_by_xpath('/html/body/div/div/div/div/main/div/div/div/div[2]/div/div[2]/div[2]/span/div')
    # 鼠标移动到指定元素以使用 js 将头像图片动态加载出来
    for info_element in info_elements:
        ActionChains(browser).move_to_element(info_element).perform()

    for info_element in info_elements:
        # ActionChains(browser).move_to_element(info_element).perform()
        time.sleep(0.2)
        uid_fans_dict = {}
        uid_info = info_element.find_element_by_css_selector('div.row.no-gutters').text
        # 获取排行榜 up主 的 uid
        uid = uid_info.split()[2]
        # 获取排行榜 up主 的用户名
        username = uid_info.split()[0]
        # print(uid)
        # 获取排行榜 up主 的粉丝数
        general_info = info_element.find_element_by_css_selector('div.row.mt-2.no-gutters').text
        fans_num = general_info.split()[1].replace(',', '')
        # print(fans_num)
        # 获取排行榜 up主 的头像
        face_element = info_element.find_element_by_css_selector("div.v-image__image.v-image__image--cover")
        face_url = face_element.get_attribute('style').split("\"")[1]
        # print(face_url)
        uid_fans_dict['name'] = username
        uid_fans_dict['uid'] = int(uid)
        uid_fans_dict['fans'] = int(fans_num)
        uid_fans_dict['face'] = face_url
        up_info_list.append(uid_fans_dict)

    browser.quit()
    return up_info_list


# def

# if __name__ == '__main__':
#     info_list = get_up_info()
#     for info in info_list:
#         print(info)
