import tkinter as tk
import json
import os

def theme():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    theme_dir = os.path.join(script_dir, 'theme')
    theme_file = os.path.join(theme_dir, 'theme.json')

    with open(theme_file, 'r') as f:
        settings = json.load(f)

    return settings



calc = ""
def click(button_text):
    global calc
    if button_text == "=":
        try:
            if "√" in calc:
                calc = str(((int(calc[1:])))**0.5)
            elif "^" in calc:
                calc = calc.replace("^", "**")
            result = eval(calc)
            calc = str(result)
        except Exception as e:
            calc = "Error"
            window.after(1, lambda: set_calc(""))
    elif button_text == "<":
        calc = calc[:-1]
    elif button_text == "C":
        calc = ""
    else:
        calc += button_text
    entry.delete(0, tk.END)
    entry.insert(tk.END, calc)
    entry.update_idletasks()
    
def set_calc(value):
    global calc
    calc = value

def create_button(window, button_text, theme, row_idx, col_idx):
    if button_text:
        btn_name = button_text
        if btn_name in "0123456789.()":
            btn_style = theme["BTN_NUMER"]
        elif btn_name in "+-*/":
            btn_style = theme["BTN_OPER"]
        elif btn_name == "C":
            btn_style = theme["BTN_CLEAR"]
        else:
            btn_style = theme["BTN_DEFAULT"]

        button = tk.Button(
            window,
            text=button_text,
            font=("Arial", 20),
            padx=3,
            pady=2,
            bg=btn_style["bg"],
            fg=btn_style["fg"],
            activebackground=btn_style["activebackground"],
            activeforeground=btn_style["activeforeground"],
            command=lambda text=button_text: click(text),
        )
        button.grid(
            row=row_idx + 1,
            column=col_idx,
            columnspan=3 if button_text == "." else 1,
            rowspan=2 if button_text == "=" else 1,
            sticky="nsew",
        )

def apply_theme(theme):
    window.config(bg=theme["master_bg"])
    entry.config(bg=theme["INPUT"]["bg"], fg=theme["INPUT"]["fg"], font=theme["INPUT"]["font"], justify=theme["INPUT"]["justify"])

    for widget in window.winfo_children():
        if isinstance(widget, tk.Button):
            btn_name = widget.cget("text")

            if btn_name in "0123456789.()":
                btn_style = theme["BTN_NUMER"]
            elif btn_name in "+-*/":
                btn_style = theme["BTN_OPER"]
            elif btn_name == "C":
                btn_style = theme["BTN_CLEAR"]
            else:
                btn_style = theme["BTN_DEFAULT"]

            widget.config(
                bg=btn_style["bg"],
                fg=btn_style["fg"],
                activebackground=btn_style["activebackground"],
                activeforeground=btn_style["activeforeground"],
                font=theme["global"]["font"],
                borderwidth=theme["global"]["borderwidth"],
                highlightthickness=theme["global"]["highlightthickness"],
                width=theme["global"]["width"],
                height=theme["global"]["height"]
            )
if __name__ == "__main__":
    window = tk.Tk()
    window.title("Calculator")
    window.geometry("400x500")
    window.resizable(False, False)

    settings = theme()
    current_theme = settings["current_theme"]
    theme = next((t for t in settings["themes"] if t["name"] == current_theme), None)
    if not theme:
        theme = settings["themes"][0]
    entry = tk.Entry(window, font=("Arial", 30))
    entry.grid(row=0, column=0, columnspan=5, sticky="nsew")

    apply_theme(theme)

    buttons = [
        ("7", "8", "9", "C", "/"),
        ("4", "5", "6", "√", "*"),
        ("1", "2", "3", "<", "+"),
        ("0", "(", ")", "-", "="),
        (".", None, None, "^"),
    ]

    for row_idx, row in enumerate(buttons):
        for col_idx, button_text in enumerate(row):
            create_button(window, button_text, theme, row_idx, col_idx)

    for i in range(5):
        window.grid_columnconfigure(i, weight=1)
    for i in range(len(buttons) + 1):
        window.grid_rowconfigure(i, weight=1)

    window.mainloop()