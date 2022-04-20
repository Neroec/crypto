import os
import rsa
import crypto
from tkinter import END, Text


def get_signature_path(path, from_name):
    if path.find('decrypted') != -1:
        return f'{crypto.SIGNATURES_DIR}{from_name}_{os.path.basename(path).replace("decrypted_", "")}'
    return f'{crypto.SIGNATURES_DIR}{from_name}_{os.path.basename(path)}'


def get_encrypted_file_path(common_path):
    return f'{crypto.FILES_DIR}encrypted_{os.path.basename(common_path)}'


def get_decrypted_file_path(encrypted_path):
    return encrypted_path.replace('encrypted', 'decrypted')


def get_session_key_path(from_name, to_name, key_name):
    if key_name.find('encrypted') != -1:
        return f'{rsa.SESSION_KEYS_DIR}{to_name}_to_{from_name}_{key_name}.txt'
    return f'{rsa.SESSION_KEYS_DIR}{from_name}_to_{to_name}_{key_name}.txt'


def get_private_key_path(name):
    return f'{rsa.PRIVATE_KEYS_DIR}{name}.txt'


def get_public_key_path(name):
    return f'{rsa.PUBLIC_KEYS_DIR}{name}.txt'


def read_session_key(from_name, to_name, key_name, code):
    session_key_path = get_session_key_path(from_name, to_name, key_name)
    if key_name.find('encrypted') != -1:
        private_key_path = get_private_key_path(from_name)
        private_key = rsa.get_private_key(code, private_key_path)
        key = rsa.decrypt(private_key, session_key_path)
    else:
        with open(session_key_path, 'rb') as file:
            key = file.read()
    return key


def save_session_key(from_name, to_name, key_name, key):
    common_path = f'{rsa.SESSION_KEYS_DIR}{from_name}_to_{to_name}_{key_name}.txt'
    with open(common_path, 'wb') as file:
        file.write(key)

    encrypted_path = f'{rsa.SESSION_KEYS_DIR}{from_name}_to_{to_name}_encrypted_{key_name}.txt'
    public_key_path = f'{rsa.PUBLIC_KEYS_DIR}{to_name}.txt'
    public_key = rsa.get_public_key(public_key_path)
    rsa.encrypt(key, public_key, encrypted_path)


def delete_session_keys(from_name, to_name, key_name):
    parts = [
        from_name + '_to_' + to_name + '_' + key_name,
        to_name + '_to_' + from_name + '_' + key_name,
        from_name + '_to_' + to_name + '_encrypted_' + key_name,
        to_name + '_to_' + from_name + '_encrypted_' + key_name
    ]
    for part in parts:
        path = f'{rsa.SESSION_KEYS_DIR}{part}.txt'
        if os.path.exists(path):
            os.remove(path)


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


def load_name_box(box, values, name='from'):
    if name == 'from':
        path = f'{rsa.PRIVATE_KEYS_DIR}'
    else:
        path = f'{rsa.PUBLIC_KEYS_DIR}'

    i = 0
    values.clear()
    for _, _, filenames in os.walk(path):
        for filename in filenames:
            name = filename.replace('.txt', '')
            values.append(name)
            i += 1
    box['values'] = values

    if len(values) > 0:
        box.set(values[0])
    else:
        box.set('')


def load_keys_box(box, values, from_name, to_name):
    values.clear()
    box.set('')
    if from_name == '' or to_name == '':
        return

    length = len(from_name) + 4 + len(to_name)
    for _, __, filenames in os.walk(f'{rsa.SESSION_KEYS_DIR}'):
        for filename in filenames:
            if filename[:length].find(f'{from_name}_to_{to_name}') != -1\
                    or filename[:length].find(f'{to_name}_to_{from_name}') != -1:
                values.append(f'{filename[length+1:-4]}')

    box['values'] = values
    if len(values) > 0:
        box.set(values[0])


def delete_from_combobox(box, values, value):
    old_value = box.get()
    box.set(value)
    index = box.current()
    if index != -1:
        values.remove(value)
    box['values'] = values
    if value != old_value:
        box.set(old_value)
    elif len(values) > 1:
        box.set(values[0])
    else:
        box.set('')


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
    secret_code_1 = 'neroe_code'
    rsa.generate_keys(secret_code_1)
    private_key_1 = rsa.get_private_key(secret_code_1)
    public_key_1 = rsa.get_public_key()
    e1, n1 = rsa.get_public_key_pair(public_key_1)
    d1, _ = rsa.get_private_key_pair(private_key_1)
    print(f'Отправляющая сторона:\n- секретный код - {secret_code_1}')
    print(f'- открытый ключ (\n{e1}\n{n1}\n)')
    print(f'- закрытый ключ (\n{d1}\n{n1}\n)\n')

    secret_code_2 = 'anton_code'
    rsa.generate_keys(secret_code_2)
    private_key_2 = rsa.get_private_key(secret_code_2)
    public_key_2 = rsa.get_public_key()
    e2, n2 = rsa.get_public_key_pair(public_key_2)
    d2, _ = rsa.get_private_key_pair(private_key_2)
    print(f'Принимающая сторона:\n- секретный код - {secret_code_2}')
    print(f'- открытый ключ (\n{e2}\n{n2}\n)')
    print(f'- закрытый ключ (\n{d2}\n{n2}\n)\n')

    session_key = crypto.generate_session_key()
    print(f'Сессионный ключ:\n{session_key}')

    crypto.encrypt_file(session_key)
    rsa.encrypt(session_key, public_key_2)
    with open(rsa.SESSION_KEY_PATH, 'rb') as file:
        encrypted_session_key = file.read()
    print(f'Зашифрованный сессионный ключ:\n{encrypted_session_key}')
    crypto.sign_file_and_encrypt(private_key_1, public_key_2)

    session_key = rsa.decrypt(private_key_2)
    print(f'Расшифрованный сессионный ключ:\n{session_key}\n')

    with open(crypto.STANDARD_FILE_PATH, 'r') as file:
        print(f'Исходное сообщение:\n{file.read()}')
    with open(crypto.ENCRYPTED_FILE_PATH, 'r') as file:
        print(f'Зашифрованное сообщение:\n{file.read()}')

    crypto.decrypt_file(session_key)
    with open(crypto.DECRYPTED_FILE_PATH, 'r') as file:
        print(f'Расшифрованное сообщение:\n{file.read()}\n')

    print('Проверка подписи:')
    print(crypto.verify_sign(public_key_1, private_key_2))
