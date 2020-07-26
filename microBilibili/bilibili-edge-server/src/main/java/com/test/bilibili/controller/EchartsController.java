package com.test.bilibili.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/bilibili")
public class EchartsController {

    @GetMapping("/elements")
    public String elements() {return "elements";}
    @GetMapping("/generic")
    public String generic() {return "generic";}
    @GetMapping("/heat")
    public String heat() {return "heat";}
    @GetMapping("/index")
    public String index() {return "index";}
}
