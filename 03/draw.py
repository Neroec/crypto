from os import walk
from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog as fd
import rsa
import crypto
import logic


window = Tk()

# Константы
FONT = 11

# Переменные
session_key = bytes()

# Генерация ключей
generate_frame = LabelFrame(window, text='Генерация ключей', font=f'Arial {FONT + 1}', bg='white')
generate_name_label = Label(generate_frame, text='Имя:', font=f'Arial {FONT}', justify='right',
                            bg='white')
generate_name_entry = Entry(generate_frame, font=f'Arial {FONT}', justify='center', relief='solid')
generate_code_label = Label(generate_frame, text='Секретный код:', font=f'Arial {FONT}', justify='right',
                            bg='white')
generate_code_entry = Entry(generate_frame, font=f'Arial {FONT}', justify='center', show='*',
                            relief='solid')
generate_private_label = Label(generate_frame, text='Путь к приватному ключу:', font=f'Arial {FONT}',
                               bg='white')
generate_private_entry = Entry(generate_frame, font=f'Arial {FONT}', relief='solid', state='readonly',
                               readonlybackground='white')
generate_public_label = Label(generate_frame, text='Путь к публичному ключу:', font=f'Arial {FONT}',
                              bg='white')
generate_public_entry = Entry(generate_frame, font=f'Arial {FONT}', relief='solid', state='readonly',
                              readonlybackground='white')
generate_generate_button = Button(generate_frame, text='Сгенерировать', font=f'Arial {FONT}', bg='white')
generate_delete_button = Button(generate_frame, text='Удалить', font=f'Arial {FONT}', bg='white')

# Настройки сессии
session_frame = LabelFrame(window, text='Настройка сессии', font=f'Arial {FONT + 1}', bg='white')
session_keys_label = Label(session_frame, text='Сессионные ключи:', font=f'Arial {FONT}', bg='white')
session_from_label = Label(session_frame, text='От кого:', font=f'Arial {FONT}', bg='white')
session_from_box_values = []
session_from_box = ttk.Combobox(session_frame, font=f'Arial {FONT}', justify='center', state='readonly')
session_key_from_box_values = []
session_key_from_box = ttk.Combobox(session_frame, font=f'Arial {FONT}', justify='center',
                                    state='readonly')
session_to_label = Label(session_frame, text='Кому:', font=f'Arial {FONT}', bg='white')
session_to_box_values = []
session_to_box = ttk.Combobox(session_frame, font=f'Arial {FONT}', justify='center', state='readonly')
session_code_label = Label(session_frame, text='Секретный код:', font=f'Arial {FONT}', bg='white')
session_code_entry = Entry(session_frame, font=f'Arial {FONT}', show='*', relief='solid')
session_key_label = Label(session_frame, text='Путь к сессионному ключу:', font=f'Arial {FONT}',
                          bg='white')
session_key_entry = Entry(session_frame, font=f'Arial {FONT}', relief='solid')
session_button = Button(session_frame, text='Сгенерировать', font=f'Arial {FONT}', bg='white')

# Шифрование/Расшифрование
cypher_frame = LabelFrame(window, text='Шифрование/Расшифрование', font=f'Arial {FONT + 1}', bg='white')
add_button_image = PhotoImage(file='images/add_button.png')
cypher_input_file_label = Label(cypher_frame, text='Входной файл:', font=f'Arial {FONT}', bg='white')
cypher_input_file_entry = Entry(cypher_frame, font=f'Arial {FONT}', relief='solid', state='readonly',
                                readonlybackground='white')
cypher_input_add_button = Button(cypher_frame, image=add_button_image, font=f'Arial {FONT}', bg='white',
                                 relief='flat')
cypher_input_file_text = Text(cypher_frame, wrap=WORD, font=f'Arial {FONT}', relief='solid',
                              state='disabled', padx=5, pady=3)
cypher_output_file_label = Label(cypher_frame, text='Выходной файл:', font=f'Arial {FONT}', bg='white')
cypher_output_file_entry = Entry(cypher_frame, font=f'Arial {FONT}', relief='solid', state='readonly',
                                 readonlybackground='white')
cypher_output_add_button = Button(cypher_frame, image=add_button_image, font=f'Arial {FONT}', bg='white',
                                  relief='flat')
cypher_output_file_text = Text(cypher_frame, wrap=WORD, font=f'Arial {FONT}', relief='solid',
                               state='disabled', padx=5, pady=3)
