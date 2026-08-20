import os
import time
import paho.mqtt.client as mqtt
from gpiozero import DistanceSensor, LED


# -----------------------------------------------------------------------------
# Adafruit IO MQTT Communication Class
# -----------------------------------------------------------------------------
class AdafruitIO:
    """
    A simple wrapper for communicating with Adafruit IO using MQTT.

    This class authenticates using the environment variables:
        - IO_USERNAME
        - IO_KEY

    It provides helper functions to:
        - Publish data to a feed.
        - Subscribe to feeds.
        - Notify the application whenever a subscribed feed changes.
    """

    def __init__(self):
        """
        Initializes the MQTT client and connects to the Adafruit IO broker.
        """

        # Read Adafruit IO credentials from environment variables
        self.username = os.getenv("IO_USERNAME")
        self.key = os.getenv("IO_KEY")

        # Ensure both credentials exist before continuing
        if self.username is None or self.key is None:
            raise RuntimeError(
                "IO_USERNAME or IO_KEY environment variable is not set."
            )

        # User callback executed whenever a subscribed feed changes.
        # The application can replace this function with its own handler.
        self.feed_changed = None

        # Create the MQTT client
        self.client = mqtt.Client()

        # Set the MQTT username and password
        self.client.username_pw_set(
            username=self.username,
            password=self.key
        )

        # Register MQTT callback functions
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # Connect to the Adafruit IO MQTT broker
        self.client.connect(
            "io.adafruit.com",
            1883,
            60
        )

        # Start the MQTT background thread
        self.client.loop_start()

    def publish(self, feed_name, value):
        """
        Publishes a value to the specified Adafruit IO feed.

        Args:
            feed_name (str):
                Feed key.

            value:
                Value to publish.
        """

        topic = f"{self.username}/feeds/{feed_name}"
        self.client.publish(topic, value)

    def subscribe(self, feed_name):
        """
        Subscribes to the specified Adafruit IO feed.

        Args:
            feed_name (str):
                Feed key.
        """

        topic = f"{self.username}/feeds/{feed_name}"
        self.client.subscribe(topic)

    def on_connect(self, client, userdata, flags, rc):
        """
        Callback executed whenever the MQTT client connects.
        """

        if rc == 0:
            print("Connected to Adafruit IO MQTT Broker")
        else:
            print(f"Connection failed. Error code = {rc}")

    def on_message(self, client, userdata, msg):
        """
        Callback executed whenever a subscribed feed receives new data.

        The received feed name and value are forwarded to the user-defined
        callback function if one has been registered.
        """

        # Extract the feed name from the MQTT topic
        feed_name = msg.topic.split("/")[-1]

        # Decode the received payload
        value = msg.payload.decode()

        # Notify the application
        if self.feed_changed is not None:
            self.feed_changed(feed_name, value)


# -----------------------------------------------------------------------------
# Main Execution Loop
# -----------------------------------------------------------------------------
if __name__ == "__main__":

    # Initialize the HC-SR04 ultrasonic distance sensor
    sensor = DistanceSensor(
        echo=23,
        trigger=24,
        max_distance=2,
        threshold_distance=0.1
    )

    # Initialize LED connected to BCM GPIO17
    led1 = LED(17)

    # Create the Adafruit IO MQTT object
    aio = AdafruitIO()

    # Feed names
    DISTANCE_FEED = "dist"
    LED1_FEED = "led1"

    # -------------------------------------------------------------------------
    # MQTT Feed Callback
    # -------------------------------------------------------------------------
    def mqtt_feed_changed(feed_name, value):
        """
        Application callback executed whenever a subscribed MQTT feed changes.

        Args:
            feed_name (str):
                Feed that generated the event.

            value (str):
                New value received from the feed.
        """

        print(f"MQTT Received -> {feed_name}: {value}")

        if feed_name == LED1_FEED:

            if value.upper() in ("1", "ON", "TRUE"):
                led1.on()
            else:
                led1.off()

    # Register the callback
    aio.feed_changed = mqtt_feed_changed

    # Subscribe to the LED control feed
    aio.subscribe(LED1_FEED)

    print("Starting Adafruit IO MQTT monitoring. Press Ctrl+C to stop.")

    try:

        while True:

            # Read distance in centimeters
            distance_cm = sensor.distance * 100

            # Publish the distance measurement
            aio.publish(DISTANCE_FEED, distance_cm)

            print(f"Distance: {distance_cm:.2f} cm")

            # Wait before taking the next measurement
            time.sleep(1)

    except KeyboardInterrupt:

        print("\nMonitoring stopped safely.")

        aio.client.loop_stop()
        aio.client.disconnect()
