# Uploading Motor Circuit Code to CH32V003

The flashing process we now have working [here](https://github.com/Hack-a-Day/2024-Supercon-8-Add-On-Badge/tree/main/i2c_proto_petal_tutorial) can flash any pre-compiled .bin file.  So the challenge is now to write and compile a simple code example for our motor circuit. For this we can dig into the [ch32v003fun library](https://github.com/cnlohr/ch32v003fun) a bit more.

# Building and compiling a blink example

## Building the stock blink example

Let's start real basic by just seeing if we can compile the existing blink example

1. Clone the [ch32v003fun repo](https://github.com/cnlohr/ch32v003fun)
2. Open the root directory of the repo in a terminal
3. `cd ./examples/blink`
4. `make clean` - to start from scratch
5. `make` - to build and flash. flash will fail but that's ok...

```
riscv64-unknown-elf-objdump -S blink.elf > blink.lst
riscv64-unknown-elf-objcopy -O binary blink.elf blink.bin
riscv64-unknown-elf-objcopy -O ihex blink.elf blink.hex
```

Note that projects will only compile from within the ch32v003fun repo folder structure, so it's best to copy and modify folders within `/examples`. The code folders I made the the badge repo should be moved here for now to test them

## Modifying the stock blink example for the I2C Proto Petal

Our onboard LED is connected to PD0. PD0 is already used in the existing example, so all we need to do is trim it down as follows:

1. Open the root directory of the repo in a terminal
2. `cd ./examples`
3. `cp -r blink blink-petal`
4. `cd blink-petal`
5. `make clean`
6. Rename `blink.c` to `blink-petal.c`
7. Open `blink-petal.c` (here)[https://github.com/cnlohr/ch32v003fun/blob/master/examples/blink/blink.c] and prune it down to just the lines that use the PD0 pin, as follows

```
#include "ch32v003fun.h"
#include <stdio.h>

// use defines to make more meaningful names for our GPIO pins
#define PIN_1 PD0

int main()
{
	SystemInit();

	// Enable GPIOs
	funGpioInitAll();
	
	funPinMode( PIN_1,     GPIO_Speed_10MHz | GPIO_CNF_OUT_PP );

	while(1)
	{
		funDigitalWrite( PIN_1,     FUN_HIGH );
		Delay_Ms( 250 );
		funDigitalWrite( PIN_1,     FUN_LOW );
		Delay_Ms( 250 );
	}
}
```

8. Open `Makefile`, edit target to `blink-petal` and save
9. `Make`
10. Follow the process in the flash tutorial [here](https://github.com/Hack-a-Day/2024-Supercon-8-Add-On-Badge/tree/main/i2c_proto_petal_tutorial), but copy over our `blink-petal.bin` instead of their `blink.bin`

You should now see a relatively fast flash (250ms on/off)

Now we can move on to the actual circuit we'd like to make

# What Our Motor Circuit Needs

Three things:
1. Connect one side of our push button to digital pin PC0, configured to GPIO
https://github.com/cnlohr/ch32v003fun/blob/master/examples/GPIO/GPIO.c
2. Connect the wiper of our potentiometer to analog pin PD4, configured to ADC
https://github.com/cnlohr/ch32v003fun/blob/master/examples/adc_polled/adc_polled.c
3. Connect analog pin PC4, configured to output PWM, to our motor (via transistor)
https://github.com/cnlohr/ch32v003fun/tree/master/examples/tim1_pwm

# Building a GPIO Button Example (PC0)

This I got working. See `petal-GPIO` folder in `./hardware/sao/i2c_proto_petal_motor_circuit/code` for an example I made that turns on onboard PD0 LED when button is connected to C0 in pullup configuration (see Kicad schematic)

# Building an ADC Potentiometer Example (PD4)

For this I'm making a hybrid of the `adc_polled.c` and `tim1_pwm` examples. In the former, we connect an analog voltage source that varies between 0V and 3.3v to GPIO pin PD4. In the latter we fade the onboard LED on PD0 using PWM. `tim1_pwm` is trying to fade two different LEDs at different rates, so we could comment out remove the code for the non-PD0 one.

The hybrid file can be found in the `petal-adc_polled_tim1_pwm` folder. Unfortunately it doesn't work. The LED lights but doesn't respond to the turning of the potentiometer. This is perhaps because it's not scaled to 0-255 as PWM output is expecting. Can we check what values are coming in?

# Building a PWM Motor Example (PC4)

Next we can also test `tim1_pwm` but using it to drive the DC motor via PWM instead of the LED.

# Putting it All Together

Coming soon
