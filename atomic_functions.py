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

# =============================================================================
# Function class 
# =============================================================================

class Function():
    def __init__(self,F1,F2,Op):
        
        self.__F1 = F1
        self.__F2 = F2
        self.__Op = Op

        self.__Depth = max(F1.Depth(),F2.Depth())+1
        
        self.__Atomic = False

        self.__Function = None
        
        self.__bases__=(Function,)
        
        self.Compile()
        
        self.__StringMethod= Op.CombineStringMethods(F1.StringMethod(),F2.StringMethod())
        self.__StringMethodDefined = bool(F1.StringMethodDefined()*F2.StringMethodDefined())
        
        self.__DerivativeDefined = bool(F1.DerivativeDefined()*F2.DerivativeDefined())
    def Depth(self):
        return self.__Depth
    
    def Operation(self):
        return self.__Op
    
    def IsAtomic(self):
        return self.__Atomic 

    def Compile(self):
        """ Generate callable function """
        if self.IsAtomic():
            f=self.__F1.F()
        
        else:
            
            Op = self.__Op
            F1 = self.__F1
            F2 = self.__F2
            
            f1 = F1.F()
            f2 = F2.F()
            
            f = Op(f1,f2)
        
        self.__Function = f
        self.__Compiled = True
        
    def IsCompiled(self):
        return self.__Compiled 
    
    def F(self):
        """ Return callable function """
        if not self.IsCompiled():
            self.Compile()
            
        return self.__Function
 
# =============================================================================
# String representation
# =============================================================================
    def StringMethod(self):
        if self.StringMethodDefined():
            return self.__StringMethod
        else:
            raise ValueError("String name for function is not defined")

    def StringMethodDefined(self):
        return self.__StringMethodDefined
    
    def __repr__(self):
        return("function f(x) = "+self._Function__StringMethod('x'))
        
    def __str__(self):
        return(self._Function__StringMethod('x'))   
        
        
# =============================================================================
# Derivative 
# =============================================================================
    def DerivativeDefined(self):
        return self.__DerivativeDefined
    def Derivative(self,index = None):
        """ Take derivative. If index is specified, take derivative wrt Index'th entry"""
        
        if not self.DerivativeDefined():
            raise ValueError("Derivative of function is not defined")
            
            
        F1 = self.__F1
        F2 = self.__F2
        Op = self.__Op
        
        if Op == Call :
            Out = F1.Derivative(index = index)(F2)*F2.Derivative(index = index)
            
        if Op == Mul:
            Out = F1.Derivative(index = index)*F2 + F2.Derivative(index = index) * F1
            
        if Op == Add:
            Out = F1.Derivative(index = index) + F2.Derivative(index = index)
            
        if Op == Sub:
            Out = F1.Derivative(index = index) - F2.Derivative(index = index)
            
        if Op == TrueDiv:
            Out = F1.Derivative(index = index)/F2 - (F1*F2.Derivative(index = index))/(F2**2)
            
        if Op == Pow :
            if type(F2)==Constant:
                N = F2.Number()
                
                Out = N*F1**(N-1)
                
            else:
                Out = (F1**F2)*(F2.Derivative(index = index)*Log(F1)+F1.Derivative(index = index)*F2/F1)
            
        return Out
    
    
# =============================================================================
#     Numeric methods:
# =============================================================================
    def __call__(self,Arg):

        if not self.IsCompiled():
            self.Compile()
            
        if isinstance(Arg,Number) or type(Arg)==ndarray:
            return self.__Function(Arg)
        
        elif type(Arg)==Constant:
            return Constant(self.__Function(Arg.Number()))
        
        elif Function in Arg.__bases__:
            Out = Function(self,Arg,Call)

            return Out
        else:
            raise ValueError("Argument must be number or Function")
            
    def __mul__(self,Arg):
        if isinstance(Arg,Number):
            Arg = Constant(Arg)        

        if type(Arg)==Constant:  
            if Arg.Number()==1:
                return self
                
            if Arg.Number()==0:
                return Arg
            
            if type(self)==Constant:
                Nout = Arg.Number()*self.Number()
                return Constant(Nout)
            
            else:
                pass
            
        if type(self)==Constant:
            if self.Number()==1:
                return Arg
            if self.Number()==0:
                return self
            
                            
                
        if not self.IsCompiled():
             self.Compile()
            
        Out = Function(self,Arg,Mul)
        return Out 
        

            
            

                
    def __rmul__(self,Arg):
        return self*Arg
    
    def __add__(self,Arg):
        if isinstance(Arg,Number):
            Arg = Constant(Arg)
            
        if type(Arg)==Constant:
            if Arg.Number()==0:
                return self
            
            elif type(self)==Constant:
                return Constant(self.Number()+Arg.Number())
        
        if type(self)==Constant:
            if self.Number()==0:
                return Arg
            

            
        if not self.IsCompiled():
            self.Compile()
                        
        Out = Function(self,Arg,Add)
        return Out 

    def __radd__(self,Arg):
        return self + Arg
    
    def __sub__(self,Arg):
        if isinstance(Arg,Number):
            Arg = Constant(Arg)
            
        if type(Arg)==Constant:
            if Arg.Number()==0:
                return self
            
            elif type(self)==Constant:
                return Constant(self.Number()-Arg.Number())
        
        if type(self)==Constant:
            if self.Number()==0:
                return -1*Arg
        
        if not self.IsCompiled():
            self.Compile()
               
        Out = Function(self,Arg,Sub)
        return Out 
    
    def __rsub__(self,Arg):
        return self - Arg    


    
    def __truediv__(self,Arg):
        if isinstance(Arg,Number):
            Arg = Constant(Arg)        

        if type(Arg)==Constant:  
            if Arg.Number()==1:
                return self
                
            if Arg.Number()==0:
                raise ZeroDivisionError("division by zero")
            
            if type(self)==Constant:
                Nout = self.Number()/Arg.Number()
                return Constant(Nout)
            
            else:
                pass
            
        if type(self)==Constant:
            if self.Number()==0:
                return self
            
                            
                
        if not self.IsCompiled():
             self.Compile()
            
        Out = Function(self,Arg,TrueDiv)
        
        
        return Out 
    
    def __rtruediv__(self,Arg):
        if not self.IsCompiled():
            self.Compile()
            
        if isinstance(Arg,Number):
            Arg = Constant(Arg)

                
        return Arg / self 
                

        
    def __pow__(self,Arg):
        if isinstance(Arg,Number):
            Arg = Constant(Arg)
            
        if type(Arg)==Constant:
            if Arg.Number()==0:
                return Constant(1)
            
            elif type(self)==Constant:
                return Constant(self.Number()**Arg.Number())
        
        

        if type(self)==Constant:
            if self.Number()==1:
                return self
            

            
        if not self.IsCompiled():
            self.Compile()
            

                
        Out = Function(self,Arg,Pow)
        return Out 
    

    def __rpow__(self,Arg):
        if not self.IsCompiled():
            self.Compile()
            
        if isinstance(Arg,Number):
            Arg = Constant(Arg)

                
        Out = Arg**self
        return Out
    

        
