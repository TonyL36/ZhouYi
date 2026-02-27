package com.zhouyi.demo.model;

import lombok.Data;
import java.util.List;

@Data
public class Hexagram {
    private int id;
    private String name;
    private String binaryCode;
    private String imageUrl;
    private String description; // 卦辞
    private String xiang; // 象曰
    private String tuan; // 彖传
    private List<Yao> yaos; // 六爻
    private String fullText; // Markdown content for this hexagram
}