cypher_encrypt_button = Button(cypher_frame, text='Зашифровать', font=f'Arial {FONT}', bg='white')
cypher_decrypt_button = Button(cypher_frame, text='Расшифровать', font=f'Arial {FONT}', bg='white')
arrow_button_image = PhotoImage(file='images/arrow_button.png')
cypher_arrow_button = Button(cypher_frame, image=arrow_button_image, font=f'Arial {FONT}', bg='white',
                             relief='flat')

# Цифровая подпись
signature_frame = LabelFrame(window, text='Цифровая подпись', font=f'Arial {FONT + 1}', bg='white')
signature_file_label = Label(signature_frame, text='Путь к подписи:', font=f'Arial {FONT}', bg='white')
signature_file_entry = Entry(signature_frame, font=f'Arial {FONT}', relief='solid')
signature_file_add_button = Button(signature_frame, image=add_button_image, font=f'Arial {FONT}',
                                   bg='white', relief='flat')
signature_sign_button = Button(signature_frame, text='Подписать', font=f'Arial {FONT}', bg='white')
signature_verify_button = Button(signature_frame, text='Проверить', font=f'Arial {FONT}', bg='white')
signature_verify_label = Label(signature_frame, text='Ожидание проверки', font=f'Arial {FONT}', bg='white')


def update_generate_paths():
    name = generate_name_entry.get()

    data = f'{rsa.PRIVATE_KEYS_DIR}{name}.txt'
    logic.replace_object_data(generate_private_entry, data)

    data = f'{rsa.PUBLIC_KEYS_DIR}{name}.txt'
    logic.replace_object_data(generate_public_entry, data)


def generate_generate_button_click():
    window.focus()
    name = generate_name_entry.get()
    if name == '':
        logic.change_color(generate_name_entry, 'red')
        return

    secret_code = generate_code_entry.get()
    if secret_code == '':
        logic.change_color(generate_code_entry, 'red')
        return

    private_path = generate_private_entry.get()
    public_path = generate_public_entry.get()
    color = 'lightgreen' if rsa.generate_keys(secret_code, private_path, public_path) else 'red'
    logic.change_color(generate_generate_button, color)

    if color == 'lightgreen':
        try:
            session_from_box_values.index(name)
        except ValueError:
            session_from_box_values.append(name)
            session_from_box['values'] = session_from_box_values

        try:
            session_to_box_values.index(name)
        except ValueError:
            session_to_box_values.append(name)
            session_to_box['values'] = session_from_box_values


def generate_delete_button_click():
    window.focus()
    name = generate_name_entry.get()
    if name == '':
        logic.change_color(generate_name_entry, 'red')
        return

    dirs_paths = [
        f'{rsa.PRIVATE_KEYS_DIR}',
        f'{rsa.PUBLIC_KEYS_DIR}',
        f'{rsa.SESSION_KEYS_DIR}',
        f'{crypto.FILES_DIR}',
        f'{crypto.SIGNATURES_DIR}'
    ]
    for dir_path in dirs_paths:
        logic.delete_files(dir_path, name)

    logic.delete_from_combobox(session_from_box, session_from_box_values, name)
    logic.delete_from_combobox(session_to_box, session_to_box_values, name)

    from_name = session_from_box.get()
    to_name = session_to_box.get()
    logic.load_keys_box(session_key_from_box, session_key_from_box_values, from_name, to_name)
    update_entries()


def session_button_click():
    global session_key
    window.focus()
    from_name = session_from_box.get()
    to_name = session_to_box.get()
    path = session_key_entry.get()
    if from_name == '' or to_name == ''\
            or path.find(f'{rsa.SESSION_KEYS_DIR}{from_name}_to_{to_name}') == -1:
        logic.change_color(session_key_entry, 'red')
        return

    try:
        session_key = crypto.generate_session_key()
        public_key = rsa.get_public_key(f'{rsa.PUBLIC_KEYS_DIR}{to_name}.txt')
        rsa.encrypt(session_key, public_key, path)
        color = 'lightgreen'
    except ValueError:
        color = 'red'

    try:
        session_key_from_box_values.index(path)
    except ValueError:
        session_key_from_box_values.append(path)
        session_key_from_box['values'] = session_key_from_box_values
    session_key_from_box.set(path)
    logic.change_color(session_button, color)


