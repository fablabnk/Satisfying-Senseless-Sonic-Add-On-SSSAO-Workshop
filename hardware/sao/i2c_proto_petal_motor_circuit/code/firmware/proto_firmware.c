/*
 * Example for using ADC with polling
 * 03-27-2023 E. Brombaugh
 */

#include "ch32v003fun.h"
#include "ch32v003_GPIO_branchless.h"
#include <stdio.h>

//#define AUTO_RELOAD 1024
#define AUTO_RELOAD 32768

/*
 * initialize adc for polling
 */
void adc_init( void )
{
	// ADCCLK = 24 MHz => RCC_ADCPRE = 0: divide by 2
	// RCC - Reset & Clock Control
	// CFGR0 - Register to configure system clocks and prescalers
	// bits 11-15 hold the ADC prescaler config 
		//-> setting them to 0 puts them into default 
		//-> updates on every tick of the system clock
		//-> increase value to adjust frequency
	RCC->CFGR0 &= ~(0x1F<<11);
	
	// Enable GPIOD and ADC
	// APB2PCENR -> APB2 (BUS) Peripheral Clock Enable Register
	RCC->APB2PCENR |= RCC_APB2Periph_GPIOD | RCC_APB2Periph_ADC1;
	
	// PD4 is analog input chl 7
	// GPIO Port D
	// CFGLR - Configuration Register Low - for pins D0 to D7
	// Bits [16:19] for PD4
	// &= ~(0xf<<(4*4)) - clears all 4 bits of PD4, setting it to Analog Input Mode
	GPIOD->CFGLR &= ~(0xf<<(4*4));	// CNF = 00: Analog, MODE = 00: Input
	
	// Reset the ADC to init all regs
	// APB2 Peripheral Reset Register
	RCC->APB2PRSTR |= RCC_APB2Periph_ADC1; // Overwrites all of ADC1s and clears all corresponding registers
	RCC->APB2PRSTR &= ~RCC_APB2Periph_ADC1; // back to normal operation
	
	// Set up single conversion on chl 7
	ADC1->RSQR1 = 0;	// enable single conversion (only PD4)
	ADC1->RSQR2 = 0;	// clear multi channel sequence
	ADC1->RSQR3 = 7;	// 0-9 for 8 ext inputs and two internals 
		// -> sets ADC channel 7 aka. PD4 aka. A7 as the input source for the ADC
	
	// set sampling time for chl 7
	// SAMPTR2 sample rate register for channel 0-9
	// SAMPTR1 for channel 9 - 17 WHY???? AAhhhhhh
	ADC1->SAMPTR2 &= ~(ADC_SMP0<<(3*7)); // resetting sample rate for channel 7
	ADC1->SAMPTR2 |= 7<<(3*7);	// 0:7 => 3/9/15/30/43/57/73/241 cycles 
	// -> sets 3bit val for channel 7 to 21 -> maximum sample rate 241
		
	// turn on ADC and set rule group to sw trig (software trigger // not Analog Input triggered)
	ADC1->CTLR2 |= ADC_ADON | ADC_EXTSEL;
	
	// Reset calibration
	ADC1->CTLR2 |= ADC_RSTCAL;
	while(ADC1->CTLR2 & ADC_RSTCAL);
	
	// Calibrate with the adjusted controoler CTRL2
	ADC1->CTLR2 |= ADC_CAL;
	while(ADC1->CTLR2 & ADC_CAL);
	
	// should be ready for SW conversion now
}

/*
 * start conversion, wait and return result
 */
uint16_t adc_get( void )
{
	// start sw conversion (auto clears)
	// sat software activated adc read to on
	ADC1->CTLR2 |= ADC_SWSTART;
	
	// wait for conversion complete
	// run until (Status Read?)reaches End of cycle
	while(!(ADC1->STATR & ADC_EOC));
	
	// get result
	// read result from register DATAread
	return ADC1->RDATAR;
}


/*
 * initialize TIM1 for PWM
 */
