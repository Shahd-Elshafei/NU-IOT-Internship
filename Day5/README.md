# Day 5 - TI CC1352P7, SimpleLink, Bluetooth Low Energy (BLE)


## Overview

Day 5 marked a significant transition from Raspberry Pi development to embedded systems programming using Texas Instruments' CC1352P7 microcontroller. We explored the TI SimpleLink SDK, learned about BLE (Bluetooth Low Energy) communication, and implemented wireless control between devices using the CC1352P7 LaunchPad kits.

---

## Tasks Completed

### Task 1: Code Composer Studio Setup
- Installed Code Composer Studio (CCS) - TI's integrated development environment
- Installed SimpleLink CC13xx/CC26xx SDK
- Configured workspace and project settings
- Learned the TI project structure and build system

### Task 2: SimpleLink SDK Exploration
- Explored the SimpleLink SDK architecture
- Learned about the BLE stack implementation
- Reviewed example projects structure (simple_peripheral, simple_central)
- Understood the RTOS (TI-RTOS) integration

### Task 3: LED Example - Button Controlled LED
- Loaded the LED example on a single CC1352P7 kit
- Configured GPIO pins for LED and button
- Implemented button press to toggle LED
- Tested basic GPIO functionality

### Task 4: BLE Connection with Mobile (nRF Connect)
- Installed nRF Connect mobile app on smartphone
- Enabled Bluetooth on the phone
- Ran simple_peripheral example on CC1352P7 kit
- Discovered the device using nRF Connect
- Connected to the BLE device
- Controlled LED via BLE characteristics
- Sent and received data between mobile and MCU

### Task 5: BLE Communication Between Two Kits
- Flashed simple_peripheral on Kit 1 (Peripheral/Server)
- Flashed simple_central on Kit 2 (Central/Client)
- Kit 2 scanned and discovered Kit 1 using MAC address
- Established BLE connection between the two kits
- Sent messages between kits using BLE characteristics
- Verified communication using debug output via Putty

### Task 6: Debugging with Putty
- Configured UART serial connection
- Used Putty as serial terminal for debugging
- Viewed BLE connection logs and status messages
- Monitored data transmission between devices

---

## Hardware Setup

### CC1352P7 LaunchPad Overview
- **Microcontroller**: TI CC1352P7 dual-band wireless MCU
- **Processor**: ARM Cortex-M4F
- **Wireless**: Sub-1 GHz + Bluetooth 5.2
- **Memory**: 352KB Flash, 80KB RAM
- **Features**: Low power, dual-band operation

### Kit 1 Configuration (Peripheral)
| Component | Description |
|-----------|-------------|
| **Role** | BLE Peripheral (Server) |
| **Firmware** | simple_peripheral |
| **Function** | Advertises BLE services, responds to requests |
| **LED** | GPIO controlled via BLE write |
| **Button** | Sends notifications on press |

### Kit 2 Configuration (Central)
| Component | Description |
|-----------|-------------|
| **Role** | BLE Central (Client) |
| **Firmware** | simple_central |
| **Function** | Scans for peripherals, connects, reads/writes |
| **Discovery** | Uses MAC address to find Kit 1 |
| **Control** | Sends messages to Kit 1 via BLE |


## BLE Communication Flow

1. **Peripheral (Kit 1) Advertising**: simple_peripheral broadcasts BLE advertisements containing device name, service UUIDs, MAC address
2. **Central (Kit 2) Scanning**: simple_central scans for BLE devices, detects Kit 1 advertisements
3. **Connection Establishment**: Central initiates connection request, Peripheral accepts
4. **Service Discovery**: Central discovers GATT services on peripheral, reads handles
5. **Data Exchange**: Central writes to characteristics, Peripheral sends notifications

---

## Key Learnings

### BLE Concepts
- **GATT**: Generic Attribute Profile - defines data exchange
- **Services**: Collection of characteristics (e.g., LED service)
- **Characteristics**: Data values (e.g., LED state, button state)
- **UUIDs**: Universally Unique Identifiers for services and characteristics
- **Advertising**: Broadcasting device presence and services
- **Scanning**: Discovering nearby BLE devices
- **Central/Peripheral**: Roles in BLE connection
- **Client/Server**: Data exchange roles (GATT client/server)

### TI SimpleLink SDK
- **TI-RTOS**: Real-time operating system for TI devices
- **BLE Stack**: TI's implementation of Bluetooth LE
- **Board Files**: Hardware abstraction for specific boards
- **Project Structure**: Organized examples and libraries

### Embedded Development
- **CCS IDE**: Code Composer Studio for development
- **Debugging**: JTAG/SWD debugging with XDS110
- **UART**: Serial communication for debugging with Putty
- **Flashing**: Loading firmware to MCU

---

## Tools & Technologies

- **IDE**: Code Composer Studio (TI)
- **SDK**: SimpleLink CC13xx/CC26xx SDK
- **Hardware**: TI CC1352P7 LaunchPad (2 kits)
- **Protocol**: Bluetooth Low Energy (BLE) 5.2
- **App**: nRF Connect (mobile debugging)
- **Debug**: Putty (serial terminal)
- **MCU Architecture**: ARM Cortex-M4F

