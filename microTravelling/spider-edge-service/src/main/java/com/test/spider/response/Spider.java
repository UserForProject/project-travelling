package com.test.spider.response;

import com.test.thrift.spider.SceneryInfo;

import java.io.Serializable;
import java.util.List;
import java.util.Map;

public class Spider implements Serializable {

    private List<SceneryInfo> sceneryInfos;

    public Spider() {
    }

    public Spider(List<SceneryInfo> sceneryInfos) {
        this.sceneryInfos = sceneryInfos;
    }

    public List<SceneryInfo> getSceneryInfos() {
        return sceneryInfos;
    }

    public void setSceneryInfos(List<SceneryInfo> sceneryInfos) {
        this.sceneryInfos = sceneryInfos;
    }
}