def add_button_click(entry, dir, text=None):
    path = fd.askopenfilename(initialdir=dir, title='Выбор аудио', filetypes=[('Текстовые', 'txt')])
    if path == '':
        return

    logic.replace_object_data(entry, path)

    if text is None:
        return
    with open(path, 'r') as file:
        logic.replace_object_data(text, file.read())


def update_entries():
    from_name = session_from_box.get()
    if from_name == '':
        return
    data = f'{crypto.SIGNATURES_DIR}{from_name}.txt'
    logic.replace_object_data(signature_file_entry, data)

    to_name = session_to_box.get()
    if to_name == '':
        return
    data = f'{rsa.SESSION_KEYS_DIR}{from_name}_to_{to_name}.txt'
    logic.replace_object_data(session_key_entry, data)


def name_box_selected(_):
    from_name = session_from_box.get()
    to_name = session_to_box.get()
    logic.load_keys_box(session_key_from_box, session_key_from_box_values, from_name, to_name)
    update_entries()


def load_boxes():
    i = 0
    for _, _, filenames in walk(f'{rsa.PRIVATE_KEYS_DIR}'):
        for filename in filenames:
            name = filename.replace('.txt', '')
            session_from_box_values.append(name)
            session_to_box_values.append(name)
            i += 1
    session_from_box['values'] = session_from_box_values
    session_to_box['values'] = session_to_box_values

    if len(session_from_box_values) > 0:
        session_from_box.set(session_from_box_values[0])
    length = len(session_to_box_values)
    if length > 1:
        session_to_box.set(session_to_box_values[1])
    elif length > 0:
        session_to_box.set(session_to_box_values[0])

    from_name = session_from_box.get()
    to_name = session_to_box.get()
    logic.load_keys_box(session_key_from_box, session_key_from_box_values, from_name, to_name)
    update_entries()


def change_place():
    data = cypher_output_file_entry.get()
    logic.replace_object_data(cypher_input_file_entry, data)
    logic.replace_object_data(cypher_output_file_entry, '')

    data = cypher_output_file_text.get(0.0, END)
    logic.replace_object_data(cypher_input_file_text, data)
    logic.replace_object_data(cypher_output_file_text, '')


def encrypt():
    in_path = cypher_input_file_entry.get()
    if in_path == '':
        logic.change_color(cypher_input_file_entry, 'red', 'readonlybackground')
        return

    out_path = cypher_output_file_entry.get()
    if out_path == '':
        logic.change_color(cypher_output_file_entry, 'red', 'readonlybackground')
        return

    try:
        crypto.encrypt_file(session_key, in_path, out_path)
    except ValueError:
        logic.change_color(session_key_entry, 'red')
        return

    with open(out_path, 'r') as file:
        logic.replace_object_data(cypher_output_file_text, file.read())


def decrypt():
    in_path = cypher_input_file_entry.get()
    if in_path == '':
        logic.change_color(cypher_input_file_entry, 'red', 'readonlybackground')
        return

    out_path = cypher_output_file_entry.get()
    if out_path == '':
        logic.change_color(cypher_output_file_entry, 'red', 'readonlybackground')
        return

    to_name = session_to_box.get()
    secret_code = session_code_entry.get()
    session_key_path = session_key_entry.get()

    try:
        private_key = rsa.get_private_key(secret_code,
                                          f'{rsa.PRIVATE_KEYS_DIR}{to_name}.txt')
    except ValueError:
        logic.change_color(session_code_entry, 'red')
        return
    ses_key = rsa.decrypt(private_key, session_key_path)
    crypto.decrypt_file(ses_key, in_path, out_path)

    with open(out_path, 'r') as file:
        logic.replace_object_data(cypher_output_file_text, file.read())


def sign():
    in_path = cypher_input_file_entry.get()
    from_name = session_from_box.get()
    to_name = session_to_box.get()
    secret_code = session_code_entry.get()
    signature_path = signature_file_entry.get()

    try:
        private_key = rsa.get_private_key(secret_code, f'{rsa.PRIVATE_KEYS_DIR}{from_name}.txt')
        public_key = rsa.get_public_key(f'{rsa.PUBLIC_KEYS_DIR}{to_name}.txt')
        crypto.sign_file(private_key, public_key, in_path, signature_path)
        color = 'lightgreen'
    except ValueError:
        color = 'red'
    logic.change_color(signature_sign_button, color)


