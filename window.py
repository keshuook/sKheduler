from tkinter import Tk,Button,messagebox,Label,LEFT,RIGHT
import ctypes
from winsound import PlaySound, SND_ASYNC

class Window():
    def __init__(self, reason, description):
        window = Tk()

        def dismiss_window():
            PlaySound(None, SND_ASYNC)
            window.destroy()

        title = Label(text=reason, font=("Arial", 32, "bold"), bg="#222222", fg="#eeeeee")
        description = Label(text=description, font=("Arial", 20, "italic"),bg="#222222", fg="#eeeeee")
        minimise = Button(text="Minimise")
        dismiss = Button(text="Dismiss",command=dismiss_window)

        self._set_button_code(minimise)
        self._set_button_code(dismiss)

        def hide():
            window.attributes("-toolwindow", False)
            window.iconify()
        def window_event(e):
            if(window.state() != "iconic"):
                window.attributes("-toolwindow", True)
        def on_closing():
            if messagebox.askokcancel("Alarm", "Do You Want to Dismiss This Alarm?"):
                PlaySound(None, SND_ASYNC)
                window.destroy()
        def mh(e):
            self._hover(minimise)
        def mu(e):
            self._unhover(minimise)
        def dh(e):
            self._hover(dismiss)
        def du(e):
            self._unhover(dismiss)

        minimise.config(command=hide)

        minimise.bind("<Enter>", mh)
        minimise.bind("<Leave>", mu)
        dismiss.bind("<Enter>", dh)
        dismiss.bind("<Leave>", du)

        window.protocol("WM_DELETE_WINDOW", on_closing)
        window.bind("<Configure>", window_event)
        window.resizable(False, False)

        window.attributes('-topmost', True)
        window.attributes('-toolwindow', True)

        title.pack()
        description.pack()
        minimise.pack(side=LEFT)
        dismiss.pack(side=RIGHT)
        
        hp = window.winfo_screenheight()/100
        wp = window.winfo_screenwidth()/100

        window.title("sKhedule Alarm")
        window.iconbitmap("assets/alarm.ico")
        window.configure(background="#222222")
        window.geometry(f'{int(40*wp)}x{int(40*hp)}+{int(30*wp)}+{int(25*hp)}')
        
        PlaySound(r'C:\Windows\media\Alarm01.wav', SND_ASYNC)

        window.mainloop()
    def _set_button_code(self, button):
        button.configure(background="#ffffff",border=None,font=("Arial", 20), fg="#666666", activebackground="#222222", activeforeground="#eeeeee")
    def _hover(self, button):
        button.configure(fg="#ffffff",background="#666666")
    def _unhover(self, button):
        button.configure(background="#ffffff",fg="#666666")