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

// EXTI (external interrupts) macros and function definitions

#include <ch32v00x_exti.h>

/* No interrupt selected */
#define EXTI_LINENONE    ((uint32_t)0x00000)

/*********************************************************************
 * @fn      EXTI_DeInit
 *
 * @brief   Deinitializes the EXTI peripheral registers to their default
 *        reset values.
 *
 * @return  none.
 */
void EXTI_DeInit(void)
{
    EXTI->INTENR = 0x00000000;
    EXTI->EVENR = 0x00000000;
    EXTI->RTENR = 0x00000000;
    EXTI->FTENR = 0x00000000;
    EXTI->INTFR = 0x000FFFFF;
}

/*********************************************************************
 * @fn      EXTI_Init
 *
 * @brief   Initializes the EXTI peripheral according to the specified
 *        parameters in the EXTI_InitStruct.
 *
 * @param   EXTI_InitStruct: pointer to a EXTI_InitTypeDef structure
 *
 * @return  none.
 */
void EXTI_Init(EXTI_InitTypeDef *EXTI_InitStruct)
{
    uint32_t tmp = 0;

    tmp = (uint32_t)EXTI_BASE;
    if(EXTI_InitStruct->EXTI_LineCmd != DISABLE)
    {
        EXTI->INTENR &= ~EXTI_InitStruct->EXTI_Line;
        EXTI->EVENR &= ~EXTI_InitStruct->EXTI_Line;
        tmp += EXTI_InitStruct->EXTI_Mode;
        *(__IO uint32_t *)tmp |= EXTI_InitStruct->EXTI_Line;
        EXTI->RTENR &= ~EXTI_InitStruct->EXTI_Line;
        EXTI->FTENR &= ~EXTI_InitStruct->EXTI_Line;
        if(EXTI_InitStruct->EXTI_Trigger == EXTI_Trigger_Rising_Falling)
        {
            EXTI->RTENR |= EXTI_InitStruct->EXTI_Line;
            EXTI->FTENR |= EXTI_InitStruct->EXTI_Line;
        }
        else
        {
            tmp = (uint32_t)EXTI_BASE;
            tmp += EXTI_InitStruct->EXTI_Trigger;
            *(__IO uint32_t *)tmp |= EXTI_InitStruct->EXTI_Line;
        }
    }
    else
    {
        tmp += EXTI_InitStruct->EXTI_Mode;
        *(__IO uint32_t *)tmp &= ~EXTI_InitStruct->EXTI_Line;
    }
}

/*********************************************************************
 * @fn      EXTI_StructInit
 *
 * @brief   Fills each EXTI_InitStruct member with its reset value.
 *
 * @param   EXTI_InitStruct - pointer to a EXTI_InitTypeDef structure
 *
 * @return  none.
 */
void EXTI_StructInit(EXTI_InitTypeDef *EXTI_InitStruct)
{
    EXTI_InitStruct->EXTI_Line = EXTI_LINENONE;
    EXTI_InitStruct->EXTI_Mode = EXTI_Mode_Interrupt;
    EXTI_InitStruct->EXTI_Trigger = EXTI_Trigger_Falling;
    EXTI_InitStruct->EXTI_LineCmd = DISABLE;
}

/*********************************************************************
 * @fn      EXTI_GenerateSWInterrupt
 *
 * @brief   Generates a Software interrupt.
 *
 * @param   EXTI_Line - specifies the EXTI lines to be enabled or disabled.
 *
 * @return  none.
 */
void EXTI_GenerateSWInterrupt(uint32_t EXTI_Line)
{
    EXTI->SWIEVR |= EXTI_Line;
}

/*********************************************************************
 * @fn      EXTI_GetFlagStatus
 *
 * @brief   Checks whether the specified EXTI line flag is set or not.
 *
 * @param   EXTI_Line - specifies the EXTI lines to be enabled or disabled.
 *
 * @return  The new state of EXTI_Line (SET or RESET).
 */
FlagStatus EXTI_GetFlagStatus(uint32_t EXTI_Line)
{
    FlagStatus bitstatus = RESET;
    if((EXTI->INTFR & EXTI_Line) != (uint32_t)RESET)
    {
        bitstatus = SET;
    }
    else
    {
        bitstatus = RESET;
    }
    return bitstatus;
}

/*********************************************************************
 * @fn      EXTI_ClearFlag
 *
 * @brief   Clears the EXTI's line pending flags.
 *
 * @param   EXTI_Line - specifies the EXTI lines to be enabled or disabled.
 *
 * @return  None
 */
void EXTI_ClearFlag(uint32_t EXTI_Line)
{
    EXTI->INTFR = EXTI_Line;
}

/*********************************************************************
 * @fn      EXTI_GetITStatus
 *
 * @brief   Checks whether the specified EXTI line is asserted or not.
 *
 * @param   EXTI_Line - specifies the EXTI lines to be enabled or disabled.
 *
 * @return  The new state of EXTI_Line (SET or RESET).
 */
ITStatus EXTI_GetITStatus(uint32_t EXTI_Line)
{
    ITStatus bitstatus = RESET;
    uint32_t enablestatus = 0;

    enablestatus = EXTI->INTENR & EXTI_Line;
    if(((EXTI->INTFR & EXTI_Line) != (uint32_t)RESET) && (enablestatus != (uint32_t)RESET))
    {
        bitstatus = SET;
    }
    else
    {
        bitstatus = RESET;
    }
    return bitstatus;
}

/*********************************************************************
 * @fn      EXTI_ClearITPendingBit
 *
 * @brief   Clears the EXTI's line pending bits.
 *
 * @param   EXTI_Line - specifies the EXTI lines to be enabled or disabled.
 *
 * @return  none
 */
void EXTI_ClearITPendingBit(uint32_t EXTI_Line)
{
    EXTI->INTFR = EXTI_Line;
}
