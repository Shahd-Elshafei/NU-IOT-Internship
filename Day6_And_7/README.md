# Day 6 & 7 - Zigbee Communication with TI CC1352P7

## Overview

Day 6 and 7 focused on implementing Zigbee wireless communication between multiple CC1352P7 LaunchPad kits using the TI SimpleLink SDK. We explored Zigbee network formation with coordinator, router, and end device roles, and implemented both LED control and temperature monitoring examples with bidirectional communication across the network.

---

## Tasks Completed

### Task 1: Zigbee Network Formation
- Configured Kit 1 as Zigbee Coordinator to form the network
- Configured Kit 2 as Zigbee Router to extend network range
- Configured Kit 3 as Zigbee End Device to join the network
- Established PAN ID and channel for network communication
- All devices successfully joined the network

### Task 2: Zigbee Light Example (LED Control)
- Implemented Zigbee light example on all devices
- Coordinator formed network and controlled LEDs
- Router and End Device joined and could control LEDs
- Any device in network could toggle LEDs on any other device
- Bidirectional LED state synchronization across network

### Task 3: Zigbee Temperature Example
- Loaded temperature sensor example on all devices
- Coordinator displayed temperature readings
- Router and End Device could read and adjust temperature values
- Discovered temperature sensor measures internal chip temperature
- Bidirectional temperature data exchange across network

### Task 4: Device-to-Device Communication
- Any device in network could send messages to any other
- LED states synchronized across all devices
- Temperature data shared between all network members
- Verified communication reliability and message delivery

---

## Zigbee Network Topology

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          Zigbee Network (PAN)                          │
│                                                                         │
│                      ┌─────────────────────────┐                       │
│                      │   Coordinator (Kit 1)    │                       │
│                      │   - Forms Network        │                       │
│                      │   - PAN ID: 0x1234       │                       │
│                      │   - Channel: 25          │                       │
│                      │   - LED Control          │                       │
│                      │   - Temperature Reading  │                       │
│                      └───────────┬─────────────┘                       │
│                                  │                                      │
│                                  │ Zigbee Connection                    │
│                                  │                                      │
│                      ┌───────────┴─────────────┐                       │
│                      │   Router (Kit 2)         │                       │
│                      │   - Extends Network      │                       │
│                      │   - Forwards Messages    │                       │
│                      │   - LED Control          │                       │
│                      │   - Temperature Reading  │                       │
│                      └───────────┬─────────────┘                       │
│                                  │                                      │
│                                  │ Zigbee Connection                    │
│                                  │                                      │
│                      ┌───────────┴─────────────┐                       │
│                      │   End Device (Kit 3)     │                       │
│                      │   - Joins Network        │                       │
│                      │   - LED Control          │                       │
│                      │   - Temperature Reading  │                       │
│                      └─────────────────────────┘                       │
│                                                                         │
│  Communication Flow:                                                    │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐                       │
│  │   Kit 1    │◄─►│   Kit 2    │◄─►│   Kit 3    │                       │
│  │ (Coord)    │  │  (Router)  │  │ (End Dev)  │                       │
│  │ LED/Temp   │  │  LED/Temp  │  │  LED/Temp  │                       │
│  └────────────┘  └────────────┘  └────────────┘                       │
│                                                                         │
│  All devices can control LEDs and share temperature data               │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Zigbee Device Roles

| Role | Device | Responsibilities |
|------|--------|------------------|
| **Coordinator** | Kit 1 | Forms network, manages joining, routes messages |
| **Router** | Kit 2 | Extends network range, forwards messages, joins network |
| **End Device** | Kit 3 | Joins network, sends/receives data, can sleep |

---

## Examples Implemented

### 1. Zigbee Light Example (LED Control)
- **Purpose**: Control LEDs across Zigbee network
- **Functionality**:
  - Any device can toggle LED on any other device
  - LED state synchronized across all devices
  - Bidirectional control using Zigbee clusters
  - Network-wide LED status updates

**How It Works:**
1. User presses button on Kit 1
2. Kit 1 toggles its own LED
3. Kit 1 sends message to all devices in network
4. Kit 2 and Kit 3 receive message and toggle their LEDs
5. All LEDs synchronized across network

### 2. Zigbee Temperature Example
- **Purpose**: Monitor and share temperature data
- **Functionality**:
  - All devices read internal chip temperature
  - Temperature data shared across network
  - Each device displays its own and received temperatures
  - Bidirectional temperature data exchange

**How It Works:**
1. Each device reads its internal temperature sensor
2. Devices broadcast temperature to network
3. All devices display received temperatures
4. Network-wide temperature monitoring

---

## Communication Flow

