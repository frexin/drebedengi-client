import json
import os
import re
from mysql.connector import MySQLConnection, Error


class ReceiptProcessor:

    file_path = ""
    file_name = None
    db_conn = None
    id = None
    patterns = []

    def __init__(self, path, db_conn):
        self.file_path = path
        self.db_conn = db_conn

        self.file_name = os.path.split(path)[1]

        self.load_patterns()

    def process_file(self):
        with open(self.file_path, encoding='utf-8') as json_data:
            rc = json.load(json_data)

            query = "INSERT INTO receipts (dt_create, dt_process, shop_name, total_amount, doc_number, filename) " \
                    "VALUES (FROM_UNIXTIME(%s), NOW(), %s, %s, %s, %s)"
            args = (rc['dateTime'], rc['user'], rc['totalSum'], rc['fiscalDocumentNumber'], self.file_name)

            try:
                cursor = self.db_conn.cursor()
                cursor.execute(query, args)

                self.id = cursor.lastrowid
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
        args = (self.id, item['name'], item['quantity'], item['price'], cat_id)

        cursor = self.db_conn.cursor()
        cursor.execute(query, args)
        self.db_conn.commit()

    def handle_items(self, items):

        for item in items:
            cat_id = self.find_category_for_item(item['name'])
            self.save_item(item, cat_id)



