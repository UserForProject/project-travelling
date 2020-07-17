package com.test.spider.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

@Controller
//@RequestMapping("/travelling")
public class SpiderController {
    @GetMapping("/homepage")
    public String display(){
        return "index";
    }

//    @RequestMapping(value = "/search_result", method = RequestMethod.GET)
//    public String test(){
//        return "test1";
//    }

}
