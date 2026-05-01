# Импортирование библиотек
import tkinter as tk
from tkinter import ttk, messagebox
import json
import datetime

# Настройки
FILE_NAME = "weather.json"

# Глобальные данные
records = []  # Список для хранения записей


# Функции

def load_data():
    """Загружает записи из файла."""
    try:
        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_data():
    """Сохраняет записи в файл."""
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=4)


def add_record():
    """Обрабатывает нажатие кнопки 'Добавить запись'."""
    # 1. Получаем данные из полей ввода
    date = date_entry.get()
    temp = temp_entry.get()
    desc = desc_entry.get()
    rain = "Да" if rain_var.get() else "Нет"

    # 2. Проверяем корректность ввода
    if not date or not temp or not desc:
        messagebox.showerror("Ошибка", "Все поля (Дата, Температура, Описание) должны быть заполнены!")
        return

    try:
        float(temp)
    except ValueError:
        messagebox.showerror("Ошибка", "Температура должна быть числом!")
        return

    # 3. Создаем запись и добавляем в список
    record = {"date": date, "temp": temp, "desc": desc, "rain": rain}
    records.append(record)
    save_data()  # Сохраняем в файл

    # 4. Очищаем поля ввода
    date_entry.delete(0, tk.END)
    temp_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)
    rain_var.set(False)

    # 5. Добавляем запись в таблицу
    tree.insert("", tk.END, values=(date, temp, desc, rain))


def apply_filter():
    """Фильтрует записи по дате и температуре."""
    filter_date = filter_date_entry.get()
    filter_temp = filter_temp_entry.get()

    # Очищаем таблицу
    for i in tree.get_children():
        tree.delete(i)

    # Проходим по записям и выводим подходящие
    for rec in records:
        show = True

        if filter_date and rec["date"] != filter_date:
            show = False

        if filter_temp:
            try:
                if float(rec["temp"]) <= float(filter_temp):
                    show = False
            except ValueError:
                pass

        if show:
            tree.insert("", tk.END, values=(rec["date"], rec["temp"], rec["desc"], rec["rain"]))


def reset_filter():
    """Сбрасывает фильтр и показывает все записи."""
    filter_date_entry.delete(0, tk.END)
    filter_temp_entry.delete(0, tk.END)

    # Очищаем таблицу и заполняем заново
    for i in tree.get_children():
        tree.delete(i)

    for rec in records:
        tree.insert("", tk.END, values=(rec["date"], rec["temp"], rec["desc"], rec["rain"]))


# Главное окно
root = tk.Tk()
root.title("Дневник погоды")
root.geometry("800x500")

# Загрузка данных при старте
records = load_data()

# РАМКА 1: Ввод новой записи
input_frame = ttk.LabelFrame(root, text="Новая запись", padding=(10, 5))
input_frame.pack(pady=10, padx=10, fill="x")

# Поле для даты
ttk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, sticky="e", padx=5)
date_entry = ttk.Entry(input_frame)
date_entry.grid(row=0, column=1, sticky="w", padx=5)

# Поле для температуры
ttk.Label(input_frame, text="Температура (°C):").grid(row=1, column=0, sticky="e", padx=5)
temp_entry = ttk.Entry(input_frame)
temp_entry.grid(row=1, column=1, sticky="w", padx=5)

# Поле для описания погоды
ttk.Label(input_frame, text="Описание:").grid(row=2, column=0, sticky="e", padx=5)
desc_entry = ttk.Entry(input_frame)
desc_entry.grid(row=2, column=1, sticky="ew", padx=5)

# Флажок для осадков
ttk.Label(input_frame, text="Осадки:").grid(row=3, column=0, sticky="e", padx=5)
rain_var = tk.BooleanVar()
ttk.Checkbutton(input_frame, text="Да", variable=rain_var).grid(row=3, column=1, sticky="w")

# Кнопка добавления записи
ttk.Button(input_frame, text="Добавить запись", command=add_record).grid(
    row=4, column=0, columnspan=2, pady=10)

# РАМКА 2: Фильтрация
filter_frame = ttk.LabelFrame(root, text="Фильтр", padding=(10, 5))
filter_frame.pack(pady=(0, 10), padx=10, fill="x")

# Поле для фильтра по дате
ttk.Label(filter_frame, text="Дата:").grid(row=0, column=0, sticky="e", padx=5)
filter_date_entry = ttk.Entry(filter_frame)
filter_date_entry.grid(row=0, column=1, sticky="w", padx=5)

# Поле для фильтра по температуре
ttk.Label(filter_frame, text="Температура выше:").grid(row=1, column=0, sticky="e", padx=5)
filter_temp_entry = ttk.Entry(filter_frame)
filter_temp_entry.grid(row=1, column=1, sticky="w", padx=5)

# Кнопка применения фильтра
ttk.Button(filter_frame, text="Применить", command=apply_filter).grid(
    row=2, columnspan=2, pady=(5), ipadx=35)
# Кнопка сброса фильтра
ttk.Button(filter_frame, text="Сбросить", command=reset_filter).grid(
    row=3, columnspan=2, ipadx=42)

# РАМКА 3: Таблица записей
tree_frame = ttk.Frame(root)
tree_frame.pack(padx=10, fill="both", expand=True)

# Определение колонок таблицы
columns = ("date", "temp", "desc", "rain")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
# Заголовки столбцов
tree.heading("date", text="Дата")
tree.heading("temp", text="Температура")
tree.heading("desc", text="Описание")
tree.heading("rain", text="Осадки")

# ширина столбцов
tree.column("date", width=120)
tree.column("temp", width=80)
tree.column("desc", width=400)
tree.column("rain", width=80)

# Полоса прокрутки для таблицы
yscroll = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
yscroll.pack(side="right", fill="y")
tree.configure(yscrollcommand=yscroll.set)
tree.pack(fill="both", expand=True)

# Заполняем таблицу данными из файла при запуске
for rec in records:
    tree.insert("", tk.END,
                values=(rec["date"], rec["temp"], rec["desc"], rec["rain"]))

# Запуск приложения
root.mainloop()
