"""
main.py

Main application that starts all system processes.

Processes:
    1. Sensor Process
    2. MQTT Process
    3. LED Process
"""

from multiprocessing import Process, Queue

from sensor import sensor_process
from mqtt import mqtt_process
from led import led_process


def main():
    """
    Creates the IPC queues and starts all application processes.
    """

    # Queue used to send sensor readings to the MQTT process
    distance_queue = Queue()

    # Queue used to send LED commands from MQTT to the LED process
    led_queue = Queue()

    # Create the processes
    sensor = Process(
        target=sensor_process,
        args=(distance_queue,)
    )

    mqtt = Process(
        target=mqtt_process,
        args=(distance_queue, led_queue)
    )

    led = Process(
        target=led_process,
        args=(led_queue,)
    )

    # Start all processes
    sensor.start()
    mqtt.start()
    led.start()

    try:
        # Wait until all processes terminate
        sensor.join()
        mqtt.join()
        led.join()

    except KeyboardInterrupt:

        print("\nStopping all processes...")

        sensor.terminate()
        mqtt.terminate()
        led.terminate()

        sensor.join()
        mqtt.join()
        led.join()

        print("System stopped successfully.")


if __name__ == "__main__":
    main()
