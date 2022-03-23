import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
import matplotlib.pyplot as plt
from PIL import Image, ImageTk


root = tk.Tk()
root.title("Quizzo")
root.geometry("1200x700+350+150")
root.resizable(False, False)
style = Style(theme="darkly")

header = ttk.Frame(root, )
app_name = ttk.Label(header, text="Quizzo", font=("Tahoma", 24, "bold"),
                            justify="center", style="warning.TLabel")
app_name.grid(sticky="nw")
def load():
    global z
    y = Image.open("./moon.png").resize((200, 200))
    print(y)
    z = ImageTk.PhotoImage(y)
    print(z)
load()
def show():
    theme_mode = ttk.Button(
        header, text="hello", image=z, style="warning.TButton")
    theme_mode.grid(row=0, column=1)
    print(theme_mode["image"])
show()
header.pack(side="top", fill="x")

root.mainloop()
