import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from PIL import Image, ImageTk
from database import QuizDB


class QuizApp(tk.Tk):
    DARK = True

    def __init__(self):
        super().__init__()
        self.title("Quizzo")
        self.geometry("1200x700+350+150")
        # self.resizable(False, False)
        self.style = Style(theme="darkly")
        self.style.configure("Toolbutton", font=("Tahoma", 16))

    def change_theme(self):
        self.style.theme_use(themename="flatly" if self.DARK else "darkly")
        self._img = ImageTk.PhotoImage(Image.open(
            "./moon.png" if self.DARK else "./sun.png").resize((30, 30)))
        self.theme_mode.configure(image=self._img)
        self.DARK = not self.DARK
        self.style.configure("Toolbutton", font=("Tahoma", 16))

    def _header(self):
        self.header = ttk.Frame(self, style="TFrame")
        self.app_name = ttk.Label(self.header, text="Quizzo", font=("Tahoma", 24, "bold"),
                                  justify="center", style="warning.TLabel", padding=(510, 5))
        self.app_name.grid(sticky="nw", row=0, column=0)
        self._img = ImageTk.PhotoImage(
            Image.open("./sun.png").resize((30, 30)))
        self.theme_mode = ttk.Button(
            self.header, image=self._img, style="warning.Outline.TButton", command=self.change_theme)
        self.theme_mode.grid(row=0, column=1)
        self.header.pack(side="top", fill="x")

        self.sep1 = ttk.Separator(self, orient="horizontal",
                                  style="warning.Horizontal.TSeparator")
        self.sep1.pack(side="top", fill="x")

    def quiz(self):
        self.quiz_area = ttk.Frame(self, style="TFrame")
        self.mcq = self.get_mcqs()
        no, question, op_a, op_b, op_c, op_d, correct = next(self.mcq)
        no, question, op_a, op_b, op_c, op_d, correct = next(self.mcq)
        # no, question, op_a, op_b, op_c, op_d, correct = next(self.mcq)
        # no, question, op_a, op_b, op_c, op_d, correct = next(self.mcq)
        # no, question, op_a, op_b, op_c, op_d, correct = next(self.mcq)
        # no, question, op_a, op_b, op_c, op_d, correct = next(self.mcq)

        print(no, question, op_a, op_b, op_c, op_d, correct)
        width = len(max((op_a, op_b, op_c, op_d), key=len))+4
        self.question = ttk.Label(self.quiz_area, text=f"Q{no}. {question}",
                                  font=("Tahoma", 20), style="info.TLabel",
                                  wraplength=680, anchor="n", padding=(0, 8), width=45)
        self.question.place(x=250, y=100)
        self.op_var = tk.StringVar()
        self.op_a = ttk.Radiobutton(self.quiz_area, text=f"a. {op_a}",
                               style="warning.Outline.Toolbutton", width=width, value="a", variable=self.op_var)
        self.op_a.place(x=300-(width*3), y=230)

        self.op_b = ttk.Radiobutton(self.quiz_area, text=f"b. {op_b}",
                               style="warning.Outline.Toolbutton", width=width, value="b", variable=self.op_var)
        self.op_b.place(x=600+width, y=230)

        self.op_c = ttk.Radiobutton(self.quiz_area, text=f"c. {op_c}",
                               style="warning.Outline.Toolbutton", width=width, value="c", variable=self.op_var)
        self.op_c.place(x=300-(width*3), y=350)

        self.op_d = ttk.Radiobutton(self.quiz_area, text=f"d. {op_d}",
                               style="warning.Outline.Toolbutton", width=width, value="d", variable=self.op_var)
        self.op_d.place(x=600+width, y=350)

        # configure radio button
        # spinbox on right of question showing time
        # confirm button below
        # when press confirm user will get popped when answer is true or false, 
        # and after 2 second, new question will load

        self.quiz_area.pack(side="top", fill="both", expand=1)

        ...

    def get_mcqs(self):
        for i in QuizDB().get_all_mcq():
            yield i

    def run(self):
        self._header()
        self.quiz()
        self.mainloop()


if __name__ == "__main__":
    app = QuizApp()
    app.run()
