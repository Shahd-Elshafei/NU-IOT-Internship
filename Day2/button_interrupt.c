#include <gpiod.h>
#include <stdio.h>
#include <time.h>
#include <unistd.h>

#define CONSUMER "debounce_toggle"
#define BUTTON_PIN 17
#define LED_PIN 27
#define DEBOUNCE_MS 200 // 200 milliseconds debounce window

// Helper function to get current system time in milliseconds
long long get_time_ms(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (long long)ts.tv_sec * 1000 + (ts.tv_nsec / 1000000);
}

int main(void) {
    struct gpiod_chip *chip;
    struct gpiod_line *btn_line;
    struct gpiod_line *led_line;
    struct gpiod_line_event event;
    
    long long last_press_time = 0;
    int led_state = 0;

    // 1. Open the GPIO chip (GPIO chip 0 is default on most Pis)
    chip = gpiod_chip_open_by_number(0);
    if (!chip) {
        perror("Failed to open GPIO chip");
        return 1;
    }

    // 2. Configure the LED pin as a standard output
    led_line = gpiod_chip_get_line(chip, LED_PIN);
    gpiod_line_request_output(led_line, CONSUMER, led_state);

    // 3. Configure the Button pin for Falling Edge Interrupts
    btn_line = gpiod_chip_get_line(chip, BUTTON_PIN);
    gpiod_line_request_falling_edge_events(btn_line, CONSUMER);

    printf("System active. Press the button to toggle the LED...\n");

    // 4. Main Event Loop
    while (1) {
        // Blocks here absorbing 0% CPU until a physical edge is detected
        if (gpiod_line_event_wait(btn_line, NULL) > 0) {
            
            // Read the event to clear the event queue buffer
            gpiod_line_event_read(btn_line, &event);
            
            // Get the exact time of this trigger
            long long current_time = get_time_ms();

            // Calculate how much time passed since the last VALID press
            if (current_time - last_press_time > DEBOUNCE_MS) {
                
                // Toggle the state variable (0 becomes 1, 1 becomes 0)
                led_state = !led_state;
                gpiod_line_set_value(led_line, led_state);
                
                printf("Valid press detected! LED turned %s\n", led_state ? "ON" : "OFF");

                // Update the last valid timestamp checkpoint
                last_press_time = current_time;
            } else {
                // If it triggered too quickly, it's just noisy contact bouncing
                printf("[Ignored] Button bounce filtered.\n");
            }
        }
    }

    // Clean up hardware resources (unreachable here but good practice)
    gpiod_line_release(btn_line);
    gpiod_line_release(led_line);
    gpiod_chip_close(chip);
    return 0;
}
