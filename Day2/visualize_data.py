import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

DB_FILE = "sensor_data.db"

def fetch_data():
    """Fetch all data from the database."""
    conn = sqlite3.connect(DB_FILE)
    query = "SELECT timestamp, distance_cm FROM distance_logs ORDER BY id"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def visualize_data():
    """Create a plot of distance readings over time."""
    df = fetch_data()
    
    if df.empty:
        print("No data found in database.")
        return
    
    # Convert timestamp strings to datetime objects
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.plot(df['timestamp'], df['distance_cm'], marker='o', linestyle='-', linewidth=2)
    plt.title('Ultrasonic Sensor Distance Readings Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Distance (cm)')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Show statistics
    print(f"Total readings: {len(df)}")
    print(f"Min distance: {df['distance_cm'].min():.2f} cm")
    print(f"Max distance: {df['distance_cm'].max():.2f} cm")
    print(f"Average distance: {df['distance_cm'].mean():.2f} cm")
    
    plt.show()

if __name__ == "__main__":
    visualize_data()
