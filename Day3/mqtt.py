"""
mqtt.py

Handles all MQTT communication with Adafruit IO.

Responsibilities:
    - Receives sensor readings from the sensor process.
    - Publishes sensor data to Adafruit IO.
    - Subscribes to LED control feeds.
    - Sends LED commands to the LED process.
"""

import os
import paho.mqtt.client as mqtt


def mqtt_process(distance_queue, led_queue):
    """
    MQTT process.

    Args:
        distance_queue:
            Queue used to receive distance measurements from
            the sensor process.

        led_queue:
            Queue used to send LED commands to the LED process.
    """

    # Read Adafruit IO credentials
    username = os.getenv("IO_USERNAME")
    key = os.getenv("IO_KEY")

    if username is None or key is None:
        raise RuntimeError(
            "IO_USERNAME or IO_KEY environment variable is not set."
        )

    # Feed names
    DISTANCE_FEED = "dist"
    LED1_FEED = "led1"

    # ---------------------------------------------------------
    # MQTT Callback Functions
    # ---------------------------------------------------------

    def on_connect(client, userdata, flags, rc):

        if rc == 0:

            print("MQTT process connected.")

            # Subscribe to the LED control feed
            client.subscribe(f"{username}/feeds/{LED1_FEED}")

        else:

            print(f"MQTT connection failed. Error code = {rc}")

    def on_message(client, userdata, msg):

        # Get feed name from topic
        feed_name = msg.topic.split("/")[-1]

        # Decode payload
        value = msg.payload.decode()

        print(f"[MQTT] {feed_name} = {value}")

        # Forward LED commands to the LED process
        if feed_name == LED1_FEED:
            led_queue.put(value)

    # ---------------------------------------------------------
    # MQTT Client
    # ---------------------------------------------------------

    client = mqtt.Client()

    client.username_pw_set(
        username=username,
        password=key
    )

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(
        "io.adafruit.com",
        1883,
        60
    )

    client.loop_start()

    print("MQTT process started.")

    try:

        while True:

            # Wait for a new sensor reading
            distance = distance_queue.get()

            print(f"[MQTT] Publishing: {distance:.2f} cm")

            # Publish to Adafruit IO
            client.publish(
                f"{username}/feeds/{DISTANCE_FEED}",
                distance
            )

    except KeyboardInterrupt:

        print("MQTT process stopped.")

        client.loop_stop()
        client.disconnect()
