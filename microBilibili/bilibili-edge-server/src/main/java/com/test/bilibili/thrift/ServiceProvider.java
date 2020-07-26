package com.test.bilibili.thrift;

import com.test.thrift.bilibili.BilibiliService;
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
    @Value("${thrift.bilibili.ip}")
    private String BilibiliServerIp;     // message-thrift-python-service 地址
    @Value("${thrift.bilibili.port}")
    private int BilibiliServerPort;   // message-thrift-python-service 端口


    // 声明枚举类型，完成服务类型的区分
    private enum ServiceType{
        BILIBILI
    }


    //  声明一个 Socket 用来连接 ServerSocket
    public TSocket makesocket(){
        TSocket socket = new TSocket(BilibiliServerIp, BilibiliServerPort, 20000);
        return socket;
    }


    // 获取远程服务 = 参数：ip、端口、服务类型(enum)
    // 获取远程服务 == 返回类型(用户、消息) -- 泛型
    public <T> T getService(TSocket socket, ServiceType serverType) {
        // 指定生成一个传输方式对象 -- 基于 Socket 连接创建一个帧传输对象
        TTransport transport = new TFramedTransport(socket);
        // 开启|打开帧传输
        try {
            transport.open();
        } catch (TTransportException e) {
            e.printStackTrace();
            return null;
        }
        // 指定传输发送的协议 - 二进制
        TProtocol protocol = new TBinaryProtocol(transport);

        // 获取服务的客户端
        TServiceClient result = null;
        // 判断服务类型，并根据服务类型，返回不同的客户端
        switch (serverType) {
            case BILIBILI:
                result = new BilibiliService.Client(protocol);
                break;
        }

        // 强制类型转换为对应的泛型接口
        return (T)result;

    }


    // 获取爬虫服务的客户端
    public BilibiliService.Client getBilibiliService(TSocket socket){

        return getService(socket, ServiceType.BILIBILI);

    }


}
















