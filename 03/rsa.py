from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP


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


def encrypt(messages, public_key, out_path=SESSION_KEY_PATH):
    """
    Шифрует сообщение и сохраняет его в файл
    :param messages: сообщение
    :param public_key: публичный ключ RSA
    :param out_path: путь к файлу для сохранения
    :return: зашифрованное сообщение
    """
    msg = messages
    if type(messages[0]) is str:
        msg = messages.encode()
    with open(out_path, 'wb') as file:
        cipher_rsa = PKCS1_OAEP.new(public_key)
        step = 190
        enc_msg = bytes()
        for part in [msg[n:n+step] for n in range(0, len(msg), step)]:
            encrypted_message = cipher_rsa.encrypt(part)
            file.write(encrypted_message)
            enc_msg += encrypted_message
    return enc_msg


def decrypt(private_key, in_path=SESSION_KEY_PATH, mode='bytes'):
    """
    Считывает зашифрованное сообщение из файла и расшифровывает его
    :param private_key: приватный ключ RSA
    :param in_path: путь к зашифрованному сообщению
    :param mode: вид расшифрованного сообщения ('bytes', 'str')
    :return: расшифрованное сообщение
    """
    with open(in_path, 'rb') as file:
        cipher_rsa = PKCS1_OAEP.new(private_key)
        step = 256
        decrypted_data = bytes()
        encrypted_data = file.read(step)
        while len(encrypted_data) != 0:
            decrypted_data += cipher_rsa.decrypt(encrypted_data)
            encrypted_data = file.read(step)
        if mode == 'str':
            decrypted_data = decrypted_data.decode()
        return decrypted_data
