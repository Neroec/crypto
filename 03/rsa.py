from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP as cipher


PRIVATE_KEY_PATH = 'keys/encrypted_private_rsa_key.txt'
PUBLIC_KEY_PATH = 'keys/public_rsa_key.txt'
SESSION_KEY_PATH = 'keys/encrypted_session_key.txt'


def save_private_key(key: RSA.RsaKey, secret_code, private_key_path=PRIVATE_KEY_PATH):
    """
    Сохраняет зашифрованный приватный ключ в файл
    :param key: ключи RSA
    :param secret_code: секретный код для шифрования
    :param private_key_path: путь к файлу для сохранения приватного ключа
    :return: None
    """
    encrypted_private_key = key.exportKey(
        passphrase=secret_code,
        pkcs=8,
        protection='scryptAndAES128-CBC'
    )
    with open(private_key_path, 'wb') as file:
        file.write(encrypted_private_key)


def save_public_key(key: RSA.RsaKey, public_key_path=PUBLIC_KEY_PATH):
    """
    Сохраняет публичный ключ в файл
    :param key: ключи RSA
    :param public_key_path: путь к файлу для сохранения публичного ключа
    :return: None
    """
    public_key = key.publickey().exportKey()
    with open(public_key_path, 'wb') as file:
        file.write(public_key)


def generate_keys(secret_code, private_key_path=PRIVATE_KEY_PATH, public_key_path=PUBLIC_KEY_PATH):
    """
    Генерирует ключи RSA, которые сохраняются в файлы
    :param secret_code: секретный код для шифрования приватного ключа
    :param private_key_path: путь к файлу для сохранения приватного ключа
    :param public_key_path: путь к файлу для сохранения публичного ключа
    :return: None
    """
    key = RSA.generate(2048)
    save_private_key(key, secret_code, private_key_path)
    save_public_key(key, public_key_path)


def get_public_key(public_key_path=PUBLIC_KEY_PATH):
    """
    Считывает и возвращает публичный ключ из файла
    :param public_key_path: путь к файлу с публичным ключом
    :return: публичный ключ RSA
    """
    with open(public_key_path, 'r') as file:
        data = file.read()
        public_key = RSA.importKey(data)
        return public_key


def get_private_key(secret_code, private_key_path=PRIVATE_KEY_PATH):
    """
    Считывает и возвращает приватный ключ из файла
    :param secret_code: секретный код для расшифрования приватного ключа
    :param private_key_path: путь к файлу с приватным ключом
    :return: приватный ключ RSA
    """
    with open(private_key_path, 'r') as file:
        data = file.read()
        private_key = RSA.importKey(data, secret_code)
        return private_key


def get_public_key_pair(public_key: RSA.RsaKey):
    """
    Возвращает пару (e, n) открытого ключа
    :param public_key: публичный ключ RSA
    :return: пара (e, n)
    """
    return public_key.e, public_key.n


def get_private_key_pair(private_key: RSA.RsaKey):
    """
    Возвращает пару (d, n) закрытого ключа
    :param private_key: приватный ключ RSA
    :return: пара (d, n)
    """
    return private_key.d, private_key.n


def encrypt_session_key(session_key, public_key, out_path=SESSION_KEY_PATH):
    """
    Шифрует сессионный ключ и сохраняет его в файл
    :param session_key: сообщение
    :param public_key: публичный ключ RSA
    :param out_path: путь к файлу для сохранения
    :return: зашифрованный сессионный ключ
    """
    with open(out_path, 'wb') as file:
        cipher_rsa = cipher.new(public_key)
        encrypted_message = cipher_rsa.encrypt(session_key)
        file.write(encrypted_message)
        return encrypted_message


def decrypt_session_key(private_key, in_path=SESSION_KEY_PATH):
    """
    Считывает зашифрованный сессионный ключ из файла и расшифровывает его
    :param private_key: приватный ключ RSA
    :param in_path: путь к файлу с ключем
    :return: расшифрованный сессионный ключ
    """
    with open(in_path, 'rb') as file:
        cipher_rsa = cipher.new(private_key)
        return cipher_rsa.decrypt(file.read())
