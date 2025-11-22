package com.algsoch.analytics.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class RealtimeMetricsDTO {
    private String type;
    private Instant timestamp;
    private MetricsPayload payload;
    
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class MetricsPayload {
        private Long uptime;
        private Integer activeConnections;
        private Integer totalRequests;
        private String status;
    }
}
