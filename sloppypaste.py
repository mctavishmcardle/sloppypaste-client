from tkinter import *
import sys

WATCH_RATE = 4000

class GUI:
    def __init__(self):
        self.tk = Tk()
        self.tk.resizable(0,0)
        self.tk.title('sloppy coppy')

        self.clipboard_content = u''

        self.tk.after(WATCH_RATE, self.watch_clipboard)

        self.listen = IntVar()
        self.listen.set(True)

        Radiobutton(
            self.tk, text='on', indicatoron=0, 
            variable=self.listen, value=True,
            command=self.listen_on).pack(anchor=W)
        Radiobutton(
            self.tk, text='off', indicatoron=0,
            variable=self.listen, value=False,
            command=self.listen_off).pack(anchor=W)
        Button(
            self.tk, text='quit',
            command=sys.exit).pack(anchor=W)

        self.tk.mainloop()

    def listen_off(self):
        self.listen = False

    def listen_on(self):
        self.listen = True

    def watch_clipboard(self):
        try:
            if self.listen:
                content = self.tk.clipboard_get()

                if content != self.clipboard_content:
                    self.clipboard_content = content
                    print(content)
        except TclError:
            pass

        self.tk.after(WATCH_RATE, self.watch_clipboard)

if __name__ == '__main__':
    gui = GUI()
