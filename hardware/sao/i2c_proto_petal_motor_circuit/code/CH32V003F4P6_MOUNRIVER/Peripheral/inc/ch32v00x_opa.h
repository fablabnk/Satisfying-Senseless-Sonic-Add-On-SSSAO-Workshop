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

// OPA (Operational Amplifier) macros and function declarations

#ifndef __CH32V00x_OPA_H
#define __CH32V00x_OPA_H

#ifdef __cplusplus
extern "C" {
#endif

#include "ch32v00x.h"

/* OPA PSEL enumeration */
typedef enum
{
    CHP0 = 0,
    CHP1
} OPA_PSEL_TypeDef;

/* OPA NSEL enumeration */
typedef enum
{
    CHN0 = 0,
    CHN1
} OPA_NSEL_TypeDef;


/* OPA Init Structure definition */
typedef struct
{
    OPA_PSEL_TypeDef PSEL;    /* Specifies the positive channel of OPA */
    OPA_NSEL_TypeDef NSEL;    /* Specifies the negative channel of OPA */
} OPA_InitTypeDef;

void OPA_DeInit(void);
void OPA_Init(OPA_InitTypeDef *OPA_InitStruct);
void OPA_StructInit(OPA_InitTypeDef *OPA_InitStruct);
void OPA_Cmd(FunctionalState NewState);

#ifdef __cplusplus
}
#endif

#endif
