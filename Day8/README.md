# Day 8 - CC1352P7 to Raspberry Pi Communication via UART


## Overview

Day 8 focused on establishing wired communication between the CC1352P7 LaunchPad and Raspberry Pi using UART over USB. We connected an ultrasonic sensor to the CC1352P7, read distance measurements, and transmitted the data via UART to the Raspberry Pi for display.

---

## Tasks Completed

- Connected HC-SR04 ultrasonic sensor to CC1352P7 LaunchPad (TRIG and ECHO pins)
- Configured GPIO pins on CC1352P7 for sensor reading
- Implemented distance measurement code on CC1352P7
- Configured UART on CC1352P7 for serial communication
- Connected CC1352P7 to Raspberry Pi via USB cable
- Wrote Python script on Raspberry Pi to read serial data
- Displayed distance readings clearly on Raspberry Pi terminal
- Verified real-time data transmission and reception

---

## Hardware Setup

| Component | Connection |
|-----------|------------|
| HC-SR04 VCC | CC1352P7 5V |
| HC-SR04 GND | CC1352P7 GND |
| HC-SR04 TRIG | CC1352P7 GPIO (DIO13) |
| HC-SR04 ECHO | CC1352P7 GPIO (DIO14) |
| CC1352P7 USB | Raspberry Pi USB Port |

---

## Data Flow

1. CC1352P7 sends trigger pulse to ultrasonic sensor
2. Sensor returns echo pulse 
3. CC1352P7 calculates distance in cm
4. CC1352P7 formats data and sends via UART over USB
5. Raspberry Pi reads serial data
6. Distance displayed on terminal

---

## Key Learnings

- **UART Communication**: Serial data transmission over USB
- **Baud Rate**: 115200 (must match on both devices)
- **Virtual COM Port**: CC1352P7 appears as /dev/ttyUSB0 or /dev/ttyACM0
- **Ultrasonic Sensor**: distance_cm = pulseWidth / 58
- **Data Formatting**: CSV format for easy parsing

---

## Commands Used

```bash
# Check serial port
ls -l /dev/ttyUSB*
ls -l /dev/ttyACM0

# Add user to dialout group for permissions
sudo usermod -a -G dialout pi

# Run Python receiver script
python3 read_uart.py
```

---

## Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| Serial port not found | Checked /dev/ttyUSB* and /dev/ttyACM0 |
| Permission denied | Added user to dialout group |
| No data received | Verified baud rate (115200) |
| Garbage characters | Checked data format and baud rate |

---

## Tools & Technologies

- **IDE**: Code Composer Studio (TI)
- **Hardware**: CC1352P7 LaunchPad, HC-SR04 Sensor, Raspberry Pi
- **Communication**: UART over USB
- **Languages**: C (CC1352P7), Python (Raspberry Pi)

