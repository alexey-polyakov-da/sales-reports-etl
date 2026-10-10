import os
import glob
import re
import csv


def process_files(src_folder, dest_folder):
    """
    Объединяет CSV-чеки магазинов в один файл.

    src_folder: папка с исходными файлами
    dest_folder: папка для сохранения результата
    """

    # Шаблон имени: ГГГГ-ММ-ДД-ЧЧ-ММ-idмагазина.csv
    pattern = r'\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d+\.csv'

    # Столбцы, которые должны остаться в итоговом файле
    columns = ['date', 'product', 'store', 'cost']

    # Находим CSV-файлы и сортируем по названию
    files = sorted(glob.glob(os.path.join(src_folder, '*.csv')))

    # Создаём папку для итогового файла
    os.makedirs(dest_folder, exist_ok=True)

    # Формируем путь к итоговому CSV
    output_path = os.path.join(dest_folder, 'combined_data.csv')

    count_files = 0
    count_rows = 0

    # Открываем итоговый файл для записи
    with open(output_path, 'w', newline='', encoding='utf-8') as output_file:

        # Выходной разделитель — запятая
        writer = csv.writer(output_file, delimiter=',')

        # Записываем заголовок
        writer.writerow(columns)

        # Перебираем найденные файлы
        for file_path in files:
            filename = os.path.basename(file_path)

            # Пропускаем файлы с неподходящими названиями
            if not re.fullmatch(pattern, filename):
                continue

            # Читаем подходящий CSV-файл
            with open(file_path, 'r', newline='', encoding='utf-8') as input_file:

                # Исходный разделитель — точка с запятой
                reader = csv.DictReader(input_file, delimiter=';')

                # Проверяем наличие обязательных столбцов
                if not set(columns).issubset(reader.fieldnames or []):
                    continue

                count_files += 1

                # Обрабатываем каждую строку
                for row in reader:

                    # Оставляем только нужные столбцы
                    selected_row = [row[column] for column in columns]

                    # Записываем строку в итоговый файл
                    writer.writerow(selected_row)

                    count_rows += 1

    print(f'Обработано файлов: {count_files}')
    print(f'Записано строк: {count_rows}')
    print(f'Результат сохранён: {output_path}')


# Этот блок выполняется только при прямом запуске скрипта
if __name__ == '__main__':
    src_folder = 'sample_data'
    dest_folder = 'output'

    process_files(src_folder, dest_folder)
