import random
import string
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def img_process(dir, digits):
    try:
        password = []
        im = Image.open(dir).convert('L')
        img_width, img_height = im.width, im.height
        if img_width == 0 or img_height == 0:
            raise ValueError("Invalid image dimensions.")
        if alpha_var.get():
            vals = string.ascii_letters
            rand_vals = [vals[random.randint(0, 51)] for _ in range(256)]
        if num_var.get():
            vals = string.digits
            rand_vals = [vals[random.randint(0, 9)] for _ in range(256)]
        if sym_var.get():
            vals = string.punctuation
            rand_vals = [vals[random.randint(0, 31)] for _ in range(256)]
        if random_var.get():
            vals = string.printable
            rand_vals = [vals[random.randint(0, 93)] for _ in range(256)]

        for i in range(digits):
            rand_width = random.randint(0, img_width - 1)
            rand_height = random.randint(0, img_height - 1)
            pixel_value = im.getpixel((rand_width, rand_height))
            password.append(rand_vals[pixel_value])
        return ''.join(password)
    except Exception as e:
        raise ValueError(f"Error in image processing: {e}")

def get_img():
    global file_path, label_img_disp
    file_path = filedialog.askopenfilename(
        title="Select an Image", 
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")]
    )
    if file_path:
        label_img.config(text=f"Selected Image:")
        img = Image.open(file_path)
        img.thumbnail((250, 250))
        img = ImageTk.PhotoImage(img)
        label_img_disp.image = img
        label_img_disp.config(image=img)

def generate_password():
    try:
        if not file_path:
            raise ValueError("No image selected. Please select an image first.")
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
    global entry_digits, button_submit, label_img, label_img_disp, text_password, file_path, alpha_var, sym_var, num_var, random_var
    file_path = None
    root = tk.Tk()
    root.title("Password Generator from Image")
    root.geometry("600x400")
    root.resizable(True, True)

    try:
        logo = ImageTk.PhotoImage(Image.open('logo.png'))
        root.iconphoto(False, logo)
    except:
        pass

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

    alpha_var = tk.BooleanVar()
    radio_for_alpha = ttk.Checkbutton(root, text='Select if you want only alphabets in your password.', variable=alpha_var)
    radio_for_alpha.pack(pady=5)

    num_var = tk.BooleanVar()
    radio_for_num = ttk.Checkbutton(root, text='Select if you want only numbers in your password.', variable=num_var)
    radio_for_num.pack(pady=5)

    sym_var = tk.BooleanVar()
    radio_for_sym = ttk.Checkbutton(root, text='Select if you want only symbols in your password.', variable=sym_var)
    radio_for_sym.pack(pady=5)

    random_var = tk.BooleanVar()
    radio_for_random = ttk.Checkbutton(root, text='Select if you want your password to contain all characters.', variable=random_var)
    radio_for_random.pack(pady=5)

    entry_label = ttk.Label(root, text='Enter number of digits (greater than 0):')
    entry_label.pack(pady=5)

    entry_digits = ttk.Entry(root)
    entry_digits.pack(pady=5)

    label_img = ttk.Label(root, text='')
    label_img.pack(pady=5)

    label_img_disp = ttk.Label(root, image='')
    label_img_disp.pack(pady=5)

    button_submit = ttk.Button(root, text='Generate Password', command=generate_password)
    button_submit.pack(pady=5)

    text_password = tk.Text(root, height=5, width=50, font=('Helvetica', 12), wrap='word')
    text_password.pack(pady=10, expand=True, fill=tk.BOTH)
    text_password.config(state='disabled')

    root.mainloop()

gui_for_input()
