import requests
from bs4 import BeautifulSoup
import csv
from collections import defaultdict
import time

def get_animals_count():
    base_url = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"
    letter_counts = defaultdict(int)
    russian_letters = set('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')

    while base_url:

        try:
            response = requests.get(base_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Находим все группы категорий
            category_groups = soup.find_all('div', class_='mw-category-group')

            if not category_groups:
                print("Не найдено групп категорий!")
                break

            for group in category_groups:
                letter = group.find('h3').text.strip().upper()  # Приводим к верхнему регистру
                if not letter or len(letter) > 1 or letter not in russian_letters:
                    continue


                animals = group.find_all('a')
                letter_counts[letter] += len(animals)
                print(f"Буква {letter}: +{len(animals)}")  # Для отладки

            # Ищем ссылку на следующую страницу
            next_page_link = soup.find('a', string='Следующая страница')
            base_url = "https://ru.wikipedia.org" + next_page_link['href'] if next_page_link else None

        except Exception as e:
            print(f"Ошибка: {e}")
            break


    return letter_counts



def write_to_csv(letter_counts):
    # Русский алфавит в правильном порядке
    russian_alphabet = [
        'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й',
        'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф',
        'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я'
    ]
    sorted_letters = sorted(
        letter_counts.items(),
        key=lambda x: russian_alphabet.index(x[0]) if x[0] in russian_alphabet else 999
    )

    with open('../beasts.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for letter, count in sorted_letters:
            writer.writerow([letter, count])


if __name__ == "__main__":
    start_time = time.time()
    print("Начинаю сбор данных...")
    counts = get_animals_count()
    print("Данные собраны, записываю в файл...")
    write_to_csv(counts)
    print(f"Время выполнения: {time.time() - start_time:.2f} секунд")
    print("Готово! Результат сохранён в beasts.csv")