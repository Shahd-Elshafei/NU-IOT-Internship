#include <gpiod.h>
#include <stdio.h>
#include <unistd.h>

// Define the chip and physical GPIO pin number (BCM layout)
#define CHIP_NAME "gpiochip0" 
#define LINE_NUMBER 17        // Physical Pin 11 (GPIO17)

void delay_ms(int ms) {
    usleep(ms * 1000); // Converts milliseconds to microseconds
}

int main(void) {
    struct gpiod_chip *chip;
    struct gpiod_line *line;
    int req;

    // 1. Open the specific GPIO controller chip
    chip = gpiod_chip_open_by_name(CHIP_NAME);
    if (!chip) {
        perror("Open chip failed");
        return 1;
    }

    // 2. Locate the specific pin line on that chip
    line = gpiod_chip_get_line(chip, LINE_NUMBER);
    if (!line) {
        perror("Get line failed");
        gpiod_chip_close(chip);
        return 1;
    }

    // 3. Request the line to act as an OUTPUT pin
    req = gpiod_line_request_output(line, "blink_consumer", 0);
    if (req < 0) {
        perror("Request line as output failed");
        gpiod_chip_close(chip);
        return 1;
    }

    printf("Blinking LED on GPIO %d. Press Ctrl+C to exit...\n", LINE_NUMBER);

    // 4. Infinite Loop to toggle the LED high and low
    while (1) {
        gpiod_line_set_value(line, 1); // Turn LED ON
        delay_ms(500);                // Wait 0.5 seconds (500,000 microseconds)

        gpiod_line_set_value(line, 0); // Turn LED OFF
        delay_ms(500);                // Wait 0.5 seconds
    }

    // 5. Cleanup system resources (Unreachable in an infinite loop, but good practice)
    gpiod_line_release(line);
    gpiod_chip_close(chip);
    return 0;
}
