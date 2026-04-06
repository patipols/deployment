# Field Mapping

## Source A — GPS Vendor

| Source Field    | Unified Field  |
| --------------- | -------------- |
| registration    | vehicle_id     |
| local_timestamp | timestamp      |
| lat / lon       | lat / lon      |
| speed           | speed          |
| course          | heading        |
| fuel_sensor     | fuel_level     |
| fuel_canbus     | fuel_rate      |
| mileage         | mileage        |
| event_en        | raw_event_type |

---

## Source B — Toyota

### Event Table

| Source Field  | Target     |
| ------------- | ---------- |
| Event type    | event_type |
| Timestamp     | timestamp  |
| Vehicle speed | speed      |

---

### Unified Table

| Source Field  | Unified Field  |
| ------------- | -------------- |
| GPS.lat/lon   | lat / lon      |
| Timestamp     | timestamp      |
| Event type    | raw_event_type |
| Vehicle speed | speed          |

---

### Timeseries Table

| Source Field    | Target           |
| --------------- | ---------------- |
| CAN signal name | signal_name      |
| CAN value       | signal_value     |
| Timestamp       | signal_timestamp |

---

## Source C — Logistics

| Source Field         | Unified Field |
| -------------------- | ------------- |
| TKNO                 | vehicle_id    |
| GPS_TIME             | timestamp     |
| LATITUDE / LONGITUDE | lat / lon     |
| SPEED                | speed         |
| DIRECTION            | heading       |
| ENGINE_STATUS        | engine_status |
| ALTITUDE             | altitude      |
