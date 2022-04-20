import os
from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog as fd
import rsa
import crypto
import logic
import dialog


window = Tk()

# Константы
FONT = 11

# Настройки сессии
session_frame = LabelFrame(window, text='Настройка сессии', font=f'Arial {FONT + 1}', bg='white')
from_label = Label(session_frame, text='Я:', font=f'Arial {FONT}', bg='white')
from_box_values = []
from_box = ttk.Combobox(session_frame, font=f'Arial {FONT}', justify='center', state='readonly')
name_delete_button_image = PhotoImage(file='images/delete_button.png')
name_delete_button = Button(session_frame, image=name_delete_button_image,
                            font=f'Arial {FONT}', bg='white')
name_add_button_image = PhotoImage(file='images/add_button.png')
name_add_button = Button(session_frame, image=name_add_button_image,
                         font=f'Arial {FONT}', bg='white')
keys_label = Label(session_frame, text='Сессионные ключи:', font=f'Arial {FONT}', bg='white')
keys_box_values = []
keys_box = ttk.Combobox(session_frame, font=f'Arial {FONT}', justify='center',
                        state='readonly')
key_delete_button_image = PhotoImage(file='images/delete_button.png')
key_delete_button = Button(session_frame, image=key_delete_button_image,
                           font=f'Arial {FONT}', bg='white')
key_add_button_image = PhotoImage(file='images/add_button.png')
key_add_button = Button(session_frame, image=key_add_button_image,
                        font=f'Arial {FONT}', bg='white')
to_label = Label(session_frame, text='Кто-то:', font=f'Arial {FONT}', bg='white')
to_box_values = []
to_box = ttk.Combobox(session_frame, font=f'Arial {FONT}', justify='center', state='readonly')
code_label = Label(session_frame, text='Секретный код:', font=f'Arial {FONT}', bg='white')
code_entry = Entry(session_frame, font=f'Arial {FONT}', show='*', relief='solid', justify='center')

# Шифрование/Расшифрование/Подпись
cypher_frame = LabelFrame(window, text='Шифрование/Расшифрование/Подпись', font=f'Arial {FONT + 1}',
                          bg='white')
add_file_button_image = PhotoImage(file='images/add_file_button.png')
file_label = Label(cypher_frame, text='Входной файл:', font=f'Arial {FONT}', bg='white')
file_entry = Entry(cypher_frame, font=f'Arial {FONT}', relief='solid', state='readonly')
file_add_button = Button(cypher_frame, image=add_file_button_image, font=f'Arial {FONT}', bg='white',
                         relief='flat')
file_text = Text(cypher_frame, wrap=WORD, font=f'Arial {FONT}', relief='solid',
                 state='disabled', padx=5, pady=3)
encrypt_button = Button(cypher_frame, text='Зашифровать', font=f'Arial {FONT}', bg='white', disabledforeground='gray77')
decrypt_button = Button(cypher_frame, text='Расшифровать', font=f'Arial {FONT}', bg='white', disabledforeground='gray77')
sign_button = Button(cypher_frame, text='Подписать', font=f'Arial {FONT}', bg='white', disabledforeground='gray77')
verify_button = Button(cypher_frame, text='Проверить', font=f'Arial {FONT}', bg='white', disabledforeground='gray77')
signature_label = Label(cypher_frame, text='', font=f'Arial {FONT + 5}', bg='white')


def get_options():
    return from_box.get(), to_box.get(), keys_box.get(), code_entry.get()


def update_state():
    window.focus()
    logic.load_keys_box(keys_box, keys_box_values,
                        from_box.get(), to_box.get())
    check_buttons_state()
    signature_label['text'] = ''


def validate_name(name):
    if name == '':
        return -1

    for value in from_box_values:
        if value == name:
            return -1

    return 0


def add_name(name, code):
    from_box_values.append(name)
    to_box_values.append(name)

    from_box['values'] = from_box_values
    to_box['values'] = to_box_values

    generate_new_keys(name, code)

    from_box.set(name)
    update_state()


def delete_name_button_clicked():
    window.focus()
    name = from_box.get()

    dirs_paths = [
        f'{rsa.PRIVATE_KEYS_DIR}',
        f'{rsa.PUBLIC_KEYS_DIR}',
        f'{rsa.SESSION_KEYS_DIR}',
        f'{crypto.FILES_DIR}',
        f'{crypto.SIGNATURES_DIR}'
    ]
    for dir_path in dirs_paths:
        logic.delete_files(dir_path, name)

    logic.delete_from_combobox(from_box, from_box_values, name)
    logic.delete_from_combobox(to_box, to_box_values, name)

    if len(from_box_values) > 0:
        from_box.set(from_box_values[0])
    else:
        from_box.set('')

    update_state()


def validate_key_name(name):
    if name == '' or name.find('encrypted_') != -1:
        return -1

    for value in keys_box_values:
        if name == value:
            return -1

    return 0


def generate_new_keys(name, code):
    window.focus()
    private_path = f'{rsa.PRIVATE_KEYS_DIR}{name}.txt'
    public_path = f'{rsa.PUBLIC_KEYS_DIR}{name}.txt'
    rsa.generate_keys(code, private_path, public_path)


