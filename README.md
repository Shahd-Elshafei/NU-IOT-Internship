# NU-IOT-Internship

## 📋 Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Day 1 - Emirp Number Finder & GPIO LED Control](#day-1---emirp-number-finder--gpio-led-control)
- [Day 2 - Interrupts, Debouncing, Ultrasonic Sensor & Data Logging](#day-2---interrupts-debouncing-ultrasonic-sensor--data-logging)
- [Day 3 - Adafruit IO, HTTP, MQTT & Inter-Process Communication](#day-3---adafruit-io-http-mqtt--inter-process-communication)
- [Day 4 - Grafana, InfluxDB, HiveMQ & Data Visualization](#day-4---grafana-influxdb-hivemq--data-visualization)
- [Day 5 - TI CC1352P7, SimpleLink & Bluetooth Low Energy](#day-5---ti-cc1352p7-simplelink--bluetooth-low-energy)
- [Days 6 & 7 - Zigbee Communication with TI CC1352P7](#days-6--7---zigbee-communication-with-ti-cc1352p7)
- [Day 8 - CC1352P7 to Raspberry Pi Communication via UART](#day-8---cc1352p7-to-raspberry-pi-communication-via-uart)
- [Days 9 & 10 - Wi-SUN Connection with CC1352P7](#days-9--10---wi-sun-connection-with-cc1352p7)
- [Technologies Used](#technologies-used)
- [Key Learnings](#key-learnings)
- [Conclusion](#conclusion)

---

## Overview

This repository documents the complete IoT internship experience, covering a wide range of technologies from embedded systems programming to cloud integration and wireless communication protocols. The internship progressed from basic C programming on Raspberry Pi to advanced wireless protocols on TI CC1352P7 LaunchPad kits.

---

## Repository Structure

```
IoT-Internship/
├── day1/
│   ├── README.md
│   ├── task1.c              # Emirp number finder
│   └── led_blink.c          # GPIO LED control
├── day2/
│   ├── README.md
│   ├── button_interrupt.c   # Interrupt-driven button with debouncing
│   ├── ultrasonic_sensor.py # Distance measurement with SQLite logging
│   └── visualize_data.py    # Data visualization script
├── day3/
│   ├── README.md
│   ├── http_adafruit.py     # HTTP communication with Adafruit IO
│   ├── mqtt_adafruit.py     # MQTT communication with Adafruit IO
│   ├── sensor.py            # Sensor process
│   ├── mqtt.py              # MQTT process
│   ├── led.py               # LED control process
│   ├── main.py              # Main orchestrator
│   └── task9.service        # systemd service file
├── day4/
│   ├── README.md
│   ├── mqtt.py              # Modified for HiveMQ + InfluxDB
│   ├── sensor.py            # Unchanged from day3
│   ├── led.py               # Unchanged from day3
│   ├── main.py              # Unchanged from day3
│   └── task9.service        # Updated service file
├── day5/
│   ├── README.md
│   └── simplelink_projects/ # TI SimpleLink SDK projects
│       ├── simple_peripheral
│       └── simple_central
├── day6-7/
│   ├── README.md
│   └── zigbee_examples/
│       ├── zc_light         # Coordinator - Light Example
│       ├── zr_light         # Router - Light Example
│       ├── zed_light        # End Device - Light Example
│       ├── zc_temperaturesensor # Coordinator - Temperature
│       └── zed_temperaturesensor # End Device - Temperature
├── day8/
│   ├── README.md
│   ├── display.c            # CC1352P7 UART firmware
│   └── read_uart.py         # Raspberry Pi receiver
├── day9-10/
│   ├── README.md
│   └── ns_node/             # Wi-SUN ns_node example
└── README.md                # This file
```

---

## Day 1 - Emirp Number Finder & GPIO LED Control

### Tasks Completed
- Developed C program to find emirp numbers (prime numbers whose reverse is also prime)
- Implemented primality testing optimized to sqrt(n)
- Used dynamic memory allocation for storing emirp pairs
- Learned GPIO control on Raspberry Pi using libgpiod
- Created bash function for automated compilation

### Key Files
- `task1.c` - Emirp number finder
- `led_blink.c` - GPIO LED blinking

---

## Day 2 - Interrupts, Debouncing, Ultrasonic Sensor & Data Logging

### Tasks Completed
- Implemented hardware interrupts with falling edge detection
- Added 200ms software debounce for button
- Integrated HC-SR04 ultrasonic sensor
- Stored readings in SQLite database
- Created data visualization with matplotlib

### Key Files
- `button_interrupt.c` - Interrupt-driven button with debouncing
- `ultrasonic_sensor.py` - Distance measurement with SQLite logging
- `visualize_data.py` - Data visualization script

---

## Day 3 - Adafruit IO, HTTP, MQTT & Inter-Process Communication

### Tasks Completed
- Implemented HTTP communication with Adafruit IO
- Implemented MQTT communication with Adafruit IO
- Split code into modular processes (sensor, MQTT, LED)
- Used multiprocessing queues for inter-process communication
- Created systemd service for auto-start

### Key Files
- `http_adafruit.py` - HTTP communication
- `mqtt_adafruit.py` - MQTT communication
- `sensor.py` - Sensor process
- `mqtt.py` - MQTT process
- `led.py` - LED control process
- `main.py` - Main orchestrator
- `task9.service` - systemd service

---

## Day 4 - Grafana, InfluxDB, HiveMQ & Data Visualization

### Tasks Completed
- Set up HiveMQ Cloud MQTT broker
- Configured InfluxDB Cloud for time-series data
- Modified mqtt.py to write data to InfluxDB
- Created Grafana Cloud dashboard for visualization
- Set up real-time data updates with auto-refresh

### Key Files
- `mqtt.py` - Modified for HiveMQ + InfluxDB
- `task9.service` - Updated with new environment variables

---

## Day 5 - TI CC1352P7, SimpleLink & Bluetooth Low Energy

### Tasks Completed
- Installed Code Composer Studio and SimpleLink SDK
- Loaded LED example on CC1352P7
- Connected mobile phone using nRF Connect app
- Controlled LED via BLE from mobile
- Established BLE connection between two kits
- Learned debugging with Putty serial terminal

### Key Projects
- `simple_peripheral` - BLE peripheral (Kit 1)
- `simple_central` - BLE central (Kit 2)

---

## Days 6 & 7 - Zigbee Communication with TI CC1352P7

### Tasks Completed
- Configured Coordinator (Kit 1) to form Zigbee network
- Configured Router (Kit 2) to extend network
- Configured End Device (Kit 3) to join network
- Implemented Light Example - LED control across network
- Implemented Temperature Example - sensor data sharing
- Any device can control LEDs on any other device

### Key Projects
- `zc_light` - Coordinator LED control
- `zr_light` - Router LED control
- `zed_light` - End Device LED control
- `zc_temperaturesensor` - Coordinator temperature
- `zed_temperaturesensor` - End Device temperature

---

## Day 8 - CC1352P7 to Raspberry Pi Communication via UART

### Tasks Completed
- Connected HC-SR04 ultrasonic sensor to CC1352P7
- Implemented distance measurement on CC1352P7
- Configured UART communication over USB
- Sent sensor data from CC1352P7 to Raspberry Pi
- Displayed readings clearly on Raspberry Pi terminal

### Key Files
- `display.c` - CC1352P7 UART firmware
- `read_uart.py` - Raspberry Pi receiver

---

## Days 9 & 10 - Wi-SUN Connection with CC1352P7

### Tasks Completed
- Flashed ns_node firmware on three CC1352P7 kits
- Established Wi-SUN FAN mesh network
- All devices joined network as router nodes
- Verified self-healing mesh topology

### Key Projects
- `ns_node` - Wi-SUN router node example

---

## Technologies Used

### Hardware
- **Raspberry Pi 4** - IoT gateway and prototyping
- **TI CC1352P7 LaunchPad** - Dual-band wireless MCU (sub-1GHz + BLE)
- **HC-SR04 Ultrasonic Sensor** - Distance measurement
- **LEDs and Buttons** - Input/output components

### Software & Tools
- **Programming Languages**: C, Python
- **IDEs**: Code Composer Studio, Visual Studio Code
- **Cloud Platforms**: Adafruit IO, HiveMQ, InfluxDB Cloud, Grafana Cloud
- **Protocols**: HTTP, MQTT, BLE, Zigbee, Wi-SUN, UART
- **Libraries**: libgpiod, gpiozero, paho-mqtt, influxdb_client, matplotlib, pandas
- **Debug Tools**: Putty, nRF Connect, Logic Analyzer

---

## Key Learnings

### Programming Concepts
- C programming for embedded systems
- Python for IoT applications
- Inter-Process Communication (IPC)
- Dynamic memory management
- Input validation and error handling

### Communication Protocols
- **UART**: Wired serial communication
- **BLE**: Bluetooth Low Energy for short-range wireless
- **Zigbee**: Mesh networking for smart home
- **Wi-SUN**: Large-scale mesh for smart city
- **MQTT**: Lightweight publish/subscribe for IoT
- **HTTP**: REST API communication

### Cloud & Databases
- Time-series databases (InfluxDB)
- Data visualization (Grafana)
- MQTT brokers (HiveMQ, Adafruit IO)
- Systemd services for auto-start

### Embedded Systems
- GPIO programming
- Interrupt handling
- Debouncing techniques
- Sensor interfacing
- Firmware development with TI SDK

---

## Conclusion

This internship provided comprehensive hands-on experience in IoT systems development, covering the entire stack from embedded hardware programming to cloud-based data visualization. The progression from basic C programming on Raspberry Pi to advanced wireless protocols on TI CC1352P7 demonstrates a complete IoT development journey.

---

*Report prepared for IoT Internship*
