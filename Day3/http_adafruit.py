import os
import requests
import sqlite3
import time
from datetime import datetime
from gpiozero import DistanceSensor, LED

# -----------------------------------------------------------------------------
# Adafruit IO Communication Class
# -----------------------------------------------------------------------------
class AdafruitIO:
    """
    A simple wrapper for communicating with Adafruit IO using HTTP requests.

    This class authenticates using the environment variables:
        - IO_USERNAME
        - IO_KEY

    It provides helper functions to:
        - Upload data to a feed (POST)
        - Read the latest value from a feed (GET)
    """

    def __init__(self):
        """
        Initializes the Adafruit IO connection.

        Reads the username and API key from the operating system
        environment variables and prepares the HTTP headers and
        base URL used for all requests.
        """

        # Read Adafruit IO credentials from environment variables
        self.username = os.getenv("IO_USERNAME")
        self.key = os.getenv("IO_KEY")

        # Ensure both credentials exist before continuing
        if self.username is None or self.key is None:
            raise RuntimeError(
                "IO_USERNAME or IO_KEY environment variable is not set."
            )

        # HTTP request headers required by Adafruit IO
        self.headers = {
            "X-AIO-Key": self.key,
            "Content-Type": "application/json"
        }

        # Base URL for all feed requests
        self.base_url = f"https://io.adafruit.com/api/v2/{self.username}/feeds"


    def post(self, feed_name, value):
        """
        Uploads a value to the specified Adafruit IO feed.

        Args:
            feed_name (str): Name (key) of the feed.
            value: Value to upload.

        Returns:
            bool:
                True if the upload succeeded.
                False otherwise.
        """

        # Build the URL for the selected feed
        url = f"{self.base_url}/{feed_name}/data"

        # Send the HTTP POST request
        response = requests.post(
            url,
            json={"value": value},
            headers=self.headers
        )

        # Check if the upload succeeded
        if response.status_code == 200:
            return True

        # Print the error returned by the server
        print(f"POST Error ({response.status_code}): {response.text}")
        return False


    def get(self, feed_name):
        """
        Retrieves the latest value stored in the specified Adafruit IO feed.

        Args:
            feed_name (str): Name (key) of the feed.

        Returns:
            str | None:
                Latest feed value if successful.
                None if the request fails.
        """

        # Build the URL for the latest feed value
        url = f"{self.base_url}/{feed_name}/data/last"

        # Send the HTTP GET request
        response = requests.get(
            url,
            headers=self.headers
        )

        # Return the latest feed value
        if response.status_code == 200:
            return response.json()["value"]

        # Print the error returned by the server
        print(f"GET Error ({response.status_code}): {response.text}")
        return None


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
    
    led1 = LED(17)       # BCM GPIO17

    # Create an Adafruit IO communication object
    aio = AdafruitIO()

    # Feed names used by this application
    DISTANCE_FEED = "dist"
    LED1_FEED = "led1"

    print("Starting ADAfruit monitoring. Press Ctrl+C to stop.")

    try:
        while True:

            # Read sensor
            distance_cm = sensor.distance * 100

            # Upload distance
            aio.post(DISTANCE_FEED, distance_cm)

            # Read LED state from Adafruit IO
            led1_value = aio.get(LED1_FEED)

            if led1_value is not None:
                if led1_value.upper() in ("1", "ON", "TRUE"):
                    led1.on()
                else:
                    led1.off()

            print(
                f"Distance: {distance_cm:.2f} cm | "
                f"LED1 Feed: {led1_value}"
            )

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nMonitoring stopped safely.")
