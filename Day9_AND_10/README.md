# Day 9 & 10 - Wi-SUN Connection with CC1352P7 LaunchPad


## Overview

Day 9 and 10 focused on establishing a Wi-SUN (Wireless Smart Ubiquitous Network) connection using three CC1352P7 LaunchPad kits. We used the `ns_node` example on all three kits to create a Wi-SUN mesh network.

---

## Tasks Completed

- Configured three CC1352P7 LaunchPad kits with the `ns_node` example from the SimpleLink SDK
- Flashed the `ns_node` firmware onto all three kits using Code Composer Studio
- Established a Wi-SUN FAN (Field Area Network) mesh connection between the three devices
- Verified that all three kits successfully joined the Wi-SUN network
- Tested communication between the devices in the network

---

## What is Wi-SUN?

Wi-SUN (Wireless Smart Ubiquitous Network) is a protocol based on IEEE 802.15.4 that enables:
- Large-scale mesh networks
- Long-range communication
- Low power consumption
- Self-healing capabilities (devices automatically reroute around failed nodes)
- Smart city applications (street lighting, utility metering, environmental monitoring)

---

## Hardware Setup

| Component | Quantity | Description |
|-----------|----------|-------------|
| CC1352P7 LaunchPad | 3 kits | TI wireless MCU with sub-1GHz transceiver |
| USB Cables | 3 | For power and programming |
| Computer | 1 | Running Code Composer Studio |

### Device Roles:
| Device | Role | Description |
|--------|------|-------------|
| Kit 1 | Router Node (ns_node) | Connected to network, routes packets |
| Kit 2 | Router Node (ns_node) | Connected to network, routes packets |
| Kit 3 | Router Node (ns_node) | Connected to network, routes packets |

---

## Network Topology

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          Wi-SUN Mesh Network                          │
│                                                                         │
│                      ┌─────────────────────────┐                       │
│                      │      Kit 1 (ns_node)     │                       │
│                      │   - Router Node          │                       │
│                      │   - Routes Packets       │                       │
│                      └───────────┬─────────────┘                       │
│                                  │                                      │
│                                  │ Wi-SUN Connection                    │
│                                  │                                      │
│                      ┌───────────┴─────────────┐                       │
│                      │      Kit 2 (ns_node)     │                       │
│                      │   - Router Node          │                       │
│                      │   - Routes Packets       │                       │
│                      └───────────┬─────────────┘                       │
│                                  │                                      │
│                                  │ Wi-SUN Connection                    │
│                                  │                                      │
│                      ┌───────────┴─────────────┐                       │
│                      │      Kit 3 (ns_node)     │                       │
│                      │   - Router Node          │                       │
│                      │   - Routes Packets       │                       │
│                      └─────────────────────────┘                       │
│                                                                         │
│  All devices form a mesh network with self-healing capabilities        │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Setup and Configuration

### Project Import
```
1. Open Code Composer Studio
2. File → Import → CCS Projects
3. Browse to SDK examples path:
   /ti/simplelink_cc13xx_cc26xx_sdk_x_xx_xx_xx/examples/rtos/CC1352P7_4/
4. Select: wi-sun/ns_node
5. Click Finish
```

### Build and Flash
```bash
# Build the ns_node project
Project → Build All

# Flash to each board
Run → Debug

# Repeat for all three kits
```

### Debug with Putty
```
1. Connect USB to each LaunchPad
2. Open Putty for each COM port
3. Settings:
   - Speed: 115200
4. View Wi-SUN network debug messages
```

---

## Key Learnings

- **Wi-SUN FAN**: Field Area Network for large-scale mesh networks
- **Router Node**: Device that forwards packets to other devices (ns_node)
- **Mesh Topology**: Self-healing network with automatic rerouting
- **CC1352P7**: Supports sub-1GHz communication with integrated PA
- **Self-Healing**: Network automatically reroutes around failed nodes

---

## Tools & Technologies

- **IDE**: Code Composer Studio (TI)
- **SDK**: SimpleLink CC13xx/CC26xx SDK
- **Protocol**: Wi-SUN FAN (IEEE 802.15.4)
- **Hardware**: TI CC1352P7 LaunchPad (3 kits)
- **Debug**: Putty (serial terminal)

