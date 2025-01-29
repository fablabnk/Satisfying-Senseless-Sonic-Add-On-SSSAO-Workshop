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

// declarations of convenience functions for mcu peripherals setup

#ifndef __SETUP_H
# define __SETUP_H

/**
 * @brief Sets up system clock with HSI @48MHs, disables HSE and GPIO remapping enables APB2
 */
void setup_mcu(void);

/**
 * @brief Sets up port and pin
 * 
 * @param port pointer, ie GPIOA
 * @param pin index macro, ie GPIO_Pin_0
 * @param mode pin mode, ie GPIO_Mode_Out_PP
 * @param speed one of macros, ie GPIO_Speed_30MHz
 */
void setup_gpio(GPIO_TypeDef *port, uint16_t pin, GPIOMode_TypeDef mode, GPIOSpeed_TypeDef speed);

/**
 * @brief Sets up GPIO external interrupts (for key press)
 * 
 * @param port pointer, ie GPIOA
 * @param pin index macro, ie GPIO_Pin_0
 * @param line Specifies the EXTI line to be enabled
 * @param trigger signal active edge, ie EXTI_Trigger_Falling
 */
void setup_gpio_interrupt(uint8_t port, uint8_t pin, uint32_t line, EXTITrigger_TypeDef trigger);

/**
 * @brief Sets up timer (for PWM or timer interrupts)
 * 
 * @param TIM pointer to timer, ie TIM2
 * @param period max value of counter in timer, value in range[0x0000, 0xFFFF)
 * @param prescaler value in range[0x0000, 0xFFFF)
 * @param mode counter mode, ie TIM_CounterMode_Up
 */
void setup_timer(TIM_TypeDef *TIM, uint16_t period, uint16_t prescaler, uint16_t mode);

/**
 * @brief Sets up timer interrupt
 * 
 * @param TIM pointer to timer, ie TIM2
 */
void setup_timer_interrupt(TIM_TypeDef *TIM);

/**
 * @brief Sets up pwm
 * 
 * @param TIM pointer to timer, ie TIM1
 * @param ch index of timer channel in range[0..4)
 * @param pulse_len lentgth of the pulse in range[0x0-0xFFFF)
 * @param mode timer mode, one of TIM_OCMode_
 * @param output_state whether to forward PWM signal to an actual pin, ie TIM_OutputState_Enable
 * @param polarity polarity of the signal, ie TIM_OCPolarity_High
 */
void setup_pwm(TIM_TypeDef *TIM, uint8_t ch, uint16_t pulse_len, uint16_t mode, uint16_t output_state, uint16_t polarity);

#endif // __SETUP_H
