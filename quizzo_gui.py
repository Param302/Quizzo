import os
import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style, Meter
from PIL import Image, ImageTk
from database import QuizDB


class QuizApp(tk.Tk):
    DARK = True
    image_path = os.getcwd() + "/"
    # folder name added in path, for $ python quizzo
    image_path += "quizzo/" if "quizzo" not in os.getcwd() else ""
    image_path += "assets"

    def __init__(self):
        super().__init__()
        self.title("Quizzo")
        self.iconbitmap(f"{self.image_path}/icon.ico")
        self.geometry("1200x700+350+150")
        self.resizable(False, False)
        self.style = Style(theme="darkly")
        # changing some properties
        self.style.configure("Toolbutton", font=("Tahoma", 16))
        self.style.configure("TButton", font=("Tahoma", 18), justify="center")
        self.quiz_db = QuizDB()

    def _header(self):
        """Makes header for the window having App name and day-night btn"""

        self.header = ttk.Frame(self, style="TFrame")
        self.app_name = ttk.Label(self.header, text="Quizzo", font=("Tahoma", 26, "bold"),
                                  justify="center", style="warning.TLabel", padding=(550, 10, 460, 10))
        self.app_name.grid(sticky="nw", row=0, column=0)
        self._img = ImageTk.PhotoImage(
            Image.open(f"{self.image_path}/sun.png").resize((30, 30)))
        self.theme_mode = ttk.Button(
            self.header, image=self._img, style="warning.Outline.TButton", command=self._change_theme)
        self.theme_mode.grid(row=0, column=1)
        self.header.pack(side="top", fill="x")

        self.sep1 = ttk.Separator(self, orient="horizontal",
                                  style="warning.Horizontal.TSeparator")
        self.sep1.pack(side="top", fill="x")

    def _starting_win(self):
        """Make starting window, ask from user to Play / QUIT, 
        or to Add / delete a question"""

        frame_1 = ttk.Frame(self, style="TFrame")
        start_lbl = ttk.Label(frame_1, text="Start Quiz ?\nTopic: Networking (CS)",
                              font=("Tahoma", 24), style="info.TLabel",
                              justify="center", padding=(60, 5))
        start_lbl.place(x=380, y=150)
        start_btn = ttk.Button(frame_1, text="Start", style="success.TButton", padding=(40, 5),
                               # delete this frame and start quiz
                               command=lambda: frame_1.destroy() or self._quiz_window())
        start_btn.place(x=450, y=300)
        start_btn.focus_force()
        quit_btn = ttk.Button(frame_1, text="Quit", style="danger.TButton",
                              padding=(40, 5), command=self.destroy)
        quit_btn.place(x=650, y=300)
        self.add_img = ImageTk.PhotoImage(
            Image.open(f"{self.image_path}/add.png").resize((30, 30)))
        add_btn = ttk.Button(frame_1, text="  Add question", image=self.add_img, compound="left",
                             style="success.Outline.TButton", padding=(30, 5), command=self._add_mcq)
        add_btn.place(x=500, y=400)
        self.del_img = ImageTk.PhotoImage(
            Image.open(f"{self.image_path}/delete.png").resize((30, 30)))
        del_btn = ttk.Button(frame_1, text=" Delete question", image=self.del_img, compound="left",
                             style="danger.Outline.TButton", padding=(20, 5), command=self._delete_mcq)
        del_btn.place(x=500, y=480)
        frame_1.pack(side="top", fill="both", expand=1)

    def _quiz_window(self):
        """Make Quiz Window
        Ask Question with a duration of 10 seconds
        Shows score, question, timer, options and a submit button."""

        self.quiz_area = ttk.Frame(self, style="TFrame")
        self.mcq = self._get_mcqs()
        self.current_score = 0
        self.time_spent = 0
        self.correct, self.incorrect, self.unattempted = 0, 0, 0
        no, question, op_a, op_b, op_c, op_d, \
            self.correct_option = next(self.mcq)

        self.current_score_lbl = ttk.Label(self.quiz_area, text="Score:  0",
                                           font=("Arial", 18), style="primary.TLabel")
        self.current_score_lbl.place(x=50, y=20)
        self.timer = Meter(self.quiz_area, amounttotal=10, amountused=0,
                           metersize=150, textfont=("Arial", 40, "bold"), bootstyle="info.TMeter")
        self.timer.place(x=1000, y=20)
        # updating meter after 1 second, storing it's id to cancel when time ends
        self.call_id = self.timer.after(1000, self._update_time)
        self.question = ttk.Label(self.quiz_area, text=f"Q{no}. {question}",
                                  font=("Arial", 22, "bold"), style="info.TLabel",
                                  wraplength=680, anchor="n", padding=(0, 8), width=45)
        self.question.place(x=250, y=90)
        # calculating width for size of options and padding
        width = len(max((op_a, op_b, op_c, op_d), key=len))+4

        # ---------------- Options Frame ----------------
        self.options = ttk.Frame(self.quiz_area, style="TFrame")
        self.selected_option = tk.StringVar()
        self.op_a = ttk.Radiobutton(self.options, text=f"a. {op_a}",
                                    style="warning.Outline.Toolbutton", width=width,
                                    value="a", variable=self.selected_option)
        self.op_a.grid(row=0, column=0, padx=20, pady=30)

        self.op_b = ttk.Radiobutton(self.options, text=f"b. {op_b}",
                                    style="warning.Outline.Toolbutton", width=width,
                                    value="b", variable=self.selected_option, )
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
                                 padding=(30, 5), command=self._check_answer)
        self.submit.place(x=540, y=450)

        self.quiz_area.pack(side="top", fill="both", expand=1)

    def _end_display(self):
        """Display End screen and shows:
        Total score, Your score, correct, incorrect, unattempted.
        Also, ask user to play again or quit."""

        end_frame = ttk.Frame(self, style="TFrame")
        end_label = ttk.Label(end_frame, text="Quiz Summary",
                              font=("Tahoma", 28, "bold", "underline"), style="info.TLabel")
        end_label.place(x=500, y=20)

        total_score = ttk.Label(end_frame, font=("Arial", 20), style="success.TLabel",
                                text=f"Total Score: {(self.correct+self.incorrect+self.unattempted)*10}")
        total_score.place(x=450, y=100)

        your_score = ttk.Label(end_frame, text=f"Your Score: {self.current_score}",
                               font=("Arial", 20), style="info.TLabel")
        your_score.place(x=450, y=150)
        correct = ttk.Label(end_frame, text=f"No. of Correct answers: {self.correct}",
                            font=("Arial", 20), style="success.TLabel")
        correct.place(x=450, y=200)
        incorrect = ttk.Label(end_frame, text=f"No. of Incorrect answers: {self.incorrect}",
                              font=("Arial", 20), style="danger.TLabel")
        incorrect.place(x=450, y=250)
        correct = ttk.Label(end_frame, text=f"Unattempted: {self.unattempted}",
                            font=("Arial", 20), style="warning.TLabel")
        correct.place(x=450, y=300)

        play_again = ttk.Label(end_frame, text="Want to Play again ?", font=("Tahoma", 24),
                               style="info.TLabel", justify="center", padding=(60, 5))
        play_again.place(x=400, y=400)
        start_btn = ttk.Button(end_frame, text="Yes", style="success.Outline.TButton", padding=(40, 5),
                               command=lambda: end_frame.destroy() or self._quiz_window())
        start_btn.place(x=450, y=500)
        quit_btn = ttk.Button(end_frame, text="Quit", style="danger.Outline.TButton",
                              padding=(40, 5), command=self.destroy)
        quit_btn.place(x=650, y=500)

        end_frame.pack(side="top", fill="both", expand=1)

    def _add_mcq(self):
        """A new window - takes all required fields and 
        store that mcq in the database."""

        add_win = tk.Toplevel(self)
        add_win.focus()
        add_win.title("ADD QUESTION - QUIZZO")
        add_win.geometry("800x500+500+300")
        add_win.resizable(False, False)
        ques_lbl = ttk.Label(add_win, text="Enter question: ",
                             style="info.TLabel", font=("Tahoma", 16), padding=10)
        ques_lbl.place(x=100, y=50)
        question = tk.Text(add_win)
        question.config(font=("Arial", 18), highlightcolor=self.style.colors.info,
                        highlightbackground=self.style.colors.info, width=50, height=3,)
        question.place(x=110, y=100)
        properties = {"style": "warning.TLabel",
                      "font": ("Tahoma", 16), "padding": 10}
        ttk.Label(add_win, text="a.", **properties).place(x=100, y=220)
        op_a = ttk.Entry(add_win, font=("Arial", 18),
                         style="warning.TEntry", width=30)
        op_a.place(x=140, y=220)
        ttk.Label(add_win, text="b.", **properties).place(x=100, y=280)
        op_b = ttk.Entry(add_win, font=("Arial", 18),
                         style="warning.TEntry", width=30)
        op_b.place(x=140, y=280)
        ttk.Label(add_win, text="c.", **properties).place(x=100, y=340)
        op_c = ttk.Entry(add_win, font=("Arial", 18),
                         style="warning.TEntry", width=30)
        op_c.place(x=140, y=340)
        ttk.Label(add_win, text="d.", **properties).place(x=100, y=400)
        op_d = ttk.Entry(add_win, font=("Arial", 18),
                         style="warning.TEntry", width=30)
        op_d.place(x=140, y=400)
        ttk.Label(add_win, text="Correct", font=("Tahoma", 16),
                  style="success.TLabel").place(x=640, y=220)
        correct = ttk.Entry(add_win, font=("Arial", 18),
                            justify="center", style="success.TEntry", width=5)
        correct.place(x=640, y=260)
        add = ttk.Button(add_win, text="Add\nQuestion", style="info.TButton", width=10, command=lambda:
                         # if all fields are filled only then it will be inserted into database.
                         self.quiz_db.insert_mcq(*x) if all(x := (question.get(0.0, "end").strip(),
                                                                  op_a.get(), op_b.get(), op_c.get(), op_d.get(), correct.get(), correct.get() in 'abcd')) else None)

        add.place(x=600, y=320)
        add_win.mainloop()
        self.focus()

    def _delete_mcq(self):
        """A new window - takes question no and
        delete that question from database, if qno is correct."""

        del_win = tk.Toplevel(self)
        del_win.focus()
        del_win.title("DELETE QUESTION - QUIZZO")
        del_win.geometry("400x300+800+400")
        del_win.resizable(False, False)
        ttk.Label(del_win, text="Enter Question no.", font=("Tahoma", 16),
                  style="warning.TLabel").place(x=110, y=50)
        question_no = ttk.Entry(del_win, font=("Arial", 18),
                                style="info.TEntry", width=10)
        question_no.place(x=120, y=90)
        show_lbl = ttk.Label(del_win, text="", font=(
            "Tahoma", 16), width=25, justify="center")
        show_lbl.place(x=80, y=150)

        def validate_qno():
            """Check if provided question no is in the database or not.
            If yes, then delete it."""
            n = int(question_no.get())
            # all mcqs are list of tuples, * will unpack the list
            # zipped them, 1st element will have all the question nos. (1, 2, 3, 4, 5,...)
            if n not in next(zip(*self.quiz_db.get_all_mcq())):
                show_lbl.config(style="danger.TLabel",
                                text="Enter a valid question no.")
                return
            self.quiz_db.delete_mcq(n)
            show_lbl.config(style="success.TLabel",
                            text="Question deleted!")

        del_btn = ttk.Button(del_win, text="Delete\nquestion",
                             style="danger.TButton", width=12, command=validate_qno)
        del_btn.place(x=100, y=200)
        del_win.mainloop()
        self.focus()

    def _change_theme(self):
        """Change night mode to day mode and vice-versa."""
        self.style.theme_use(themename="flatly" if self.DARK else "darkly")
        self._img = ImageTk.PhotoImage(Image.open(
            self.image_path + ("moon.png" if self.DARK else "sun.png")).resize((30, 30)))
        self.theme_mode.configure(image=self._img)
        self.DARK = not self.DARK

        # manually changing properties again uuggghhhh...
        self.style.configure("Toolbutton", font=("Tahoma", 16))
        self.style.configure("TButton", font=("Tahoma", 18), justify="center")

    def _update_time(self):
        """Updates time of meter"""
        self.time_spent += 1
        # self.timer.step() is making issues so...
        self.timer.configure(amountused=self.time_spent)
        if self.time_spent != 10:   # if not 10 seconds spent, update time again
            self.call_id = self.timer.after(1000, self._update_time)
            return
        # if user doesn't selected any option, selected_option will set to None
        if not self.selected_option.get():
            self.selected_option.set("None")
        # checking answer if time over...
        self._check_answer()
        return

    def _check_answer(self):
        """Check user selected answer.
        If correct marked as Correct,
        If wrong, marked as Incorrect,
        If not attempted marked as Unattempted."""

        choosed = self.selected_option.get()
        if not choosed:
            return  # if user abuses submit button without choosing
        # stop updating time
        self.timer.after_cancel(self.call_id)
        self.submit.place_forget()
        is_correct = False
        if self.correct_option == choosed:
            is_correct = True
            self.correct += 1
            self.current_score += 10
            self.current_score_lbl.config(text=f"Score: {self.current_score}")
            text = "correct"
        elif choosed == "None":
            self.unattempted += 1
            text = "Unattempted"
        else:
            self.incorrect += 1
            text = "incorrect"

        self.img = ImageTk.PhotoImage(      # shows appropriate image with text
            Image.open(f"{self.image_path}/{text}.png").resize((50, 50)))
        self.show_result = ttk.Label(self.quiz_area, text=text.capitalize(),
                                     font=("Tahoma", 22), image=self.img, compound="left",
                                     style=f"{'success' if is_correct else 'danger'}.TLabel")
        self.show_result.place(x=530, y=450)
        # freeze options and btn for 2 seconds and then update quiz
        self._freeze_options(choosed, is_correct)
        self.quiz_area.after(2000, self._update_quiz)

    def _freeze_options(self, choosed, is_correct):
        """Disabled rest of the options with submit btn and 
        selected option remains selected until 2 seconds.
        """
        # getting all options with values using
        # `children` property which returns a dict
        #     value   : widget
        self.option_widgets = {i[1]["value"]: i[1]
                               for i in self.options.children.items()}
        # change color of selected option accordingly,
        # if any of the options selected
        new_style = "success.Outline.Toolbutton" if is_correct else "danger.Outline.Toolbutton"
        if choosed != "None":
            self.option_widgets[choosed].configure(
                style=new_style, state="selected")
        # disabling rest options and submit btn
        for option, widget in self.option_widgets.items():
            if option == choosed:
                continue
            widget.configure(state="disabled")
        self.submit.configure(state="disabled")

    def _update_quiz(self):
        """Update the quiz, shows new quiz, if question(s) left
        else show end screen..."""

        self.show_result.destroy()
        try:
            no, question, op_a, op_b, op_c, op_d, self.correct_option = next(
                self.mcq)
        # if no more questions left
        except StopIteration:
            # destroying quiz frame
            self.quiz_area.destroy()
            self._end_display()
            return

        # updating mcq
        self.submit.configure(state="normal")
        self.submit.place_configure(x=540, y=450)
        self.question.configure(text=f"Q{no}. {question}")
        # again, calculating width for options & padding
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
        self.timer.configure(amountused=0)
        self.time_spent = 0
        self.call_id = self.timer.after(1000, self._update_time)
        self.options.place_configure(x=370 if width < 15 else 350-(width*5))

    def _get_mcqs(self):
        """Generate a MCQ"""
        for i in self.quiz_db.get_all_mcq():
            yield i

    def run(self):
        """Run the GUI.
        Call all required methods."""

        self._header()
        self._starting_win()
        self.mainloop()
        self.quiz_db.close()


if __name__ == "__main__":
    app = QuizApp()
    app.run()
