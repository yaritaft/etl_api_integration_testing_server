def decorator(func,):
    def wrapper(num2):
        print("antes")
        func(num2)
        print("despues")
    return wrapper


@decorator
def my_print(x):
    print(x)

my_print("hola")