### LED Control Example
```
Button Press on Kit 1:
  ┌────────────┐
  │ Kit 1 (Coord) │──┐
  └────────────┘  │
                   │ Zigbee Message
  ┌────────────┐  │  ┌────────────┐
  │ Kit 2 (Router)│◄─┘ │ Kit 3 (End) │
  └────────────┘      └────────────┘
   LED Toggles         LED Toggles
```

### Temperature Example
```
Temperature Readings:
  ┌────────────┐    ┌────────────┐    ┌────────────┐
  │ Kit 1 (Coord)│    │ Kit 2 (Router)│    │ Kit 3 (End) │
  │  28.5°C     │    │  27.8°C     │    │  27.2°C     │
  └────────────┘    └────────────┘    └────────────┘
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │
              Zigbee Broadcast to All
                          │
       ┌──────────────────┼──────────────────┐
       ▼                  ▼                  ▼
  ┌────────────┐    ┌────────────┐    ┌────────────┐
  │ Kit 1      │    │ Kit 2      │    │ Kit 3      │
  │ Shows All  │    │ Shows All  │    │ Shows All  │
  └────────────┘    └────────────┘    └────────────┘
```

---

## Setup and Configuration

### Project Import
```
1. Open Code Composer Studio
2. File → Import → CCS Projects
3. Browse to SDK examples path:
   /ti/simplelink_cc13xx_cc26xx_sdk_x_xx_xx_xx/examples/rtos/CC1352P7_1/
4. Select:
   - zigbee/zc_light (Coordinator)
   - zigbee/zr_light (Router)
   - zigbee/zed_light (End Device)
   - zigbee/zc_temperaturesensor (Coordinator)
   - zigbee/zed_temperaturesensor (End Device)
5. Click Finish
```

### Build and Flash
```bash
# Build each project
Project → Build All

# Flash to respective boards
Run → Debug

# Coordinator → Kit 1
# Router → Kit 2
# End Device → Kit 3
```

### Debug with Putty
```
1. Connect USB to each LaunchPad
2. Open Putty for each COM port
3. Settings:
   - Speed: 115200
4. View Zigbee debug messages
```

---

## Debug Output Examples

### Coordinator Debug (Light Example)
```
[ZIGBEE] Coordinator Initialized
[ZIGBEE] Network Formed - PAN ID: 0x1234
[ZIGBEE] Device Address: 0x0000
[ZIGBEE] Network Open for Joining
[ZIGBEE] Device Joined: 0x0001 (Router)
[ZIGBEE] Device Joined: 0x0002 (End Device)
[LIGHT] Button Pressed - Toggling LED
[ZIGBEE] LED State Sent to All Devices
[ZIGBEE] Received LED State from 0x0001
```

### Router Debug (Light Example)
```
[ZIGBEE] Router Initialized
[ZIGBEE] Scanning for Networks...
[ZIGBEE] Found Network - PAN ID: 0x1234
[ZIGBEE] Joining Network...
[ZIGBEE] Joined Successfully - Address: 0x0001
[ZIGBEE] Received LED Toggle from 0x0000
[LIGHT] LED State Updated
```

### End Device Debug (Temperature Example)
```
[ZIGBEE] End Device Initialized
[ZIGBEE] Joining Network...
[ZIGBEE] Joined Successfully - Address: 0x0002
[TEMP] Reading: 27.2°C
[TEMP] Sending to Network
[TEMP] Received from 0x0000: 28.5°C
[TEMP] Received from 0x0001: 27.8°C
```

---

## Key Learnings

### Zigbee Network Concepts
- **Coordinator**: Network formation and management
- **Router**: Network extension and message forwarding
- **End Device**: Network node that can sleep
- **PAN ID**: Network identifier
- **Channel**: RF communication channel
- **Addressing**: 16-bit short addresses

### Zigbee Examples
- **Light Example**: LED control across network
- **Temperature Example**: Sensor data sharing
- **Any-to-Any Communication**: All devices can talk to all devices

### Temperature Sensor Insight
- **Internal Sensor**: Measures chip temperature, not external
- **Range**: -40°C to +125°C
- **Accuracy**: ±5°C typical
- **Usage**: Chip thermal monitoring

---

## Tools & Technologies

- **IDE**: Code Composer Studio (TI)
- **SDK**: SimpleLink CC13xx/CC26xx SDK
- **Protocol**: Zigbee (IEEE 802.15.4)
- **Hardware**: TI CC1352P7 LaunchPad (3 kits)
- **Debug**: Putty (serial terminal)
- **MCU**: ARM Cortex-M4F

---

## Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| Router not forwarding messages | Verified router configuration and addressing |
| End Device not joining | Checked channel and PAN ID matching |
| LED not synchronizing | Verified cluster and attribute settings |
| Temperature readings inaccurate | Understood it's internal chip temperature |
| Devices not discovering each other | Ensured coordinator network open for joining |

