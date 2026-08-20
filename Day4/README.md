# Day 4 - Grafana, InfluxDB, HiveMQ & Data Visualization


## Overview

Day 4 focused on building a complete IoT data pipeline by integrating our existing sensor system with cloud-based time-series database and visualization tools. We replaced Adafruit IO with HiveMQ (MQTT broker) and InfluxDB (time-series database) with Grafana for real-time data visualization and monitoring.

---

## Tasks Completed

### Task 1: HiveMQ Cloud MQTT Broker Setup
- Created account on HiveMQ Cloud (free tier)
- Created an MQTT broker instance
- Obtained broker URL, port (8883), username, and password
- Configured TLS/SSL encryption for secure communication
- Replaced Adafruit IO with HiveMQ for MQTT communication

### Task 2: InfluxDB Cloud Setup
- Created account on InfluxDB Cloud (free tier)
- Created an organization and bucket for data storage
- Generated API token for authentication
- Obtained InfluxDB URL and credentials
- Configured Python script to write sensor data to InfluxDB

### Task 3: Python Script Modifications
- Modified `mqtt.py` to use HiveMQ instead of Adafruit IO
- Added InfluxDB client integration
- Wrote distance measurements to InfluxDB as time-series data
- Used Points and field formatting for proper data structure
- Kept MQTT publishing functionality for real-time updates

### Task 4: Grafana Cloud Setup and Visualization
- Created account on Grafana Cloud
- Connected Grafana to InfluxDB as data source
- Configured InfluxDB connection using: URL, Organization, Token, Bucket
- Created dashboard for real-time visualization
- Configured panel with distance measurements
- Set up auto-refresh rate for live updates

### Task 5: Integration and Testing
- Started the IPC system (sensor → MQTT → LED)
- Verified data flow: Sensor → Queue → MQTT → InfluxDB → Grafana
- Tested real-time visualization on Grafana dashboard
- Verified LED control through MQTT messages

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           Raspberry Pi 4                               │
│                                                                         │
│  ┌────────────┐     ┌────────────┐     ┌────────────┐                  │
│  │  Sensor.py  │────▶│  MQTT.py   │────▶│   LED.py   │                  │
│  │  (HC-SR04) │     │  (Process) │     │  (GPIO17)  │                  │
│  └────────────┘     └─────┬──────┘     └─────▲──────┘                  │
│         │                  │                  │                         │
│    Distance            MQTT              MQTT                          │
│    Reading            Publish            Subscribe                      │
│         │                  │                  │                         │
│         └──────────────────┼──────────────────┘                         │
│                            │                                            │
└────────────────────────────┼────────────────────────────────────────────┘
                             │
                             │ MQTT (TLS/SSL) & HTTP (InfluxDB API)
                             │
             ┌───────────────┼───────────────────────────────┐
             │               │                               │
             ▼               ▼                               ▼
    ┌────────────────┐ ┌────────────────┐          ┌────────────────┐
    │  HiveMQ Cloud  │ │  InfluxDB      │          │  Grafana       │
    │  (MQTT Broker) │ │  Cloud         │          │  Cloud         │
    │                │ │  (Time Series) │          │  (Dashboard)   │
    │  - Publish     │ │  - Store Data  │          │  - Visualize   │
    │  - Subscribe   │ │  - Query Data  │          │  - Real-time   │
    └────────────────┘ └────────────────┘          └────────────────┘
         │                    │                            │
         │                    │                            │
         └────────────────────┼────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │  Grafana Dashboard  │
                    │  - Live Chart       │
                    │  - Auto-Refresh     │
                    │  - Distance Trend   │
                    └─────────────────────┘
```

---

## Data Flow

1. **Sensor Reading**: HC-SR04 → GPIO → distance_queue
2. **MQTT Processing**: distance_queue → MQTT Publish (HiveMQ) + InfluxDB Write
3. **Cloud Storage**: HiveMQ stores messages, InfluxDB stores time-series data
4. **Visualization**: InfluxDB → Grafana Query → Live Dashboard
5. **Remote Control**: Dashboard → MQTT → LED Process → LED ON/OFF

---

## Key Learnings

### Time-Series Databases
- **InfluxDB**: Specialized database for time-stamped data with efficient storage and querying
- **Data Points**: Each measurement stored with timestamp and field values
- **Buckets**: Containers for organizing data (similar to databases)
- **Organizations**: Logical grouping for multi-team setups
- **Tokens**: Authentication mechanism for API access with granular permissions

### Visualization Tools
- **Grafana**: Open-source analytics and monitoring platform
- **Dashboards**: Customizable views for data visualization with multiple panels
- **Panels**: Individual visual elements (graphs, tables, stats, gauges)
- **Auto-Refresh**: Automatic dashboard updates at set intervals (5s)

### Cloud MQTT Brokers
- **HiveMQ**: Cloud-based MQTT broker service with free tier
- **TLS/SSL**: Secure encrypted MQTT communication on port 8883
- **Broker Credentials**: Authentication via username/password

### Integration Challenges Overcome
- **InfluxDB URL format**: Correct endpoint structure includes region
- **Token permissions**: Ensure token has write access to bucket
- **Grafana connection**: Using correct data source URL and credentials
- **Refresh rates**: Setting appropriate update intervals for live data
- **Data formatting**: Sending proper Point structure to InfluxDB

---

## Tools & Technologies

- **Cloud Platforms**: HiveMQ, InfluxDB Cloud, Grafana Cloud
- **Protocols**: MQTT (TLS/SSL), HTTP (InfluxDB API)
- **Python Libraries**: paho-mqtt, influxdb_client, gpiozero
- **Database**: InfluxDB (Time-Series Database)
- **Visualization**: Grafana
- **Hardware**: Raspberry Pi 4, HC-SR04 Sensor, LED

---

## Environment Variables Setup

```bash
# MQTT Configuration (HiveMQ)
MQTT_HOST=xxxxxxxxx.s1.eu.hivemq.cloud
MQTT_PORT=8883
MQTT_USERNAME=your_username
MQTT_PASSWORD=your_password

