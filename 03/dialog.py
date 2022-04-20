from tkinter import *
import logic


def show_add_name_dialog(master, fnt, check_name_func, add_name_func):
    def create_button_clicked():
        dialog.focus()
        name = name_entry.get()
        if check_name_func(name) == -1:
            logic.change_color(name_entry, 'red')
            return

        code = code_entry.get().strip()
        if code == '':
            logic.change_color(code_entry, 'red')
            return

        recode = recode_entry.get().strip()
        if recode != code:
            logic.change_color(recode_entry, 'red')
            return

        add_name_func(name, code)
        dialog.destroy()

    dialog = Toplevel(master)
    dialog.title('Новый профиль')
    dialog.geometry('400x200+450+250')
    dialog.resizable(width=False, height=False)

    frame = Frame(dialog, bg='white')

    name_label = Label(frame, text='Название:', font=f'Arial {fnt}', bg='white', anchor='w')
    code_label = Label(frame, text='Секретный код:', font=f'Arial {fnt}', bg='white', anchor='w')
    recode_label = Label(frame, text='Повторите код:', font=f'Arial {fnt}', bg='white', anchor='w')

    name_entry = Entry(frame, font=f'Arial {fnt}', relief='solid')
    code_entry = Entry(frame, font=f'Arial {fnt}', relief='solid', show='*')
    recode_entry = Entry(frame, font=f'Arial {fnt}', relief='solid', show='*')

    cancel_button = Button(frame, text='Отмена', font=f'Arial {fnt}', bg='white')
    create_button = Button(frame, text='Создать', font=f'Arial {fnt}', bg='white')

    frame.place(anchor='nw', relx=0, relwidth=1, rely=0, relheight=1)
    name_label.place(anchor='nw', relx=0.0415, relwidth=0.9, rely=0.01, relheight=0.12)
    name_entry.place(anchor='n', relx=0.5, relwidth=0.9, rely=0.14, relheight=0.12)
    code_label.place(anchor='nw', relx=0.0415, relwidth=0.9, rely=0.27, relheight=0.12)
    code_entry.place(anchor='n', relx=0.5, relwidth=0.9, rely=0.40, relheight=0.12)
    recode_label.place(anchor='nw', relx=0.0415, relwidth=0.9, rely=0.53, relheight=0.12)
    recode_entry.place(anchor='n', relx=0.5, relwidth=0.9, rely=0.66, relheight=0.12)
    cancel_button.place(anchor='ne', relx=0.48, relwidth=0.4, rely=0.83, relheight=0.12)
    create_button.place(anchor='nw', relx=0.52, relwidth=0.4, rely=0.83, relheight=0.12)

    cancel_button['command'] = dialog.destroy
    create_button['command'] = create_button_clicked
    name_entry.bind('<FocusIn>', lambda _: logic.change_color(name_entry, 'white'))
    name_entry.bind('<Return>', lambda _: code_entry.focus())
    code_entry.bind('<FocusIn>', lambda _: logic.change_color(code_entry, 'white'))
    code_entry.bind('<Return>', lambda _: recode_entry.focus())
    recode_entry.bind('<FocusIn>', lambda _: logic.change_color(recode_entry, 'white'))
    recode_entry.bind('<Return>', lambda _: create_button_clicked())

    name_entry.focus()
    dialog.transient(master)
    dialog.grab_set()
    dialog.wait_window()


def show_add_key_dialog(master, fnt, check_name_func, add_key_func):
    def create_button_clicked():
        dialog.focus()
        name = name_entry.get()
        if check_name_func(name) == -1:
            logic.change_color(name_entry, 'red')
            return

        add_key_func(name)
        dialog.destroy()

    dialog = Toplevel(master)
    dialog.title('Новый ключ')
    dialog.geometry('400x80+450+250')
    dialog.resizable(width=False, height=False)

    frame = Frame(dialog, bg='white')

    name_label = Label(frame, text='Название:', font=f'Arial {fnt}', bg='white', anchor='w')
    name_entry = Entry(frame, font=f'Arial {fnt}', relief='solid')

    cancel_button = Button(frame, text='Отмена', font=f'Arial {fnt}', bg='white')
    create_button = Button(frame, text='Сгенерировать', font=f'Arial {fnt}', bg='white')

    frame.place(anchor='nw', relx=0, relwidth=1, rely=0, relheight=1)
    name_label.place(anchor='nw', relx=0.0415, relwidth=0.9, rely=0.01, relheight=0.28)
    name_entry.place(anchor='n', relx=0.5, relwidth=0.9, rely=0.30, relheight=0.28)
    cancel_button.place(anchor='ne', relx=0.48, relwidth=0.4, rely=0.63, relheight=0.32)
    create_button.place(anchor='nw', relx=0.52, relwidth=0.4, rely=0.63, relheight=0.32)

    cancel_button['command'] = dialog.destroy
    create_button['command'] = create_button_clicked
    name_entry.bind('<FocusIn>', lambda _: logic.change_color(name_entry, 'white'))
    name_entry.bind('<Return>', lambda _: create_button_clicked())

    name_entry.focus()
    dialog.transient(master)
    dialog.grab_set()
    dialog.wait_window()
