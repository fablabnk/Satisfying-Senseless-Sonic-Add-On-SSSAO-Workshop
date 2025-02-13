#include "ch32v003fun.h"
#include "ch32v003_GPIO_branchless.h"
#include <stdio.h>

#define PIN_1 PD0

int main()
{
  SystemInit();
  
  funGpioInitAll();
  funPinMode( PIN_1,     GPIO_Speed_10MHz | GPIO_CNF_OUT_PP );
	
  GPIO_port_enable(GPIO_port_C);
  GPIO_pinMode(GPIOv_from_PORT_PIN(GPIO_port_C, 0), GPIO_pinMode_I_pullUp, GPIO_Speed_In);
  
  while(1)
  {
    uint8_t button_is_pressed = !GPIO_digitalRead(GPIOv_from_PORT_PIN(GPIO_port_C, 0));
    if (button_is_pressed) {
      funDigitalWrite( PIN_1,     FUN_LOW );
    }
    else {
      funDigitalWrite( PIN_1,     FUN_HIGH );
    }
    Delay_Ms(50);
  }
}
