from tkinter import *


window = Tk()

general_frame = Frame(window, bg='white')


def draw_all():
    window.title('Гибридная криптосистема')
    window.geometry('1250x700+10+10')

    general_frame.place(anchor='nw', relwidth=1, relx=0, relheight=0.3, rely=0)
