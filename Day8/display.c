/*
 * Copyright (c) 2018-2022, Texas Instruments Incorporated
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * *  Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *
 * *  Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * *  Neither the name of Texas Instruments Incorporated nor the names of
 *    its contributors may be used to endorse or promote products derived
 *    from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 * THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
 * CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
 * OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 * WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
 * OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
 * EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

/*
 *  ======== display.c ========
 */
#include <stdint.h>
#include <unistd.h>

/* TI-Drivers Header files */
#include <ti/drivers/GPIO.h>

/* Display Header files */
#include <ti/display/Display.h>
#include <ti/display/DisplayUart2.h>
#include <ti/display/DisplayExt.h>
#include <ti/display/AnsiColor.h>

/* Driver Configuration */
#include "ti_drivers_config.h"

/* Example GrLib image */
#include "splash_image.h"

/*
 *  ======== mainThread ========
 */
void *mainThread(void *arg0)
{
    unsigned int ledPinValue;
    unsigned int loopCount = 0;

    GPIO_init();
    Display_init();

    GPIO_write(CONFIG_GPIO_LED_0, CONFIG_GPIO_LED_ON);

    /* Initialize display and try to open both UART and LCD types of display. */
    Display_Params params;
    Display_Params_init(&params);
    params.lineClearMode = DISPLAY_CLEAR_BOTH;

    /*
     * Open both an available LCD display and an UART display.
     * Whether the open call is successful depends on what is present in the
     * Display_config[] array of the driver configuration file.
     */
    //Display_Handle hLcd    = Display_open(Display_Type_LCD, &params);
    Display_Handle hSerial = Display_open(Display_Type_UART, &params);

    uint8_t temperature = 25;
    uint8_t humidity = 60;


    /* Loop forever, alternating LED state and Display output. */
    while (1)
    {
        ledPinValue = GPIO_read(CONFIG_GPIO_LED_0);
        
        

        Display_printf(hSerial, 0, 0, "%d,%d", temperature, humidity);

        temperature++;
        humidity++;

        if (temperature > 35)
            temperature = 25;

        if (humidity > 70)
            humidity = 60;

        sleep(1);

        /* Toggle LED */
        GPIO_toggle(CONFIG_GPIO_LED_0);
    }
}
