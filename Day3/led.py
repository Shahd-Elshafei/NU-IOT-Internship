"""
led.py

Receives LED control commands through an IPC queue
and controls the Raspberry Pi GPIO output.
"""

from gpiozero import LED


def led_process(led_queue):
    """
    LED process.

    Waits for LED commands from the IPC queue and updates
    the LED state accordingly.

    Args:
        led_queue:
            Queue used to receive LED commands from the MQTT process.
    """

    # Initialize the LED connected to BCM GPIO17
    led = LED(17)

    print("LED process started.")

    try:

        while True:

            # Wait for the next LED command
            value = led_queue.get()

            print(f"[LED] Received: {value}")

            # Turn the LED on or off
            if value.upper() in ("1", "ON", "TRUE"):
                led.on()
                print("[LED] ON")

            else:
                led.off()
                print("[LED] OFF")

    except KeyboardInterrupt:

        print("LED process stopped.")
