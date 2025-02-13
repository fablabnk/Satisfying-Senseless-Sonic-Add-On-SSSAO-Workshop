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

// NVIC (Nested Vectored Interrupt Controller) macros and function declarations
#ifndef __CH32V00X_MISC_H
#define __CH32V00X_MISC_H

#ifdef __cplusplus
 extern "C" {
#endif

#include <ch32v00x.h>

/* CSR_INTSYSCR_INEST_definition */
#define INTSYSCR_INEST_NoEN   0x00   /* interrupt nesting disable(CSR-0x804 bit1 = 0) */
#define INTSYSCR_INEST_EN     0x01   /* interrupt nesting enable(CSR-0x804 bit1 = 1) */

/* Check the configuration of CSR(0x804) in the startup file(.S)
*   interrupt nesting enable(CSR-0x804 bit1 = 1)
*     priority - bit[7] - Preemption Priority
*                bit[6] - Sub priority
*                bit[5:0] - Reserve
*   interrupt nesting disable(CSR-0x804 bit1 = 0)
*     priority - bit[7:6] - Sub priority
*                bit[5:0] - Reserve
*/

#ifndef INTSYSCR_INEST
#define INTSYSCR_INEST   INTSYSCR_INEST_EN
#endif

/* NVIC Init Structure definition
 *   interrupt nesting enable(CSR-0x804 bit1 = 1)
 *     NVIC_IRQChannelPreemptionPriority - range from 0 to 1.
 *     NVIC_IRQChannelSubPriority - range from 0 to 1.
 *
 *   interrupt nesting disable(CSR-0x804 bit1 = 0)
 *     NVIC_IRQChannelPreemptionPriority - range is 0.
 *     NVIC_IRQChannelSubPriority - range from 0 to 3.
 *
 */
typedef struct
{
  uint8_t NVIC_IRQChannel;
  uint8_t NVIC_IRQChannelPreemptionPriority;
  uint8_t NVIC_IRQChannelSubPriority;
  FunctionalState NVIC_IRQChannelCmd;
} NVIC_InitTypeDef;

/* Preemption_Priority_Group */
#if (INTSYSCR_INEST == INTSYSCR_INEST_NoEN)
#define NVIC_PriorityGroup_0           ((uint32_t)0x00) /* interrupt nesting enable(CSR-0x804 bit1 = 1) */
#else
#define NVIC_PriorityGroup_1           ((uint32_t)0x01) /* interrupt nesting disable(CSR-0x804 bit1 = 0) */
#endif


void NVIC_PriorityGroupConfig(uint32_t NVIC_PriorityGroup);
void NVIC_Init(NVIC_InitTypeDef* NVIC_InitStruct);

#ifdef __cplusplus
}
#endif

#endif /* __CH32V00x_MISC_H */

