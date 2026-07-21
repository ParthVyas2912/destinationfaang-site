# Design an IoT Platform & Device Telemetry System

| | |
|---|---|
| **Publish order** | 054 |
| **Course #** | 116 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~30 min |
| **Primary search keyword** | `design iot system` |
| **Demand** | Moderate |

**Thumbnail text idea:** IOT FIREHOSE
**One-line hook (first 15s):** Designing IoT is not just ‘send MQTT to a database’—devices go offline, clocks lie, and firmware breaks protocols.

## Learning objectives
- Design secure telemetry ingestion for millions of intermittent devices.
- Model devices, telemetry, commands, certificates, and firmware versions.
- Handle reconnect storms, ordering, time-series storage, and command delivery.

## Topics & items to cover
- Requirements: devices publish temperature/location/battery every 10s, receive commands, authenticate per device, tolerate offline reconnect, dashboard freshness under 30s.
- Estimation: 5M devices, 500K online, 50K msg/sec average with outage bursts. Partition streams by `device_id`; store by `tenant_id + day + device_hash`.
- API/Data model: MQTT topic `tenant/{tenant_id}/device/{device_id}/telemetry`, HTTP `POST /devices`, `POST /devices/{id}/commands`; entities: Device, Certificate, TelemetryPoint, Command, FirmwareVersion.
- High-level design: device → MQTT broker fleet → auth/registry → Kafka → rules/stream processor → time-series DB + object storage → dashboards. Command path uses broker retained messages or per-device command queue.
- Deep dives/bottlenecks: reconnect storms need exponential backoff/jitter and broker autoscaling; device identity uses per-device certs and revocation; late telemetry stores both device timestamp and ingestion timestamp.
- Wrap-up: separate telemetry firehose, command/control, and fleet registry.

## Anecdotes & war stories to use
- AWS IoT and Azure IoT Hub both make device identity and MQTT first-class primitives.
- Mirai showed why weak IoT credentials are systemic risk.
- Industrial IoT deployments routinely require offline buffering because field networks fail.

## Things to mention / interview tips
- Ask whether commands need exactly-once; usually use idempotent command IDs.
- Mention provisioning and cert rotation.
- Include firmware/schema version compatibility.

## Common mistakes to call out
- Trusting client clocks blindly.
- Putting all tenant devices on one partition.
- Treating device commands like web push notifications.

## Diagrams / visuals to draw on screen
- MQTT broker ingestion to Kafka and TSDB.
- Device certificate trust/provisioning flow.
- Offline buffer and reconnect burst timeline.

## Series glue
- Uses time-series concepts from the previous video. Next: layered caching. Subscribe and use GitHub assets.
