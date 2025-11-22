package com.algsoch.analytics.controller;

import com.algsoch.analytics.dto.RealtimeMetricsDTO;
import com.algsoch.analytics.service.AnalyticsService;
import org.springframework.messaging.handler.annotation.MessageMapping;
import org.springframework.messaging.handler.annotation.SendTo;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Controller;

@Controller
@EnableScheduling
public class WebSocketController {
    
    private final SimpMessagingTemplate messagingTemplate;
    private final AnalyticsService analyticsService;
    
    public WebSocketController(SimpMessagingTemplate messagingTemplate, 
                               AnalyticsService analyticsService) {
        this.messagingTemplate = messagingTemplate;
        this.analyticsService = analyticsService;
    }
    
    @MessageMapping("/metrics")
    @SendTo("/topic/metrics")
    public RealtimeMetricsDTO sendMetrics() {
        return analyticsService.getRealtimeMetrics();
    }
    
    @Scheduled(fixedRate = 2000)
    public void broadcastMetrics() {
        RealtimeMetricsDTO metrics = analyticsService.getRealtimeMetrics();
        messagingTemplate.convertAndSend("/topic/metrics", metrics);
    }
}
