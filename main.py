import random
import string
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def img_process(dir, digits):
    password = []
    im = Image.open(dir).convert('L')
    img_width, img_height = im.width, im.height
    vals = string.printable
    rand_vals = [vals[random.randint(0, 93)] for _ in range(256)]
    for i in range(digits):
        rand_width = random.randint(0, img_width - 1)
        rand_height = random.randint(0, img_height - 1)
        pixel_value = im.getpixel((rand_width, rand_height))
        password.append(rand_vals[pixel_value])
    return ''.join(password)

def get_img():
    global file_path
    file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")])
    if file_path:
        label_img.config(text=f"Selected Image: {file_path}")

def generate_password():
    try:
        digits = int(entry_digits.get())
        if digits <= 0:
            raise ValueError("Number of digits should be positive.")
        
        password = img_process(file_path, digits)
        
        text_password.config(state='normal')
        text_password.delete('1.0', tk.END)
        text_password.insert(tk.END, password)
        text_password.config(state='disabled')
    except Exception as e:
        messagebox.showerror("Error", str(e))

def gui_for_input():
    global entry_digits, button_submit, label_img, text_password
    
    root = tk.Tk()
    root.title("Password Generator from Image")
    
    root.geometry("600x400")
    
    logo = ImageTk.PhotoImage(Image.open('logo.png'))
    root.iconphoto(False, logo)
    
    root.resizable(True, True)
    
    style = ttk.Style()
    style.configure('TLabel', font=('Helvetica', 12))
    style.configure('TButton', font=('Helvetica', 12))
    style.configure('TEntry', font=('Helvetica', 12))
    
    label1 = ttk.Label(root, text='Please select the image and enter the number of digits:')
    label1.pack(pady=10)
    
    label2 = ttk.Label(root, text='Make sure that the images are busy and not bland, which could result in weaker passwords!')
    label2.pack(pady=10)
    
    button1 = ttk.Button(root, text='Select Image', command=get_img)
    button1.pack(pady=5)

    entry_label = ttk.Label(root, text='Enter number of digits (greater than 0):')
    entry_label.pack(pady=5)

    entry_digits = ttk.Entry(root)
    entry_digits.pack(pady=5)

    label_img = ttk.Label(root, text='')
    label_img.pack(pady=5)
    
    button_submit = ttk.Button(root, text='Generate Password', command=generate_password)
    button_submit.pack(pady=5)

    text_password = tk.Text(root, height=5, width=50, font=('Helvetica', 12), wrap='word')
    text_password.pack(pady=10, expand=True, fill=tk.BOTH)
    text_password.config(state='disabled')
    
    root.mainloop()

gui_for_input()
