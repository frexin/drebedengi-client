from mysql.connector import Error


class ReceiptModel:

    conn = None
    id = None

    def __init__(self, conn):
        self.conn = conn

    def set_id(self, receipt_id):
        self.id = receipt_id

    def get_receipt(self):
        query = "SELECT * FROM receipts WHERE id = %(id)s LIMIT 1"
        cursor = self._run_query(query, {'id': self.id}, True)

        return cursor.fetchone()

    def get_categories(self):
        query = "SELECT id, name FROM categories ORDER BY id"
        cursor = self._run_query(query)

        return cursor.fetchall()

    def get_items(self, without_cat=False):
        query = "SELECT ri.id, ri.name, quantity, price, cat_id, c.name as category FROM receipts_items ri " \
                "LEFT JOIN categories c ON ri.cat_id = c.id WHERE receipt_id = %(rec)s"

        if without_cat:
            query += " AND cat_id IS NULL"

        cursor = self._run_query(query, {'rec': self.id}, True)

        return cursor.fetchall()

    def attach_category(self, pattern, cat_id, item_id):
        query = "INSERT INTO patterns (pattern, category_id) VALUES (%s, %s)"

        try:
            self._run_query(query, (pattern, cat_id))
            query = "UPDATE receipts_items SET cat_id = %s WHERE id = %s"
            self._run_query(query, (cat_id, item_id))

        except Error as error:
            print(error)

    def _run_query(self, query, params=None, is_dict=False):
        # self.conn.reconnect()

        cursor = self.conn.cursor(dictionary=is_dict)
        cursor.execute(query, params)

        return cursor