def verify():
    in_path = cypher_input_file_entry.get()
    from_name = session_from_box.get()
    to_name = session_to_box.get()
    secret_code = session_code_entry.get()
    signature_path = signature_file_entry.get()

    try:
        public_key = rsa.get_public_key(f'{rsa.PUBLIC_KEYS_DIR}{from_name}.txt')
        private_key = rsa.get_private_key(secret_code, f'{rsa.PRIVATE_KEYS_DIR}{to_name}.txt')
        result = crypto.verify_sign(public_key, private_key, in_path, signature_path)
    except ValueError:
        logic.change_color(session_code_entry, 'red')
        return

    text = 'Подпись верна' if result else 'Подпись ложна'
    color = 'lightgreen' if result else 'red'
    signature_verify_label['text'] = text
    logic.change_color(signature_verify_label, color)


def reset_verify_label():
    signature_verify_label['text'] = 'Ожидание проверки'
    signature_verify_label['bg'] = 'white'


def draw_all():
    window.title('Гибридная криптосистема')
    window.geometry('1250x700+10+10')
    window.resizable(width=False, height=False)
    logic.check_and_create_dirs()

    # Области
    generate_frame.place(anchor='nw', relwidth=1, relx=0, relheight=0.2, rely=0)
    session_frame.place(anchor='nw', relwidth=1, relx=0, relheight=0.2, rely=0.2)
    cypher_frame.place(anchor='nw', relwidth=1, relx=0, relheight=0.5, rely=0.4)
    signature_frame.place(anchor='nw', relwidth=1, relx=0, relheight=0.1, rely=0.9)

    # Генерация ключа
    generate_name_label.place(anchor='nw', relx=0.01, relwidth=0.05, rely=0.04, relheight=0.2)
    generate_name_entry.place(anchor='nw', relx=0.07, relwidth=0.35, rely=0.04, relheight=0.2)
    generate_code_label.place(anchor='nw', relx=0.43, relwidth=0.1, rely=0.04, relheight=0.2)
    generate_code_entry.place(anchor='nw', relx=0.54, relwidth=0.45, rely=0.04, relheight=0.2)
    generate_private_label.place(anchor='n', relx=0.25, relwidth=0.48, rely=0.26, relheight=0.2)
    generate_private_entry.place(anchor='n', relx=0.25, relwidth=0.48, rely=0.47, relheight=0.2)
    generate_public_label.place(anchor='n', relx=0.75, relwidth=0.48, rely=0.26, relheight=0.2)
    generate_public_entry.place(anchor='n', relx=0.75, relwidth=0.48, rely=0.47, relheight=0.2)
    generate_generate_button.place(anchor='n', relx=0.425, relwidth=0.14, rely=0.7, relheight=0.27)
    generate_delete_button.place(anchor='n', relx=0.575, relwidth=0.14, rely=0.7, relheight=0.27)
    # События
    sv1 = StringVar()
    sv1.trace("wu", lambda _, __, ___, ____=sv1: update_generate_paths())
    generate_name_entry['textvariable'] = sv1
    generate_name_entry.bind('<FocusIn>', lambda _: logic.change_color(generate_name_entry, 'white'))
    generate_code_entry.bind('<FocusIn>', lambda _: logic.change_color(generate_code_entry, 'white'))
    generate_generate_button['command'] = generate_generate_button_click
    generate_delete_button['command'] = generate_delete_button_click
    generate_generate_button.bind('<Leave>', lambda _: logic.change_color(generate_generate_button, 'white'))
    generate_delete_button.bind('<Leave>', lambda _: logic.change_color(generate_delete_button, 'white'))

    # Настройка сессии
    session_from_label.place(anchor='nw', relx=0.01, relwidth=0.3, rely=0.04, relheight=0.2)
    session_to_label.place(anchor='ne', relx=0.99, relwidth=0.3, rely=0.04, relheight=0.2)
    session_keys_label.place(anchor='n', relx=0.5, relwidth=0.2, rely=0.04, relheight=0.2)
    session_from_box.place(anchor='nw', relx=0.01, relwidth=0.3, rely=0.25, relheight=0.2)
    session_to_box.place(anchor='ne', relx=0.99, relwidth=0.3, rely=0.25, relheight=0.2)
    session_key_from_box.place(anchor='n', relx=0.5, relwidth=0.3, rely=0.25, relheight=0.2)
    session_code_label.place(anchor='nw', relx=0.01, relwidth=0.2, rely=0.47, relheight=0.2)
    session_code_entry.place(anchor='nw', relx=0.01, relwidth=0.2, rely=0.68, relheight=0.2)
    session_key_label.place(anchor='nw', relx=0.22, relwidth=0.5, rely=0.47, relheight=0.2)
    session_key_entry.place(anchor='nw', relx=0.22, relwidth=0.5, rely=0.68, relheight=0.2)
    session_button.place(anchor='nw', relx=0.74, relwidth=0.25, rely=0.63, relheight=0.3)
    # События
    session_from_box.bind("<<ComboboxSelected>>", name_box_selected)
    session_to_box.bind("<<ComboboxSelected>>", name_box_selected)
    session_button['command'] = session_button_click
    session_key_entry.bind('<Enter>', lambda _: logic.change_color(session_key_entry, 'white'))
    session_code_entry.bind('<FocusIn>', lambda _: logic.change_color(session_code_entry, 'white'))
    session_button.bind('<Leave>', lambda _: logic.change_color(session_button, 'white'))

    # Шифрование/Расшифрование
    cypher_input_file_label.place(anchor='n', relx=0.25, relwidth=0.5, rely=0.02, relheight=0.08)
    cypher_arrow_button.place(anchor='n', relx=0.5, relwidth=0.053, rely=-0.005, relheight=0.11)
    cypher_input_file_entry.place(anchor='nw', relx=0.005, relwidth=0.467, rely=0.11, relheight=0.08)
    cypher_input_add_button.place(anchor='nw', relx=0.475, relwidth=0.02, rely=0.11, relheight=0.08)
    cypher_input_file_text.place(anchor='nw', relx=0.005, relwidth=0.49, rely=0.2, relheight=0.68)
    cypher_output_file_label.place(anchor='n', relx=0.75, relwidth=0.5, rely=0.02, relheight=0.08)
    cypher_output_file_entry.place(anchor='nw', relx=0.505, relwidth=0.467, rely=0.11, relheight=0.08)
    cypher_output_add_button.place(anchor='nw', relx=0.975, relwidth=0.02, rely=0.11, relheight=0.08)
    cypher_output_file_text.place(anchor='nw', relx=0.505, relwidth=0.49, rely=0.2, relheight=0.68)
    cypher_encrypt_button.place(anchor='n', relx=0.39, relwidth=0.2, rely=0.89, relheight=0.1)
    cypher_decrypt_button.place(anchor='n', relx=0.61, relwidth=0.2, rely=0.89, relheight=0.1)
    dir1 = f'{crypto.FILES_DIR}'
    cypher_input_add_button.bind('<ButtonRelease-1>',
                                 lambda _: add_button_click(cypher_input_file_entry, dir1,
                                                            cypher_input_file_text))
    cypher_output_add_button.bind('<ButtonRelease-1>',
                                  lambda _: add_button_click(cypher_output_file_entry, dir1))
    cypher_input_file_entry.bind('<Enter>', lambda _: logic.change_color(cypher_input_file_entry, 'white',
                                                                         'readonlybackground'))
    cypher_output_file_entry.bind('<Enter>', lambda _: logic.change_color(cypher_output_file_entry,
                                                                          'white', 'readonlybackground'))
    cypher_arrow_button['command'] = change_place
    cypher_encrypt_button['command'] = encrypt
    cypher_decrypt_button['command'] = decrypt

    # Цифровая подпись
    signature_file_label.place(anchor='nw', relx=0.01, relwidth=0.5, rely=0.01, relheight=0.46)
    signature_file_entry.place(anchor='nw', relx=0.01, relwidth=0.5, rely=0.48, relheight=0.46)
    signature_file_add_button.place(anchor='nw', relx=0.515, relwidth=0.02, rely=0.44, relheight=0.54)
    signature_sign_button.place(anchor='n', relx=0.69, relwidth=0.16, rely=0.01, relheight=0.49)
    signature_verify_button.place(anchor='n', relx=0.87, relwidth=0.16, rely=0.01, relheight=0.49)
    signature_verify_label.place(anchor='n', relx=0.78, relwidth=0.345, rely=0.51, relheight=0.49)
    dir2 = f'{crypto.SIGNATURES_DIR}'
    signature_file_add_button.bind('<ButtonRelease-1>',
                                   lambda _: add_button_click(signature_file_entry, dir2))
    signature_sign_button['command'] = sign
    signature_verify_button['command'] = verify
    signature_sign_button.bind('<Leave>', lambda _: logic.change_color(signature_sign_button, 'white'))
    signature_verify_button.bind('<Leave>', lambda _: reset_verify_label())

    load_boxes()
