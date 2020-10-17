from api_naumen import API_Naumen
import create_request
import create_list_kkt
import csv
import os.path
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from selenium.common.exceptions import NoSuchElementException
from version import get_version


class App:
    api = API_Naumen()

    def __init__(self, gui_window):
        self.gui_window = gui_window
        self.gui_window.title('Пулл-мастер 3000')
        self.gui_window.iconbitmap(os.getcwd() + '\\icon.ico')
        self.gui_window.geometry('600x600')
        self.gui_window['bg'] = '#5F5F5F'

        """Блок авторизации в системе"""

        self.lbl_l_naumen = tk.Label(self.gui_window, text='Login Naumen', font=("Arial Bold", 20), bg='#5F5F5F',
                                     fg='white')
        self.lbl_p_naumen = tk.Label(self.gui_window, text='Password Naumen', font=("Arial Bold", 20), bg='#5F5F5F',
                                     fg='white')
        self.login_area = tk.Entry(self.gui_window, width=30)
        self.password_area = tk.Entry(self.gui_window, width=30, show='*')

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

        """Проверка на обновления"""
        if get_version():
            answer = messagebox.askyesno('Обновление', 'Хорошие новости!\nВышло обновлени\nОбновить?')
            if answer:
                self.api.driver.get('https://github.com/NearBirdEZ/Pull_master_naumen/tree/master/Pull_Master_3000')

        """----------------------------------------------------------------------------------------------------------"""

        self.rad_view_address = tk.IntVar()  # Информации с радиокнопок о виде адреса

        self.rad_prefix_store = tk.StringVar(value=0)  # Информация о префиксе магазина
        self.rad_entry_prefix11 = tk.Entry(self.gui_window, width=35, state='disable', font=("Courier", 12, "italic"))
        # Текст, который требуется написать в заявку
        self.text_request = scrolledtext.ScrolledText(gui_window, width=52, height=3, font=("Courier", 12, "italic"))
        # слова "Срок действия" или "срок выполнения"
        self.entry_period_of_execution = tk.Entry(self.gui_window, width=54, font=("Courier", 12, "italic"))

        self.name_area = tk.Entry(self.gui_window, width=50)  # Контактное лицо
        self.phone_area = tk.Entry(self.gui_window, width=50)  # Контактный телефон
        self.email_area = tk.Entry(self.gui_window, width=50)  # Контактный емаил

        self.btn_start = tk.Button(gui_window, text='Запустить выполнение пулла', command=self.begin, bg='#5F5F5F',
                                   fg='white', font=("Arial", 13))

    """-------------------------------------------------------------------------------------------------------------"""

    def clear(self):
        """Функция очиски логина и пароля"""
        self.login_area.delete('0', tk.END)
        self.password_area.delete('0', tk.END)

    def send_log_pass(self):
        """Функция авторизации в ИС Наумен с помощью логина и пароля"""
        login = self.login_area.get()
        password = self.password_area.get()
        if login == '' or password == '':
            messagebox.showinfo('Ошибка', 'Не заполнены\nлогин и пароль')
            self.clear()
            return
        login = self.login_area.get()
        password = self.password_area.get()
        """---------------------------------------------------------------------------------------------------------"""
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
            self.btn_clear.destroy()
            self.btn_send.destroy()
            self.lbl_p_naumen.destroy()
            self.lbl_l_naumen.destroy()
            self.login_area.destroy()
            self.password_area.destroy()
            self.gui_window.geometry('600x750')

            """-----------------------------------------------------------------------------------------------------"""

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
            rad_view1.place(relx=0.05, rely=0.055)
            rad_view2.place(relx=0.3, rely=0.055)
            rad_view3.place(relx=0.6, rely=0.055)
            self.rad_view_address.set(1)

            lbl_prefix = tk.Label(text='Для какого магазина запускаем пулл?', bg='#5F5F5F', fg='white',
                                  font=("Arial", 14))

            rad_prefix1 = tk.Radiobutton(self.gui_window, text='Алькор и Ко', value='алькор и ко',
                                         variable=self.rad_prefix_store, bg='#5F5F5F', font=("Arial", 13),
                                         selectcolor='#5F5F5F', fg='white',
                                         command=self.disable_entry)
            rad_prefix2 = tk.Radiobutton(self.gui_window, text='Атак', value='атак', variable=self.rad_prefix_store,
                                         bg='#5F5F5F', font=("Arial", 13), selectcolor='#5F5F5F', fg='white',
                                         command=self.disable_entry)
            rad_prefix3 = tk.Radiobutton(self.gui_window, text='Эсте Лаудер', value='эсте лаудер',
                                         variable=self.rad_prefix_store, bg='#5F5F5F', font=("Arial", 13),
                                         selectcolor='#5F5F5F', fg='white',
                                         command=self.disable_entry)
            rad_prefix4 = tk.Radiobutton(self.gui_window, text='Детский Мир', value='детский мир',
                                         variable=self.rad_prefix_store, bg='#5F5F5F', font=("Arial", 13),
                                         selectcolor='#5F5F5F', fg='white',
                                         command=self.disable_entry)
            rad_prefix5 = tk.Radiobutton(self.gui_window, text='Иль де Ботэ', value='иль де ботэ',
                                         variable=self.rad_prefix_store, bg='#5F5F5F', font=("Arial", 13),
                                         selectcolor='#5F5F5F', fg='white',
                                         command=self.disable_entry)
            rad_prefix6 = tk.Radiobutton(self.gui_window, text="Levi's", value='леви', variable=self.rad_prefix_store,
                                         bg='#5F5F5F', font=("Arial", 13), selectcolor='#5F5F5F', fg='white',
                                         command=self.disable_entry)
            rad_prefix7 = tk.Radiobutton(self.gui_window, text='Манго Раша', value='манго',
                                         variable=self.rad_prefix_store,
                                         bg='#5F5F5F', font=("Arial", 13), selectcolor='#5F5F5F', fg='white',
                                         command=self.disable_entry)
            rad_prefix8 = tk.Radiobutton(self.gui_window, text='Нью Йоркер РУС', value='нью йоркер рус',
                                         variable=self.rad_prefix_store, bg='#5F5F5F', font=("Arial", 13),
                                         selectcolor='#5F5F5F', fg='white',
                                         command=self.disable_entry)
            rad_prefix9 = tk.Radiobutton(self.gui_window, text='Тами и Ко', value='тами и ко',
                                         variable=self.rad_prefix_store, bg='#5F5F5F', font=("Arial", 13),
                                         selectcolor='#5F5F5F', fg='white',
                                         command=self.disable_entry)
            rad_prefix10 = tk.Radiobutton(self.gui_window, text='Другое', value='другое',
                                          variable=self.rad_prefix_store, bg='#5F5F5F', font=("Arial", 13),
                                          selectcolor='#5F5F5F', fg='white',
                                          command=self.enable_entry)
            self.rad_prefix_store.set('алькор и ко')

            lbl_prefix.place(relx=0.2, rely=0.13)
            rad_prefix1.place(relx=0.05, rely=0.18)
            rad_prefix2.place(relx=0.05, rely=0.25)
            rad_prefix3.place(relx=0.05, rely=0.32)
            rad_prefix4.place(relx=0.35, rely=0.18)
            rad_prefix5.place(relx=0.35, rely=0.25)
            rad_prefix6.place(relx=0.35, rely=0.32)
            rad_prefix7.place(relx=0.65, rely=0.18)
            rad_prefix8.place(relx=0.65, rely=0.25)
            rad_prefix9.place(relx=0.65, rely=0.32)
            rad_prefix10.place(relx=0.05, rely=0.39)

            lbl_text_request = tk.Label(text='Текст заявки', bg='#5F5F5F', fg='white', font=("Arial", 14))

            lbl_text_request.place(relx=0.4, rely=0.45)
            self.text_request.place(relx=0.05, rely=0.505)
            self.text_request.insert(tk.END, 'Требуется замена фискального накопителя')

            lbl_period_of_execution = tk.Label(text='Текст после серийного номера и до даты', bg='#5F5F5F', fg='white',
                                               font=("Arial", 14))

            lbl_period_of_execution.place(relx=0.20, rely=0.62)

            self.entry_period_of_execution.place(relx=0.05, rely=0.68)
            self.entry_period_of_execution.insert(tk.END, 'Срок действия до')

            lbl_contact_human = tk.Label(text='ФИО контактного лица', bg='#5F5F5F', fg='white',
                                         font=("Arial", 12))
            lbl_contact_phone = tk.Label(text='Контактный телефон', bg='#5F5F5F', fg='white',
                                         font=("Arial", 12))
            lbl_contact_email = tk.Label(text='Контактный email', bg='#5F5F5F', fg='white',
                                         font=("Arial", 12))

            lbl_contact_human.place(relx=0.05, rely=0.78)
            lbl_contact_phone.place(relx=0.05, rely=0.83)
            lbl_contact_email.place(relx=0.05, rely=0.88)
            self.name_area.place(relx=0.4, rely=0.78)
            self.phone_area.place(relx=0.4, rely=0.83)
            self.email_area.place(relx=0.4, rely=0.88)

            self.btn_start.place(relx=0.305, rely=0.95)

            """-----------------------------------------------------------------------------------------------------"""

    def disable_entry(self):
        self.rad_entry_prefix11.place(relx=-1)
        self.rad_entry_prefix11.configure(state='disable')

    def enable_entry(self):
        self.rad_entry_prefix11.place(relx=0.25, rely=0.4)
        self.rad_entry_prefix11.configure(state='normal')

    def func(self):

        """Основная функция запуска выполнения пулла"""
        self.btn_start.configure(state='disable')  # Отключение кнопки старт
        lbl_process = tk.Label(text='Процесс запущен, требуется время для выполнения', bg='#5F5F5F', fg='white',
                               font=("Arial", 10))
        lbl_process.place(relx=0.25, rely=0.91)

        """Экстренный выход нужно сделать, может быть, если будет место"""
        #  Место кончилось - экстренный выход: крестик в углу проги

        view_address = self.rad_view_address.get()
        """Если вид адреса сгенерирован науменом, то префикс ничему не равен"""
        if view_address == 3:
            prefix_store = ' '

        else:
            """Иначе берем значение префикса магазина из радиокнопки"""
            prefix_store = self.rad_prefix_store.get()
            """Если радиокнопка вернула значение 'другое', значит значение необходимо взять из поля Entry напротив"""
            if prefix_store == 'другое':
                prefix_store = self.rad_entry_prefix11.get().lower()
        period_of_execution = self.entry_period_of_execution.get()
        text_request = self.text_request.get('0.1', tk.END)
        contact_human = self.name_area.get()
        contact_phone = self.phone_area.get()
        contact_email = self.email_area.get()

        store_kkt_date = create_list_kkt.create_dict_with_kkt(prefix_store, view_address)
        """Файлы создаются при любом раскладе, т.к. ВСЕГДА что-то может пойти не так и эту информацию 
        нужно записывать"""
        with open('final.csv', "w", newline="") as final:
            with open('what_happened.csv', "w", newline="") as bad:
                writer_final = csv.writer(final, delimiter=';')
                writer_bad = csv.writer(bad, delimiter=';')
                count = 0
                total = len(store_kkt_date)
                for row in store_kkt_date:
                    count += 1
                    """Распаковка листа на составляющие адреса и списка ккт"""
                    address, kkt = row
                    serial_number = ' '.join(kkt)
                    try:
                        """После всех подготовок начинается создание заявок. 
                        Программа как автопило Теслы - человек должен следить"""
                        number, link = create_request.create_request(address,
                                                                     serial_number,
                                                                     text_request,
                                                                     period_of_execution,
                                                                     contact_human,
                                                                     contact_phone,
                                                                     contact_email, )
                        #  writer_final.writerow([address, serial_number, number]) устаревшая запись в файл
                        """Запись каждой ккт на новой строке
                        Сделано для последующего использования ВПР"""
                        for alone_serial_number in serial_number.split():
                            writer_final.writerow(
                                [address, alone_serial_number.split('*')[0].split(':')[1], number, link])

                    except NoSuchElementException:
                        """Вероятно, если вылетел эксепшен, значит в магазине отсутвует услуга 'Замена ФН'"""
                        for alone_serial_number in serial_number.split():
                            writer_bad.writerow(
                                [address, alone_serial_number.split('*')[0].split(':')[1],
                                 alone_serial_number.split('*')[1],
                                 'Не уалось зарегистрировать. Требуется проверка человеком'])
                    lbl_process.configure(text=f'Выполнено {count} из {total}')

    def begin(self):
        threading.Thread(target=self.func, daemon=True).start()


if __name__ == '__main__':
    gui_window = tk.Tk()
    app = App(gui_window)
    gui_window.mainloop()
