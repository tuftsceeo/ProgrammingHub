from threading import Thread

def func1():
    print('func2 Working')

def func2():
    print('func1 Working')

if __name__ == '__main__':
    Thread(target = func1).start()
    Thread(target = func2).start()