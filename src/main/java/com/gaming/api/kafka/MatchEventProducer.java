package com.gaming.api.kafka;

import lombok.RequiredArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class MatchEventProducer {

    private static final Logger log = LoggerFactory.getLogger(MatchEventProducer.class);
    private static final String TOPIC = "match-events";

    private final KafkaTemplate<String, String> kafkaTemplate;

    public void sendMatchCreated(Long matchId, String gameMode, String region) {
        String payload = String.format(
                "{\"event\":\"MATCH_CREATED\",\"matchId\":%d,\"gameMode\":\"%s\",\"region\":\"%s\"}",
                matchId, gameMode, region
        );
        kafkaTemplate.send(TOPIC, String.valueOf(matchId), payload);
        log.debug("Kafka event sent: {}", payload);
    }

    public void sendMatchFinished(Long matchId) {
        String payload = String.format(
                "{\"event\":\"MATCH_FINISHED\",\"matchId\":%d}", matchId
        );
        kafkaTemplate.send(TOPIC, String.valueOf(matchId), payload);
    }
}
