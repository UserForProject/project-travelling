import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


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
        load_more.click()
        time.sleep(3)

    info_elements = browser.find_elements_by_xpath('/html/body/div/div/div/div/main/div/div/div/div[2]/div/div[2]/div[2]/span/div')
    for info_element in info_elements:
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
        face_url = face_element.get_attribute('style')
        'v-image__image v-image__image--cover'
        print(face_url)
        uid_fans_dict['name'] = username
        uid_fans_dict['uid'] = int(uid)
        uid_fans_dict['fans'] = int(fans_num)
        up_info_list.append(uid_fans_dict)

    browser.quit()
    return up_info_list


# def

if __name__ == '__main__':
    info_list = get_up_info()
    for info in info_list:
        print(info)
