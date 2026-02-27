package com.zhouyi.demo.service;

import com.zhouyi.demo.model.Hexagram;
import com.zhouyi.demo.model.Yao;
import jakarta.annotation.PostConstruct;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Service;
import org.springframework.util.FileCopyUtils;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Service
public class HexagramService {

    private final List<Hexagram> hexagrams = new ArrayList<>();

    @Value("${zhouyi.data.path:}")
    private String dataPath;

    @PostConstruct
    public void init() throws IOException {
        String content;
        if (dataPath != null && !dataPath.isBlank()) {
            Path path = Path.of(dataPath);
            if (Files.exists(path) && Files.isRegularFile(path)) {
                byte[] data = Files.readAllBytes(path);
                content = new String(data, StandardCharsets.UTF_8);
            } else {
                ClassPathResource resource = new ClassPathResource("data/ZhouYi.md");
                byte[] data = FileCopyUtils.copyToByteArray(resource.getInputStream());
                content = new String(data, StandardCharsets.UTF_8);
            }
        } else {
            ClassPathResource resource = new ClassPathResource("data/ZhouYi.md");
            byte[] data = FileCopyUtils.copyToByteArray(resource.getInputStream());
            content = new String(data, StandardCharsets.UTF_8);
        }
        parseContent(content);
    }

    private void parseContent(String content) {
        // Regex to split by hexagram headers
        String[] parts = content.split("(?=## 第\\d+卦)");
        for (String part : parts) {
            if (!part.startsWith("## 第")) continue;
            
            Hexagram hex = new Hexagram();
            
            // Extract ID and Name
            Pattern headerPattern = Pattern.compile("## 第(\\d+)卦 (\\S+)");
            Matcher headerMatcher = headerPattern.matcher(part);
            if (headerMatcher.find()) {
                hex.setId(Integer.parseInt(headerMatcher.group(1)));
                hex.setName(headerMatcher.group(2));
            }

            // Extract Image URL
            Pattern imagePattern = Pattern.compile("!\\[.*?\\]\\((.*?)\\)");
            Matcher imageMatcher = imagePattern.matcher(part);
            if (imageMatcher.find()) {
                // Adjust path for frontend serving if needed, currently it's "images/01_乾.svg"
                // We will serve it via static resources, so "images/..." is fine if relative to static root
                // But in frontend we might need "/images/..."
                hex.setImageUrl(imageMatcher.group(1));
            }

            // Extract Binary Code
            Pattern codePattern = Pattern.compile("\\*\\*卦象编码\\*\\*：([01]+)");
            Matcher codeMatcher = codePattern.matcher(part);
            if (codeMatcher.find()) {
                hex.setBinaryCode(codeMatcher.group(1));
            }

            // Extract Description (Gua Ci)
            // Simplified parsing: just store the whole markdown part as fullText for now
            // But we can try to extract specific sections
            hex.setFullText(part);

            // Generate Yaos based on binary code (placeholder logic as text is missing in generated file)
            List<Yao> yaos = new ArrayList<>();
            if (hex.getBinaryCode() != null) {
                String binary = hex.getBinaryCode();
                for (int i = 0; i < 6; i++) {
                    Yao yao = new Yao();
                    yao.setId(i + 1);
                    // Binary is bottom to top (0 is Chu Yao)
                    char bit = binary.charAt(i);
                    yao.setYang(bit == '1');
                    yao.setName(getYaoName(i, bit == '1'));
                    yaos.add(yao);
                }
            }
            hex.setYaos(yaos);

            hexagrams.add(hex);
        }
    }

    private String getYaoName(int index, boolean isYang) {
        String[] positionNames = {"初", "二", "三", "四", "五", "上"};
        String yinYang = isYang ? "九" : "六";
        if (index == 0 || index == 5) {
            return positionNames[index] + yinYang;
        } else {
            return yinYang + positionNames[index];
        }
    }

    public List<Hexagram> getAllHexagrams() {
        return hexagrams;
    }

    public Hexagram getHexagramById(int id) {
        return hexagrams.stream().filter(h -> h.getId() == id).findFirst().orElse(null);
    }
    
    public List<Hexagram> search(String query) {
        return hexagrams.stream()
                .filter(h -> h.getName().contains(query) || h.getFullText().contains(query))
                .toList();
    }
}
