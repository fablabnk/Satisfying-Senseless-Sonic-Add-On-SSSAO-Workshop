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

// definitions of convenience functions for mcu peripherals setup

#include <ch32v00x_conf.h>

void setup_mcu(void) {
    	SystemInit();
		NVIC_PriorityGroupConfig(NVIC_PriorityGroup_1);
		SystemCoreClockUpdate();
		
		// Disable GPIO Alternate Functions and extrnal oscilator
		// Othewize GPIO PORT A does not work
		RCC_HSEConfig(RCC_HSE_OFF);
		GPIO_PinRemapConfig(GPIO_Remap_PA1_2, DISABLE);

		// Remapping
		RCC_APB2PeriphClockCmd(RCC_APB2Periph_AFIO, ENABLE);
}

void setup_gpio(GPIO_TypeDef *port, uint16_t pin, GPIOMode_TypeDef mode, GPIOSpeed_TypeDef speed) {
    GPIO_InitTypeDef config = { // initialize configuration
        .GPIO_Pin = pin,
        .GPIO_Speed = speed,
        .GPIO_Mode = mode
    };
    if (port == GPIOA) { // enable peripheral clock
        RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);
    } else if (port == GPIOC) {
        RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOC, ENABLE);
    } else if (port == GPIOD) {
        RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOD, ENABLE);
    }
    GPIO_Init(port, &config); // initialize port
}

void setup_gpio_interrupt(uint8_t port, uint8_t pin, uint32_t line, EXTITrigger_TypeDef trigger) {
    GPIO_EXTILineConfig(port, pin);

    EXTI_InitTypeDef gpio_exti = {
        .EXTI_Line = line,
        .EXTI_Mode = EXTI_Mode_Interrupt,
        .EXTI_Trigger = trigger,
        .EXTI_LineCmd = ENABLE,
    };
    EXTI_Init(&gpio_exti);

    NVIC_InitTypeDef gpio_nvic = {
        .NVIC_IRQChannel = EXTI7_0_IRQn,
        .NVIC_IRQChannelPreemptionPriority = 0,
        .NVIC_IRQChannelSubPriority = 1,
        .NVIC_IRQChannelCmd = ENABLE,
    };
    NVIC_Init(&gpio_nvic);
}

void setup_timer(TIM_TypeDef *TIM, uint16_t period, uint16_t prescaler, uint16_t mode) {
    if (TIM == TIM2) {
        RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM2, ENABLE);
    } else if (TIM == TIM1) {
        RCC_APB2PeriphClockCmd(RCC_APB2Periph_TIM1, ENABLE);
    }
    TIM_TimeBaseInitTypeDef TimerConfig = {
        .TIM_Prescaler = prescaler,
        .TIM_CounterMode = mode,
        .TIM_Period = period,
        .TIM_ClockDivision = TIM_CKD_DIV1,
    };
    TIM_TimeBaseInit(TIM, &TimerConfig);
}

void setup_timer_interrupt(TIM_TypeDef *TIM) {
    NVIC_InitTypeDef NVIC_InitStruct={
        .NVIC_IRQChannel = 0,
        .NVIC_IRQChannelPreemptionPriority = 1,
        .NVIC_IRQChannelSubPriority = 1,
        .NVIC_IRQChannelCmd = ENABLE
    };
    if (TIM == TIM1) {
        TIM_ITConfig(TIM, TIM_IT_Update, ENABLE);
        NVIC_InitStruct.NVIC_IRQChannel = TIM1_UP_IRQn;
    } else if (TIM == TIM2) {
        TIM_ITConfig(TIM, TIM_IT_Update, ENABLE);
        NVIC_InitStruct.NVIC_IRQChannel = TIM2_IRQn;
    }
    NVIC_Init(&NVIC_InitStruct);
}

void setup_pwm(TIM_TypeDef *TIM, uint8_t ch, uint16_t pulse_len, uint16_t mode, uint16_t output_state, uint16_t polarity) {
    TIM_OCInitTypeDef config={
        .TIM_OCMode = mode,
        .TIM_OutputState = output_state,
        .TIM_Pulse = pulse_len,
        .TIM_OCPolarity = polarity
    };

    // use function pointer array instead of if-else
    typedef void (*TIM_OCInit)(TIM_TypeDef *, TIM_OCInitTypeDef *);
    const TIM_OCInit oi[4] = {TIM_OC1Init, TIM_OC2Init,
                                    TIM_OC3Init, TIM_OC4Init};
    oi[ch](TIM, &config);
    TIM_CtrlPWMOutputs(TIM, ENABLE);

    // use function pointer array instead of if-else
    typedef void (*TIM_OCConfig)(TIM_TypeDef *, uint16_t);
    const TIM_OCConfig oc[4] = {TIM_OC1PreloadConfig,
        TIM_OC2PreloadConfig, TIM_OC3PreloadConfig, TIM_OC4PreloadConfig};
    oc[ch](TIM, TIM_OCPreload_Disable);
    TIM_ARRPreloadConfig(TIM, ENABLE);
}