---

## SimpleLink Example Projects

### simple_peripheral (Kit 1)
- **Purpose**: BLE peripheral/server role
- **Functionality**: Advertises BLE services, accepts incoming connections, provides GATT services, responds to read/write requests, sends notifications for button events

### simple_central (Kit 2)
- **Purpose**: BLE central/client role
- **Functionality**: Scans for BLE devices, initiates connections, discovers GATT services, reads/writes characteristics, receives notifications

---

## Setup and Configuration

### Code Composer Studio Installation
```bash
# Download CCS from TI website
# Install with default options
# Add SimpleLink SDK path
```

### Project Import
```
1. Open Code Composer Studio
2. File → Import → CCS Projects
3. Browse to SDK examples path:
   /ti/simplelink_cc13xx_cc26xx_sdk_x_xx_xx_xx/examples/rtos/CC1352P7_1/
4. Select:
   - ble5stack/simple_peripheral
   - ble5stack/simple_central
5. Click Finish
```

### Build and Flash
```bash
# Build project
Project → Build All

# Flash to board
Run → Debug
or
Flash using UniFlash
```

### Serial Debug with Putty
```
1. Connect USB to LaunchPad
2. Note COM port (Windows) or /dev/ttyUSB* (Linux)
3. Open Putty with:
   - Connection type: Serial
   - Port: COMx or /dev/ttyUSBx
   - Speed: 115200
4. View BLE debug messages
```

---

## nRF Connect Mobile App Steps

1. Download nRF Connect from App Store/Play Store
2. Open app and scan for BLE devices
3. Find "Simple Peripheral" device
4. Tap CONNECT to establish connection
5. Navigate to GATT Server
6. Find LED service characteristic
7. Write 0x01 to turn LED ON, 0x00 to turn OFF
8. Enable notifications for button characteristic
9. Press button on kit and see notification received

---

## BLE Pairing Between Kits

### Prerequisites
- **Kit 1**: Flashed with simple_peripheral
- **Kit 2**: Flashed with simple_central
- **Known MAC address**: Obtain from Kit 1 console logs

### Connection Process
1. Kit 2 starts scanning for BLE devices
2. Detects Kit 1 advertising
3. Filters by MAC address
4. Sends connection request
5. Kit 1 accepts connection
6. Connection established
7. Kit 2 discovers services
8. Kit 2 writes to characteristics

### Message Sending
- Kit 2 writes to LED characteristic to control Kit 1's LED
- Kit 1 sends notifications when button is pressed
- Bidirectional communication established

---

## Key Functions (simple_peripheral.c)

```c
// BLE Stack initialization
static void SimplePeripheral_init(void)

// Advertising start
static void SimplePeripheral_startAdvertising(void)

// BLE connection callback
static void SimplePeripheral_connCallback(void)

// GATT service callback
static void SimplePeripheral_processGattMsg(void)

// GPIO callback (button)
static void SimplePeripheral_btnCallback(void)
```

## Key Functions (simple_central.c)

```c
// Scanner initialization
static void SimpleCentral_init(void)

// Scanning start
static void SimpleCentral_startScanning(void)

// Device discovery callback
static void SimpleCentral_deviceDiscoveryCallback(void)

// Connection callback
static void SimpleCentral_connCallback(void)

// GATT discovery callback
static void SimpleCentral_processGattDiscCallback(void)
```

---

## Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| CCS installation issues | Installed with administrative privileges |
| SDK not found in workspace | Manually added SDK path in preferences |
| BLE devices not discovering | Ensured both kits powered and advertising |
| Connection refused error | Checked MAC address and connection parameters |
| LED not responding to writes | Verified characteristic UUID and write permissions |
| Putty not showing debug output | Checked UART baud rate (115200) |
| Notification not received | Enabled notifications in nRF Connect |
| Two kits not connecting | Flashed one with peripheral, one with central |
| Mobile app cannot connect | Ensured device advertising correctly |
| Build errors | Set correct build configuration (Debug/Release) |

---

## Real-World Applications

- **Home Automation**: Bluetooth controlled lighting
- **Smart Sensors**: BLE temperature/humidity sensors
- **Healthcare**: Wireless medical devices
- **Industrial**: Wireless control and monitoring
- **Asset Tracking**: BLE beacons
- **Smart Wearables**: Fitness trackers, smartwatches
- **Automotive**: Keyless entry systems

---

## Key Takeaways

- **Embedded Systems**: Transition from high-level Pi to low-level MCU development
- **BLE Communication**: Understanding wireless protocol stack and data exchange
- **TI Ecosystem**: Learning Code Composer Studio and SimpleLink SDK
- **Debugging Skills**: Using UART and Putty for embedded debugging
- **Mobile Integration**: Interfacing with nRF Connect for testing and debugging
- **Device-to-Device**: Wireless communication between embedded devices
- **MAC Addressing**: Identifying and connecting specific BLE devices
