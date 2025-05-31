import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
import cv2
import numpy as np

def sharpen_image(image):
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    return cv2.filter2D(image, -1, kernel)

def unsharp_mask(image, blur_ksize=(5, 5), strength=1.5):
    blurred = cv2.GaussianBlur(image, blur_ksize, 0)
    sharpened = cv2.addWeighted(image, 1 + strength, blurred, -strength, 0)
    return sharpened

def restore_image(img_path):
    try:
        pil_image = Image.open(img_path).convert('RGB')
        image = np.array(pil_image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        sharpened = sharpen_image(image)
        final = unsharp_mask(sharpened)
        return pil_image, Image.fromarray(cv2.cvtColor(final, cv2.COLOR_BGR2RGB))
    except Exception as e:
        print(f"Помилка при обробці зображення: {e}")
        messagebox.showerror("Помилка", f"Не вдалося обробити зображення:\n{e}")
        return None, None

def open_file():
    global current_image
    file_path = filedialog.askopenfilename(filetypes=[
        ("Image files", "*.png *.jpg *.jpeg *.bmp *.webp"),
        ("All files", "*.*")
    ])
    if file_path:
        original, restored = restore_image(file_path)
        if original and restored:
            current_image = restored
            show_images_side_by_side(original, restored)

def show_images_side_by_side(img1, img2):
    img1_resized = img1.resize((350, 300))
    img2_resized = img2.resize((350, 300))

    img1_with_border = ImageOps.expand(img1_resized, border=2, fill='white')
    img2_with_border = ImageOps.expand(img2_resized, border=2, fill='white')

    img1_tk = ImageTk.PhotoImage(img1_with_border)
    img2_tk = ImageTk.PhotoImage(img2_with_border)

    panel_original.config(image=img1_tk)
    panel_original.image = img1_tk

    panel_restored.config(image=img2_tk)
    panel_restored.image = img2_tk

def save_image():
    if current_image is None:
        messagebox.showwarning("Увага", "Спочатку завантажте зображення")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"),
                                                        ("JPEG files", "*.jpg"),
                                                        ("All files", "*.*")])
    if file_path:
        current_image.save(file_path)
        messagebox.showinfo("Готово", "Зображення збережено успішно!")

# === GUI ===
current_image = None
root = tk.Tk()
root.title("Відновлення зображень")
root.geometry("1000x650")
root.configure(bg="#2c2f33")

# Стиль заголовка
title_label = tk.Label(root, text="🖼️ Відновлення розмитих зображень", font=("Helvetica", 20, "bold"),
                       fg="#ffffff", bg="#2c2f33")
title_label.pack(pady=20)

# Кнопки
btn_frame = tk.Frame(root, bg="#2c2f33")
btn_frame.pack(pady=10)

style = {"font": ("Helvetica", 12, "bold"), "padx": 14, "pady": 8, "bd": 0}

btn_load = tk.Button(btn_frame, text="📂 Завантажити", command=open_file,
                     bg="#BA324F", fg="white", activebackground="#A02E47", **style)
btn_load.grid(row=0, column=0, padx=10)

btn_save = tk.Button(btn_frame, text="💾 Зберегти", command=save_image,
                     bg="#4BA3C3", fg="white", activebackground="#1565c0", **style)
btn_save.grid(row=0, column=1, padx=10)

# Рамка зображень
image_frame = tk.Frame(root, bg="#2c2f33")
image_frame.pack(pady=20)

label_style = {"font": ("Helvetica", 13, "bold"), "fg": "#ffffff", "bg": "#2c2f33"}

panel_original = tk.Label(image_frame, bg="#2c2f33")
panel_original.grid(row=1, column=0, padx=25)

panel_restored = tk.Label(image_frame, bg="#2c2f33")
panel_restored.grid(row=1, column=1, padx=25)

label_original = tk.Label(image_frame, text="Оригінал", **label_style)
label_original.grid(row=0, column=0, pady=5)

label_restored = tk.Label(image_frame, text="Відновлене", **label_style)
label_restored.grid(row=0, column=1, pady=5)

root.mainloop()
