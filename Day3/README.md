# Day 3 - Adafruit IO, HTTP, MQTT & Inter-Process Communication

## Tasks Completed

### Task 1: Adafruit IO HTTP Communication
- Implemented HTTP communication with Adafruit IO cloud platform
- Created `AdafruitIO` class wrapper for HTTP requests
- Implemented POST method to upload sensor data to feeds
- Implemented GET method to retrieve latest values from feeds
- Used environment variables for secure credential management (`IO_USERNAME`, `IO_KEY`)
- Uploaded ultrasonic sensor distance readings to Adafruit IO
- Controlled LED remotely by reading feed values from Adafruit IO
- Real-time cloud-based monitoring and control

### Task 2: Adafruit IO MQTT Communication
- Implemented MQTT protocol for lightweight cloud communication
- Created `AdafruitIO` MQTT class wrapper
- Published sensor data to Adafruit IO feeds using MQTT
- Subscribed to LED control feed for remote control
- Implemented callback function for automatic feed updates
- Reduced network overhead compared to HTTP
- Real-time bidirectional communication with cloud

### Task 3: Inter-Process Communication (IPC)
- Split monolithic code into modular processes using multiprocessing
- Created three separate processes:
  - **Sensor Process:** Reads ultrasonic sensor and sends data to queue
  - **MQTT Process:** Handles cloud communication and LED commands
  - **LED Process:** Controls LED based on queue messages
- Used `multiprocessing.Queue` for inter-process communication
- Implemented clean process termination on KeyboardInterrupt
- Modular design for better maintainability and scalability

**Files Created:**
- `sensor.py` - Ultrasonic sensor reading process
- `mqtt.py` - MQTT communication process
- `led.py` - LED control process
- `main.py` - Main application orchestrator

### Task 4: Auto-Start Service Configuration
- Created systemd service for automatic startup on boot
- Configured service to restart automatically on failure
- Set environment variables for Adafruit IO credentials
- Service starts after network is available
- Process runs in background with automatic recovery

**Service File:** `/etc/systemd/system/task9.service`

---

## Key Learnings

- **Cloud Integration:** Connecting IoT devices to cloud platforms (Adafruit IO)
- **HTTP Protocol:** REST API communication for data upload and retrieval
- **MQTT Protocol:** Lightweight publish/subscribe messaging for IoT
- **Protocol Comparison:** HTTP vs MQTT for different use cases
- **Inter-Process Communication:** Using queues for data exchange between processes
- **Modular Design:** Breaking applications into focused, maintainable components
- **System Services:** Creating auto-start services with systemd
- **Environment Variables:** Secure credential management

---

## Tools & Technologies

- **Languages:** Python
- **Libraries:** requests, paho-mqtt, gpiozero, multiprocessing, os, time
- **Cloud Platform:** Adafruit IO
- **Protocols:** HTTP, MQTT
- **Hardware:** Raspberry Pi 4, HC-SR04 Ultrasonic Sensor, LED, Resistors
- **System:** systemd for service management
- **Version Control:** Git/GitHub

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        main.py                             │
│                  (Process Orchestrator)                     │
└────────────┬────────────────────┬─────────────────────────┘
             │                    │
    ┌────────▼────────┐  ┌────────▼────────┐
    │  sensor.py      │  │   mqtt.py      │
    │  (Sensor Proc)  │  │  (MQTT Proc)    │
    └────────┬────────┘  └────────┬────────┘
             │                    │
    ┌────────▼────────┐  ┌────────▼────────┐
    │   Queue         │  │   Queue         │
    │  distance_queue │  │   led_queue     │
    └─────────────────┘  └─────────────────┘
                                │
                       ┌────────▼────────┐
                       │   led.py        │
                       │  (LED Proc)     │
                       └─────────────────┘
```

---

## Communication Flow

1. **Sensor → MQTT:** Sensor reads distance → puts in `distance_queue` → MQTT process reads and publishes to Adafruit IO
2. **MQTT → LED:** Adafruit IO feed changes → MQTT callback receives → puts in `led_queue` → LED process reads and controls LED
3. **HTTP Flow:** Direct upload/download using REST API calls

---

## Code Files

| File | Description |
|------|-------------|
| `http_adafruit.py` | HTTP communication with Adafruit IO |
| `mqtt_adafruit.py` | MQTT communication with Adafruit IO |
| `sensor.py` | Ultrasonic sensor reading process |
| `mqtt.py` | MQTT communication process |
| `led.py` | LED control process |
| `main.py` | Main application orchestrator |
| `task9.service` | systemd service file |

---

## Commands Used

**Environment Variables Setup:**
```bash
export IO_USERNAME="your_username"
export IO_KEY="your_adafruit_key"
```

**Running Applications:**
```bash
# HTTP Version
python3 http_adafruit.py

# MQTT Version
python3 mqtt_adafruit.py

# IPC Version
python3 main.py
```

**Systemd Service Configuration:**
```bash
sudo nano /etc/systemd/system/task9.service
sudo systemctl daemon-reload
sudo systemctl enable task9.service
sudo systemctl start task9.service
sudo systemctl status task9.service
```

---

## Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| Environment variables not loading | Added to .bashrc and systemd service file |
| MQTT connection dropping | Implemented automatic reconnect logic |
| Process communication overhead | Used efficient Queue implementation |
| Service not starting on boot | Configured systemd with proper dependencies |
| Credential security | Used environment variables instead of hardcoding |
| Process cleanup on exit | Implemented proper termination handling |

---

## Real-World Applications

- **Cloud-Connected Sensors:** Remote environmental monitoring
- **Smart Home:** Remote control of devices via cloud
- **Industrial IoT:** Machine monitoring and control
- **Data Logging:** Cloud-based data collection and analysis
- **Alert Systems:** Cloud-triggered notifications
- **Device Orchestration:** Coordinating multiple devices

---

## Protocol Comparison

| Feature | HTTP | MQTT |
|---------|------|------|
| Protocol | Request/Response | Publish/Subscribe |
| Overhead | High | Low |
| Bandwidth | High | Low |
| Latency | Higher | Lower |
| Connection | Stateless | Persistent |
| Bidirectional | Polling required | Native |
| Use Case | Web APIs | IoT/M2M |

---

## Service Configuration Details

**Systemd Service Parameters:**
- `Type=simple`: Standard process
- `Restart=always`: Auto-restart on failure
- `RestartSec=5`: Wait 5 seconds before restart
- `After=network.target`: Start after network is up
- `Environment`: Credentials passed securely
