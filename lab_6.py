import random
import tkinter as tk
from tkinter import ttk
import time
import concurrent.futures
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading


# function to generate array of random numbers of given size
def generate_array(arr, size):

    for i in range(size):
        arr.append(random.randint(1, 100000))


# Selection Sort
def selection_sort(array):

    for i in range(len(array)):
        min_index = i
        for j in range(i + 1, len(array)):
            if array[min_index] > array[j]:
                min_index = j

        array[i], array[min_index] = array[min_index], array[i]


# Shell Sort
def shell_sort(array):

    n = len(array)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = array[i]
            j = i
            while j >= gap and array[j - gap] > temp:
                array[j] = array[j - gap]
                j -= gap
            array[j] = temp
        gap //= 2


# Quick Sort
def quick_sort(array):
    if len(array) <= 1:
        return array

    stack = [(0, len(array) - 1)]
    while stack:
        low, high = stack.pop()
        if low < high:
            pi = partition(low, high, array)
            stack.append((low, pi - 1))
            stack.append((pi + 1, high))


def partition(low, high, array):
    # Your partition logic here
    pivot = array[high]
    i = low - 1

    for j in range(low, high):
        if array[j] <= pivot:
            i += 1
            array[i], array[j] = array[j], array[i]

    array[i + 1], array[high] = array[high], array[i + 1]
    return i + 1


# Merge Sort
def merge_sort(array):
    if len(array) > 1:
        left_arr = array[:len(array) // 2]
        right_arr = array[len(array) // 2:]

        merge_sort(left_arr)
        merge_sort(right_arr)

        i = 0
        j = 0
        k = 0

        while i < len(left_arr) and j < len(right_arr):
            if left_arr[i] < right_arr[j]:
                array[k] = left_arr[i]
                i += 1
            else:
                array[k] = right_arr[j]
                j += 1
            k += 1

        while i < len(left_arr):
            array[k] = left_arr[i]
            i += 1
            k += 1

        while j < len(right_arr):
            array[k] = right_arr[j]
            j += 1
            k += 1


# Counting Sort
def counting_sort(array):
    max_num = max(array)
    min_num = min(array)

    count_arr = [0] * (max_num - min_num + 1)
    sorted_arr = [0] * len(array)

    for i in range(len(array)):
        count_arr[array[i] - min_num] += 1

    for i in range(1, len(count_arr)):
        count_arr[i] += count_arr[i - 1]

    for i in range(len(array)):
        sorted_arr[count_arr[array[i] - min_num] - 1] = array[i]
        count_arr[array[i] - min_num] -= 1

    for i in range(len(array)):
        array[i] = sorted_arr[i]


# test_sizes = [1024, 4096, 16384, 65536, 262144, 1048576, 4194304]
# functions = [quick_sort, merge_sort, counting_sort]


def perform_test(args):
    function, array = args
    start = time.perf_counter()
    function(array.copy())
    end = time.perf_counter()
    return end - start, function.__name__


def run_tests(test_sizes, functions, time_result, app):
    for size in test_sizes:
        if size >= 65536:
            functions = [quick_sort, merge_sort, counting_sort]
        array = []
        generate_array(array, size)
        print(f"Size: {size}")

        with concurrent.futures.ProcessPoolExecutor() as executor:
            args = [(f, array) for f in functions]
            results = [executor.submit(perform_test, arg) for arg in args]

            for f in concurrent.futures.as_completed(results):
                result, name = f.result()
                print(f'time: {result} seconds function: {name}')
                time_result[name].append(result)
                app.plot_data(time_result)
                app.fill_treeview()


class Application(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Lab 6")

        self.array = []
        self.test_sizes = [1024, 4096, 16384, 65536, 262144, 1048576, 4194304]
        self.time_result = {selection_sort.__name__: [], shell_sort.__name__: [], quick_sort.__name__: [],
                            merge_sort.__name__: [], counting_sort.__name__: []}
        self.functions = [selection_sort, shell_sort, quick_sort, merge_sort, counting_sort]

        self.controls_frame = tk.Frame(self)
        self.diagrame_frame = tk.Frame(self)
        self.treeview_frame = tk.Frame(self)

        self.controls_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.diagrame_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.treeview_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.run_tests_button = ttk.Button(self.controls_frame, text="Run tests", command=self.run_tests_button_action)
        self.run_tests_button.pack(side="left", padx=10, pady=10)

        # Creating the plot
        self.figure, self.subplot = plt.subplots(figsize=(6, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.diagrame_frame)

        self.subplot.set_title("Sorting Algorithms")

        self.subplot.set_xlabel("Size")
        self.subplot.set_ylabel("Time, seconds")

        self.canvas.get_tk_widget().pack()

        # Creating the treeview for displaying the results
        self.treeview = ttk.Treeview(self.treeview_frame, show="headings", height=5)

        self.configure_treeview_frame_layout()

        self.mainloop()

    def configure_treeview_frame_layout(self):

        columns_names = ('sort\\size', '1 024', '4 096', '16 384', '65 536', '262 144', '1 048 576', '4 194 304')
        self.treeview["columns"] = columns_names

        # setting up treeview columns
        self.treeview.column("sort\\size", width=80, stretch=tk.NO)
        self.treeview.column("1 024", width=80, anchor="center")
        self.treeview.column("4 096", width=80, anchor="center")
        self.treeview.column("16 384", width=80, anchor="center")
        self.treeview.column("65 536", width=80, anchor="center")
        self.treeview.column("262 144", width=80, anchor="center")
        self.treeview.column("1 048 576", width=80, anchor="center")
        self.treeview.column("4 194 304", width=80, anchor="center")

        # setting up treeview headings
        for col in columns_names:
            self.treeview.heading(col, text=col)

        self.treeview.pack()

    def clear_treeview(self):
        for item in self.treeview.get_children():
            self.treeview.delete(item)

    def fill_treeview(self):
        self.clear_treeview()

        for key in self.time_result:
            # round values
            self.time_result[key] = [round(value, 7) for value in self.time_result[key]]
            self.treeview.insert("", "end", values=[key] + self.time_result[key])

    def run_tests_button_action(self):
        # Clear the previous results
        for key in self.time_result:
            self.time_result[key].clear()

        # Clear the previous plot
        self.subplot.clear()
        self.canvas.draw()

        # Create a separate thread to run tests while keeping the GUI responsive
        testing_thread = threading.Thread(target=self.run_tests)
        testing_thread.start()

        # fill treeview
        self.fill_treeview()

    def run_tests(self):
        run_tests(self.test_sizes, self.functions, self.time_result, self)
        self.plot_data(self.time_result)

    def clear_plot(self):
        self.subplot.clear()  # Clear the previous plot
        self.subplot.set_xlabel("Size")
        self.subplot.set_ylabel("Time, seconds")

        self.subplot.set_title("Sorting Algorithms")

        # Set the X-axis ticks and labels based on self.test_sizes
        x_ticks = range(len(self.test_sizes))
        x_labels = [str(size) for size in self.test_sizes]

        self.subplot.set_xticks(x_ticks)
        self.subplot.set_xticklabels(x_labels, rotation=45)  # Rotate the labels for better visibility

    def plot_data(self, data):

        self.clear_plot()
        self.subplot.plot(data['quick_sort'], label='Quick Sort')
        self.subplot.plot(data['merge_sort'], label='Merge Sort')
        self.subplot.plot(data['counting_sort'], label='Counting Sort')

        # self.subplot.set_title("Sorting Algorithms")
        self.subplot.legend()
        self.canvas.draw()  # Redraw the canvas


if __name__ == '__main__':
    Application()



