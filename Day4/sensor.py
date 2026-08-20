"""
sensor.py

Reads the HC-SR04 ultrasonic sensor and sends the measured
distance to the MQTT process through an IPC queue.
"""

import time
from gpiozero import DistanceSensor


def sensor_process(distance_queue):
    """
    Sensor process.

    Continuously reads the HC-SR04 distance sensor and places the
    measured distance (in centimeters) into the IPC queue.

    Args:
        distance_queue:
            Queue used to send distance measurements to the MQTT process.
    """

    # Initialize the HC-SR04 ultrasonic sensor
    sensor = DistanceSensor(
        echo=23,
        trigger=24,
        max_distance=2,
        threshold_distance=0.1
    )

    print("Sensor process started.")

    try:

        while True:

            # Read distance in centimeters
            distance_cm = sensor.distance * 100

            # Send the distance to the MQTT process
            distance_queue.put(distance_cm)

            print(f"[Sensor] Distance = {distance_cm:.2f} cm")

            # Read once every second
            time.sleep(1)

    except KeyboardInterrupt:

        print("Sensor process stopped.")
