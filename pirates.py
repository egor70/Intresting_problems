Три пирата делят награбленные N монет. Первого устраивает a% добычи, второго b%, третьего c%. Гарантируется, что a,b,c<=100.

Найдите все распределения награбленного, которые устроят всех пиратов.
Формат входных данных
Строка 1: N (>0 типа int), a (>=0, float), b (>=0, float), c (>=0, float)
Формат выходных данных
Строки 1..N: все распределения монет, в одной строке пишется через пробел количество монет у каждого: na, nb, nc.

Строки выводятся в лексикографическом (алфавитном) порядке.

Если удовлетворительных дележей нет, нужно написать EMPTY.
Пример 1
Входные данные

10 30 30 20
Выходные данные

3 3 4
3 4 3
3 5 2
4 3 3
4 4 2
5 3 2




import math



N, a, b, c = map(float, input().split())
N = int(N)

min_a = math.ceil(a * N / 100.0)
min_b = math.ceil(b * N / 100.0)
min_c = math.ceil(c * N / 100.0)

if min_a + min_b + min_c > N:
    print("EMPTY")


solutions = []
for na in range(min_a, N + 1):
    for nb in range(min_b, N - na + 1):
        nc = N - na - nb
        if nc >= min_c:
                solutions.append((na, nb, nc))

if not solutions:
    print("EMPTY")
else:
    for na, nb, nc in solutions:
        print(na, nb, nc)


