from tkinter import *
import sys, urllib

WATCH_RATE = 4000
URL = "foo"

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

    def post_paste(self):
        payload = urllib.parse.urlencode({
            'text': content
        })
        payload = payload.encode('utf-8')
        urllib.request.Request(
            URL + '/item', data=payload)

    def get_paste(self):
        req = urllib.request.Request(
            URL + '/item')

        with urllib.request.urlopen(req) as response:
            return response.read()

    def listen_off(self):
        self.listen = False

    def listen_on(self):
        self.listen = True

    def watch_clipboard(self):
        try:
            content = self.tk.clipboard_get()

            if content != self.clipboard_content:
                self.clipboard_content = content
                print(content)
                self.post_paste()

            if self.listen:
                new_paste = self.get_paste()
                if new_past != self.clipboard_content:
                    self.tk.clipboard_clear()
                    self.tk.clipboard_append(new_paste)

        except TclError:
            pass

        self.tk.after(WATCH_RATE, self.watch_clipboard)

if __name__ == '__main__':
    gui = GUI()
