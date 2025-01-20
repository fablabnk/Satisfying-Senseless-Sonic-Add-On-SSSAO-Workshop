#include "ch32v00x.h"

#define MOTOR_PIN GPIO_Pin_2
#define POT_PIN   GPIO_Pin_1
#define BUTTON_PIN GPIO_Pin_3

void ADC_Config(void);
void TIM1_PWM_Config(void);
void GPIO_Config(void);
uint16_t ADC_Read(void);
uint8_t Button_Read(void);

int main(void)
{
    SystemInit();
    ADC_Config();
    TIM1_PWM_Config();
    GPIO_Config();

    while(1)
    {
        uint16_t potValue = ADC_Read();
        uint16_t motorSpeed = potValue * 100 / 4095; // Scale to 0-100%
        
        if(Button_Read() == 0) // Button is pressed (active low)
        {
            TIM_SetCompare2(TIM1, motorSpeed);
        }
        else
        {
            TIM_SetCompare2(TIM1, 0); // Turn off motor
        }
    }
}

void ADC_Config(void)
{
    // Configure ADC for potentiometer reading
}

void TIM1_PWM_Config(void)
{
    // Configure Timer1 for PWM output
}

void GPIO_Config(void)
{
    GPIO_InitTypeDef GPIO_InitStructure;

    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);

    // Configure button pin as input with pull-up
    GPIO_InitStructure.GPIO_Pin = BUTTON_PIN;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;
    GPIO_Init(GPIOA, &GPIO_InitStructure);
}

uint16_t ADC_Read(void)
{
    // Read ADC value
    return ADC_GetConversionValue(ADC1);
}

uint8_t Button_Read(void)
{
    return GPIO_ReadInputDataBit(GPIOA, BUTTON_PIN);
}

