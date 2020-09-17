import threading
import tkinter as tk
import time
from api_naumen import API_Naumen
from tkinter import messagebox
from selenium.common.exceptions import NoSuchElementException
import create_list_kkt
import csv
import create_request


class App:
    api = API_Naumen()

    def __init__(self, gui_window):
        self.gui_window = gui_window
        self.gui_window.title('Лидия 2.0')
        self.gui_window.geometry('600x600')
        self.gui_window['bg'] = '#5F5F5F'

        self.lbl_l_naumen = tk.Label(self.gui_window, text='Login Naumen', font=("Arial Bold", 20), bg='#5F5F5F',
                                     fg='white')
        self.lbl_p_naumen = tk.Label(self.gui_window, text='Password Naumen', font=("Arial Bold", 20), bg='#5F5F5F',
                                     fg='white')

        self.login_area = tk.Entry(self.gui_window, width=30)
        self.password_area = tk.Entry(self.gui_window, width=30)

        self.btn_send = tk.Button(text='Отправить логин\nи пароль', command=self.send_log_pass, bg='#5F5F5F',
                                  fg='white', font=("Arial", 13))
        self.btn_clear = tk.Button(text='Очистить поле\nлогина и пароля', command=self.clear, bg='#5F5F5F', fg='white',
                                   font=("Arial", 13))

        self.lbl_l_naumen.place(relx=0.35, rely=0.35)
        self.login_area.place(relx=0.35, rely=0.41)
        self.lbl_p_naumen.place(relx=0.32, rely=0.45)
        self.password_area.place(relx=0.35, rely=0.51)

        self.btn_send.place(relx=0.24, rely=0.59)
        self.btn_clear.place(relx=0.54, rely=0.59)

        self.rad_view_address = tk.IntVar()
        self.rad_prefix_store = tk.StringVar(value=0)
        self.scale_amount_zero = tk.Scale(self.gui_window, from_=0, to=10, orient=tk.HORIZONTAL, length=400,
                                          bg='#5F5F5F', fg='white', font=("Arial", 13))
        self.rad_model_kkt = tk.StringVar(value=0)

        self.name_area = tk.Entry(self.gui_window, width=50)
        self.phone_area = tk.Entry(self.gui_window, width=50)
        self.email_area = tk.Entry(self.gui_window, width=50)

        self.btn_start = tk.Button(gui_window, text='Запустить выполнение пулла', command=self.begin, bg='#5F5F5F',
                                   fg='white', font=("Arial", 13))
        self.btn_view = tk.Button(text='Показать процесс в браузере', command=self.view, bg='#5F5F5F',
                                  fg='white', font=("Arial", 13))

    def view(self):
        self.api.driver.set_window_position(0, 0)
        self.btn_view.configure(state='disabled')

    def clear(self):
        self.login_area.delete('0', tk.END)
        self.password_area.delete('0', tk.END)

    def send_log_pass(self):
        login = self.login_area.get()
        password = self.password_area.get()
        if login == '' or password == '':
            messagebox.showinfo('Ошибка', 'Не заполнены\nлогин и пароль')
            self.clear()
            return
        login = self.login_area.get()
        password = self.password_area.get()
        """ЗАПУСК НАУМЕНА"""
        self.api.start_naumen(login, password)
        self.clear()
        flag = False
        try:
            self.api.driver.find_element_by_xpath('//*[@id="LogonForm"]/p')
            messagebox.showinfo('Ошибка', 'Не верный логин или пароль')
        except NoSuchElementException:
            flag = True

        if flag:
            """Сокрытие кнопок"""
            self.btn_send.configure(state='disabled')
            self.btn_clear.configure(state='disabled')
            self.btn_send.place(relx=-1, rely=0.59)
            self.btn_clear.place(relx=1, rely=0.59)
            self.lbl_l_naumen.place(relx=-1, rely=0.35)
            self.login_area.place(relx=-1, rely=0.41)
            self.lbl_p_naumen.place(relx=-1, rely=0.45)
            self.password_area.place(relx=-1, rely=0.51)

            """Появление другого фрейма"""
            lbl_view_address = tk.Label(text='Какой формат адреса предоставил заказчик?', bg='#5F5F5F', fg='white',
                                        font=("Arial", 14))
            rad_view1 = tk.Radiobutton(self.gui_window, text='Адрес\nмагазина', value=1, variable=self.rad_view_address,
                                       bg='#5F5F5F', font=("Arial", 13), selectcolor='#5F5F5F', fg='white')
            rad_view2 = tk.Radiobutton(self.gui_window, text='Номер магазина\nили код точки', value=2,
                                       variable=self.rad_view_address, bg='#5F5F5F', font=("Arial", 13),
                                       selectcolor='#5F5F5F', fg='white')
            rad_view3 = tk.Radiobutton(self.gui_window, text='Адреса, сгенерированные\nNaumenом', value=3,
                                       variable=self.rad_view_address, bg='#5F5F5F', font=("Arial", 13),
                                       selectcolor='#5F5F5F', fg='white')

            lbl_view_address.pack()
            rad_view1.place(relx=0.05, rely=0.05)
            rad_view2.place(relx=0.3, rely=0.05)
            rad_view3.place(relx=0.6, rely=0.05)

            lbl_prefix = tk.Label(text='Для какого магазина запускаем пулл?', bg='#5F5F5F', fg='white',
                                  font=("Arial", 14))

            rad_prefix1 = tk.Radiobutton(self.gui_window, text='Алькор и Ко', value='алькор и ко',
                                         variable=self.rad_prefix_store, bg='#5F5F5F', font=("Arial", 13),
                                         selectcolor='#5F5F5F', fg='white')
            rad_prefix2 = tk.Radiobutton(self.gui_window, text='Атак', value='атак', variable=self.rad_prefix_store,
                                         bg='#5F5F5F', font=("Arial", 13), selectcolor='#5F5F5F', fg='white')
            rad_prefix3 = tk.Radiobutton(self.gui_window, text='Ашан', value='ашан', variable=self.rad_prefix_store,
                                         bg='#5F5F5F', font=("Arial", 13), selectcolor='#5F5F5F', fg='white')
            rad_prefix4 = tk.Radiobutton(self.gui_window, text='Детский Мир', value='детский мир',
                                         variable=self.rad_prefix_store, bg='#5F5F5F', font=("Arial", 13),
                                         selectcolor='#5F5F5F', fg='white')
            rad_prefix5 = tk.Radiobutton(self.gui_window, text='Иль де Ботэ', value='иль де ботэ',
                                         variable=self.rad_prefix_store, bg='#5F5F5F', font=("Arial", 13),
                                         selectcolor='#5F5F5F', fg='white')
            rad_prefix6 = tk.Radiobutton(self.gui_window, text="Levi's", value='леви', variable=self.rad_prefix_store,
                                         bg='#5F5F5F', font=("Arial", 13), selectcolor='#5F5F5F', fg='white')
            rad_prefix7 = tk.Radiobutton(self.gui_window, text='Манго Раша', value='манго',
                                         variable=self.rad_prefix_store,
                                         bg='#5F5F5F', font=("Arial", 13), selectcolor='#5F5F5F', fg='white')
            rad_prefix8 = tk.Radiobutton(self.gui_window, text='Нью Йоркер РУС', value='нью йоркер рус',
                                         variable=self.rad_prefix_store, bg='#5F5F5F', font=("Arial", 13),
                                         selectcolor='#5F5F5F', fg='white')
            rad_prefix9 = tk.Radiobutton(self.gui_window, text='Тами и Ко', value='тами и ко',
                                         variable=self.rad_prefix_store, bg='#5F5F5F', font=("Arial", 13),
                                         selectcolor='#5F5F5F', fg='white')

            lbl_prefix.place(relx=0.2, rely=0.16)
            rad_prefix1.place(relx=0.05, rely=0.21)
            rad_prefix2.place(relx=0.05, rely=0.26)
            rad_prefix3.place(relx=0.05, rely=0.31)
            rad_prefix4.place(relx=0.35, rely=0.21)
            rad_prefix5.place(relx=0.35, rely=0.26)
            rad_prefix6.place(relx=0.35, rely=0.31)
            rad_prefix7.place(relx=0.65, rely=0.21)
            rad_prefix8.place(relx=0.65, rely=0.26)
            rad_prefix9.place(relx=0.65, rely=0.31)

            lbl_amount_zero = tk.Label(text='Требуется добавить в начало серийного\nномера нули?', bg='#5F5F5F',
                                       fg='white',
                                       font=("Arial", 14))

            lbl_amount_zero.place(relx=0.2, rely=0.38)
            self.scale_amount_zero.place(relx=0.16, rely=0.47)

            lbl_model_kkt = tk.Label(text='Какого вида модель ККТ у заказчика?', bg='#5F5F5F', fg='white',
                                     font=("Arial", 14))

            rad_model1 = tk.Radiobutton(self.gui_window,
                                        text='KKT_PILOT_FP510-Ф_SN:0255100193912\nKKT_PILOT_FP410-Ф_SN:0254100193912',
                                        value='KKT_PILOT_FP*-Ф_SN:', variable=self.rad_model_kkt,
                                        bg='#5F5F5F', font=("Arial", 9), selectcolor='#5F5F5F', fg='white')
            rad_model2 = tk.Radiobutton(self.gui_window, text='KKT_SHTRIH_РИТЕЙЛ-01Ф_SN:0478930012035313',
                                        value='KKT_SHTRIH_РИТЕЙЛ-01Ф_SN:',
                                        variable=self.rad_model_kkt, bg='#5F5F5F', font=("Arial", 9),
                                        selectcolor='#5F5F5F', fg='white')
            rad_model3 = tk.Radiobutton(self.gui_window, text='KKT_VIKI_MINI_SN:0491002948', value='KKT_VIKI_MINI_SN:',
                                        variable=self.rad_model_kkt, bg='#5F5F5F', font=("Arial", 9),
                                        selectcolor='#5F5F5F', fg='white')

            lbl_model_kkt.place(relx=0.2, rely=0.57)
            rad_model1.place(relx=0.01, rely=0.63)
            rad_model2.place(relx=0.46, rely=0.63)
            rad_model3.place(relx=0.46, rely=0.66)

            lbl_contact_human = tk.Label(text='ФИО контактного лица', bg='#5F5F5F', fg='white',
                                         font=("Arial", 12))
            lbl_contact_phone = tk.Label(text='Контактный телефон', bg='#5F5F5F', fg='white',
                                         font=("Arial", 12))
            lbl_contact_email = tk.Label(text='Контактный email', bg='#5F5F5F', fg='white',
                                         font=("Arial", 12))

            lbl_contact_human.place(relx=0.05, rely=0.71)
            lbl_contact_phone.place(relx=0.05, rely=0.76)
            lbl_contact_email.place(relx=0.05, rely=0.81)
            self.name_area.place(relx=0.4, rely=0.71)
            self.phone_area.place(relx=0.4, rely=0.76)
            self.email_area.place(relx=0.4, rely=0.81)

            self.btn_start.place(relx=0.305, rely=0.88)

    def func(self):
        self.btn_start.place(relx=-1, rely=-1)
        self.btn_start.configure(state='disabled')
        self.btn_view.place(relx=0.305, rely=0.88)
        lbl_process = tk.Label(text='Процесс запущен, требуется время для выполнения', bg='#5F5F5F', fg='white',
                               font=("Arial", 10))
        lbl_process.place(relx=0.25, rely=0.95)

        """Экстренный выход и отключить все виджеты! Доделать"""
        view_address = self.rad_view_address.get()
        if view_address == 3:
            prefix_store = ' '
        else:
            prefix_store = self.rad_prefix_store.get()
        scale_amount_zero = self.scale_amount_zero.get()
        model_kkt = self.rad_model_kkt.get()
        contact_human = self.name_area
        contact_phone = self.phone_area
        contact_email = self.email_area
        create_list_kkt.take_tmp(prefix_store, view_address)

        store_kkt_date = create_list_kkt.create_dict_with_kkt(scale_amount_zero)
        print(store_kkt_date)
        with open('final.csv', "w", newline="") as final:
            with open('what_happened.csv', "w", newline="") as bad:
                writer_final = csv.writer(final, delimiter=';')
                writer_bad = csv.writer(bad, delimiter=';')
                count = 0
                total = len(store_kkt_date)
                for row in store_kkt_date:
                    count += 1
                    address, kkt = row
                    serial_number = ' '.join(kkt)
                    try:
                        number = create_request.create_request(address,
                                                               serial_number,
                                                               contact_human,
                                                               contact_phone,
                                                               contact_email,
                                                               model_kkt)
                        writer_final.writerow([address, serial_number, number])
                    except NoSuchElementException:
                        writer_bad.writerow(row)
                    lbl_process.configure(text=f'Выполнено {count} из {total}')

    def begin(self):
        threading.Thread(target=self.func, daemon=True).start()


if __name__ == '__main__':
    gui_window = tk.Tk()
    app = App(gui_window)
    gui_window.mainloop()
