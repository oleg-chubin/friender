from threading import Thread
from time import sleep


def parallel_func(name, number_of_iterations, iteration_period):
    for i in range(number_of_iterations):
        print('I am inside thread', name, i)
        sleep(iteration_period)


th = Thread(target=parallel_func, args=('first', 20, 0.5))
second_th = Thread(target=parallel_func, args=('second', 10, 1))
th.start()
sleep(0.1)
second_th.start()

for i in range(40):
    print('main', i)
    sleep(0.25)

