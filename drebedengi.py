#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

# взаимодействие реализовано по HTTP - притворяемся браузер-клиентом
# возможна реализация через SOAP: http://www.drebedengi.ru/soap/dd.wsdl

http_login_url = "https://www.drebedengi.ru/?module=v2_start&action=login"
http_csv_send_url = "https://www.drebedengi.ru/?module=v2_homeBuhPrivateImport&action=csv_submit"
http_csv_confirm_url = "https://www.drebedengi.ru/?module=v2_homeBuhPrivateImport&action=confirm"
http_search_url = "https://www.drebedengi.ru/?module=v2_homeBuhPrivateReport"
http_delete_item_url = "https://www.drebedengi.ru/?module=v2_homeBuhPrivateTextReportMain"


class Drebedengi:
    session = None
    categories = []

    def __init__(self, user, passw):
        session = requests.Session()

        data = {
            "o": "",
            "email": user,
            "password": passw,
            "ssl": "on"
        }

        login = session.post(http_login_url, data)
        soup = BeautifulSoup(login.content, 'html.parser')
        categories = [option.text.encode(
            'utf-8') for option in soup.find(id="add_w_category_id").find_all("option")]

        self.categories = categories[1:]
        self.session = session

    def create_file(self, receipt_model):
        receipt_data = receipt_model.get_receipt()
        receipt_items = receipt_model.get_items()

        filename = receipt_data['filename'].replace('.json', '.txt')
        f = open(filename, 'w', encoding='utf-8')

        for item in receipt_items:
            price = round(item['price'] / 100, 2) * -1
            line = [str(price), 'руб', item['category'], 'Тинькоф', receipt_data['dt_create'].strftime('%Y-%m-%d %H:%M'),
                    item['name'], '', '1']

            str_line = ';'.join(line)
            f.write(str_line + '\n')

        f.close()

        return filename

    def logged_in(self):
        return self.session != None


    def get_categories(self):
        return self.categories


    def send_csv(self, filename):
        data = {
            'imp_fmt': 'imp_in_fmt',
            'csvFile': (filename, open(filename, 'rb'), 'text/csv')
        }

        r = self.session.post(http_csv_send_url, files=data)
        post1 = r.status_code
        r = self.session.post(http_csv_confirm_url)
        post2 = r.status_code

        if post1 == 200 and post2 == 200:
            print("Successfully imported!")
            return True
        else:
            print("Something went wrong...")
            return False
