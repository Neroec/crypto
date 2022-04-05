# import rsa
# import crypto
import draw
import rsa


def main():
    draw.draw_all()
    draw.window.mainloop()

# def main():
#     secret_code_1 = 'my_secret_code_1'
#     rsa.generate_keys(secret_code_1)
#     private_key_1 = rsa.get_private_key(secret_code_1)
#     public_key_1 = rsa.get_public_key()
#
#     secret_code_2 = 'my_secret_code_2'
#     rsa.generate_keys(secret_code_2)
#     private_key_2 = rsa.get_private_key(secret_code_2)
#     public_key_2 = rsa.get_public_key()
#
#     session_key = crypto.generate_session_key()
#     crypto.encrypt_file(session_key)
#     rsa.encrypt(session_key, public_key_1)
#     crypto.sign_file(private_key_2, public_key_1)
#
#     session_key = rsa.decrypt(private_key_1)
#     crypto.decrypt_file(session_key)
#     print('Расшифрованное сообщение:')
#     with open(crypto.DECRYPTED_FILE_PATH, 'r') as file:
#         print(file.read())
#     print('Проверка подписи:')
#     print(crypto.verify_sign(public_key_2, private_key_1))


if __name__ == '__main__':
    main()
