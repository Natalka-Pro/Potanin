import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# 2786 288

class ImageSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Sorter - Good/Bad/Error")

        # Папки (устанавливаются при выборе входной папки)
        self.input_folder = ""
        self.good_folder = ""
        self.bad_folder = ""
        self.error_folder = ""

        # Текущий файл
        self.current_image_path = ""

        # GUI элементы
        self.setup_ui()

    def setup_ui(self):
        # Кнопка выбора папки с изображениями
        self.btn_select_folder = tk.Button(
            self.root,
            text="Select Image Folder",
            command=self.select_input_folder
        )
        self.btn_select_folder.pack(pady=10)

        # Область для отображения изображения
        self.image_label = tk.Label(self.root)
        self.image_label.pack()

        # Кнопки сортировки
        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(pady=10)

        # Кнопки теперь соответствуют названиям папок
        self.btn_good = tk.Button(
            self.btn_frame,
            text="Good",
            command=lambda: self.process_image("Good"),
            state=tk.DISABLED
        )
        self.btn_good.pack(side=tk.LEFT, padx=5)

        self.btn_bad = tk.Button(
            self.btn_frame,
            text="Bad",
            command=lambda: self.process_image("Bad"),
            state=tk.DISABLED
        )
        self.btn_bad.pack(side=tk.LEFT, padx=5)

        self.btn_error = tk.Button(
            self.btn_frame,
            text="Error",
            command=lambda: self.process_image("Error"),
            state=tk.DISABLED
        )
        self.btn_error.pack(side=tk.LEFT, padx=5)

        # Статус (сколько осталось)
        self.status_label = tk.Label(self.root, text="")
        self.status_label.pack(pady=10)

    def select_input_folder(self):
        # Выбор папки с изображениями
        self.input_folder = filedialog.askdirectory(title="Select Image Folder")

        if not self.input_folder:
            return

        # Создаем папки Good, Bad и Error (если их нет)
        self.good_folder = os.path.join(self.input_folder, "Good")
        self.bad_folder = os.path.join(self.input_folder, "Bad")
        self.error_folder = os.path.join(self.input_folder, "Error")

        os.makedirs(self.good_folder, exist_ok=True)
        os.makedirs(self.bad_folder, exist_ok=True)
        os.makedirs(self.error_folder, exist_ok=True)

        # Получаем список изображений
        self.image_files = [
            f for f in os.listdir(self.input_folder)
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))
        ]

        if not self.image_files:
            messagebox.showinfo("Info", "No images found in the folder!")
            return

        # Активируем кнопки
        self.btn_good.config(state=tk.NORMAL)
        self.btn_bad.config(state=tk.NORMAL)
        self.btn_error.config(state=tk.NORMAL)

        # Загружаем первое изображение
        self.load_next_image()

    def load_next_image(self):
        if not self.image_files:
            messagebox.showinfo("Done", "All images processed!")
            self.btn_good.config(state=tk.DISABLED)
            self.btn_bad.config(state=tk.DISABLED)
            self.btn_error.config(state=tk.DISABLED)
            self.status_label.config(text="Processing complete!")
            return

        self.current_image_path = os.path.join(self.input_folder, self.image_files.pop(0))

        # Открываем и масштабируем изображение
        try:
            img = Image.open(self.current_image_path)
            img.thumbnail((900, 900))  # Уменьшаем для отображения

            photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=photo)
            self.image_label.image = photo  # Чтобы не удалялось сборщиком мусора
        except Exception as e:
            print(f"!!!!!!!!!! Error loading image: {e} !!!!!!!!!!")
            self.load_next_image()
            return

        # Обновляем статус
        self.status_label.config(text=f"Remaining: {len(self.image_files)}")

    def process_image(self, action):
        if not self.current_image_path:
            return

        filename = os.path.basename(self.current_image_path)

        if action == "Good":
            dst = os.path.join(self.good_folder, filename)
        elif action == "Bad":
            dst = os.path.join(self.bad_folder, filename)
        elif action == "Error":
            dst = os.path.join(self.error_folder, filename)
        else:
            return

        shutil.move(self.current_image_path, dst)
        print(f"Image copied to '{action}': {filename}")

        # Загружаем следующее изображение
        self.load_next_image()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSorterApp(root)
    root.mainloop()
