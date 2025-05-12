import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

SIZE = 800

# 2786 288

class ImageSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Sorter - Move to Good/Bad/Error")

        # Папки
        self.input_folder = ""
        self.corresponding_folder = ""
        self.good_folder = ""
        self.bad_folder = ""
        self.error_folder = ""

        # Текущие файлы
        self.current_image_path = ""
        self.current_corresponding_image_path = ""

        # GUI элементы
        self.setup_ui()

    def setup_ui(self):
        # Фрейм для кнопок выбора папок
        self.folder_select_frame = tk.Frame(self.root)
        self.folder_select_frame.pack(pady=10)

        # Кнопка выбора папки с изображениями
        self.btn_select_folder = tk.Button(
            self.folder_select_frame,
            text="Select Image Folder",
            command=self.select_input_folder
        )
        self.btn_select_folder.pack(side=tk.LEFT, padx=5)

        # Кнопка выбора
        self.btn_select_corresponding_folder = tk.Button(
            self.folder_select_frame,
            text="Select corresponding Folder",
            command=self.select_corresponding_folder,
            state=tk.DISABLED
        )
        self.btn_select_corresponding_folder.pack(side=tk.LEFT, padx=5)

        # Фрейм для отображения изображений
        self.image_frame = tk.Frame(self.root)
        self.image_frame.pack()

        # Метки для изображений
        self.corresponding_image_label = tk.Label(self.image_frame)
        self.corresponding_image_label.pack(side=tk.LEFT, padx=10)

        self.input_image_label = tk.Label(self.image_frame)
        self.input_image_label.pack(side=tk.LEFT, padx=10)

        # Кнопки сортировки
        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(pady=10)

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

        # Статус
        self.status_label = tk.Label(self.root, text="")
        self.status_label.pack(pady=10)

    def select_input_folder(self):
        self.input_folder = filedialog.askdirectory(title="Select Image Folder")

        if not self.input_folder:
            return

        # Создаем папки для сортировки
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

        # Активируем кнопку выбора папки
        self.btn_select_corresponding_folder.config(state=tk.NORMAL)

        # Загружаем первое изображение
        self.load_next_image()

    def select_corresponding_folder(self):
        self.corresponding_folder = filedialog.askdirectory(title="Select corresponding Folder")
        if self.corresponding_folder:
            self.load_next_image()  # Перезагружаем текущее изображение с учетом новой папки

    def load_next_image(self):
        if not self.image_files:
            messagebox.showinfo("Done", "All images processed!")
            self.btn_good.config(state=tk.DISABLED)
            self.btn_bad.config(state=tk.DISABLED)
            self.btn_error.config(state=tk.DISABLED)
            self.status_label.config(text="Processing complete!")
            return

        # Очищаем предыдущие изображения
        self.corresponding_image_label.config(image='')
        self.corresponding_image_label.image = None
        self.input_image_label.config(image='')
        self.input_image_label.image = None

        # Загружаем основное изображение
        self.current_image_path = os.path.join(self.input_folder, self.image_files[0])

        # Проверяем наличие соответствующего изображения
        self.current_corresponding_image_path = ""
        if self.corresponding_folder:
            corresponding_image_path = os.path.join(self.corresponding_folder, self.image_files[0])
            if os.path.exists(corresponding_image_path):
                self.current_corresponding_image_path = corresponding_image_path

        try:
            # Загружаем и отображаем изображения
            if self.current_corresponding_image_path:
                corresponding_img = Image.open(self.current_corresponding_image_path)
                corresponding_img.thumbnail((SIZE, SIZE))
                corresponding_photo = ImageTk.PhotoImage(corresponding_img)
                self.corresponding_image_label.config(image=corresponding_photo)
                self.corresponding_image_label.image = corresponding_photo
                self.corresponding_image_label.pack(side=tk.LEFT, padx=5)
            else:
                self.corresponding_image_label.pack_forget()

            input_img = Image.open(self.current_image_path)
            input_img.thumbnail((SIZE, SIZE))
            input_photo = ImageTk.PhotoImage(input_img)
            self.input_image_label.config(image=input_photo)
            self.input_image_label.image = input_photo
            self.input_image_label.pack(side=tk.LEFT, padx=5)

            # Активируем кнопки сортировки
            self.btn_good.config(state=tk.NORMAL)
            self.btn_bad.config(state=tk.NORMAL)
            self.btn_error.config(state=tk.NORMAL)

            # Обновляем статус
            self.status_label.config(text=f"Remaining: {len(self.image_files)}")

        except Exception as e:
            print(f"Error loading images: {e}")
            self.image_files.pop(0)
            self.load_next_image()

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

        try:
            shutil.move(self.current_image_path, dst)
            print(f"Image moved to '{action}': {filename}")

            # Удаляем текущий файл из списка
            self.image_files.pop(0)

            # Загружаем следующее изображение
            self.load_next_image()

        except Exception as e:
            print(f"Error moving file: {e}")
            messagebox.showerror("Error", f"Failed to move file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSorterApp(root)
    root.mainloop()