def delete_key_button_clicked():
    from_name, to_name, key_name, _ = get_options()

    logic.delete_session_keys(from_name, to_name, key_name)
    parts = [key_name, f'encrypted_{key_name}', key_name.replace('encrypted_', '')]
    for part in parts:
        logic.delete_from_combobox(keys_box, keys_box_values, part)

    if len(keys_box_values) > 0:
        keys_box.set(keys_box_values[0])
    else:
        keys_box.set('')

    check_buttons_state()


def generate_session_key(key_name):
    from_name = from_box.get()
    to_name = to_box.get()

    session_key = crypto.generate_session_key()
    logic.save_session_key(from_name, to_name, key_name, session_key)

    keys_box_values.append(key_name)
    keys_box['values'] = keys_box_values
    keys_box.set(key_name)

    check_buttons_state()


def clear_buttons_state():
    buttons = [encrypt_button, decrypt_button, sign_button, verify_button]
    for button in buttons:
        button['state'] = 'normal'


def change_buttons_state(buttons, states):
    for i in range(len(buttons)):
        buttons[i]['state'] = 'normal' if states[i] else 'disable'


def check_buttons_state():
    from_name, to_name, key_name, _ = get_options()
    buttons = [name_delete_button, key_add_button, key_delete_button]
    from_flag = from_name != ''
    to_flag = to_name != ''
    key_flag = key_name != ''
    if not from_flag:
        change_buttons_state(buttons, [False, False, False])
    elif not to_flag and not key_flag:
        change_buttons_state(buttons, [True, False, False])
    else:
        change_buttons_state(buttons, [True, True, True])

    buttons = [encrypt_button, decrypt_button, sign_button, verify_button]
    path = file_entry.get()
    if path == '':
        change_buttons_state(buttons, [False, False, False, False])
        return

    common_file_name = os.path.basename(path).replace('encrypted_', '').replace('decrypted_', '')
    encrypted_flag = path.find('encrypted_') != -1
    decrypted_flag = path.find('decrypted_') != -1
    verify_path = f'{crypto.SIGNATURES_DIR}{to_name}_{common_file_name}'
    verify_flag = os.path.exists(verify_path)

    if encrypted_flag:
        change_buttons_state(buttons, [False, True, False, False])
    elif decrypted_flag:
        if verify_flag:
            change_buttons_state(buttons, [False, False, False, True])
        else:
            change_buttons_state(buttons, [False, False, False, False])
    elif key_flag:
        change_buttons_state(buttons, [True, False, True, False])
    else:
        change_buttons_state(buttons, [False, False, True, False])


def add_file_button_click():
    logic.change_color(file_entry, 'gray95', 'readonlybackground')
    path = fd.askopenfilename(initialdir=crypto.FILES_DIR, title='Выбор файла',
                              filetypes=[('Текстовые', 'txt'), ('Все', '*')])
    if path == '':
        return

    logic.replace_object_data(file_entry, path)
    with open(path, 'rb') as file:
        logic.replace_object_data(file_text, file.read())

    signature_label['text'] = ''
    check_buttons_state()


def encrypt():
    common_path = file_entry.get()
    if common_path == '':
        logic.change_color(file_entry, 'red', 'readonlybackground')
        return

    from_name, to_name, key_name, code = get_options()
    encrypted_path = logic.get_encrypted_file_path(common_path)
    try:
        session_key = logic.read_session_key(from_name, to_name, key_name, code)
        crypto.encrypt_file(session_key, common_path, encrypted_path)
    except ValueError:
        keys_box.set('Bad key!')
        return

    logic.replace_object_data(file_entry, encrypted_path)
    with open(encrypted_path, 'rb') as file:
        logic.replace_object_data(file_text, file.read())

    signature_label['text'] = ''
    check_buttons_state()


def decrypt():
    window.focus()
    encrypted_path = file_entry.get()
    if encrypted_path == '':
        logic.change_color(file_entry, 'red', 'readonlybackground')
        return

    decrypted_path = logic.get_decrypted_file_path(encrypted_path)
    from_name, to_name, key_name, code = get_options()
    try:
        session_key = logic.read_session_key(from_name, to_name, key_name, code)
    except ValueError:
        logic.change_color(code_entry, 'red')
        return

    try:
        crypto.decrypt_file(session_key, encrypted_path, decrypted_path)
    except ValueError:
        keys_box.set('Bad key!')
        return

    logic.replace_object_data(file_entry, decrypted_path)
    with open(decrypted_path, 'rb') as file:
        logic.replace_object_data(file_text, file.read())

    signature_label['text'] = ''
    check_buttons_state()


def sign():
    window.focus()
    common_path = file_entry.get()
    if common_path == '':
        logic.change_color(file_entry, 'red', 'readonlybackground')
        return
    from_name, to_name, _, code = get_options()

    private_key_path = logic.get_private_key_path(from_name)
    try:
        private_key = rsa.get_private_key(code, private_key_path)
    except ValueError:
        logic.change_color(code_entry, 'red')
        return

    signature_path = logic.get_signature_path(common_path, from_name)
    crypto.sign_file(private_key, common_path, signature_path)
    signature_label['text'] = 'Файл подписан'
    logic.change_color(signature_label, 'black', 'fg')
    check_buttons_state()


