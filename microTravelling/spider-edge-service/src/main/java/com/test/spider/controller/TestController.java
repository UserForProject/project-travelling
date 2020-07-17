package com.test.spider.controller;

import com.test.spider.response.Spider;
import com.test.spider.response.Spider2;
import com.test.spider.thrift.ServiceProvider;
import com.test.thrift.spider.SceneryInfo;
import com.test.thrift.spider.SpiderService;
import org.apache.thrift.TException;
import org.apache.thrift.transport.TSocket;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;
import javax.servlet.http.HttpServletRequest;
import java.util.List;
import java.util.Map;

@Controller     // 声明为一个 Controller
//@RequestMapping("/test")        // 声明借助浏览器访问该 Controller 的 url Path
public class TestController {

    // 声明一个 ServiceProvider 进行注入，用来调用服务器端服务
    @Resource       // 注入 ThriftClient
    private ServiceProvider serviceProvider;


    @GetMapping("/location_data")
    @ResponseBody       // 返回的数据是 Json 数据
    public Spider2 Locationinfo()  {
        Spider2 spider2 = this.fillSpider2();  //得到地图初始化相关数据
        return spider2;
    }

    @RequestMapping(value = "/homepage", method = RequestMethod.POST)
//    @GetMapping("/scenery_data")
//    @ResponseBody
    public String Scenery(HttpServletRequest request,
                          Model model) {   //得到具体景点的相关数据
        String name = request.getParameter("name");
        Spider spider = this.fillSpider(name);
        model.addAttribute("sceneryInfo", spider);
        return "search_result";
    }


    private Spider2 fillSpider2() {
        TSocket socket = serviceProvider.makesocket();
        SpiderService.Iface spiderService = serviceProvider.getSpiderService(socket);

        Map<String, Map<String, Integer>> locationinfo = null;
        try {
            locationinfo = spiderService.getLocationInfo();
        } catch (TException e) {
            e.printStackTrace();
        }

        socket.close();
        Spider2 spider2 = new Spider2(locationinfo);
        return spider2;
    }


    private Spider fillSpider(String name){
        TSocket socket = serviceProvider.makesocket();
        SpiderService.Iface spiderService = serviceProvider.getSpiderService(socket);
        List<SceneryInfo> scenry = null;
        try {
            scenry =  spiderService.searchSceneryInfo(name);
        } catch (TException e) {
            e.printStackTrace();
        }
        socket.close();
        Spider spider = new Spider(scenry);
        return spider;

    }
}
