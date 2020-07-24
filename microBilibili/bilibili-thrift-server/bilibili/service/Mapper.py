import datetime
import time

import pymongo

user = "root"
pwd = "root"
host = "192.168.2.108"
port = "27017"


class Mapper:
    client = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(user, pwd, host, port))
    bilibiliData = client["bilibili"]
    def getTopUpFans(self):
        """
        返回当日粉丝数最多的前五十位up主具体信息，包括id，昵称，头像url和粉丝总数
        """
        date = datetime.datetime.now().strftime("%Y%m%d")
        data = self.bilibiliData["users"].find().sort([(date, -1)]).limit(50)
        for item in data:
            print(item)

    def getTopIncreasingUp(self):
        """
        返回当日涨粉最快的前五十位up主具体信息，包括id，昵称，头像url和涨粉数
        """
        pass

    def getTopDecreasingUp(self):
        """
        返回当日掉粉最快的前五十位up主具体信息，包括id，昵称，头像url和掉粉数
        """
        pass

    def getUpInfo(self, uid):
        """
        返回up主的具体信息
        """
        pass


    def getSubareaPlayAmount(self):
        """
        返回当日各分区热度字典
        """
        pass


if __name__ == "__main__":
    m = Mapper()
    m.getTopUpFans()