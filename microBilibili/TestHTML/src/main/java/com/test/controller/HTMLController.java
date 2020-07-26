package com.test.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/echartstest")
public class HTMLController {

    @GetMapping("/testone")
    public String testone(){
        return "testone";
    }
//
    @GetMapping("/testtwo")
    public String testtwo(){
        return "testtwo";
    }
    @GetMapping("/testthree")
    public String testthree(){
        return "testthree";
    }
//    @GetMapping("/testfour")
//    public String testfour(){
//        return "testfour";
//    }
//    @GetMapping("searchtest")
//    public String searchtest() {return "searchtest";}
//    @GetMapping("doublesubmit")
//    public String doublesubmit() {return "doublesubmit";}
    @GetMapping("/elements")
    public String elements() {return "elements";}
    @GetMapping("/generic")
    public String generic() {return "generic";}
    @GetMapping("/heat")
    public String heat() {return "heat";}
    @GetMapping("/index")
    public String index() {return "index";}


}
