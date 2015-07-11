from tkinter import *
import sys, json, argparse
import urllib.parse
import urllib.request

WATCH_RATE = 4000
URL = "http://ec2-52-6-196-223.compute-1.amazonaws.com:1337"

parser = argparse.ArgumentParser(description='The sloppypaste client.')
parser.add_argument('--url', dest='url', default=URL, 
        help='the server url to connect to')
parser.add_argument('--rate', dest='rate', default=WATCH_RATE,
        help='how long (in ms) between buffer checks')

class GUI:
    def __init__(self):
        args = parser.parse_args()
        self.url = args.url
        self.rate = args.rate

        self.tk = Tk()
        self.tk.resizable(0,0)
        self.tk.title('sloppy coppy')

        self.clipboard_content = u''

        self.tk.after(self.rate, self.watch_clipboard)

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

    def post_paste(self, content):
        payload = urllib.parse.urlencode({
            'text': content
        })
        payload = payload.encode('utf-8')
        req = urllib.request.Request(
            self.url + '/item', data=payload)
        return req

    def get_paste(self):
        req = urllib.request.Request(
            self.url + '/item')

        with urllib.request.urlopen(req) as response:
            payload = response.read().decode('utf-8')
            decoded_payload = json.loads(payload)
            return json.loads(payload)[-1]['text']

            if type(decoded_payload) is list:
                return decoded_payload[-1]['text']
            elif type(decoded_payload) is dict:
                return decoded_payload['text']
            else:
                return ''

    def listen_off(self):
        self.listen = False

    def listen_on(self):
        self.listen = True

    def watch_clipboard(self):
        try:
            content = self.tk.clipboard_get()

            if content != self.clipboard_content:
                self.clipboard_content = content
                req = self.post_paste(content)
                with urllib.request.urlopen(req) as response:
                    payload = response.read().decode('utf-8')

            if self.listen:
                new_paste = self.get_paste()
                if new_paste != self.clipboard_content:
                    self.tk.clipboard_clear()
                    self.tk.clipboard_append(new_paste)

        except TclError:
            pass

        self.tk.after(self.rate, self.watch_clipboard)

if __name__ == '__main__':
    gui = GUI()
