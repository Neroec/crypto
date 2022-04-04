from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES

STANDARD_FILE_PATH = 'files/standard_file.txt'
ENCRYPTED_FILE_PATH = 'files/encrypted_file.txt'
DECRYPTED_FILE_PATH = 'files/decrypted_file.txt'


def generate_session_key(size=16):
    """
    Генерирует сессионный ключ
    :param size: размер ключа
    :return: сессионный ключ
    """
    return get_random_bytes(size)


def encrypt_file(session_key, in_path=STANDARD_FILE_PATH, out_path=ENCRYPTED_FILE_PATH):
    """
    Шифрует и сохраняет файл симметричным алгоритмом AES
    :param session_key: сессионный ключ симметричного алгоритма
    :param in_path: путь к шифруемому файлу
    :param out_path: путь к зашифрованному файлу
    :return: зашифрованное содержимое файла
    """
    with open(in_path, 'rb') as input_file:
        data = input_file.read()
        with open(out_path, 'wb') as output_file:
            cipher_aes = AES.new(session_key, AES.MODE_EAX)
            output_file.write(cipher_aes.nonce)
            encrypted_data = cipher_aes.encrypt(data)
            output_file.write(encrypted_data)
            return encrypted_data


def decrypt_file(session_key, in_path=ENCRYPTED_FILE_PATH, out_path=DECRYPTED_FILE_PATH):
    """
    Расшифровывает и сохраняет файл симметричным алгоритмом AES
    :param session_key: сессионный ключ симметричного алгоритма
    :param in_path: путь к зашифрованному файлу
    :param out_path: путь к расшифрованному файлу
    :return: расшифрованное содержимое файла
    """
    with open(in_path, 'rb') as input_file:
        nonce, data = [input_file.read(size) for size in (16, -1)]
        with open(out_path, 'wb') as output_file:
            cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
            decrypted_data = cipher_aes.decrypt(data)
            output_file.write(decrypted_data)
            return decrypted_data.decode()
