import datetime

import pymongo

from bilibili.spider.biliob_fans_spider import get_up_info, get_fans_num

user = "root"
pwd = "root"
host = "192.168.2.108"
port = "27017"
client = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(user, pwd, host, port))
bilibiliData = client["bilibili"]


def getUpInfo():
    """
    进行up主信息的更新，包括当日粉丝数以及粉丝变化量
    """
    users = bilibiliData["users"]
    today = datetime.datetime.now()
    yesterday = today + datetime.timedelta(-1)
    removeDate = today + datetime.timedelta(-7)
    today = today.strftime("%Y%m%d")
    yesterday = yesterday.strftime("%Y%m%d")
    removeDate = removeDate.strftime("%Y%m%d")
    users.update_many({}, {"$unset": {removeDate: ""}})
    upInfos = get_up_info()
    if users.count() != 0:
        for up in upInfos:
            users.update_one({"uid": up["uid"]}, {"$set": {today: up["fans"]}}, True)
    else:
        for up in upInfos:
            users.insert_one({"uid": up["uid"], today: up["fans"]})
    data = users.find({}, {"uid": 1, today: 1, yesterday: 1})
    for up in data:
        if yesterday not in up.keys():
            users.update_one({"uid": up["uid"]}, {"change": ""})
        elif today not in up.keys():
            # 紧急获取该up当日粉丝数
            fans = get_fans_num(up["uid"])
            users.update_one({"uid": up["uid"]}, {"$set": {today: fans, "change": (fans - up[yesterday])}})
        else:
            users.update_one({"uid": up["uid"]}, {"change": (up[today] - up[yesterday])})



if __name__ == "__main__":
    get_up_info()