/* ***************************************************************************
MIT License

Copyright (c) 2025 k-off pacovali@student.42berlin.de

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*************************************************************************** */

// main

#include <ch32v00x_conf.h>
#include "setup.h"

/**
 * @brief Initial system setup
 */
void setup(void) {
    setup_mcu();                                            // enable HSI (clock) and APB2 (peripheral bus)
    setup_systick();                                        // setup System Tick
    Delay_Init();
    setup_gpio(GPIOA, GPIO_Pin_2, GPIO_Mode_AIN, GPIO_Speed_30MHz); // PA2 as analog input
    setup_gpio(GPIOD, GPIO_Pin_0, GPIO_Mode_Out_PP, GPIO_Speed_30MHz); // PD4 as analog input

        GPIO_WriteBit(GPIOD, GPIO_Pin_0, Bit_SET);
        Delay_Ms(500u);
        GPIO_WriteBit(GPIOD, GPIO_Pin_0, Bit_RESET);
        Delay_Ms(500u);

    setup_timer(TIM1, 48000u, 0u, TIM_CounterMode_Up);      // 1ms period
    setup_timer_interrupt(TIM1, TIM_TRGOSource_Update);     // enable timer interrupt for ADC sampling and set the source of trigger output
    setup_pwm(                                              // pwm initial setup
        TIM1,
        2u,
        24000u,                             // 50% duty cycle
        TIM_OCMode_PWM1,
        TIM_OutputState_Enable,
        TIM_OCPolarity_High
    );
    setup_adc(                                              // adc initial set up
        ADC1,                               // address of the ADC
        ADC_Mode_Independent,               // independent or dual mode
        DISABLE,                            // conversion in Scan (multichannels) or Single (one channel)
        DISABLE,                            // conversion is performed in Continuous or Single mode
        ADC_ExternalTrigInjecConv_T1_CC3,   // external trigger used to start conversion
        ADC_DataAlign_Right,                // ADC data alignment is left or right
        1u,                                 // 1 to 16, number of ADC channels that will be converted using the sequencer for regular channel group
        RCC_PCLK2_Div8                      // adc clock ratio compared to APB2 clock, ie RCC_PCLK2_Div8
    );
    ADC_InjectedSequencerLengthConfig(ADC1, 1);
    ADC_InjectedChannelConfig(ADC1, ADC_Channel_2, 1, ADC_SampleTime_241Cycles);  // channel number must correspond to analog input pin
    ADC_ExternalTrigInjectedConvCmd(ADC1, ENABLE);
    setup_adc_interrupt();                                  // allows to trigger an event when a new sample is ready
}

int main(void) {
    setup();
    while (1) {
        // GPIO_WriteBit(GPIOD, GPIO_Pin_0, Bit_SET);
        // Delay_Ms(500u);
        GPIO_WriteBit(GPIOD, GPIO_Pin_0, Bit_RESET);
        // Delay_Ms(500u);
    }
    return (0);
    
}


void NMI_Handler(void) __attribute__((interrupt("WCH-Interrupt-fast")));
void HardFault_Handler(void) __attribute__((interrupt("WCH-Interrupt-fast")));
void TIM2_IRQHandler(void) __attribute__((interrupt("WCH-Interrupt-fast")));
void ADC1_IRQHandler(void) __attribute__((interrupt("WCH-Interrupt-fast")));

/**
 * @brief Handles NMI exception
 */
void NMI_Handler(void) { while (1) ; }

/**
 * @brief Handles Hard Fault exception
 */
void HardFault_Handler(void) { while (1) ; }

/**
 * @brief TIM2 Interrupt Handler
 */
void TIM2_IRQHandler(void) { /* do stuff */ }

/**
 * @brief ADC1_2 Interrupt Service Function
 */
void ADC1_IRQHandler(void) {
    // injected interrupt handling
    if(ADC_GetITStatus(ADC1, ADC_IT_JEOC)) {
        const uint16_t ADC_MAX = 1024;
        uint16_t ADC_val = ADC_GetInjectedConversionValue(ADC1, ADC_InjectedChannel_1); // ADC_GetConversionValue(ADC1);
        uint16_t newCompareValue = (uint16_t)((TIM1->ATRLR + 1) * ADC_val / ADC_MAX);
        TIM_SetCompare1(TIM1, newCompareValue);
    }
    ADC_ClearITPendingBit(ADC1, ADC_IT_JEOC);

    // regular interrupt handling
    if(ADC_GetITStatus(ADC1, ADC_IT_EOC)) { /* do stuff */ }
    ADC_ClearITPendingBit(ADC1, ADC_IT_EOC);
}
