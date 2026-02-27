package com.zhouyi.demo.controller;

import com.zhouyi.demo.model.Hexagram;
import com.zhouyi.demo.service.HexagramService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/hexagrams")
@CrossOrigin(origins = "*") // Allow frontend to access
public class HexagramController {

    @Autowired
    private HexagramService hexagramService;

    @GetMapping
    public List<Hexagram> getAllHexagrams() {
        return hexagramService.getAllHexagrams();
    }

    @GetMapping("/{id}")
    public Hexagram getHexagramById(@PathVariable int id) {
        return hexagramService.getHexagramById(id);
    }

    @GetMapping("/search")
    public List<Hexagram> search(@RequestParam String q) {
        return hexagramService.search(q);
    }
}
