package com.test.bilibili.controller;

import com.test.bilibili.thrift.ServiceProvider;
import com.test.thrift.bilibili.BilibiliService;
import com.test.thrift.bilibili.UserDetailedInfo;
import com.test.thrift.bilibili.UserInfo;
import org.apache.thrift.TException;
import org.apache.thrift.transport.TSocket;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;
import java.util.List;
import java.util.Map;

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

    //返回up主的具体信息，并返回Json对象
    @RequestMapping(value="/getUpInfo")
    @ResponseBody
    public UserDetailedInfo getUpInfo(@RequestParam(value = "uid") String uid){   //Uid 为从前端输入框通过ajax post请求传过来的参数
        int id = Integer.parseInt(uid);
        UserDetailedInfo upinfo = this.getupinfo(id);
        return upinfo;
    }

    //返回经mapreduce后的信息--当日热度最高的前300个词
    @RequestMapping(value = "/getWordCloud")
    @ResponseBody
    public Map<String, Double> getWordCloud(){
        Map<String, Double> wordcloud = this.wordcloud();
        return wordcloud;
    }

    //返回当日各分区热度字典
    @RequestMapping(value = "/getSubareaPlayAmount")
    @ResponseBody
    public Map<String, Integer> getSubareaPlayAmount(){
        Map<String, Integer> subareaplayamount = this.subareaplayamount();
        return subareaplayamount;
    }

    //查找up主信息--search功能
    @RequestMapping({"/getupcommoninfo"})
    public String getupname(Model model,@RequestParam(value = "uid") String uid){
        int id = Integer.parseInt(uid);
        UserDetailedInfo upinfo = this.getupinfo(id);
        String name = upinfo.name;
        int playAmount = upinfo.playAmount;
        int follower = upinfo.follower;
        int likes = upinfo.likes;
        int readingAmount = upinfo.readingAmount;
        int level = upinfo.level;
        List<Map<String, String>> videos = upinfo.videos;
        String video_one = videos.get(0).get("video_title");
        String video_two = videos.get(1).get("video_title");
        String video_three = videos.get(2).get("video_title");
        model.addAttribute("name",name);
        model.addAttribute("playAmount",playAmount);
        model.addAttribute("follower",follower);
        model.addAttribute("likes",likes);
        model.addAttribute("readingAmount",readingAmount);
        model.addAttribute("level",level);
        model.addAttribute("video_one",video_one);
        model.addAttribute("video_two",video_two);
        model.addAttribute("video_three",video_three);
        return "elements::commoninfo";
    }
    //掉粉榜数据
//    @RequestMapping({"/getRepair"})
//    public String getRepair(Model model) {
//        List<UserInfo> repairs = this.getTopDecreasingUp();
//        List<String> lists = new ArrayList<>(8);
//        for(int i=0;i<8;i++){
//            lists.add(repairs.get(i).name);
//        }
//        model.addAttribute("repairs",lists);
//        return "generic::recording";
//    }






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

    private Map<String, Double> wordcloud(){
        //利用ServiceProvider里的makesocket()函数来连接 ServerSocket
        TSocket socket = serviceProvider.makesocket();
        BilibiliService.Iface bilibiliService = serviceProvider.getBilibiliService(socket);
        Map<String, Double> cloud = null;
        try {
            cloud = bilibiliService.getWordCloud();

        } catch (TException e) {
            e.printStackTrace();
        }
        //查询一次后关闭网络连接
        socket.close();
        return cloud;
    }


    private Map<String, Integer> subareaplayamount(){
        //利用ServiceProvider里的makesocket()函数来连接 ServerSocket
        TSocket socket = serviceProvider.makesocket();
        BilibiliService.Iface bilibiliService = serviceProvider.getBilibiliService(socket);
        Map<String, Integer> subareaplayamount = null;
        try {
            subareaplayamount = bilibiliService.getSubareaPlayAmount();

        } catch (TException e) {
            e.printStackTrace();
        }
        //查询一次后关闭网络连接
        socket.close();
        return subareaplayamount;
    }



}