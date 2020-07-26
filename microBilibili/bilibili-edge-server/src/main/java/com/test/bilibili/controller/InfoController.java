package com.test.bilibili.controller;

import com.test.bilibili.thrift.ServiceProvider;
import com.test.thrift.bilibili.BilibiliService;
import com.test.thrift.bilibili.UserDetailedInfo;
import com.test.thrift.bilibili.UserInfo;
import org.apache.thrift.TException;
import org.apache.thrift.transport.TSocket;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;
import java.util.List;

@Controller     // 声明为一个 Controller
@RequestMapping("/info")        // 声明借助浏览器访问该 Controller 的 url Path
public class InfoController {

    // 声明一个 ServiceProvider 进行注入，用来调用服务器端服务
    @Resource       // 注入 ThriftClient
    private ServiceProvider serviceProvider;

    //返回当日粉丝数最多的前五十位up主具体信息，包括id，昵称，头像url和粉丝总数
    @GetMapping("/getTopUpFans")
    @ResponseBody
    public List<UserInfo> getTopUpFans(){
        List<UserInfo> TopUpFans = this.topfans();
        return TopUpFans;
    }

    //返回当日涨粉最快的前五十位up主具体信息，包括id，昵称，头像url和涨粉数
    @GetMapping("getTopIncreasingUp")
    @ResponseBody
    public List<UserInfo> getTopIncreasingUp(){
        List<UserInfo> topincreasingup = this.topincreasingup();
        return topincreasingup;

    }

    //返回当日掉粉最快的前五十位up主具体信息，包括id，昵称，头像url和掉粉数
    @GetMapping("getTopDecreasingUp")
    @ResponseBody
    public List<UserInfo> getTopDecreasingUp(){
        List<UserInfo> topdecreasingup = this.topdecreasingup();
        return topdecreasingup;

    }

    //返回up主的具体信息
    @RequestMapping(value="/getUpInfo")
    @ResponseBody
    public UserDetailedInfo getUpInfo(@RequestParam(value = "uid") String uid){
        int id = Integer.parseInt(uid);
        UserDetailedInfo upinfo = this.getupinfo(id);
        return upinfo;
    }

    //
    //返回抓取信息的函数
    //
    private List<UserInfo> topfans() {
        //利用ServiceProvider里的makesocket()函数来连接 ServerSocket
        TSocket socket = serviceProvider.makesocket();
        BilibiliService.Iface bilibiliService = serviceProvider.getBilibiliService(socket);

        List<UserInfo> topfansinfo = null;
        try {
            topfansinfo = bilibiliService.getTopUpFans();

        } catch (TException e) {
            e.printStackTrace();
        }
        //查询一次后关闭网络连接
        socket.close();
        return topfansinfo;
    }


    private List<UserInfo> topincreasingup(){
        //利用ServiceProvider里的makesocket()函数来连接 ServerSocket
        TSocket socket = serviceProvider.makesocket();
        BilibiliService.Iface bilibiliService = serviceProvider.getBilibiliService(socket);
        List<UserInfo> topincreasingup = null;
        try {
            topincreasingup = bilibiliService.getTopIncreasingUp();

        } catch (TException e) {
            e.printStackTrace();
        }
        //查询一次后关闭网络连接
        socket.close();
        return topincreasingup;
    }


    private List<UserInfo> topdecreasingup(){
        //利用ServiceProvider里的makesocket()函数来连接 ServerSocket
        TSocket socket = serviceProvider.makesocket();
        BilibiliService.Iface bilibiliService = serviceProvider.getBilibiliService(socket);
        List<UserInfo> topdecreasingup = null;
        try {
            topdecreasingup = bilibiliService.getTopDecreasingUp();

        } catch (TException e) {
            e.printStackTrace();
        }
        //查询一次后关闭网络连接
        socket.close();
        return topdecreasingup;
    }


    private UserDetailedInfo getupinfo(int uid){
        //利用ServiceProvider里的makesocket()函数来连接 ServerSocket
        TSocket socket = serviceProvider.makesocket();
        BilibiliService.Iface bilibiliService = serviceProvider.getBilibiliService(socket);
        UserDetailedInfo upinfo = null;
        try {
            upinfo = bilibiliService.getUpInfo(uid);

        } catch (TException e) {
            e.printStackTrace();
        }
        //查询一次后关闭网络连接
        socket.close();
        return upinfo;
    }



}