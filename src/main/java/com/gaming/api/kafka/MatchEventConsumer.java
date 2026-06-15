package com.gaming.api.kafka;

import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;
import lombok.RequiredArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class MatchEventConsumer {

    private static final Logger log = LoggerFactory.getLogger(MatchEventConsumer.class);

    private final MeterRegistry meterRegistry;

    @KafkaListener(topics = "match-events", groupId = "gaming-group")
    public void consume(String message) {
        Counter.builder("kafka.match.events.consumed")
                .register(meterRegistry)
                .increment();

        log.info("Event consumed: {}", message);
        // Ici : logique async (mise à jour stats, notifications, etc.)
    }
}
