#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 09:33:44 2019

@author: frederik

Solve classical equations of motion using Scipy
"""


from scipy import *
from matplotlib.pyplot import *

## First test: Harmonic Oscillator

omega = 1
#
#class Hamiltonian():
#    def __init__(self,Function,PoissonBracketMatrix):
#            self.__Function = Function
#            self.__PB = PoissonBracketMatrix
#            self.__Nvariables = shape(PoissonBracketMatrix)[0]
#            
#    def __call__(Argument):
#        return self.__Function(Argument)
#    
#
#    def Gen_EOM(self):
#        """Return F(S,t), such that \dot S(t) = F(S,t)
#        """
#        
#        F = self.__Function
#        
#        Output=zeros((self.__Nvariables))
#        for n in range(0,self.__Nvariables):
#            for m in range(0,self.__Nvariables):
#                
#                Output[n]+=Derivative(Func,m)*self.__PB[n,m]
class BaseFunction():
    """ Abstract function""" 
    def __init__(self,Input):
        if not callable(Input):

            def Function(*Arg):
                return Input
        else:
            Function = Input
            
        self.__Func=Function


    def __mul__(self,OtherFunc):
        def OutFunc(*Arg):
            return self(x)*AddedFunc(x)
        
        return MyFunc(OutFunc)
        
    def __call__(self,*Arg):
        return self.__Func(*Arg)        
    
    def __add__(self,AddedFunc):
        def OutFunc(*Arg):
            F1 = self.__Func
            F2 = AddedFunc.GetFunction()
            return F1(*Arg)+F2(*Arg)
        
        return Function(OutFunc)
    
    def __radd__(self,X):
        return X+self
    
    def __rmul__(self,X):
        return X*self

    def GetFunction(self):
        """Return ordinary function associated with abstract function"""
    
        
        return self.__Func
    


#    def __call__(self,Argument):

        
# order: term, factor, application
class Operation():
    def __init__(self,Operation,LeftString,RightString):
        
        self.__Op = Operation
        
        self.__LeftString = LeftString
        self.__RightString = RightString 
        
    def __str__(self):
        return f"Operation: Op(f,g) = f{self.__LeftString}(g){self.__RightString}" 
    
        
    def __repr__(self):
        return self.__str__()
    
    def __call__(self,*Args):
        return self.__Op(*Args)
    
    def LeftString(self):
        return self.__LeftString
    
    def RightString(self):
        return self.__RightString
    
         


""" Binary operations """ 
def call(F1,F2):
    def Output(x):
        return F1(F2(x))
    
    return Output

Call = Operation(call,"","")



class Binary():
    def __init__(self,Operation,String):
        self.__Op= Operation

class Function():
    

    def __init__(self,*Func):
        self.__FuncList=[Func]
        self.__OperationList=[Call]
        self.__LeftString = self.LeftString()
        self.__RightString = self.RightString()

    def ReturnFunction(self):
        
        FL=self.FuncList()
        OpList=self.OperationList()
        N = len(OpList)
        
        
        def OutputFunction(x):
            return x 
        
        for n in range(0,N):
            F=FL[n]
            Op=OpList[n]
            OutputFunction=Op(F,OutputFunction)            
    
        return OutputFunction
    
    def FuncList(self):
        return self.__FuncList
    
    def OperationList(self):
        return self.__OperationList   
    
    def SetLists(self,FuncList,OpList):
        self.__FuncList=FuncList
        self.__OperationList=OpList

    def __call__(self,Arg):
        if type(Arg)==Function:
            Output=Function(ID)
            
            FL1 = Arg.FuncList()
            OL1 = Arg.OperationList()
            
            FL2 = self.FuncList()
            OL2 = self.OperationList()
            
            FL3 = FL1 + FL2 
            OL3 = OL1 + OL2 
            
            
            Output.SetLists(FL3,OL3)
            
            return Output
        
        elif type(Arg)==AtomicFunction:
            Output = Function(ID)
           
            FL1 = [Arg]
            OL1 = [Call]
            
            FL2 = self.FuncList()
            OL2 = self.OperationList()
            
            FL3 = FL1 + FL2 
            OL3 = OL1 + OL2 
          
            Output.SetLists(FL3,OL3)
            
            return Output
                                
        else:
            F=self.ReturnFunction()
            return F(Arg)
        
