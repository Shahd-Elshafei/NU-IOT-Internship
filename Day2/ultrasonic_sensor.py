import sqlite3
import time
from datetime import datetime
from gpiozero import DistanceSensor

# 1. Hardware Configuration
sensor = DistanceSensor(echo=24, trigger=23)

# 2. Database Configuration
DB_FILE = "sensor_data.db"

def init_database():
    """Creates the database and table if they do not exist already."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create table with an auto-incrementing ID, timestamp, and distance float
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS distance_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            distance_cm REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def log_reading(distance_cm):
    """Inserts a single sensor reading into the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('''
        INSERT INTO distance_logs (timestamp, distance_cm)
        VALUES (?, ?)
    ''', (current_time, distance_cm))
    
    conn.commit()
    conn.close()
    print(f"[{current_time}] Logged: {distance_cm:.2f} cm")

# 3. Main Execution Loop
if __name__ == "__main__":
    print("Initializing Database...")
    init_database()
    
    print("Starting sensor monitoring. Press Ctrl+C to stop.")
    try:
        while True:
            # gpiozero returns distance in meters, multiply by 100 for cm
            distance_cm = sensor.distance * 100
            
            # Log data to SQLite
            log_reading(distance_cm)
            
            # Wait 2 seconds before the next reading
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped safely.")