void t1pwm_init( void )
{
	// Enable GPIOC, GPIOD and TIM1
	// APB2PCENR -> APB2 (BUS) Peripheral Clock Enable Register
	RCC->APB2PCENR |= 	RCC_APB2Periph_GPIOD | RCC_APB2Periph_GPIOC |
						RCC_APB2Periph_TIM1;
	
	// PD0 is using T1CH1N (Timer 1, Channel 1), 10MHz Output alt func, push-pull
	// CFGLR - Configuration Register Low - for pins Do to D7
	GPIOD->CFGLR &= ~(0xf<<(4*0)); // clear all bits of PD0
	GPIOD->CFGLR |= (GPIO_Speed_10MHz | GPIO_CNF_OUT_PP_AF)<<(4*0); 
	
	// PC4 is T1CH4(Can use Tim1 and Tim2), 10MHz Output alt func, push-pull
	//	-> Diagram says Channel 3. Why T1CH4???
	GPIOC->CFGLR &= ~(0xf<<(4*4));
	GPIOC->CFGLR |= (GPIO_Speed_10MHz | GPIO_CNF_OUT_PP_AF)<<(4*4);
		
	// Reset TIM1 to init all regs
	RCC->APB2PRSTR |= RCC_APB2Periph_TIM1;
	RCC->APB2PRSTR &= ~RCC_APB2Periph_TIM1;
	
	// CTLR1: default is up, events generated, edge align
	// SMCFGR: default clk input is CK_INT
	
	// Prescaler 
	TIM1->PSC = 0x0000; //Default prescaler option (every system tick)
	
	// Auto Reload - sets period
	TIM1->ATRLR = AUTO_RELOAD; // Timer counts to that value before restart
	
	// Reload immediately
	// SWEVGR - Software Event Generation Register
	TIM1->SWEVGR |= TIM_UG; // Update Generation - reloads the timer's prescaler, counter, and registers.
	
	// Enable CH1N output, positive pol
	// CCER - CaptureCompare Enable Reg
	TIM1->CCER |= TIM_CC1NE | TIM_CC1NP;
	
	// Enable CH4 output, positive pol
	TIM1->CCER |= TIM_CC4E | TIM_CC4NP;
	
	// CH1 Mode is output, PWM1 (CC1S = 00, OC1M = 110)
	// CHCTLR1 - Channel Control Reg 1 -> specifies behavior of the output pin
	TIM1->CHCTLR1 |= TIM_OC1M_2 | TIM_OC1M_1;
	
	// CH2 Mode is output, PWM1 (CC1S = 00, OC1M = 110)
	TIM1->CHCTLR2 |= TIM_OC4M_2 | TIM_OC4M_1;

	//What about Channel 3? 
	//What happens if CHCTLR2 is not set? No Output?
	
	// Set the Capture Compare Register value to 50% initially
	// CHxCVR - Capture/Compare Value Register
	// Sets the duty cycle compared to TIM1->ATRLR
	TIM1->CH1CVR = 128;
	TIM1->CH4CVR = 128;
	
	// Enable TIM1 outputs
	// BDTR - Break Dead Time Reg
	// Defines behaviour of Timer
	TIM1->BDTR |= TIM_MOE; // MOE - Main Output Enabled
	
	// Enable TIM1
	TIM1->CTLR1 |= TIM_CEN; // CEN - CounterENabled
}

