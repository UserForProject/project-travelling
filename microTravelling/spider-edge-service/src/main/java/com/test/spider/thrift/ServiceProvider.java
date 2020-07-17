package com.test.spider.thrift;

import com.test.thrift.spider.SpiderService;
import org.apache.thrift.TServiceClient;
import org.apache.thrift.protocol.TBinaryProtocol;
import org.apache.thrift.protocol.TProtocol;
import org.apache.thrift.transport.TFramedTransport;
import org.apache.thrift.transport.TSocket;
import org.apache.thrift.transport.TTransport;
import org.apache.thrift.transport.TTransportException;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

// 作为 Springboot 项目的中一个组件
@Component
public class ServiceProvider {

    // 获取要调用服务的地址&端口
    @Value("${thrift.spider.ip}")
    private String spiderServerIp;     // message-thrift-python-service 地址
    @Value("${thrift.spider.port}")
    private int spiderServerPort;   // message-thrift-python-service 端口


    // 声明枚举类型，完成服务类型的区分
    private enum ServiceType{
        SPIDER
    }

    // 获取远程服务 = 参数：ip、端口、服务类型(enum)
    // 获取远程服务 == 返回类型(用户、消息) -- 泛型
    public <T> T getService(String ip, int port, ServiceType serverType){
        // RPC - Socket\Transport\Protocol == client&server 保持一致
        // 1. 声明一个 Socket 用来连接 ServerSocket
        TSocket socket = new TSocket(ip, port, 300000);
        // 2. 指定生成一个传输方式对象 -- 基于 Socket 连接创建一个帧传输对象
        TTransport transport = new TFramedTransport(socket);
        // 开启|打开帧传输
        try {
            transport.open();
        } catch (TTransportException e) {
            e.printStackTrace();
            return null;
        }
        // 3. 指定传输发送的协议 - 二进制
        TProtocol protocol = new TBinaryProtocol(transport);

        // 4. 获取服务的客户端
        TServiceClient result = null;
        // 判断服务类型，并根据服务类型，返回不同的客户端
        switch (serverType) {
            case SPIDER :
                result = new SpiderService.Client(protocol);
                break;

        }

        // 强制类型转换为对应的泛型接口
        return (T)result;
    }

    // 获取爬虫服务的客户端
    public SpiderService.Client getSpiderService(){
        return getService(spiderServerIp, spiderServerPort, ServiceType.SPIDER);

    }

//    public SpiderService.Client getSpiderService2(){
//        return getService(spiderServerIp, spiderServerPort, ServiceType.SPIDER);
//
//    }


}
















