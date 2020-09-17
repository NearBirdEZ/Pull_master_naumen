import threading
import tkinter as tk
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class App:
    driver = webdriver.Chrome(ChromeDriverManager().install())

    def __init__(self, gui_window):
        gui_window.title('LDB T_T')
        gui_window.geometry('600x600')

        self.btn_start = tk.Button(gui_window, text='RUN', command=self.begin)
        self.btn_start.place(relx=0.5, rely=0.95)

    def func(self):
        pass

    def begin(self):
        '''start a thread and connect it to func'''
        self.button.config(state=tk.DISABLED)
        threading.Thread(target=self.func, daemon=True).start()


if __name__ == '__main__':
    gui_window = tk.Tk()
    app = App(gui_window)
    gui_window.mainloop()