##        
#    def __str__(self):
#        
#        
#        
#        return "Hej"
    def RightString(self):
        
        FL = self.FuncList()
        OL = self.OperationList()
        
        String=""
        for n in range(0,len(self.__FuncList)):

            
#            al = FL[n].LeftString()

            a= FL[n].RightString()

#            aleft = FL[n].LeftString()

#            oleft= OL[n].LeftString()
            o = OL[n].RightString()
            
            String = f"{String}({o}{a}"
        
        return String
          
    
    def LeftString(self):
        String = ""
        FL = self.FuncList()
        OL = self.OperationList()
        
        for n in range(0,len(self.__FuncList)):

            
#            al = FL[n].LeftString()

            print(FL[n])
            a = FL[n].LeftString()

            o= OL[n].LeftString()
            
            String = f"{a}{o}("
        
        return String
    
    def __str__(self):
        
        String = self.LeftString()+"x"+self.RightString()
        
    def __repr__(self):
        return self.__str__()

#        if type(Argument)==Function
class AtomicFunction(Function):
    def __init__(self,Function,LeftString,RightString):
        self.__LeftString=LeftString
        self.__RightString=RightString
        self._Function__FuncList = []
        self._Function__OperationList = []
        self.__Function = Function 
        

    def __str__(self):
        return f"Atomic function: f(x) = {self.__LeftString}(x){self.__RightString}" 
        
    def __repr__(self):
        return self.__str__()
    
    def LeftString(self):
        return self.__LeftString
    
    def RightString(self):
        return self.__RightString
    

    def ReturnFunction(self):
        return self.__Function

    def __call__(self,Arg)
        if type(Arg)==Function:
            Output=Function(ID)
            
            FL1 = Arg.FuncList()
            OL1 = Arg.OperationList()
            
            FL2 = self.FuncList()
            OL2 = self.OperationList()
            
            FL3 = FL1 + FL2 
            OL3 = OL1 + OL2 
            
            
            Output.SetLists(FL3,OL3)
            
            return Output
        
        elif type(Arg)==AtomicFunction:
            Output = Function(ID)
           
            FL1 = [Arg]
            OL1 = [Call]
            
            FL2 = self.FuncList()
            OL2 = self.OperationList()
            
            FL3 = FL1 + FL2 
            OL3 = OL1 + OL2 
          
            Output.SetLists(FL3,OL3)
            
            return Output
                                
        else:
            F=self.ReturnFunction()
            return F(Arg)
        
        
#    def __call__(self,Arg):

#        return self.Function()(Arg)

def Id(x):
    return x 

ID = AtomicFunction(Id,"","")

def Square(x):
    return x**2


def f(x):
    return x**2 

SQ=AtomicFunction(Square,"","^2")

F=SQ
#A= F.ReturnFunction()
G=F(F)

#
#class MyFunc():
#
#    
#class PowerSeries(MyFunc):
#    def __init__(self,Input):
#        
#        
#def f(x,y):
#    return x**2+y
#
#def g(x):
#    return 2
#
#c=4
#F=MyFunc(f)
#G=MyFunc(c)
#
#
#Y=F(1,2)
#print(Y)
#
#K = F+G

#print(K(4,3))
#def Derivative(Func,)        
#def H0(Args):
#    x=Args[0]
#    p=Args[1]
#    Out = omega*0.5*(x**2+p**2)
#    
#    return Out
#
#PBM = array([[0,1],[-1,0]])
#
#H=Hamiltonian(H0,PBM)

#class PoissonBracket(array):
#    def __init__(self,InputArray):
#        """Inputarray: array of functions"""
#        
#        
#def gen_EOM(Hamiltonian):
#    
    