package com.zhouyi.demo.controller;

import com.zhouyi.demo.model.Hexagram;
import com.zhouyi.demo.service.HexagramService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/chat")
@CrossOrigin(origins = "*")
public class AIController {

    @Value("${glm.api.key:}")
    private String apiKey;

    @Autowired
    private HexagramService hexagramService;

    private final HttpClient client = HttpClient.newHttpClient();

    @PostMapping
    public String chat(@RequestBody Map<String, String> payload) throws IOException, InterruptedException {
        String message = payload.get("message");
        if (apiKey == null || apiKey.isEmpty()) {
            return "{\"error\": \"API Key not configured\"}";
        }

        // 1. RAG: Search for relevant context
        // Search for specific hexagram name if present in query
        String searchTerm = message;
        // Simple heuristic: if query contains "乾", search "乾"
        // In a real app, use NLP or keyword extraction.
        // For now, let's just pass the whole message to search, but HexagramService.search might need improvement
        
        List<Hexagram> searchResults = hexagramService.search(searchTerm);
        String context = "";
        if (!searchResults.isEmpty()) {
            // Take top 3 results to avoid token limit issues
            context = searchResults.stream()
                    .limit(3)
                    .map(h -> "卦名：" + h.getName() + "\n内容：" + h.getFullText().substring(0, Math.min(h.getFullText().length(), 1500))) // Increase context length
                    .collect(Collectors.joining("\n---\n"));
        } else {
             // If direct search fails, try to find hexagram names in the message
             // This requires a list of all hexagram names, or just rely on the user being specific.
             // Let's assume the user mentions the hexagram name.
        }

        // 2. Construct Prompt
        String systemPrompt = "你是一个周易专家助手。请根据用户的问题，结合以下提供的《周易》相关内容进行回答。如果相关内容中没有答案，请利用你的专业知识回答。回答要引经据典，通俗易懂。";
        String prompt = "相关内容：\n" + context + "\n\n用户问题：" + message;

        // Simple JSON construction (avoiding jackson dependency if possible, but spring-boot-starter-web has jackson)
        // Using Jackson creates cleaner code.
        String jsonBody = String.format("{\"model\": \"glm-4-flash\", \"messages\": [{\"role\": \"system\", \"content\": \"%s\"}, {\"role\": \"user\", \"content\": \"%s\"}]}", 
                systemPrompt.replace("\"", "\\\""),
                prompt.replace("\"", "\\\"").replace("\n", "\\n")); // basic escaping

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://open.bigmodel.cn/api/paas/v4/chat/completions"))
                .header("Content-Type", "application/json")
                .header("Authorization", "Bearer " + apiKey)
                .POST(HttpRequest.BodyPublishers.ofString(jsonBody))
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        return response.body();
    }
}
