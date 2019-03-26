import simplejson as json
import os
import re
import csv
import datetime
import random
from mysql.connector import MySQLConnection, Error


class ReceiptProcessor:

    file_path = ""
    file_name = None
    db_conn = None
    rc_id = None
    rc_dict = {}
    patterns = []

    def __init__(self, db_conn):
        self.db_conn = db_conn
        self.load_patterns()

    def set_file(self, filepath):
        self.file_path = filepath
        self.file_name = os.path.split(filepath)[1]

    def csv_to_dict(self, filename):
        res = {'items': []}

        with open(filename, newline='', encoding='utf-8') as csvfile:
            counter = 0
            totalsum = 0
            reader = csv.reader(csvfile)

            for row in reader:
                if counter == 1:
                    res['user'] = row[1]
                    res['dateTime'] = datetime.datetime.strptime(row[0], "%d.%m.%y %H:%M").timestamp()
                    res['fiscalDocumentNumber'] = random.randint(100000, 50000000)
                if counter > 2:
                    cost = row[2].replace(",", ".")
                    cost = float(cost) * 100

                    newitem = {'name': row[0], 'price': round(cost), 'quantity': float(row[1])}
                    res['items'].append(newitem)

                    price = row[3]
                    price = price.replace(",", ".")
                    price = price.replace("\xa0", "")

                    totalsum = totalsum + float(price)

                counter = counter + 1

            res['totalSum'] = round(totalsum) * 100

        return res

    def process_file(self):
        with open(self.file_path, encoding='utf-8') as json_data:
            if self.file_path.find(".csv") != -1:
                rc = self.csv_to_dict(self.file_path)
            else:
                rc = json.load(json_data)

            query = "INSERT INTO receipts (dt_create, dt_process, shop_name, total_amount, doc_number, filename) " \
                    "VALUES (FROM_UNIXTIME(%s), NOW(), %s, %s, %s, %s)"
            shop_name = rc['user'] if rc['user'] else 'неизвестный'
            args = (rc['dateTime'], shop_name, rc['totalSum'], rc['fiscalDocumentNumber'], self.file_name)

            try:
                cursor = self.db_conn.cursor()
                cursor.execute(query, args)

                self.rc_id = cursor.lastrowid
                rc['id'] = self.rc_id
                self.rc_dict = rc

                self.db_conn.commit()
                self.handle_items(rc['items'])

            except Error as error:
                print(error)

    def load_patterns(self):
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT pattern, category_id FROM patterns")

        rows = cursor.fetchall()

        for row in rows:
            self.patterns.append(row)

    def find_category_for_item(self, name):
        result = None

        for item in self.patterns:
            regex, cat_id = item
            regex = re.compile(regex, re.IGNORECASE)

            match = re.search(regex, name)

            if match:
                result = cat_id
                break

        return result

    def save_item(self, item, cat_id):
        query = "INSERT INTO receipts_items (receipt_id, name, quantity, price, cat_id) " \
                "VALUES (%s, %s, %s, %s, %s)"
        args = (self.rc_id, item['name'], item['quantity'], item['price'], cat_id)

        cursor = self.db_conn.cursor()
        cursor.execute(query, args)
        self.db_conn.commit()

    def handle_items(self, items):
        items = self.prepare_items(items)

        for item in items:
            cat_id = self.find_category_for_item(item['name'])
            self.save_item(item, cat_id)

    def prepare_items(self, items):
        uniq_names = {}

        for item in items:
            key = item['name']

            if key not in uniq_names:
                uniq_names[key] = item
            else:
                olditem = uniq_names[key]
                price = float(olditem['price'])
                quantity = float(olditem['quantity'])

                uniq_names[key]['price'] += price
                uniq_names[key]['quantity'] += quantity

        return uniq_names.values()