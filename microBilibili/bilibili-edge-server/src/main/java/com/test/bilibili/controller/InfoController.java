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
import java.text.ParseException;
import java.text.ParsePosition;
import java.text.SimpleDateFormat;
import java.util.Date;
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

    //Up分区热度
    @RequestMapping(value = "/subareaNum")
    @ResponseBody
    public Map<String, Integer> getSubAreaNum(@RequestParam(value = "uid") String uid){
        int id = Integer.parseInt(uid);
        UserDetailedInfo upinfo = this.getupinfo(id);
        Map<String, Integer> subareaNum = upinfo.subareaNum;
        return subareaNum;
    }

    //获取Up主视频预测值
    @RequestMapping(value = "/prediction")
    public String predictGrade(Model model,
                             @RequestParam(value = "uploadTime") String uploadTime,
                             @RequestParam(value = "view") String view_nums,
                             @RequestParam(value = "favorite") String favorite_nums,
                             @RequestParam(value = "coin") String coin_nums,
                             @RequestParam(value = "share") String share_nums,
                             @RequestParam(value = "like") String like_nums) {

        // 传入的参数依次对应上传视频的日期 播放量 收藏数 硬币数 转发数 点赞数
        // 上传视频的日期如果不是“2020-7-30”这种格式的话则会返回-1，可以加一个网页上的小提示说明输入格式有误
        int view = Integer.parseInt(view_nums);
        int favorite = Integer.parseInt(favorite_nums);
        int coin = Integer.parseInt(coin_nums);
        int share = Integer.parseInt(share_nums);
        int like = Integer.parseInt(like_nums);
        long uploadTimestamp = 0;
        try {
            uploadTimestamp = (new SimpleDateFormat("yyyy-MM-dd")).parse(uploadTime).getTime() / 1000;
        } catch (ParseException e) {
            String result_wrong_one = "日期输入格式有误，请重新输入！";
            model.addAttribute("result",result_wrong_one);
            return "heat::prediction";
        }
        // 获取当日零点时间戳
        Date date = new Date();
        SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd");
        String today = simpleDateFormat.format(date.getTime());
        System.out.println("当天日期" + today);
        long todayTimestamp = simpleDateFormat.parse(today, new ParsePosition(0)).getTime();
        if(uploadTimestamp - todayTimestamp > 0){
            // 对应当前时间比上传时间更靠前的情况，说明用户输入有误
            String result_wrong_two = "日期输入有误，请检查当前日期是否比上传日期更靠前，然后重新输入！！";
            model.addAttribute("result",result_wrong_two);
            return "heat::prediction";
        }
        // 计算得到平均播放增长量
        double averageViewIncrease = view * 1.0 / (uploadTimestamp - todayTimestamp + 1);
//        double averageViewIncrease = view * 1.0 / 278420.0;

        // 平均数
        double avg1 = 2.34562582e+00;   double avg2 = 6.42593044e+04;   double avg3 = 6.33671994e+04;
        double avg4 = 1.68381311e+04;   double avg5 = 1.08385728e+05;   double avgY = 3.22437882e+05;
        // 标准差
        double stdDev1 = 1.52432101e+02;    double stdDev2 = 3.68272968e+10;    double stdDev3 = 4.40729184e+10;
        double stdDev4 = 4.89427211e+09;    double stdDev5 = 6.01396466e+10;    double stdDevY = 1.82400924e+11;
        // 标准化
        double para1 = (averageViewIncrease - avg1) / stdDev1;
        double para2 = (favorite - avg2) / stdDev2;
        double para3 = (coin - avg3) / stdDev3;
        double para4 = (share - avg4) / stdDev4;
        double para5 = (like - avg5) / stdDev5;
        // 参数值
        double theta1 = 2.01321618e-05; double theta2 = 2.33199924e-01; double theta3 = 3.88139166e-01;
        double theta4 = 5.65243002e-03; double theta5 = 1.02238574e-01;

        // 使用线性模型输出标准化的结果
        double y = theta1*para1 + theta2*para2 + theta3*para3 + theta4*para4 + theta5*para5;
        double result = y * stdDevY + avgY;
        model.addAttribute("result",result);
        return "heat::prediction";
    }
    //查找up主信息--search功能
    @RequestMapping({"/getupcommoninfo"})
    public String getupname(Model model,@RequestParam(value = "uid") String uid){
        //up uid
        int id = Integer.parseInt(uid);
        UserDetailedInfo upinfo = this.getupinfo(id);
        //up 昵称
        String name = upinfo.name;
        //up 视频播放量
        int playAmount = upinfo.playAmount/10000;
        String playAmounts = String.valueOf(playAmount)+"万";
        //up 粉丝数 （为方便阅读，显示xxx万）
        int follower = upinfo.follower/10000;
        String followers = String.valueOf(follower)+"万";
        //up 点赞数 （为方便阅读，显示xxx万）
        int like = upinfo.likes/10000;
        String likes = String.valueOf(like)+"万";
        //up 阅读专栏阅读量 （为方便阅读，显示xxx万，若阅读量为0，则表明该up主没有写过阅读专栏）
        int readingAmount = upinfo.readingAmount;
        String readingAmounts;
        if(readingAmount==0){
            readingAmounts = name+" 暂时没有写过专栏阅读哦~";
        }else if(readingAmount>10000){
            readingAmount = readingAmount/10000;
            readingAmounts = String.valueOf(readingAmount)+"万";
        }else{
            readingAmounts = String.valueOf(readingAmount);
        }
        //up 等级
        int level = upinfo.level;
        String levels = String.valueOf(level)+"级";
        //up 头像
        String face = upinfo.face;
        // 三个热门视频的标题
        List<Map<String, String>> videos = upinfo.videos;
        String video_one = videos.get(0).get("video_title");
        String video_two = videos.get(1).get("video_title");
        String video_three = videos.get(2).get("video_title");
        // 三个热门视频的视频封面
        String cover_one = videos.get(0).get("video_cover");
        String cover_two = videos.get(1).get("video_cover");
        String cover_three = videos.get(2).get("video_cover");
        //https协议降为http协议
//        cover_one = replaceIndex(4,cover_one,"");
//        cover_two = replaceIndex(4,cover_two,"");
//        cover_three = replaceIndex(4,cover_three,"");

        model.addAttribute("name",name);
        model.addAttribute("playAmount",playAmounts);
        model.addAttribute("follower",followers);
        model.addAttribute("likes",likes);
        model.addAttribute("readingAmount",readingAmounts);
        model.addAttribute("level",levels);
        model.addAttribute("face",face);
        model.addAttribute("video_one",video_one);
        model.addAttribute("video_two",video_two);
        model.addAttribute("video_three",video_three);
        model.addAttribute("cover_one",cover_one);
        model.addAttribute("cover_two",cover_two);
        model.addAttribute("cover_three",cover_three);
        return "elements::commoninfo";
    }


    //替换字符串中特定位置的字符
    private static String replaceIndex(int index,String res,String str){
        return res.substring(0, index)+str+res.substring(index+1);
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