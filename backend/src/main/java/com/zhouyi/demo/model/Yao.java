package com.zhouyi.demo.model;

import lombok.Data;

@Data
public class Yao {
    private int id; // 1-6
    private String name; // 初九, 九二, etc.
    private String text; // 爻辞
    private String xiang; // 象曰
    private boolean isYang; // true for Yang, false for Yin
}
