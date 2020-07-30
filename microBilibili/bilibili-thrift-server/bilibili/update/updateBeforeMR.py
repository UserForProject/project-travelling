import datetime

import pymongo

from bilibili.spider.biliob_fans_spider import get_up_info, get_fans_num, get_top50_up_info, get_subarea_heat, \
    get_tags_and_weight, get_up_all_video_info
#from bilibili.spider.potential_data_for_prediction import get_av_numbers, get_potential_data

user = "root"
pwd = "root"
host = "192.168.1.105"
port = "27017"
client = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(user, pwd, host, port))
bilibiliData = client["bilibili"]


def getUpInfo():
    """
    进行up主信息的更新，包括当日粉丝数以及粉丝变化量，以及榜单上可能会出现的所有up主头像及名称
    """
    users = bilibiliData["users"]
    today = datetime.datetime.now()
    yesterday = today + datetime.timedelta(-1)
    removeDate = today + datetime.timedelta(-7)
    today = today.strftime("%Y%m%d")
    yesterday = yesterday.strftime("%Y%m%d")
    upInfos = get_up_info()
    # 判断是否为第一次运行程序，防止重复更新uid带来的资源消耗
    if users.count() != 0:
        for up in upInfos:
            users.update_one({"uid": up["uid"]}, {"$set": {today: up["fans"]}}, True)
    else:
        for up in upInfos:
            users.insert_one({"uid": up["uid"], today: up["fans"]})
    # 查看数据是否有缺漏以及计算今日粉丝变化数
    upInfos = users.find({}, {"uid": 1, today: 1, yesterday: 1})
    for up in upInfos:
        if yesterday not in up.keys():
            users.update_one({"uid": up["uid"]}, {"$set": {"change": ""}})
        elif today not in up.keys():
            # 紧急获取该up当日粉丝数
            fans = get_fans_num(up["uid"])
            users.update_one({"uid": up["uid"]}, {"$set": {today: fans, "change": (fans - up[yesterday])}})
        else:
            users.update_one({"uid": up["uid"]}, {"$set": {"change": (up[today] - up[yesterday])}})
    # 获取当日需要姓名头像信息的所有uid
    userList = []
    data = users.find({}, {"uid": 1, today: 1}).sort([(today, -1)]).limit(50)
    for item in data:
        userList.append(item["uid"])
    data = users.find({"change": {"$ne": ""}}, {"uid": 1, "change": 1}).sort([("change", 1)]).limit(50)
    for item in data:
        userList.append(item["uid"])
    data = users.find({"change": {"$ne": ""}}, {"uid": 1, "change": 1}).sort([("change", -1)]).limit(50)
    for item in data:
        userList.append(item["uid"])
    # 去重并更新
    userList = list(set(userList))
    upInfos = get_top50_up_info(userList)
    for item in upInfos:
        users.update_one({"uid": item["uid"]}, {"$set":{"name": item["name"], "face": item["face"]}})

def getSubAreaInfo():
    data = get_subarea_heat()
    subAreaHeat = bilibiliData["subAreaHeat"]
    # 防止重复更新分区名带来的资源消耗，但后续分区的划分如果更新可能会出现问题
    if subAreaHeat.count() != 0:
        for key in data:
            subAreaHeat.update_one({"name": key}, {"$set": {"heat": data[key]}}, True)
    else:
        for key in data:
            subAreaHeat.insert_one({"name": key, "heat": data[key]})

# def getVideoData():
#     """
#     获取排行榜上1200个视频的详细信息（已丢弃该功能）
#     """
#     data = get_potential_data()
#     videos = bilibiliData["videos"]
#     for item in data:
#         print(item)
#         videos.insert_one(item)

def getUpVideos(uid):
    videos = get_up_all_video_info(uid)
    users = bilibiliData["users"]
    users.update_one({"uid": uid}, {"$set":{"videos": videos}}, True)


if __name__ == "__main__":
    getUpInfo()
    #getUpVideos(546195)
    getSubAreaInfo()
    # 设置词云输入文件的位置
    get_tags_and_weight("E:\Workspace\IdeaProjects\wordcloud\input\wc\input2.txt")
