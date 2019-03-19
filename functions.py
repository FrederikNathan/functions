#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 09:33:44 2019

@author: frederik

Solve classical equations of motion using Scipy
"""

from numbers import *
from scipy import *
#from matplotlib.pyplot import *
from .binary_operations import *
#from . import cleanup_rules 
#from .cleanup_rules import *
import sys 

Module = sys.modules[__name__]

# =============================================================================
# Function class 
# =============================================================================

class Function():
    def __init__(self,F1,F2,Op):
        
        F1.CleanUp()
        F2.CleanUp()
        
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
        

        self.CleanUp()

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
    
    def F1(self):
        return self.__F1
    
    def F2(self):
        return self.__F2 
 
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
# Cleaning up method        
# =============================================================================
#        
    def CleanUp(self):
        
        x = self
        y=0
        
        while y!=x:
            y=x
            x=cleanup(x)

        self.__dict__.update(x.__dict__)
        self.__class__ = x.__class__
        
  
              
        
        
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
        
        elif type(self)==Constant:
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
    """ Constant function f(x) = const. """
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
    """Picks nth entry from input vector: f(x) = x[n]. 
    X can be multidimensional
    """
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
        
class Identity(AtomicFunction):
    def __init__(self):
        self.__bases__=(Entry,AtomicFunction,Function)        

        def f(x):
            return x
        
        AtomicFunction.__init__(self,f)

        
        def SM(x):
            return f"{x}"
        
        self.SetStringMethod(SM)
                
        self._Function__DerivativeDefined=True 
        
    def Derivative(self,index=None):
        
        return Constant(1)


class Power(AtomicFunction):
    """ Power function f(x) = x^p """
    def __init__(self,power):
        if not isinstance(power,Number):
            raise ValueError("Power must be a number")
    
        self.__bases__=(Entry,AtomicFunction,Function)        
        self.__power = power
        def f(x):
            return x**power
        
        AtomicFunction.__init__(self,f)
        
        def SM(x):
            return  f"{x}^{power}"
            
        self.SetStringMethod(SM)
        
        self._Function__DerivativeDefined=True
            
    def Derivative(self,index=None):
        return Constant(self.power())*Power(self.power()-1)
            
    def power(self):
        return self.__power
    
class Exponential(AtomicFunction):
    """ Exponential function f(x) = a^x """
    
    def __init__(self,exponent):
        if not isinstance(exponent,Number):
            raise ValueError("exponent must be a number")
        self.__bases__=(Entry,AtomicFunction,Function)        
        self.__exponent = exponent
        def f(x):
            return exponent ** x 
        
        AtomicFunction.__init__(self,f)
        
        def SM(x):
            return  f"{exponent}^{x}"
            
        self.SetStringMethod(SM)
        
        self._Function__DerivativeDefined=True
        
    def Derivative(self,index=None):
        return log(self.exponent())*self
    
    def exponent(self):
        return self.__exponent

    
# =============================================================================
# Cleanup rules 
# =============================================================================

def cleanup(F):
#    if not Module == funcions:
#    if not (Module.__name__ == "__main__" or Module.__name__ == "functions"):
#    
    # =============================================================================
    # Simplification of atomic functions
    # =============================================================================

    if type(F)==Power:
        if F.power()==1:
            return Identity()

        
    A = F._Function__F1
    B = F._Function__F2
    Op = F.Operation()
    

        
    if type(A)==Constant and type(B) == Constant:
        return Constant(Op.Operation()(A.Number(),B.Number()))
    
    if type(A)==Identity and Op == Call:
        return B
    
    
    if type(B)==Identity and Op == Call:
        return A
    
    if Op == TrueDiv:
        return A*(B**-1)
    
    if Op == Pow and type(B)==Constant:
        return Power(B.Number())(A)
    
    
    if Op == Pow and type(A)==Constant:
        return Exponential(A.Number())(B)
    
    
    if type(A)==Constant:
        if A.Number()==0:
            if Op == Add:
                return B
            if Op == Mul:
                return A
            if Op == Pow:
                return Constant(1)
            if Op == TrueDiv:
                return Constant(inf)
        elif A.Number()==1:

            if Op==Mul:
                return B
            if Op==Pow:
                return B
            
    

            
    return F
    
Id= Identity()