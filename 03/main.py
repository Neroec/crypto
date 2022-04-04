import rsa
import crypto


def main():
    # draw_all()
    # window.mainloop()
    secret_code = 'my_secret_code'
    rsa.generate_keys(secret_code)
    public_key = rsa.get_public_key()
    private_key = rsa.get_private_key(secret_code)
    session_key = crypto.generate_session_key()

    crypto.encrypt_file(session_key)
    rsa.encrypt_session_key(session_key, public_key)
    session_key = rsa.decrypt_session_key(private_key)
    print(crypto.decrypt_file(session_key))


if __name__ == '__main__':
    main()