class AtomicFunction(Function):
    
    def __init__(self,f):
    
        self._Function__F1 = f
        self._Function__F2 = None
        self._Function__Op = None

        self._Function__Depth = 1
        
        self._Function__Atomic = True 
        
        self._Function__Compiled = True
        
        self._Function__Function = f
        
        self.__bases__=(AtomicFunction,Function)
 
        self._Function__StringMethod = None
        self._Function__StringMethodDefined = False
        
        self.__Derivative = None
        
        self._Function__DerivativeDefined = False
        
        
        
    def SetStringMethod(self,StringMethod):
        self._Function__StringMethod = StringMethod
        self._Function__StringMethodDefined = True
        
    def Derivative(self,index=None):
        """Derivative. If speicified, take wrt entry Index"""

        if self._Function__DerivativeDefined:
            return self.__Derivative
        else:
            raise ValueError(f"Derivative of function f(x)={self} not specified. Use SetDerivative to define the derivative")
            
    def SetDerivative(self,Value):
        self.__Derivative = Value
        self._Function__DerivativeDefined = True
        
    
    
    def Compile(self):
        raise ValueError("Atomic functions are already compiled")
    
 
        
class Constant(AtomicFunction):
    def __init__(self,N):
        self.__bases__=(Constant,AtomicFunction,Function)        
        def f(x):
            return N
        
        self.__Number = N
        

        
        AtomicFunction.__init__(self,f)
 
        def SM(x):
            return f"{N}"
        self.SetStringMethod(SM)
        
        self._Function__DerivativeDefined=True
        self._AtomicFunction__Derivative = None
        
        
        # Specify derivative 
  
    def Derivative(self,index=None):
        return Constant(0)
    
    
    def Number(self):
        return self.__Number
   
    
    

class Entry(AtomicFunction):
    """Picks nth entry from input vector"""
    def __init__(self,Index,Name=None):
        self.__bases__=(Entry,AtomicFunction,Function)        

        if not (type(Index)==int or type(Index)==tuple):
            raise ValueError("Argument must be tuple of integers or integer")
            
        def f(x):
            return x[Index]
        
        AtomicFunction.__init__(self,f)
        

        
        if type(Index)==int:
            Index = (Index,)
        self.__Index = Index
        
        if Name==None:
                
            def SM(x):
                String = f"{Index[0]}"
    
                for n in Index[1:]:
                    String+=f",{n}"
                return f"x[{String}]"
        else:
            def SM(x):
                return Name
            
            
        
        self.SetStringMethod(SM)
                
        self._Function__DerivativeDefined=True 
        
    def Derivative(self,index=None):
        
        if index ==None:
            raise ValueError("index must be specified, when taking the derivative of Entry class")
        
        if type(index)==int:
            index = (index,)
        if index == self.__Index:
            return Constant(1)
            
        else:
            return Constant(0)
        
        
Zero = Constant(0)            
        
        
X = AtomicFunction(Id)
Cos = AtomicFunction(cos)
Sin = AtomicFunction(sin)
Exp = AtomicFunction(exp)
Log = AtomicFunction(log)

def square(x):
    return x**2
def Id(x):
    return x
def SqSt(x):
    return f"({x})^2"
def IdSt(x):
    return f"{x}"#def Constant(n):
def LogSt(x):
    return f"log({x})"
def CosSt(x):
    return f"cos({x})"
def SinSt(x):
    return f"sin({x})"
def ExpSt(x):
    return f"e^({x})"




Sin.SetStringMethod(SinSt)
Cos.SetStringMethod(CosSt)
Exp.SetStringMethod(ExpSt)

Sin.SetDerivative(Cos)
Cos.SetDerivative(Sin)
Exp.SetDerivative(Exp)

#    def g(x):
#        return n
#    
#    return AtomicFunction(Constant)


S = AtomicFunction(square)




X.SetStringMethod(IdSt)
X.SetDerivative(1)

S.SetStringMethod(SqSt)
S.SetDerivative(2*X)


Log.SetDerivative(1/X)
Log.SetStringMethod(LogSt)

