import os
import rsa
import crypto
from tkinter import END, Text


def replace_object_data(object, data):
    start = 0.0 if type(object) == Text else 0
    old_state = object['state']
    object['state'] = 'normal'
    object.delete(start, END)
    object.insert(END, data)
    object['state'] = old_state


def change_color(object, color, mode='bg'):
    object[mode] = color


def delete_files(dir_path, part):
    for _, __, filenames in os.walk(dir_path):
        for filename in filenames:
            if filename.find(f'{part}.') != -1\
                    or filename.find(f'{part}_') != -1:
                os.remove(f'{dir_path}{filename}')


def load_keys_box(box, values, from_name, to_name):
    if from_name == '' or to_name == '':
        return
    values.clear()
    length = len(from_name) + 4 + len(to_name)
    for _, __, filenames in os.walk(f'{rsa.SESSION_KEYS_DIR}'):
        for filename in filenames:
            if filename[:length].find(f'{from_name}_to_{to_name}') != -1:
                values.append(f'{rsa.SESSION_KEYS_DIR}{filename}')

    box['values'] = values
    if len(values) > 0:
        box.set(values[0])
    else:
        box.set('')


def delete_from_combobox(box, values, value):
    old_value = box.get()
    box.set(value)
    index = box.current()
    if index != -1:
        values.remove(value)
    box['values'] = values
    if value != old_value:
        box.set(old_value)
    elif box.size != 0:
        box.set(values[0])


def check_and_create_dirs():
    dirs = [
        f'{rsa.KEYS_DIR}',
        f'{rsa.PRIVATE_KEYS_DIR}',
        f'{rsa.PUBLIC_KEYS_DIR}',
        f'{rsa.SESSION_KEYS_DIR}',
        f'{crypto.FILES_DIR}',
        f'{crypto.SIGNATURES_DIR}'
    ]
    for dir in dirs:
        if not os.path.exists(dir):
            os.mkdir(dir)


def example():
    secret_code_1 = 'my_secret_code_1'
    rsa.generate_keys(secret_code_1)
    private_key_1 = rsa.get_private_key(secret_code_1)
    public_key_1 = rsa.get_public_key()

    secret_code_2 = 'my_secret_code_2'
    rsa.generate_keys(secret_code_2)
    private_key_2 = rsa.get_private_key(secret_code_2)
    public_key_2 = rsa.get_public_key()

    session_key = crypto.generate_session_key()
    crypto.encrypt_file(session_key)
    rsa.encrypt(session_key, public_key_1)
    crypto.sign_file(private_key_2, public_key_1)

    session_key = rsa.decrypt(private_key_1)
    crypto.decrypt_file(session_key)
    print('Расшифрованное сообщение:')
    with open(crypto.DECRYPTED_FILE_PATH, 'r') as file:
        print(file.read())
    print('Проверка подписи:')
    print(crypto.verify_sign(public_key_2, private_key_1))
