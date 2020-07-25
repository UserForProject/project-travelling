package com.test.spider.response;

import java.io.Serializable;
import java.util.Map;

public class Spider2 implements Serializable {
    private Map<String, Map<String, Integer>> locationinfo;

    public Spider2() {
    }

    public Spider2(Map<String, Map<String, Integer>> locationinfo) {
        this.locationinfo = locationinfo;
    }

    public Map<String, Map<String, Integer>> getLocationinfo() {
        return locationinfo;
    }

    public void setLocationinfo(Map<String, Map<String, Integer>> locationinfo) {
        this.locationinfo = locationinfo;
    }
}
