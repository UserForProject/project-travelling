import pymongo
import datetime
from spider.spider_ctrip import *
from spider.api.ttypes import SceneryInfo
# import pprint

user = "root"
pwd = "root"
host = "192.168.2.108"
port = "27017"


class Mapper:
    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(user, pwd, host, port))
        self.db = self.client["microTravelling"]

    def getLocationInfo(self):
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        mapdata = self.db["mapdata"]
        if mapdata.count_documents({"date":today}) == 0:
            # 调用爬虫 爬取数据 格式化 存储进数据库
            spider_data = get_map_data()
            keys = spider_data.keys()
            for key in keys:
                temp = spider_data[key]
                temp["name"] = key
                mapdata.update_one({"name": key}, temp, True)
        all_provinces = list(mapdata.find({}, {"_id": 0, "date": 0, "url": 0}))
        # 数据格式化
        data = {}
        for item in all_provinces:
            data[item["name"]] = {}
            for key in item.keys():
                if key != "name":
                    data[item["name"]][key] = int(item[key])
        return data

    def getAttractionData(self, name):
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        mapdata = self.db["mapdata"]
        parent_data = mapdata.find({"name": {'$regex': '.*{}.*'.format(name)}}, {"name": 1, "url": 1, "date": 1})
        parent_data = list(parent_data)
        if len(parent_data) == 0:
            print("无查询结果！")
            return None
        elif len(parent_data) > 1:
            print("查询结果过多，无法返回精确结果，请重试！")
            return None
        if "date" not in parent_data[0].keys() or parent_data[0]["date"] != today:
            #调用爬虫对数据进行更新
            new_data = get_scenery_info(parent_data[0]["url"])
            mapdata.update_one({"name": parent_data[0]["name"]}, {'$set':{"date": today, "attractions": new_data}})
        attractions = list(mapdata.find({"name": parent_data[0]["name"]}, {"attractions": 1}))
        attractions = attractions[0]["attractions"]
        data = []
        for item in attractions:
            temp = SceneryInfo()
            temp.name = item['name']
            temp.tag = item['tag']
            temp.comments = {}
            for k in item['comments'].keys():
                temp.comments[k] = int(item['comments'][k])
            data.append(temp)
        return data





if __name__ == "__main__":
    # m = Mapper()
    # pprint.pprint(m.getAttractionData("上海"))
    # c = list(m.client.test.info.find({"parent":ObjectId("5f0ac42e5c57000026007281")}))
    # print(c)
    # print(get_map_data())