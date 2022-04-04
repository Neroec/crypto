import rsa


def main():
    # draw_all()
    # window.mainloop()
    rsa.generate_keys('my_secret_key')
    public_key = rsa.get_public_key()
    print(public_key)
    print(public_key.exportKey())


if __name__ == '__main__':
    main()
