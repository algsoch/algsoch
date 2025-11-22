package com.algsoch.analytics.controller;

import com.algsoch.analytics.dto.AnalyticsSummaryDTO;
import com.algsoch.analytics.dto.RealtimeMetricsDTO;
import com.algsoch.analytics.service.AnalyticsService;
import org.springframework.http.MediaType;
import org.springframework.http.codec.ServerSentEvent;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Flux;

import java.time.Duration;

@RestController
@RequestMapping("/api/analytics")
public class AnalyticsController {
    
    private final AnalyticsService analyticsService;
    
    public AnalyticsController(AnalyticsService analyticsService) {
        this.analyticsService = analyticsService;
    }
    
    @GetMapping("/summary")
    public AnalyticsSummaryDTO getSummary() {
        analyticsService.incrementRequests();
        return analyticsService.getSummary();
    }
    
    @GetMapping(value = "/realtime", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<ServerSentEvent<RealtimeMetricsDTO>> streamRealtime() {
        analyticsService.incrementActiveConnections();
        
        return Flux.interval(Duration.ofSeconds(2))
                .map(sequence -> {
                    RealtimeMetricsDTO metrics = analyticsService.getRealtimeMetrics();
                    return ServerSentEvent.<RealtimeMetricsDTO>builder()
                            .id(String.valueOf(sequence))
                            .event("metrics")
                            .data(metrics)
                            .build();
                })
                .doOnCancel(analyticsService::decrementActiveConnections)
                .doOnComplete(analyticsService::decrementActiveConnections)
                .doOnError(e -> analyticsService.decrementActiveConnections());
    }
    
    @GetMapping("/health")
    public HealthResponse health() {
        return new HealthResponse("healthy", "Analytics service is running");
    }
    
    record HealthResponse(String status, String message) {}
}
