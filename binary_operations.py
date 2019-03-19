#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 09:33:44 2019

@author: frederik

Solve classical equations of motion using Scipy
"""

import numbers
from scipy import *
from matplotlib.pyplot import *

# =============================================================================
# Binary operation
# =============================================================================
# order: term, factor, application
class Binary():
    def __init__(self,Operation,StringMethodCombiner):
        
        self.__Op = Operation
        

        self.__StringMethodCombiner = StringMethodCombiner
        

        # Construct string representation       
        def S1(x):
            return f"f{x}"
        def S2(x):
            return f"g{x}"
        
        Method = self.CombineStringMethods(S1,S2)
        self.__StringRepresentation = Method("")
        
    
    def __str__(self):
        return f"Binary operation: f,g -> {self.__StringRepresentation}"
        
    def __repr__(self):
        return f"{self.__StringRepresentation}"
    
    def __call__(self,*Args):
        return self.__Op(*Args)
    
    def LeftString(self):
        return self.__LeftString
    
    def RightString(self):
        return self.__RightString
    
    def CombineStringMethods(self,F1,F2):
        return self.__StringMethodCombiner(F1,F2)
    
""" Binary operations """ 
def call(F1,F2):
    def Output(x):
        return F1(F2(x))
    
    return Output

def Scall(S1,S2):
    
    def Output(x):
        a = S2(x)
        return S1(f"({a})")
        
    return Output

def mul(F1,F2):
    def Output(x):
        return F1(x)*F2(x)
    
    return Output

def Smul(S1,S2):
    def Output(x):
       return f"({S1(x)}*{S2(x)})"
       
    return Output

def add(F1,F2):
    def Output(x):
        return F1(x)+F2(x)
    return Output

def Sadd(S1,S2):
    def Output(x):
       return f"({S1(x)}+{S2(x)})"
       
    return Output

def sub(F1,F2):
    def Output(x):
        return F1(x)-F2(x)    
    return Output
def Ssub(S1,S2):
    def Output(x):
       return f"({S1(x)}-{S2(x)})"
       
    return Output

def truediv(F1,F2):
    def Output(x):
        return F1(x)/F2(x)    
    return Output
def Struediv(S1,S2):
    def Output(x):
       return f"({S1(x)}/{S2(x)})"
       
    return Output
def power(F1,F2):
    def Output(x):
        return F1(x)**F2(x)    
    return Output
def Spower(S1,S2):
    def Output(x):
       return f"({S1(x)}^{S2(x)})"
       
    return Output

def rpower(F1,F2):
    def Output(x):
        return F1(x)**F2(x)    
    return Output
def Srpower(S1,S2):
    def Output(x):
       return f"({S2(x)}^{S1(x)})"
       
    return Output
    
    
Call        =       Binary(call,Scall)
Mul         =       Binary(mul,Smul)
Add         =       Binary(add,Sadd)
Sub         =       Binary(sub,Ssub)
TrueDiv     =       Binary(truediv,Struediv)
Pow         =       Binary(power,Spower)
RPow        =       Binary(rpower,Srpower)
