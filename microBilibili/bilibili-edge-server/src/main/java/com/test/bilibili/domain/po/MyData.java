package com.test.bilibili.domain.po;

public class MyData {
    private String category;
    private Integer num;

    public MyData() {
    }

    public MyData(String category, Integer num) {
        this.category = category;
        this.num = num;
    }

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public Integer getNum() {
        return num;
    }

    public void setNum(Integer num) {
        this.num = num;
    }
}
