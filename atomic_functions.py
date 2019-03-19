#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 09:33:44 2019

@author: frederik

Solve classical equations of motion using Scipy
"""

import numbers
from scipy import *
from .functions import *

#import functions

               
        



# =============================================================================
# Special functions 
# =============================================================================


# Define functions first
Cos = AtomicFunction(cos)
Sin = AtomicFunction(sin)
Exp = AtomicFunction(exp)
Log = AtomicFunction(log)

# ... Gamma(x), Tanh(x) ... 

### Set properties 

# Cos
def CosSt(x):
    return f"cos({x})"
Cos.SetStringMethod(CosSt)
Cos.SetDerivative(Sin)

# Sin
def SinSt(x):
    return f"sin({x})"
Sin.SetStringMethod(SinSt)
Sin.SetDerivative(Cos)

# Exp
def ExpSt(x):
    return f"e^({x})"
Exp.SetStringMethod(ExpSt)
Exp.SetDerivative(Exp)

# Log 
def LogSt(x):
    return f"log({x})"
Log.SetDerivative(Power(-1))
Log.SetStringMethod(LogSt)

