import tkinter as tk
from tkinter import ttk, scrolledtext
import random
import time

# ===== Алгоритми сортування =====
def bubble_sort(arr):
    data = arr.copy()
    n = len(data)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
    return data

def selection_sort(arr):
    data = arr.copy()
    n = len(data)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if data[j] < data[min_idx]:
                min_idx = j
        data[i], data[min_idx] = data[min_idx], data[i]
    return data

def insertion_sort(arr):
    data = arr.copy()
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and data[j] > key:
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = key
    return data

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def quick_sort_3way(arr):
    def sort_3way(data, low, high):
        if low >= high:
            return
        lt = low
        gt = high
        pivot = data[low]
        i = low + 1
        while i <= gt:
            if data[i] < pivot:
                data[lt], data[i] = data[i], data[lt]
                lt += 1
                i += 1
            elif data[i] > pivot:
                data[i], data[gt] = data[gt], data[i]
                gt -= 1
            else:
                i += 1
        sort_3way(data, low, lt - 1)
        sort_3way(data, gt + 1, high)

    data = arr.copy()
    sort_3way(data, 0, len(data) - 1)
    return data

# ===== Генерація даних =====
def generate_scenario(case, size, vmin, vmax):
    population = list(range(vmin, vmax + 1))
    if case == "Initial":
        if size > len(population):
            return random.choices(population, k=size)
        return random.sample(population, size)
    elif case == "Updated":
        base_size = max(0, size // 2)
        base = sorted(random.sample(population, base_size))
        extras = random.choices(population, k=size - base_size)
        return base + extras
    elif case == "Final":
        return [random.randint(vmin, vmax) for _ in range(size)]
    return []

# ===== Основна функція сортування =====
def run_sort():
    try:
        case = case_combo.get()
        algo = algo_combo.get()
        size = int(size_entry.get())
        vmin = int(min_entry.get())
        vmax = int(max_entry.get())
        if vmin > vmax:
            raise ValueError("Мінімальне значення більше за максимальне.")
    except ValueError as e:
        output_text.config(state='normal')
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Помилка: {e}")
        output_text.config(state='disabled')
        return

    try:
        arr = generate_scenario(case, size, vmin, vmax)
    except Exception as e:
        output_text.config(state='normal')
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Помилка генерації даних: {e}")
        output_text.config(state='disabled')
        return

    output_text.config(state='normal')
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Початковий список ({len(arr)} елементів):\n{arr}\n\n")

    sorter = {
        "Сортування бульбашкою": bubble_sort,
        "Сортування вибором": selection_sort,
        "Сортування вставками": insertion_sort,
        "Quick Sort": quick_sort_3way if case == "Final" else quick_sort,
        "Quick Sort 3-way": quick_sort_3way
    }.get(algo, None)

    if sorter:
        start = time.perf_counter()
        sorted_arr = sorter(arr)
        elapsed = (time.perf_counter() - start) * 1000
        output_text.insert(tk.END, f"Відсортований список:\n{sorted_arr}\n\n")
        output_text.insert(tk.END, f"Час виконання ({algo}): {elapsed:.3f} мс")
    else:
        output_text.insert(tk.END, "Помилка: Алгоритм не вибрано або не знайдено.")
    output_text.config(state='disabled')

# ===== Побудова інтерфейсу =====
root = tk.Tk()
root.title("Візуалізація алгоритмів сортування")
root.geometry("1150x700")
root.configure(bg="#f0f4f8")

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#f0f4f8", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
style.configure("TCombobox", padding=5)
style.configure("TLabelframe", background="#dbe9f4", font=("Segoe UI", 10, "bold"), relief="ridge")
style.configure("TLabelframe.Label", background="#dbe9f4")

main_frame = ttk.Frame(root, padding=15, style="TLabelframe")
main_frame.pack(fill=tk.BOTH, expand=True)

controls = ttk.LabelFrame(main_frame, text="Параметри", padding=15)
controls.grid(column=0, row=0, sticky=tk.NW, padx=10, pady=10)

# Сценарій
ttk.Label(controls, text="Сценарій:").grid(column=0, row=0, sticky=tk.W, pady=2)
case_combo = ttk.Combobox(controls, values=["Initial", "Updated", "Final"], state="readonly", width=20)
case_combo.current(0)
case_combo.grid(column=1, row=0, sticky=tk.W)

# Алгоритм
ttk.Label(controls, text="Алгоритм:").grid(column=0, row=1, sticky=tk.W, pady=2)
algo_combo = ttk.Combobox(controls, values=["Сортування бульбашкою", "Сортування вибором", "Сортування вставками", "Quick Sort", "Quick Sort 3-way"], state="readonly", width=30)
algo_combo.current(0)
algo_combo.grid(column=1, row=1, sticky=tk.W)

# Параметри генерації
labels = ["Кількість елементів:", "Мінімальне значення:", "Максимальне значення:"]
def_values = ["50", "1", "150"]
entries = []
for i, (label, val) in enumerate(zip(labels, def_values)):
    ttk.Label(controls, text=label).grid(column=0, row=2+i, sticky=tk.W, pady=2)
    entry = ttk.Entry(controls, width=18)
    entry.insert(0, val)
    entry.grid(column=1, row=2+i, sticky=tk.W)
    entries.append(entry)

size_entry, min_entry, max_entry = entries

run_button = ttk.Button(controls, text="🔃 Виконати сортування", command=run_sort)
run_button.grid(column=0, row=5, columnspan=2, pady=15)

output_frame = ttk.LabelFrame(main_frame, text="Результат", padding=15)
output_frame.grid(column=1, row=0, sticky=tk.NE, padx=10, pady=10)

output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=80, height=30, font=("Consolas", 10))
output_text.pack(fill=tk.BOTH, expand=True)
output_text.config(state='disabled')

root.mainloop()
