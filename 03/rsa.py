from Cryptodome.PublicKey import RSA


PRIVATE_KEY_PATH = 'private_rsa_key.txt'
PUBLIC_KEY_PATH = 'public_rsa_key.txt'


def save_private_key(key: RSA.RsaKey, secret_code):
    encrypted_private_key = key.exportKey(
        passphrase=secret_code,
        pkcs=8,
        protection='scryptAndAES128-CBC'
    )
    with open(PRIVATE_KEY_PATH, 'wb') as file:
        file.write(encrypted_private_key)


def save_public_key(key: RSA.RsaKey):
    public_key = key.publickey().exportKey()
    with open(PUBLIC_KEY_PATH, 'wb') as file:
        file.write(public_key)


def generate_keys(secret_code):
    key = RSA.generate(2048)
    save_private_key(key, secret_code)
    save_public_key(key)


def get_public_key():
    with open(PUBLIC_KEY_PATH, 'r') as file:
        data = file.read()
        public_key = RSA.importKey(data)
        return public_key


def get_private_key(secret_code):
    with open(PRIVATE_KEY_PATH, 'r') as file:
        data = file.read()
        private_key = RSA.importKey(data, secret_code)
        return private_key