def verify():
    decrypted_path = file_entry.get()
    if decrypted_path == '':
        logic.change_color(file_entry, 'red', 'readonlybackground')
        return

    from_name, to_name, _, code = get_options()
    public_key_path = logic.get_public_key_path(to_name)
    public_key = rsa.get_public_key(public_key_path)

    signature_path = logic.get_signature_path(decrypted_path, to_name)
    result = crypto.verify_sign(public_key, decrypted_path, signature_path)

    text = 'Подпись верна' if result else 'Подпись ложна'
    color = 'lightgreen' if result else 'red'
    signature_label['text'] = text
    logic.change_color(signature_label, color, 'fg')
    check_buttons_state()


def draw_all():
    window.title('Гибридная криптосистема')
    window.geometry('1250x700+10+10')
    window.resizable(width=False, height=False)
    logic.check_and_create_dirs()

    # Области
    session_frame.place(anchor='nw', relwidth=1, relx=0, relheight=0.2, rely=0)
    cypher_frame.place(anchor='nw', relwidth=1, relx=0, relheight=0.8, rely=0.2)

    # Настройка сессии
    from_label.place(anchor='n', relx=0.25, relwidth=0.4, rely=0.04, relheight=0.2)
    from_box.place(anchor='n', relx=0.25, relwidth=0.4, rely=0.25, relheight=0.2)
    name_delete_button.place(anchor='nw', relx=0.474, relwidth=0.02, rely=0.25, relheight=0.2)
    name_add_button.place(anchor='nw', relx=0.452, relwidth=0.02, rely=0.25, relheight=0.2)
    to_label.place(anchor='n', relx=0.75, relwidth=0.4, rely=0.04, relheight=0.2)
    to_box.place(anchor='n', relx=0.75, relwidth=0.4, rely=0.25, relheight=0.2)
    code_label.place(anchor='n', relx=0.25, relwidth=0.4, rely=0.47, relheight=0.2)
    code_entry.place(anchor='n', relx=0.25, relwidth=0.4, rely=0.68, relheight=0.2)
    keys_label.place(anchor='n', relx=0.75, relwidth=0.4, rely=0.47, relheight=0.2)
    keys_box.place(anchor='n', relx=0.75, relwidth=0.4, rely=0.68, relheight=0.2)
    key_delete_button.place(anchor='nw', relx=0.974, relwidth=0.02, rely=0.68, relheight=0.2)
    key_add_button.place(anchor='nw', relx=0.952, relwidth=0.02, rely=0.68, relheight=0.2)
    # События
    from_box.bind('<<ComboboxSelected>>', lambda _: update_state())
    to_box.bind('<<ComboboxSelected>>', lambda _: update_state())
    keys_box.bind('<<ComboboxSelected>>', lambda _: window.focus())
    keys_box.bind('<FocusIn>', lambda _: logic.change_color(keys_box, 'black', 'foreground'))
    name_delete_button['command'] = delete_name_button_clicked
    name_add_button['command'] = lambda: dialog.show_add_name_dialog(window, FONT, validate_name, add_name)
    key_delete_button['command'] = delete_key_button_clicked
    key_add_button['command'] = lambda: dialog.show_add_key_dialog(window, FONT, validate_key_name,
                                                                   generate_session_key)
    code_entry.bind('<FocusIn>', lambda _: logic.change_color(code_entry, 'white'))

    # Шифрование/Расшифрование
    file_label.place(anchor='n', relx=0.5, relwidth=0.5, rely=0.02, relheight=0.05)
    file_entry.place(anchor='n', relx=0.5, relwidth=0.8, rely=0.07, relheight=0.05)
    file_add_button.place(anchor='nw', relx=0.905, relwidth=0.02, rely=0.07, relheight=0.05)
    file_text.place(anchor='n', relx=0.5, relwidth=0.98, rely=0.13, relheight=0.72)
    encrypt_button.place(anchor='nw', relx=0.01, relwidth=0.15, rely=0.88, relheight=0.1)
    decrypt_button.place(anchor='nw', relx=0.17, relwidth=0.15, rely=0.88, relheight=0.1)
    sign_button.place(anchor='nw', relx=0.33, relwidth=0.15, rely=0.88, relheight=0.1)
    verify_button.place(anchor='nw', relx=0.49, relwidth=0.15, rely=0.88, relheight=0.1)
    signature_label.place(anchor='nw', relx=0.65, relwidth=0.34, rely=0.88, relheight=0.1)
    file_add_button.bind('<ButtonRelease-1>', lambda _: add_file_button_click())
    encrypt_button['command'] = encrypt
    decrypt_button['command'] = decrypt
    sign_button['command'] = sign
    verify_button['command'] = verify

    logic.load_name_box(from_box, from_box_values, 'from')
    logic.load_name_box(to_box, to_box_values, 'to')
    logic.load_keys_box(keys_box, keys_box_values,
                        from_box.get(), to_box.get())
    check_buttons_state()
