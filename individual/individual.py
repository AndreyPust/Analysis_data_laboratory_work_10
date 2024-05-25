#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
from threading import Thread
from queue import Queue
import sympy as sp


"""
Необходимо с использованием многопоточности для заданного значения x найти сумму ряда S 
с точностью члена ряда по абсолютному значению и произвести сравнение полученной суммы с 
контрольным значением функции y(x) для двух бесконечных рядов.
Необходимо доработать программу лабораторной работы 2.23, организовать конвейер, в котором 
сначала в отдельном потоке вычисляется значение первой функции, после чего результаты 
вычисления должны передаваться второй функции, вычисляемой в отдельном потоке. 
Потоки для вычисления значений двух функций должны запускаться одновременно.
(Вариант 26 (1 и 2)).
"""
E = 1e-7  # Точность


def series_1(x, eps, queue):
    """
    Функция вычисления суммы ряда задачи №1 (x = 1).
    """
    s = 0
    n = 0
    while True:
        term = x ** n * sp.log(3) ** n / math.factorial(n)
        if abs(term) < eps:
            break
        s += term
        n += 1
    queue.put(s)


def series_2(x, eps, queue):
    """
    Функция вычисления суммы ряда задачи №2 (x = 0,7).
    """
    s = 0
    n = 0
    while True:
        term = x ** n
        if abs(term) < eps:
            break
        s += term
        n += 1
    queue.put(s)


def main():
    """
    Главная функция программы.
    """
    # Определение символа n
    n = sp.symbols('n')

    x1 = 1
    control1 = sp.Sum(x1 ** n * sp.log(3) ** n / sp.factorial(n), (n, 0, sp.oo)).evalf()

    x2 = 0.7
    control2 = sp.Sum(x2 ** n, (n, 0, sp.oo)).evalf()

    queue_1 = Queue()
    queue_2 = Queue()

    # Создание потоков для вычисления сумм.
    thread_1 = Thread(target=series_1, args=(x1, E, queue_1))
    thread_2 = Thread(target=series_2, args=(x2, E, queue_2))

    # Запуск созданных потоков.
    thread_1.start()
    thread_2.start()

    sum_1 = queue_1.get()
    sum_2 = queue_2.get()

    # Блокировка основного потока, пока эти два потока не завершатся.
    thread_1.join()
    thread_2.join()

    print(f"x1 = {x1}")
    print(f"Sum of series 1: {sum_1:.7f}")
    print(f"Control value 1: {control1:.7f}")
    print(f"Match 1: {round(sum_1, 7) == round(control1, 7)}")

    print(f"x2 = {x2}")
    print(f"Sum of series 2: {sum_2:.7f}")
    print(f"Control value 2: {control2:.7f}")
    print(f"Match 2: {round(sum_2, 7) == round(control2, 7)}")


if __name__ == '__main__':
    main()
