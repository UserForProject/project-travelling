from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift.transport import TTransport, TSocket

from bilibili.api import BilibiliService
from bilibili.service.Mapper import Mapper


class ServerHandler:
    m = Mapper()
    def getTopUpFans(self):
        """
        返回当日粉丝数最多的前五十位up主具体信息，包括id，昵称，头像url和粉丝总数
        """

        return self.m.getTopUpFans()

    def getTopIncreasingUp(self):
        """
        返回当日涨粉最快的前五十位up主具体信息，包括id，昵称，头像url和涨粉数
        """
        return self.m.getTopDecreasingUp()

    def getTopDecreasingUp(self):
        """
        返回当日掉粉最快的前五十位up主具体信息，包括id，昵称，头像url和掉粉数
        """
        return self.m.getTopDecreasingUp()

    def getUpInfo(self, uid):
        """
        返回up主的具体信息
        """
        return self.m.getUpInfo(uid)

    def getSubareaPlayAmount(self):
        """
        返回当日各分区热度字典
        """
        return self.m.getSubareaPlayAmount()

    def getWordCloud(self):
        """
        返回当日热度最高的前300个标签
        """
        return self.m.getWordCloud()


if __name__ == "__main__":
    handler = ServerHandler()
    processor = BilibiliService.Processor(handler)
    serverSocket = TSocket.TServerSocket(host='127.0.0.1', port='9091')
    transportFactory = TTransport.TFramedTransportFactory()
    protocolFactory = TBinaryProtocol.TBinaryProtocolFactory()
    server = TServer.TSimpleServer(processor, serverSocket, transportFactory, protocolFactory)
    print("Server start....")
    server.serve()
    print("Server exit")