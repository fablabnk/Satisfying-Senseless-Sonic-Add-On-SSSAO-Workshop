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

// MCU debug-mode macros and function declarations

#ifndef __CH32V00x_DBGMCU_H
#define __CH32V00x_DBGMCU_H

#ifdef __cplusplus
extern "C" {
#endif

#include <ch32v00x.h>

/* CFGR0 Register */
#define DBGMCU_IWDG_STOP             ((uint32_t)0x00000001)
#define DBGMCU_WWDG_STOP             ((uint32_t)0x00000002)
#define DBGMCU_TIM1_STOP             ((uint32_t)0x00000010)
#define DBGMCU_TIM2_STOP             ((uint32_t)0x00000020)

uint32_t DBGMCU_GetREVID(void);
uint32_t DBGMCU_GetDEVID(void);
uint32_t __get_DEBUG_CR(void);
void __set_DEBUG_CR(uint32_t value);
void DBGMCU_Config(uint32_t DBGMCU_Periph, FunctionalState NewState);
uint32_t DBGMCU_GetCHIPID( void );
#ifdef __cplusplus
}
#endif

#endif /* __CH32V00x_DBGMCU_H */