# InfluxDB Configuration
INFLUX_URL=https://us-central1-1.gcp.cloud2.influxdata.com
INFLUX_TOKEN=your_api_token
INFLUX_ORG=your_org_id
INFLUX_BUCKET=your_bucket_name
```

---

## Commands Used

```bash
# Install required packages
pip install paho-mqtt influxdb-client gpiozero

# Set environment variables (temporary)
export MQTT_HOST="your_hivemq_host"
export MQTT_PORT="8883"
export MQTT_USERNAME="your_hivemq_username"
export MQTT_PASSWORD="your_hivemq_password"
export INFLUX_URL="your_influxdb_url"
export INFLUX_TOKEN="your_influxdb_token"
export INFLUX_ORG="your_influxdb_org"
export INFLUX_BUCKET="your_influxdb_bucket"

# Run the system
python3 main.py

# View systemd logs if using service
sudo journalctl -u task9.service -f
```

---

## Modified Code: `mqtt.py` Key Additions

```python
# InfluxDB Client Creation
influx_client = InfluxDBClient(
    url=influx_url,
    token=influx_token,
    org=influx_org
)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)

# Writing data to InfluxDB
point = Point("distance").field("value", float(distance))
write_api.write(
    bucket=influx_bucket,
    org=influx_org,
    record=point
)

# MQTT TLS Configuration
client.tls_set(tls_version=ssl.PROTOCOL_TLS_CLIENT)

# MQTT Connection to HiveMQ
client.connect(host, port, 60)
```

---

## Grafana Setup Steps

### Data Source Configuration
1. Navigate to Configuration → Data Sources
2. Click "Add data source" → Select "InfluxDB"
3. Configure:
   - **URL**: InfluxDB Cloud URL
   - **Organization**: InfluxDB org ID
   - **Token**: API token
   - **Default bucket**: Bucket name
4. Click "Save & Test"

### Dashboard Panel Configuration
1. Create new dashboard → Add visualization
2. Query for distance data:
   ```
   from(bucket: "your_bucket")
     |> range(start: -5m)
     |> filter(fn: (r) => r._measurement == "distance")
     |> filter(fn: (r) => r._field == "value")
   ```
3. Configure panel:
   - **Visualization**: Time series graph
   - **Legend**: Show field names
   - **Axes**: Label as "Distance (cm)"
4. Set auto-refresh (5s, 10s, or 30s)

---

## Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| InfluxDB URL format incorrect | Used full URL with region (e.g., `https://us-central1-1.gcp.cloud2.influxdata.com`) |
| Token insufficient permissions | Generated new token with write permissions to bucket |
| Grafana not connecting to InfluxDB | Verified URL, org, token, and bucket name matched exactly |
| Dashboard not updating in real-time | Set auto-refresh rate in Grafana panel settings |
| Data not showing in InfluxDB | Verified Point structure used correct field format |
| TLS connection errors | Used `ssl.PROTOCOL_TLS_CLIENT` for secure connection |
| MQTT messages not arriving | Checked topic names matched exactly between publisher and subscriber |
| Environment variables not loading | Added to `.bashrc` and sourced file |
| Grafana query returning no data | Checked time range and bucket name in query |

---

## Files Modified

| File | Changes |
|------|---------|
| `mqtt.py` | Replaced Adafruit IO with HiveMQ, added InfluxDB integration |
| `sensor.py` | No changes from Day 3 |
| `led.py` | No changes from Day 3 |
| `main.py` | No changes from Day 3 |

---

## Real-World Applications

- **Industrial IoT**: Remote monitoring of equipment and machinery
- **Smart Agriculture**: Real-time environmental monitoring
- **Weather Stations**: Temperature, humidity, pressure data
- **Logistics**: Tracking goods across supply chains
- **Energy Management**: Power consumption monitoring
- **Predictive Maintenance**: Equipment health monitoring
- **Smart Buildings**: Occupancy, lighting, HVAC control

---

## Key Takeaways

- **Cloud Integration**: Complete IoT pipeline from device to cloud
- **Time-Series Data**: Efficient storage for time-stamped measurements
- **Real-Time Visualization**: Live updates via Grafana dashboards
- **Secure Communication**: TLS/SSL encrypted MQTT connections
- **Modular Design**: Code changes were minimal (only `mqtt.py` modified)
- **Scalable Architecture**: Can add more sensors, databases, and dashboards
- **Cloud Agnostic**: Can use different providers (Adafruit IO, HiveMQ, AWS, Azure)

