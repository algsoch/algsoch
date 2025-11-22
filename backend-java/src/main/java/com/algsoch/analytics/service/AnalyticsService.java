package com.algsoch.analytics.service;

import com.algsoch.analytics.dto.AnalyticsSummaryDTO;
import com.algsoch.analytics.dto.RealtimeMetricsDTO;
import org.springframework.stereotype.Service;

import java.time.Duration;
import java.time.Instant;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicLong;

@Service
public class AnalyticsService {
    
    private final Instant startTime = Instant.now();
    private final AtomicInteger totalRequests = new AtomicInteger(0);
    private final AtomicInteger activeConnections = new AtomicInteger(0);
    private final AtomicLong totalResponseTime = new AtomicLong(0);
    
    public void incrementRequests() {
        totalRequests.incrementAndGet();
    }
    
    public void incrementActiveConnections() {
        activeConnections.incrementAndGet();
    }
    
    public void decrementActiveConnections() {
        activeConnections.decrementAndGet();
    }
    
    public void recordResponseTime(long milliseconds) {
        totalResponseTime.addAndGet(milliseconds);
    }
    
    public AnalyticsSummaryDTO getSummary() {
        long uptime = Duration.between(startTime, Instant.now()).getSeconds();
        int requests = totalRequests.get();
        double avgResponseTime = requests > 0 ? 
            (double) totalResponseTime.get() / requests : 0.0;
        
        return AnalyticsSummaryDTO.builder()
                .uptime(uptime)
                .totalRequests(requests)
                .activeConnections(activeConnections.get())
                .avgResponseTime(avgResponseTime)
                .status("healthy")
                .timestamp(Instant.now())
                .build();
    }
    
    public RealtimeMetricsDTO getRealtimeMetrics() {
        long uptime = Duration.between(startTime, Instant.now()).getSeconds();
        
        RealtimeMetricsDTO.MetricsPayload payload = RealtimeMetricsDTO.MetricsPayload.builder()
                .uptime(uptime)
                .activeConnections(activeConnections.get())
                .totalRequests(totalRequests.get())
                .status("healthy")
                .build();
        
        return RealtimeMetricsDTO.builder()
                .type("metrics")
                .timestamp(Instant.now())
                .payload(payload)
                .build();
    }
}
