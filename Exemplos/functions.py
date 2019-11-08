def jumpline():
    print("\n")

def my_function():
    print("Hello World from a function")
my_function()

jumpline()

def machado(name,surname):
    print(name + " " + surname + " Machado")

machado("João","Paulo")

jumpline()

def multplicacao(input):
    resultado = 5*input
    return resultado

print("resultado: ", multplicacao(3))

jumpline()

# recursive functions (functions that call themselves
def recursion(k):
    if(k>0):
        result = k+recursion(k-1)
        print(result)
    else:
        result  = 0
    return result

recursion(10)

jumpline()

# lambda functions:
x = lambda a: a*5
print(x(5))

x = lambda a,b: a*b
print(x(5,6))

x = lambda a,b,c: a*b*c
print(x(1,2,3))

jumpline()

def func_lambda(n):
    return lambda a: a*n

doubler = func_lambda(2)

print(doubler(11)) # 11 is parsed as a function through doubler (a)

jumpline()

def multplier(n):
    return lambda a: a*n
doubler=multplier(2)
tripler=multplier(3)

print(doubler(10))
print(tripler(10))