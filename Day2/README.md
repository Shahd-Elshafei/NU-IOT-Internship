# Day 2 - Interrupts, Debouncing, Ultrasonic Sensor & Data Logging


## Tasks Completed

### Task 1: Interrupt-Driven Button with Debouncing
- Implemented hardware interrupts using falling edge detection instead of CPU polling
- Configured GPIO pin to trigger interrupts on button press (falling edge from HIGH to LOW)
- Added 200ms software debounce window to filter out mechanical switch bouncing
- LED toggles ON/OFF on each valid button press
- Program blocks on `gpiod_line_event_wait()` consuming 0% CPU while waiting for events
- Hardware: Button on GPIO 17, LED on GPIO 27

### Task 2: Ultrasonic Sensor Integration (HC-SR04)
- Integrated HC-SR04 ultrasonic distance sensor for object detection
- Sensor emits ultrasonic waves and measures echo return time
- Distance calculated using: Distance = (Speed of Sound × Time) / 2
- Readings taken every 2 seconds using gpiozero library
- Values converted from meters to centimeters for readability
- Hardware: TRIG → GPIO 23, ECHO → GPIO 24, VCC → 5V, GND → GND

### Task 3: SQLite Database Integration
- Created persistent data storage system for sensor readings
- Database schema with auto-incrementing ID, timestamp (YYYY-MM-DD HH:MM:SS), and distance
- Automatic table creation on first run
- Each reading logged with precise timestamp

### Task 4: Data Visualization
- Created Python script using matplotlib and pandas for data visualization
- Line plot showing distance readings over time with markers
- Generated summary statistics: total readings, min, max, and average distance
- Professional plotting with grid, labels, and rotated timestamps

---

## Key Learnings

- **Interrupt Handling:** Understanding how hardware interrupts improve efficiency by eliminating CPU polling
- **Debouncing:** Practical implementation of software debouncing to filter mechanical switch noise
- **Edge Detection:** Configuring GPIO pins for falling edge detection
- **Ultrasonic Sensing:** Understanding sound wave propagation for distance measurement
- **Data Persistence:** Using SQLite for reliable data storage in embedded systems
- **Data Visualization:** Creating professional plots for data analysis using matplotlib
- **Python Integration:** Combining hardware control with data processing and visualization

---

## Tools & Technologies

- **Languages:** C, Python
- **Libraries:** libgpiod, gpiozero, sqlite3, matplotlib, pandas, datetime
- **Hardware:** Raspberry Pi 4, HC-SR04 Ultrasonic Sensor, LED, Button, Resistors
- **Database:** SQLite3
- **Build Tools:** GCC, Python3, pip

---

## Files Created

| File | Description |
|------|-------------|
| `button_interrupt.c` | Interrupt-driven button with debouncing |
| `ultrasonic_sensor.py` | Distance measurement with SQLite logging |
| `visualize_data.py` | Data visualization script |
| `sensor_data.db` | SQLite database (auto-generated) |

---

## Commands Used

**Compilation (C):**
```bash
gcc -o button_interrupt button_interrupt.c -lgpiod
