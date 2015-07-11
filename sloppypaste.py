from tkinter import *

WATCH_RATE = 4000

class GUI:
    def __init__(self):
        self.tk = Tk()
        self.clipboard_content = ''

        self.tk.after(WATCH_RATE, self.watch_clipboard)
        self.tk.mainloop()

    def watch_clipboard(self):
        try:
            content = self.tk.clipboard_get()

            if content != self.clipboard_content:
                self.clipboard_content = content
                print(content)
        except TclError:
            pass

        self.tk.after(WATCH_RATE, self.watch_clipboard)

if __name__ == '__main__':
    gui = GUI()
