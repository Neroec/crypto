import random

MAX_N = 10 ** 25  # верхняя граница чисел
COUNT_A = 100  # количество проверок в тесте Рабина-Миллера
M = 123456789  # сообщения для подписи


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
    P = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107,
         109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
         233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359,
         367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491,
         499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641,
         643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787,
         797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941,
         947, 953, 967, 971, 977, 983, 991, 997]
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


def generate_g(N=MAX_N):
    """
    Генерирует примитивный элемент g, а также простые числа p и q
    :param N: максимальное значение больших чисел
    :return: g, q, p - параметры для криптосистемы Деффи - Хеллмана
    """
    q = generate_prime(2**256)  # большие простые числа
    while True:
        n = random.randint(2, N)
        p = n * q + 1
        if is_prime(p):
            break
    while True:
        a = random.randint(1, p - 1)
        g = mod_exp(a, n, p)
        if g != 1:
            break
    return g, q, p


def mod_exp_dh(g, x, q, p):
    """
    Возводит число g в степень x (x mod q) и вычисляет остаток от деления на p - ускоренный алгоритм
    :param g: число
    :param x: степень
    :param q: делитель для степени
    :param p: делитель
    :return: g^(x mod q) mod p
    """
    xx = x % q
    X = mod_exp(g, xx, p)
    return X


def main():
    """
    Точка входа в программу
    :return: None
    """
    x = random.randint(2, MAX_N)
    y = random.randint(2, MAX_N)
    g, q, p = generate_g()
    X = mod_exp_dh(g, x, q, p)
    print(f'Пользователь А отправил B через незащищенный канал связи:\n({X})')
    Y = mod_exp_dh(g, y, q, p)
    print(f'Пользователь B отправил A через незащищенный канал связи:\n({Y})')

    k1 = mod_exp_dh(Y, x, q, p)
    k2 = mod_exp_dh(X, y, q, p)
    if k1 == k2:
        print(f'Секретные ключи совпали:\n k = ({k1}) k\' = ({k2})')
    else:
        print(f'Секретные ключи НЕ совпали:\n k = ({k1}) k\' = ({k2})')


if __name__ == '__main__':
    main()
