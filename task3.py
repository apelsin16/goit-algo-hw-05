import timeit
from collections import namedtuple

# Алгоритм Бойера-Мура
def build_shift_table(pattern):
    """Створити таблицю зсувів для алгоритму Боєра-Мура."""
    table = {}
    length = len(pattern)
    # Для кожного символу в підрядку встановлюємо зсув рівний довжині підрядка
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    # Якщо символу немає в таблиці, зсув буде дорівнювати довжині підрядка
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore(text, pattern):
    # Створюємо таблицю зсувів для патерну (підрядка)
    shift_table = build_shift_table(pattern)
    i = 0  # Ініціалізуємо початковий індекс для основного тексту

    # Проходимо по основному тексту, порівнюючи з підрядком
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1  # Починаємо з кінця підрядка

        # Порівнюємо символи від кінця підрядка до його початку
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1  # Зсуваємось до початку підрядка

        # Якщо весь підрядок збігається, повертаємо його позицію в тексті
        if j < 0:
            return i  # Підрядок знайдено

        # Зсуваємо індекс i на основі таблиці зсувів
        # Це дозволяє "перестрибувати" над неспівпадаючими частинами тексту
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    # Якщо підрядок не знайдено, повертаємо -1
    return -1

# Алгоритм Кнута-Морріса-Пратта
def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

def kmp(text, pattern):
    M = len(pattern)
    N = len(text)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1  # якщо підрядок не знайдено

# Алгоритм Рабіна-Карпа
def rabin_karp(text, pattern):
    M = len(pattern)
    N = len(text)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1  # якщо підрядок не знайдено

# Функція для вимірювання часу виконання алгоритму
def measure_time(algorithm, text, pattern):
    start_time = timeit.default_timer()
    algorithm(text, pattern)
    return timeit.default_timer() - start_time

# Зчитуємо текстовий файл
def read_file(filename):
    with open(filename, 'r', encoding='cp1251') as file:
        return file.read()

# Текстовий файл
text2 = read_file('/text2.txt')
text1 = read_file('/text1.txt')

# Підрядки для пошуку
existing_pattern = "дійсно"
fake_pattern = "фейковий"

# Вимірюємо час виконання кожного алгоритму для кожного підрядка
AlgorithmResult = namedtuple('AlgorithmResult', ['algorithm', 'existing_time', 'fake_time'])

algorithms = [
    AlgorithmResult('Boyer-Moore', measure_time(boyer_moore, text1, existing_pattern), measure_time(boyer_moore, text1, fake_pattern)),
    AlgorithmResult('Knuth-Morris-Pratt', measure_time(kmp, text1, existing_pattern), measure_time(kmp, text1, fake_pattern)),
    AlgorithmResult('Rabin-Karp', measure_time(rabin_karp, text1, existing_pattern), measure_time(rabin_karp, text1, fake_pattern)),
    AlgorithmResult('Boyer-Moore', measure_time(boyer_moore, text2, existing_pattern), measure_time(boyer_moore, text2, fake_pattern)),
    AlgorithmResult('Knuth-Morris-Pratt', measure_time(kmp, text2, existing_pattern), measure_time(kmp, text2, fake_pattern)),
    AlgorithmResult('Rabin-Karp', measure_time(rabin_karp, text2, existing_pattern), measure_time(rabin_karp, text2, fake_pattern)),
]

# Виведемо результати
for result in algorithms:
    print(f"{result.algorithm}:")
    print(f"Час для існуючого підрядка: {result.existing_time} сек")
    print(f"Час для вигаданого підрядка: {result.fake_time} сек")
    print()