void	gpio_init()
{
	// Enable GPIOC
	RCC->APB2PCENR |= RCC_APB2Periph_GPIOC;

	// GPIO C0 Push-Pull Input
	GPIOC->CFGLR &= ~(0xf<<(4*0));
	GPIOC->CFGLR |= (GPIO_Speed_10MHz | GPIO_CNF_IN_PUPD)<<(4*0);

	// GPIO D6 Push-Pull Input
	GPIOD->CFGLR &= ~(0xf<<(4*6));
	GPIOD->CFGLR |= (GPIO_Speed_10MHz | GPIO_CNF_IN_PUPD)<<(4*6);

	// GPIO C4 Push-Pull
	GPIOC->CFGLR &= ~(0xf<<(4*4));
	GPIOC->CFGLR |= (GPIO_Speed_10MHz | GPIO_CNF_OUT_PP)<<(4*4);

	// GPIO C5 Push-Pull
	GPIOC->CFGLR &= ~(0xf<<(4*5));
	GPIOC->CFGLR |= (GPIO_Speed_10MHz | GPIO_CNF_OUT_PP)<<(4*5);

	// GPIO C6 Push-Pull
	GPIOC->CFGLR &= ~(0xf<<(4*6));
	GPIOC->CFGLR |= (GPIO_Speed_10MHz | GPIO_CNF_OUT_PP)<<(4*6);

	// GPIO D0 Push-Pull
	GPIOD->CFGLR &= ~(0xf<<(4*0));
	GPIOD->CFGLR |= (GPIO_Speed_10MHz | GPIO_CNF_OUT_PP)<<(4*0);

}
/*
 * set timer channel PW
 */
void t1pwm_setpw(uint8_t chl, uint16_t width)
{
	switch(chl&3)
	{
		case 0: TIM1->CH1CVR = width; break;
		case 1: TIM1->CH2CVR = width; break;
		case 2: TIM1->CH3CVR = width; break;
		case 3: TIM1->CH4CVR = width; break;
	}
}

/*
 * force output (used for testing / debug)
 */
void t1pwm_force(uint8_t chl, uint8_t val)
{
	uint16_t temp;
	
	chl &= 3; // clears bits higher than channel 3
	
	if(chl < 2) // Defines which ChannelControlrRegister is responsible
	{
		temp = TIM1->CHCTLR1; // Copy Curretn State of Control Reg
		temp &= ~(TIM_OC1M<<(8*chl)); // Clear output compare Mode
		temp |= (TIM_OC1M_2 | (val?TIM_OC1M_0:0))<<(8*chl); //Rewrite output compare mode depending on 'val'
		TIM1->CHCTLR1 = temp; // Overwrite register, force output
	}
	else
	{
		chl &= 1;
		temp = TIM1->CHCTLR2;
		temp &= ~(TIM_OC1M<<(8*chl));
		temp |= (TIM_OC1M_2 | (val?TIM_OC1M_0:0))<<(8*chl);
		TIM1->CHCTLR2 = temp;
	}
}

void	trigger_solenoid(int *s_triggered)
{
	//Turn on Solenoid
	GPIOC->BSHR = 1<<(5);
	Delay_Ms(500);
	//Turn off Solenoid
	GPIOC->BCR = (1<<(5));
	*s_triggered = 1;
}

/*
 * entry
 */
int main()
{
	int	button_pressed_c0;
	int	button_pressed_d6;
	int width;
	int pwm;
	int s_triggered = 0;

	SystemInit();
	Delay_Ms( 100 );

	adc_init();
	gpio_init();
	t1pwm_init();
	t1pwm_setpw(3, 0);
	t1pwm_setpw(0, 0);

	while(1)
	{
		width = adc_get();
		pwm = width*AUTO_RELOAD/1024;
		// INDR - Input Data Regsister
        button_pressed_c0 = !(GPIOC->INDR & (1 << 0));  // Active-low butto
        button_pressed_d6 = !(GPIOD->INDR & (1 << 6));  // Active-low butto
		if (button_pressed_c0 || button_pressed_d6)
		{
			// Bit Set/Reset Register
			GPIOC->BSHR = 1<<(6);
			//GPIOC->BCR = (1<<(4));
			//GPIOD->BSHR = 1<<(0);
			// Activate PWM
			//t1pwm_setpw(3, pwm);
			t1pwm_setpw(3, pwm);
			t1pwm_setpw(0, pwm);
			if (0 && !s_triggered)
				trigger_solenoid(&s_triggered);
		}
		else
		{
			// Bit CLEAR Register
			//GPIOD->BCR = (1<<(0));
			GPIOC->BCR = (1<<(6));
			// Deactivate PWM
			t1pwm_setpw(0, 0);
			t1pwm_setpw(3, 0);
			s_triggered = 0;
		}
		Delay_Ms(10);
	}
}
