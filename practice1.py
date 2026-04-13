# ==============================
# ПРАКТИЧЕСКОЕ ЗАНЯТИЕ №1
# ОСНОВЫ PYTHON
# ==============================

# --- ФУНКЦИИ ---

def find_min(a, b, c):
    """Функция возвращает наименьшее из трёх чисел"""
    if a <= b and a <= c:
        return a
    elif b <= a and b <= c:
        return b
    else:
        return c


def reverse_string(text):
    """Функция возвращает перевёрнутую строку"""
    return text[::-1]


def is_number(value):
    """Проверка: можно ли преобразовать строку в число"""
    try:
        float(value)
        return True
    except ValueError:
        return False


# --- КЛАСС ---

class NumberAnalyzer:
    """Простой класс для анализа чисел"""

    def __init__(self, numbers):
        self.numbers = numbers  # список чисел

    def get_min(self):
        return min(self.numbers)

    def get_max(self):
        return max(self.numbers)

    def get_average(self):
        return sum(self.numbers) / len(self.numbers)


# --- ОСНОВНАЯ ЧАСТЬ ПРОГРАММЫ ---

def main():
    print("=== Работа с числами ===")

    numbers = []

    # Ввод 3 чисел с проверкой
    count = 0
    while count < 3:
        user_input = input(f"Введите число {count + 1}: ")

        if is_number(user_input):
            numbers.append(float(user_input))
            count += 1
        else:
            print("Ошибка! Введите корректное число.")

    a, b, c = numbers

    # Использование функции
    minimum = find_min(a, b, c)
    print(f"Минимальное число: {minimum}")

    # Работа с классом
    analyzer = NumberAnalyzer(numbers)

    print("\n=== Анализ чисел ===")
    print("Минимум:", analyzer.get_min())
    print("Максимум:", analyzer.get_max())
    print("Среднее:", analyzer.get_average())

    # --- РАБОТА СО СТРОКАМИ ---
    print("\n=== Работа со строками ===")

    text = input("Введите строку: ")
    reversed_text = reverse_string(text)

    print("Перевёрнутая строка:", reversed_text)

    # --- ДОПОЛНИТЕЛЬНО: ЦИКЛ FOR ---
    print("\n=== Вывод чисел (цикл for) ===")
    for num in numbers:
        print("Число:", num)

    # --- ДОПОЛНИТЕЛЬНО: WHILE ---
    print("\n=== Обратный отсчёт (while) ===")
    i = 3
    while i > 0:
        print(i)
        i -= 1


# --- ЗАПУСК ПРОГРАММЫ ---
if __name__ == "__main__":
    main()