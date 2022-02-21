import random

MAX_N = 10 ** 25    # верхняя граница чисел
COUNT_A = 100       # количество прверок в тесте Рабина-Миллера
M = 123456789       # сообщения для подписи


def mod_exp(a, b, n):
    """
    Возводит число a в степень b и вычисляет остаток от деления на n
    :param a: число
    :param b: степень
    :param n: делитель
    :return: a^b mod n
    """
    k = -1
    B = []
    while True:
        k += 1
        B.append(b % 2)
        b //= 2
        if b <= 0:
            break
    d = 1
    for i in reversed(range(k + 1)):
        d = d * d % n
        if B[i] == 1:
            d = d * a % n
    return d


def euclid(a, b):
    """
    Алгоритм Евклида, вычисляющий НОД
    :param a: первое число
    :param b: второе число
    :return: НОД a и b
    """
    while a > 0 and b > 0:
        if a > b:
            a %= b
        else:
            b %= a
    return a + b


def extended_euclid(a, b):
    """
    Расширенный алгоритм Евклида, вычисляющий НОД и коэффициенты x и y в
    линейной комбинации d = a * x + b * y
    :param a: первое число
    :param b: второе число
    :return: d - НОД, x - коэфф при a, y - коэфф при b
    """
    x = yy = 1
    y = xx = 0
    while b > 0:
        q = a // b

        t = b
        b = a % b
        a = t

        t = xx
        xx = x - q * xx
        x = t

        t = yy
        yy = y - q * yy
        y = t
    return a, x, y


def rabin_miller(n, r=COUNT_A):
    """
    Тест Рабина-Миллера на простое число
    :param n: проверяемое число
    :param r: максимальное количество a
    :return: True - если тест считает число простым, False - иначе
    """
    b = n - 1
    k = -1
    B = []
    while True:
        k += 1
        B.append(b % 2)
        b //= 2
        if b <= 0:
            break
    for j in range(1, r + 1):
        a = random.randint(2, n - 1)
        if euclid(a, n) > 1:
            return False
        d = 1
        for i in reversed(range(0, k + 1)):
            x = d
            d = d * d % n
            if d == 1 and x != 1 and x != n - 1:
                return False
            if B[i] == 1:
                d = d * a % n
        if d != 1:
            return False
    return True


def is_prime(n):
    """
    Проверяет число на простоту
    :param n: проверяемое число
    :return: True - если число простое, False - иначе
    """
    P = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
    for j in range(len(P)):
        if n % P[j] == 0:
            if n == P[j]:
                return True
            return False
    return rabin_miller(n)


def generate_prime(N=MAX_N):
    """
    Генерирует большое простое число
    :param N: максимальное значение числа
    :return: большое простое число
    """
    max_rand = N // 2
    while True:
        n = random.randint(2, max_rand)
        n = 2 * n - 1
        if is_prime(n):
            break
    return n


def generate_key_rsa(N=MAX_N):
    """
    Генерирует части ключей по системе RSA
    (e, n) - открытый  ключ
    (d, n) - закрытый ключ
    :param N: максимальное значение больших чисел
    :return: e, d, n - части ключей
    """
    p = q = 1               # большие простые числа
    while p == q:
        p = generate_prime(N)
        q = generate_prime(N)

    n = p * q               # криптомодуль
    f = (p - 1) * (q - 1)   # функция Эйлера

    e = 1
    t = x = 2
    while t > 1:
        e += 2
        t, x, _ = extended_euclid(e, f)
    d = x % f
    return e, d, n


def main():
    """
    Точка входа в программу
    :return: None
    """
    e, d, n = generate_key_rsa()
    print(f'Открытый ключ:\n({e}, {n})\nЗакрытый ключ:\n({d}, {n})\n')
    m = mod_exp(M, d, n)
    mm = mod_exp(m, e, n)
    print(f'Сообщение: {M}\nС подписью: {m}\nПроверка подписи: {mm}')
    if M == mm:
        print(f'\033[32mПодпись верна!')
    else:
        print(f'\033[31mПодпись не верна!')


if __name__ == '__main__':
    main()
