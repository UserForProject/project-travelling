# 东经为正数，西经为负数；北纬为正数，南纬为负数
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift.transport import TSocket, TTransport

from spider.mapper import Mapper
from spider.api import SpiderService


class QueryHandler:
    def __init__(self):
        self.mapper = Mapper()

    def getLocationInfo(self):
        return self.mapper.getLocationInfo()

    def searchSceneryInfo(self, name):
        return self.mapper.getAttractionData(name)


if __name__ == "__main__":
    handler = QueryHandler()
    processor = SpiderService.Processor(handler)
    serverSocket = TSocket.TServerSocket(host='127.0.0.1', port='9091')
    transportFactory = TTransport.TFramedTransportFactory()
    protocolFactory = TBinaryProtocol.TBinaryProtocolFactory()
    server = TServer.TSimpleServer(processor, serverSocket, transportFactory, protocolFactory)
    print("Server start....")
    server.serve()
    print("Server exit")