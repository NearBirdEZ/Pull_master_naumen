from api_naumen import API_Naumen
import create_request
import create_list_kkt
import csv
from datetime import datetime
import logging
import os.path
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from selenium.common.exceptions import NoSuchElementException


"""Записываем логи папку logs"""
if not os.path.isdir("logs"):
    os.mkdir("logs")


"""Определяем название лога. Форматируем название по дате и времени"""
path_log = f"log_pull_{datetime.now().date()}_{datetime.now().strftime('%H.%M')}.log"

"""Для записи логов меняем деректорию"""
os.chdir('logs')

"""Инициализируем уровень логов"""
logging.basicConfig(filename=path_log, level=logging.CRITICAL)


class App:
    api = API_Naumen()

    def __init__(self, gui_window):
        self.gui_window = gui_window
        self.gui_window.title('Пулл-мастер 3000')
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

        """----------------------------------------------------------------------------------------------------------"""

        self.rad_view_address = tk.IntVar()  # Информации с радиокнопок о виде адреса

        self.rad_prefix_store = tk.StringVar(value=0)  # Информация о префиксе магазина
        self.rad_entry_prefix11 = tk.Entry(self.gui_window, width=50, state='disable')

        self.scale_amount_zero = tk.Scale(self.gui_window, from_=0, to=10, orient=tk.HORIZONTAL, length=400,
                                          bg='#5F5F5F', fg='white',
                                          font=("Arial", 13))  # Если префикса нет на радиокнопках

        self.text_request = scrolledtext.ScrolledText(gui_window, width=65,
                                                      height=5)  # Текст, который требуется написать в заявку

        self.rad_model_kkt = tk.StringVar(value=0)  # Вариант модели, у пилотовской есть * для указания разновидности

        self.name_area = tk.Entry(self.gui_window, width=50)  # Контактное лицо
        self.phone_area = tk.Entry(self.gui_window, width=50)  # Контактный телефон
        self.email_area = tk.Entry(self.gui_window, width=50)  # Контактный емаил

        self.btn_start = tk.Button(gui_window, text='Запустить выполнение пулла', command=self.begin, bg='#5F5F5F',
                                   fg='white', font=("Arial", 13))
        self.btn_view = tk.Button(text='Показать процесс в браузере', command=self.view, bg='#5F5F5F',
                                  fg='white', font=("Arial", 13))

    """-------------------------------------------------------------------------------------------------------------"""

    def view(self):
        """Функция, которая возвращает браузер из далеких земель обратно на экран"""
        self.api.driver.set_window_position(0, 0)
        self.btn_view.configure(state='disabled')

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
            self.gui_window.geometry('600x800')

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
            rad_view1.place(relx=0.05, rely=0.045)
            rad_view2.place(relx=0.3, rely=0.045)
            rad_view3.place(relx=0.6, rely=0.045)
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

            lbl_prefix.place(relx=0.2, rely=0.11)
            rad_prefix1.place(relx=0.05, rely=0.16)
            rad_prefix2.place(relx=0.05, rely=0.21)
            rad_prefix3.place(relx=0.05, rely=0.26)
            rad_prefix4.place(relx=0.35, rely=0.16)
            rad_prefix5.place(relx=0.35, rely=0.21)
            rad_prefix6.place(relx=0.35, rely=0.26)
            rad_prefix7.place(relx=0.65, rely=0.16)
            rad_prefix8.place(relx=0.65, rely=0.21)
            rad_prefix9.place(relx=0.65, rely=0.26)
            rad_prefix10.place(relx=0.05, rely=0.31)



            lbl_amount_zero = tk.Label(text='Требуется добавить в начало серийного\nномера нули?', bg='#5F5F5F',
                                       fg='white',
                                       font=("Arial", 14))

            lbl_amount_zero.place(relx=0.2, rely=0.35)
            self.scale_amount_zero.place(relx=0.16, rely=0.43)

            lbl_text_request = tk.Label(text='Текст заявки', bg='#5F5F5F', fg='white', font=("Arial", 14))

            lbl_text_request.place(relx=0.4, rely=0.49)
            self.text_request.place(relx=0.05, rely=0.53)
            self.text_request.insert(tk.END, 'Требуется замена фискального накопителя')

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

            lbl_model_kkt.place(relx=0.2, rely=0.64)
            rad_model1.place(relx=0.01, rely=0.70)
            rad_model2.place(relx=0.46, rely=0.70)
            rad_model3.place(relx=0.46, rely=0.73)

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
        self.rad_entry_prefix11.place(relx=0.25, rely=0.315)
        self.rad_entry_prefix11.configure(state='normal')

    def func(self):

        """Основная функция запуска выполнения пулла"""
        self.btn_start.destroy()  # Отключение кнопки старт
        self.btn_view.place(relx=0.305, rely=0.95)  # Подмена кнопки Старт на "Показать выполнение в браузере"
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
                prefix_store = self.rad_entry_prefix11.get()
        scale_amount_zero = self.scale_amount_zero.get()
        model_kkt = self.rad_model_kkt.get()
        text_request = self.text_request.get('0.1', tk.END).lower()
        contact_human = self.name_area.get()
        contact_phone = self.phone_area.get()
        contact_email = self.email_area.get()

        """Костыль, который был не продуман при создании gui"""
        create_list_kkt.transfer_kostil(prefix_store, view_address)

        store_kkt_date = create_list_kkt.create_dict_with_kkt(scale_amount_zero)
        """Файлы создаются при любом раскладе, т.к. ВСЕГДА что-то может пойти не так и эту информацию нужно записывать"""
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
                        number = create_request.create_request(address,
                                                               serial_number,
                                                               text_request,
                                                               contact_human,
                                                               contact_phone,
                                                               contact_email,
                                                               model_kkt)
                        #  writer_final.writerow([address, serial_number, number]) устаревшая запись в файл
                        """Запись каждой ккт на новой строке
                        Сделано для последующего использования ВПР"""
                        for alone_serial_number in serial_number.split():
                            writer_final.writerow(
                                [address, '0' * scale_amount_zero + alone_serial_number.split('_')[0], number])

                    except NoSuchElementException:
                        """Вероятно, если вылетел эксепшен, значит в магазине отсутвует услуга 'Замена ФН'"""
                        writer_bad.writerow([address, '0' * scale_amount_zero + alone_serial_number.split('_')[0],
                                             'Не уалось зарегистрировать. Требуется проверка человеком'])
                    lbl_process.configure(text=f'Выполнено {count} из {total}')

    def begin(self):
        threading.Thread(target=self.func, daemon=True).start()


if __name__ == '__main__':
    gui_window = tk.Tk()
    app = App(gui_window)
    gui_window.mainloop()
