import collections
import datetime
import time

import pymongo

from bilibili.api.ttypes import UserInfo, UserDetailedInfo
from bilibili.spider.biliob_fans_spider import get_detailed_info

user = "root"
pwd = "root"
host = "192.168.1.105"
port = "27017"

# 运行前先运行update包中的updateBeforeMR脚本
class Mapper:
    client = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(user, pwd, host, port))
    bilibiliData = client["bilibili"]
    def getTopUpFans(self):
        """
        返回当日粉丝数最多的前五十位up主具体信息，包括id，昵称，头像url和粉丝总数
        """
        today = datetime.datetime.now().strftime("%Y%m%d")
        data = self.bilibiliData["users"].find({}, {"uid": 1, "name": 1, "face": 1, today: 1}).sort([(today, -1)]).limit(50)
        # 强制转换，防止类型错误
        usersInfo = []
        for item in data:
            temp = UserInfo()
            temp.uid = int(item["uid"])
            temp.fans = int(item[today])
            temp.face = item["face"]
            temp.name = item["name"]
            usersInfo.append(temp)
        return usersInfo

    def getTopIncreasingUp(self):
        """
        返回当日涨粉最快的前五十位up主具体信息，包括id，昵称，头像url和涨粉数
        """
        data = self.bilibiliData["users"].find({"change": {"$ne": ""}}, {"uid": 1, "name": 1, "face": 1, "change": 1}).sort([("change", -1)]).limit(50)
        # 强制转换，防止类型错误
        usersInfo = []
        for item in data:
            temp = UserInfo()
            temp.uid = int(item["uid"])
            temp.fans = int(item["change"])
            temp.face = item["face"]
            temp.name = item["name"]
            usersInfo.append(temp)
        return usersInfo

    def getTopDecreasingUp(self):
        """
        返回当日掉粉最快的前五十位up主具体信息，包括id，昵称，头像url和掉粉数
        """
        data = self.bilibiliData["users"].find({"change": {"$ne": ""}}, {"uid": 1, "name": 1, "face": 1, "change": 1}).sort([("change", 1)]).limit(50)
        # 强制转换，防止类型错误
        usersInfo = []
        for item in data:
            temp = UserInfo()
            temp.uid = int(item["uid"])
            temp.fans = int(item["change"])
            temp.face = item["face"]
            temp.name = item["name"]
            usersInfo.append(temp)
        return usersInfo

    def getUpInfo(self, uid):
        """
        返回up主的具体信息
        """
        detailInfo = get_detailed_info(uid)
        detail = UserDetailedInfo()
        detail.name = detailInfo["name"]
        detail.uid = int(uid)
        detail.level = int(detailInfo["level"])
        detail.follower = int(detailInfo["follower"])
        detail.follow = int(detailInfo["follow"])
        detail.likes = int(detailInfo["likes"])
        detail.playAmount = int(detailInfo["playAmount"])
        detail.readingAmount = int(detailInfo["readingAmount"])
        detail.videos = detailInfo["video"]
        detail.face = detailInfo["face"]
        detail.fansData = []
        data = self.bilibiliData["users"].find({"uid": uid}, {"_id": 0, "change": 0, "face": 0, "name": 0, "uid": 0})
        data = list(data)
        # 判断是否有粉丝数据
        if len(data) == 0:
            return detail
        data = data[0]
        # 对日期进行排序，保证按顺序遍历，需要从当前日期开始倒序遍历，因为不确定从哪天开始记录粉丝数，当天数据是当日凌晨0点时获取的
        keyList = []
        for key in data.keys():
            keyList.append(key)
        keyList.sort()
        for key in keyList:
            detail.fansData.append(data[key])
        return detail

    def getSubareaPlayAmount(self):
        """
        返回当日各分区热度字典
        """
        heatData = list(self.bilibiliData["subAreaHeat"].find({}, {"_id": 0}))
        res = {}
        for area in heatData:
            res[area["name"]] = int(area["heat"])
        return res

    def getWordCloud(self):
        """
        返回当日热度最高的前300个词
        """
        pass


# if __name__ == "__main__":
#     m = Mapper()
#     m.getSubareaPlayAmount()