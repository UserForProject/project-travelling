package com.test.spider.controller;


import com.test.spider.response.Spider;
import com.test.spider.response.Spider2;
import com.test.spider.thrift.ServiceProvider;
import com.test.thrift.spider.SceneryInfo;
import com.test.thrift.spider.SpiderService;
import org.apache.thrift.TException;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import javax.annotation.Resource;
import java.util.List;
import java.util.Map;

@Controller     // 声明为一个 Controller
@RequestMapping("/test")        // 声明借助浏览器访问该 Controller 的 url Path
public class TestController {

    // 声明一个 ServiceProvider 进行注入，用来调用用户服务|消息服务
    @Resource       // 注入 ThriftClient
    private ServiceProvider serviceProvider;


    @GetMapping("/login1")
    @ResponseBody       // 返回的数据是 Json 数据
    public Spider2 Scenery()  {
        Spider2 spider2 = this.fillSpider2();  //得到具体景点的相关数据
        return spider2;


    }

    @GetMapping("/login2")
    @ResponseBody       // 返回的数据是 Json 数据
    public Spider Locationinfo(String name) {   //得到地图初始化相关数据
        Spider spider = this.fillSpider();
        return spider;

    }



    private Spider2 fillSpider2(){
        SpiderService.Iface spiderService = serviceProvider.getSpiderService();
        Map<String, Map<String, Integer>> locationinfo = null;
        try {
            locationinfo = spiderService.getLocationInfo();
        } catch (TException e) {
            e.printStackTrace();

        }
        Spider2 spider2 = new Spider2(locationinfo);
        return spider2;
    }

    private Spider fillSpider(){
        SpiderService.Iface spiderService = serviceProvider.getSpiderService();
        List<SceneryInfo> scenry = null;
        try {
            scenry =  spiderService.searchSceneryInfo("上海");
        } catch (TException e) {
            e.printStackTrace();
        }
        Spider spider = new Spider(scenry);
        return spider;
    }
}
