import tkinter as tk
from Calculator import Calculator

# ---------- CORE GUI ------------------------------ #

root = tk.Tk()
root.title("Calculator")
calculator = Calculator()
calc_frame = tk.Frame(root)
calc_frame.pack(padx=100, pady=50)

# ----------- LOCAL FUNCTIONS -----------------------------------------------#

# Opens new window to view calculation history
def check_history():
    history_window= tk.Toplevel(root, padx=100, pady=50)
    history_window.title('Calculation History')
    i = 0
    for e in calculator.calc_history:
        equation = tk.Label(history_window, text=str(calculator.calc_history[i]))
        equation.pack()
        i+=1

def set_num(n):
    if calculator.check_state() in ('RESULT_STATE', 'ERROR_STATE'):
        return
    display_label.config(text=f'{calculator.get_display_text(n)}')

def basic_calc():
    if calculator.check_state() != 'SECOND_STATE':
        return
    display_label.config(text=f'{calculator.basic_calc()}')


def delete():
    display_label.config(text=f'{calculator.delete()}')

def set_operator(name):
    if calculator.check_state() not in ("FIRST_STATE", "RESULT_STATE"):
        return
    calculator.set_operator(name)
    display_label.config(text=f'{name}')

def clear():
    calculator.clear()
    display_label.config(text=f'{calculator.clear()}')

# ----------------- BUTTONS AND LABELS ----------------------------------------------------------------------------------- #

display_label = tk.Label(calc_frame,text=calculator.last_num, font=('Arial', 20),borderwidth=2, relief='sunken', height=2)
display_label.grid(row=0, column=0, pady=5, padx=5, columnspan=5, stick='we')
history_btn = tk.Button(calc_frame, text='View Calculation History', command= lambda: check_history())
history_btn.grid(row=5, column=0, padx=5, pady=5, columnspan=4, stick='we')
equal_btn=tk.Button(calc_frame, text='=', height=2, width=5, command=lambda: basic_calc())
equal_btn.grid(row=1, column=4, rowspan=1, stick='ns', padx=5, pady=5)
backspace_btn = tk.Button(calc_frame, text='Delete', command=lambda: delete())
backspace_btn.grid(row=2, column = 4, rowspan=2, stick='sn', padx=5, pady=5)
clear_btn = tk.Button(calc_frame, text='Clear', command=lambda: clear(), width=5, height=2)
clear_btn.grid(row=4, column=4, rowspan=2, stick='ns', padx=5, pady=5)

# Uses a manual grid
num_buttons = [ # (num, row, column)

    (7, 1, 0), (8, 1, 1), (9, 1, 2),
    (4, 2, 0), (5, 2, 1), (6, 2, 2),
    (1, 3, 0), (2, 3, 1), (3, 3, 2),
    ('.', 4, 2)

]

operator_buttons = [ # (name, row, col)
    ('+', 1, 3),
    ('-', 2, 3),
    ('*', 3, 3),
    ('/', 4, 3),

]

# Pastes numbers one by one and links their name to the set_number function
for num, row, col in num_buttons:
    num_btn = tk.Button(calc_frame, text=str(num), width=5, height=2, command=lambda n=num: set_num(n))
    num_btn.grid(row=row, column=col, padx=5, pady=5)

# Zero needed to be bigger than the rest so it go its own separate sequence
zero_btn = tk.Button(calc_frame, text=str(0), width=5, height=2, command=lambda: set_num(0))
zero_btn.grid(row=4, column=0, padx=5, pady=5, columnspan=2, stick = 'we')

# Dealing with the operators much the same way
for name, row, col in operator_buttons:
    op_btn = tk.Button(calc_frame, text=str(name), width=5, height=2,
                       command=lambda n=name: set_operator(n))
    op_btn.grid(row=row, column=col, padx=5, pady=5)


root.mainloop()