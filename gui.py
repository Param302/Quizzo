import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from PIL import Image, ImageTk
from database import QuizDB

"""
TODO:
>>> Select a better day theme
>>> Write doc of each method
>>> At starting, a button will display which ask start quiz, quit option. (CS quiz)

>>> After submitting, the button will forget and correct/incorrect with respective images will show
>>> Each mcq is of 10 point
>>> On top left, Current score label with ...->
>>> progress bar on top shows no of points out of total
>>> Meter on right of question shows time taken after 500 seconds and time left as it's label
>>> New question came after 3 seconds (within 3 seconds correct/incorrect will display)

>>> When End, table will be shown, showing total score out of TOTAL points, total correct, total incorrect out of TOTAL mcqs
>>> Also, asking for play again or quit option.
"""


class QuizApp(tk.Tk):
    DARK = True

    def __init__(self):
        super().__init__()
        self.title("Quizzo")
        self.geometry("1200x700+350+150")
        self.resizable(False, False)
        self.style = Style(theme="darkly")
        self.style.configure("Toolbutton", font=("Tahoma", 16))
        self.style.configure("TButton", font=("Tahoma", 18))

    def change_theme(self):
        self.style.theme_use(themename="flatly" if self.DARK else "darkly")
        self._img = ImageTk.PhotoImage(Image.open(
            "./moon.png" if self.DARK else "./sun.png").resize((30, 30)))
        self.theme_mode.configure(image=self._img)
        self.DARK = not self.DARK
        self.style.configure("Toolbutton", font=("Tahoma", 16))
        self.style.configure("TButton", font=("Tahoma", 18))

    def _header(self):
        self.header = ttk.Frame(self, style="TFrame")
        self.app_name = ttk.Label(self.header, text="Quizzo", font=("Tahoma", 26, "bold"),
                                  justify="center", style="warning.TLabel", padding=(550, 10, 460, 10))
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
        no, question, op_a, op_b, op_c, op_d, self.correct = next(self.mcq)
        # no, question, op_a, op_b, op_c, op_d, self.correct = next(self.mcq)
        # no, question, op_a, op_b, op_c, op_d, self.correct = next(self.mcq)
        # no, question, op_a, op_b, op_c, op_d, self.correct = next(self.mcq)
        # no, question, op_a, op_b, op_c, op_d, self.correct = next(self.mcq)
        # no, question, op_a, op_b, op_c, op_d, self.correct = next(self.mcq)

        print(no, question, op_a, op_b, op_c, op_d, self.correct)
        self.question = ttk.Label(self.quiz_area, text=f"Q{no}. {question}",
                                  font=("Arial", 22, "bold"), style="info.TLabel",
                                  wraplength=680, anchor="n", padding=(0, 8), width=45)
        self.question.place(x=250, y=90)

        width = len(max((op_a, op_b, op_c, op_d), key=len))+4
        self.options = ttk.Frame(self.quiz_area, style="TFrame")
        self.selected_option = tk.StringVar()
        self.op_a = ttk.Radiobutton(self.options, text=f"a. {op_a}",
                                    style="warning.Outline.Toolbutton", width=width,
                                    value="a", variable=self.selected_option)
        self.op_a.grid(row=0, column=0, padx=20, pady=30)

        self.op_b = ttk.Radiobutton(self.options, text=f"b. {op_b}",
                                    style="warning.Outline.Toolbutton", width=width,
                                    value="b", variable=self.selected_option)
        self.op_b.grid(row=0, column=1, padx=200-(width*2), pady=30)

        self.op_c = ttk.Radiobutton(self.options, text=f"c. {op_c}",
                                    style="warning.Outline.Toolbutton", width=width,
                                    value="c", variable=self.selected_option)
        self.op_c.grid(row=1, column=0, padx=20, pady=30)

        self.op_d = ttk.Radiobutton(self.options, text=f"d. {op_d}",
                                    style="warning.Outline.Toolbutton", width=width,
                                    value="d", variable=self.selected_option)
        self.op_d.grid(row=1, column=1, padx=200-(width*2), pady=30)
        self.options.place(x=350-(width*7 if width < 10 else width*5), y=210)

        self.submit = ttk.Button(self.quiz_area, text="Submit", style="info.TButton",
                                 padding=(30, 5), command=self.check_mcq)
        self.submit.place(x=540, y=450)
        # configure radio button
        # meter on right of question showing time
        # confirm button below
        # when press confirm user will get popped when answer is true or false,
        # and after 2 second, new question will load

        self.quiz_area.pack(side="top", fill="both", expand=1)

        ...

    def check_mcq(self):
        print(self.correct, self.selected_option.get())
        is_correct = False
        if self.correct == self.selected_option.get():
            print("Correct answer")
            is_correct = True
        else:
            print("Incorrect answer")
        self.update_options(self.selected_option.get(), is_correct)
        print("updated")
        self.quiz_area.after(3000, self.update_quiz)
        print("Called")

    def update_options(self, choosed, is_correct):
        self.option_widgets = {i[1]["value"]: i[1]
                               for i in self.options.children.items()}
        new_style = "success.Outline.Toolbutton" if is_correct else "danger.Outline.Toolbutton"
        self.option_widgets[choosed].configure(
            style=new_style, state="selected")

        for option, widget in self.option_widgets.items():
            if option == choosed:
                continue
            widget.configure(state="disabled")
        self.submit.configure(state="disabled")

    def update_quiz(self):
        try:
            no, question, op_a, op_b, op_c, op_d, self.correct = next(self.mcq)
        except StopIteration:
            print("END OF QUESTIONS")
            self.question.destroy()
            self.options.destroy()
            self.submit.destroy()
            self.total_score()
            return

        print("worked")
        self.question.configure(text=f"Q{no}. {question}")
        width = len(max((op_a, op_b, op_c, op_d), key=len))+4
        self.selected_option.set("")
        new_values = {"style": "warning.Outline.Toolbutton",
                      "width": width, "state": "active"}
        self.op_a.configure(text=f"a. {op_a}", **new_values)
        self.op_b.configure(text=f"b. {op_b}", **new_values)
        self.op_c.configure(text=f"c. {op_c}", **new_values)
        self.op_d.configure(text=f"d. {op_d}", **new_values)
        self.op_b.grid(padx=200-(width*2))
        self.op_d.grid(padx=200-(width*2))
        self.options.place_configure(x=370 if width < 15 else 350-(width*5))
        self.submit.configure(state="active")

    def total_score(self):
        end_label = ttk.Label(self.quiz_area, text="Quiz Ended !",
                              font=("Tahoma", 24, "bold"), style="info.TLabel")
        end_label.place(x=520, y=50)

    @staticmethod
    def get_mcqs():
        for i in QuizDB().get_all_mcq():
            yield i

    def run(self):
        self._header()
        self.quiz()
        self.mainloop()


if __name__ == "__main__":
    app = QuizApp()
    app.run()
