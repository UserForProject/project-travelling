import pymongo
from threading import Timer
from spider.spider_ctrip import *
from spider.api.ttypes import SceneryInfo
# import pprint


# 数据库的基本配置信息
user = "root"
pwd = "root"
host = "192.168.2.108"
port = "27017"


class Mapper:
    client = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(user, pwd, host, port))
    mapdata = client["microTravelling"]["mapdata"]

    def __init__(self):
        # 每12小时进行一次数据更新，初始化时首先进行一次更新
        t = Timer(0, self.updateInfo)
        t.start()

    def updateInfo(self):
        # 进行地图相关数据的更新
        # 每12h更新一次数据, 使用timer保证非阻塞式更新
        # localtime = time.asctime( time.localtime(time.time()) )
        # print("本地时间为 :", localtime)
        t = Timer(43200, self.updateInfo)
        t.start()
        spider_data = get_map_data()
        keys = spider_data.keys()
        # 首先更新地图数据（访问最频繁）
        for key in keys:
            temp = spider_data[key]
            temp["name"] = key
            Mapper.mapdata.update_one({"name": key}, {"$set": temp}, True)
        # localtime = time.asctime( time.localtime(time.time()) )
        # print("本地时间为 :", localtime)
        # 根据更新后的url进行相关数据的更新
        urls = list(Mapper.mapdata.find({},{"url": 1}))
        for item in urls:
            url = item["url"]
            data = get_scenery_info(url)
            Mapper.mapdata.update_one({"url": url}, {"$set": {"attractions": data}})
        # localtime = time.asctime( time.localtime(time.time()) )
        # print("本地时间为 :", localtime)

    def getLocationInfo(self):
        # 地图初始化相关数据
        all_provinces = list(Mapper.mapdata.find({}, {"_id": 0, "url": 0, "attractions": 0}))
        # 数据格式化
        data = {}
        for item in all_provinces:
            data[item["name"]] = {}
            for key in item.keys():
                if key != "name":
                    data[item["name"]][key] = int(item[key])
        return data

    def getAttractionData(self, name):
        # 查询某具体地点的相关景点数据
        attractions = list(Mapper.mapdata.find({"name": {'$regex': '.*{}.*'.format(name)}}, {"attractions": 1, "url": 1}))
        if len(attractions) == 0:
            print("无查询结果！")
            return None
        elif len(attractions) > 1:
            print("查询结果过多，无法返回精确结果，请重试！")
            return None
        if "attractions" not in attractions[0].keys():
            # 紧急执行一次爬虫获取相关信息，但不插入数据库，防止后台更新重复操作占用资源
            attractions = get_scenery_info(attractions[0]["url"])
        else:
            attractions = attractions[0]["attractions"]
        data = []
        # 数据格式化
        for item in attractions:
            temp = SceneryInfo()
            temp.name = item['name']
            temp.tag = item['tag']
            temp.comments = {}
            # 防止返回结果是字符串
            for k in item['comments'].keys():
                temp.comments[k] = int(item['comments'][k])
            data.append(temp)
        return data

