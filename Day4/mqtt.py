"""
mqtt.py

Handles all MQTT communication with the HiveMQ Cloud broker and
stores sensor data in InfluxDB Cloud.

Responsibilities:
    - Receives sensor readings from the sensor process.
    - Publishes sensor data to the HiveMQ Cloud broker.
    - Stores sensor readings in InfluxDB Cloud.
    - Subscribes to the LED control topic.
    - Sends LED commands to the LED process.
"""

import os
import ssl

import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS


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

    # ---------------------------------------------------------
    # Read MQTT broker configuration from environment variables
    # ---------------------------------------------------------

    host = os.getenv("MQTT_HOST")
    port = int(os.getenv("MQTT_PORT", "8883"))
    username = os.getenv("MQTT_USERNAME")
    password = os.getenv("MQTT_PASSWORD")

    if (
        host is None or
        username is None or
        password is None
    ):
        raise RuntimeError(
            "MQTT broker environment variables are not set."
        )

    # ---------------------------------------------------------
    # Read InfluxDB Cloud configuration
    # ---------------------------------------------------------

    influx_url = os.getenv("INFLUX_URL")
    influx_token = os.getenv("INFLUX_TOKEN")
    influx_org = os.getenv("INFLUX_ORG")
    influx_bucket = os.getenv("INFLUX_BUCKET")

    if (
        influx_url is None or
        influx_token is None or
        influx_org is None or
        influx_bucket is None
    ):
        raise RuntimeError(
            "InfluxDB environment variables are not set."
        )

    # ---------------------------------------------------------
    # MQTT Topics
    # ---------------------------------------------------------

    # Topic used to publish distance measurements
    DISTANCE_TOPIC = "sensor/distance"

    # Topic used to receive LED commands
    LED_TOPIC = "led/control"

    # ---------------------------------------------------------
    # Create InfluxDB Client
    # ---------------------------------------------------------

    # Create a connection to the InfluxDB Cloud database
    influx_client = InfluxDBClient(
        url=influx_url,
        token=influx_token,
        org=influx_org
    )

    # Synchronous writes ensure data is written immediately
    write_api = influx_client.write_api(
        write_options=SYNCHRONOUS
    )

    # ---------------------------------------------------------
    # MQTT Callback Functions
    # ---------------------------------------------------------

    def on_connect(client, userdata, flags, rc):
        """
        Called automatically when the MQTT client connects
        to the broker.
        """

        if rc == 0:

            print("MQTT process connected to HiveMQ Cloud.")

            # Subscribe to the LED control topic
            client.subscribe(LED_TOPIC)

            print(f"Subscribed to '{LED_TOPIC}'")

        else:

            print(f"MQTT connection failed. Error code = {rc}")

    def on_message(client, userdata, msg):
        """
        Called automatically whenever a subscribed MQTT
        message is received.
        """

        # Decode the received MQTT payload
        value = msg.payload.decode()

        print(f"[MQTT] {msg.topic} = {value}")

        # Forward LED commands to the LED process
        if msg.topic == LED_TOPIC:
            led_queue.put(value)

    # ---------------------------------------------------------
    # Create MQTT Client
    # ---------------------------------------------------------

    client = mqtt.Client()

    # Configure MQTT authentication
    client.username_pw_set(
        username=username,
        password=password
    )

    # Enable TLS encryption
    client.tls_set(
        tls_version=ssl.PROTOCOL_TLS_CLIENT
    )

    # Register callback functions
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to HiveMQ Cloud
    client.connect(
        host,
        port,
        60
    )

    # Start the MQTT background thread
    client.loop_start()

    print("MQTT process started.")
    print(f"Broker = {host}:{port}")
    print(f"Username = {username}")

    try:

        while True:

            # Wait until a new sensor measurement is received
            distance = distance_queue.get()

            print(f"[MQTT] Publishing: {distance:.2f} cm")

            # -------------------------------------------------
            # Publish distance to the MQTT broker
            # -------------------------------------------------

            client.publish(
                DISTANCE_TOPIC,
                distance
            )

            # -------------------------------------------------
            # Store the same measurement in InfluxDB
            # -------------------------------------------------

            point = (
                Point("distance")
                .field("value", float(distance))
            )

            write_api.write(
                bucket=influx_bucket,
                org=influx_org,
                record=point
            )

            print("[InfluxDB] Distance stored.")

    except KeyboardInterrupt:

        print("MQTT process stopped.")

    finally:

        # Stop MQTT communication
        client.loop_stop()
        client.disconnect()

        # Close the InfluxDB connection
        influx_client.close()
