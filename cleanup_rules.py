#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 09:45:18 2019

@author: frederik
"""

from scipy import *

#from functions import *
#from atomic_functions import *
#from binary_operations import *


#A=Id(Id(Cos))


def cleanup(F,Module):
#    if not Module == funcions:
    if not (Module.__name__ == "__main__" or Module.__name__ == "functions"):
    
            raise ValueError("Calling module must be functions.py or __main__")

    
    A = F._Function__F1
    B = F._Function__F2
    Op = F.Operation()
    
    
    if type(A)==Module.Constant and type(B) == Module.Constant:
        return Module.Constant(Op.Operation()(A.Number(),B.Number()))
    
    if type(A)==Module.Identity and Op == Module.Call:
        return B
    
    
    if type(B)==Module.Identity and Op == Module.Call:
        return A
    
    if Op == Module.TrueDiv:
        return A*(B**-1)
    
    if Op == Module.Pow and type(B)==Module.Constant:
        return Module.Power(B.Number())(A)
    
    
    if Op == Module.Pow and type(A)==Module.Constant:
        return Module.Exponential(A.Number())(B)
    
    
    if type(A)==Module.Constant:
        if A.Number()==0:
            if Op == Module.Add:
                return B
            if Op == Module.Mul:
                return A
            if Op == Module.Pow:
                return Module.Constant(1)
            if Op == Module.TrueDiv:
                return Module.Constant(Inf)
        elif A.Number()==1:

            if Op==Module.Mul:
                return B
            if Op==Module.Pow:
                return B
            

    return F
    
    
#B=ConstantOperation(A)