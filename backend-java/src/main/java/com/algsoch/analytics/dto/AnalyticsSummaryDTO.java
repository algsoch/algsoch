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
public class AnalyticsSummaryDTO {
    private Long uptime;
    private Integer totalRequests;
    private Integer activeConnections;
    private Double avgResponseTime;
    private String status;
    private Instant timestamp;
}
