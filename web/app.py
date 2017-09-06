from flask import Flask, request, render_template
from flask_cors import CORS
import mysql.connector
import json
import threading
import os
import config as c
from receipt_model import ReceiptModel
from driveclient import DriveClient
from receipt import ReceiptProcessor
from push import PushoverClient
from drebedengi import Drebedengi

conn = mysql.connector.connect(host=c.host, database=c.database, user=c.user, password=c.password)

receipt_model = ReceiptModel(conn)
drive_client = DriveClient(c, receipt_model)
rc_processor = ReceiptProcessor(conn)
pushover = PushoverClient(c.push_ukey, c.push_token, c.url)
drebedengi = Drebedengi(c.duser, c.dpassword)

app = Flask(__name__)
CORS(app)


def import_files(files):
    for file in files:
        filepath = c.download_path + os.sep + file
        rc_processor.set_file(filepath)
        rc_processor.process_file()

        rc_dict = rc_processor.rc_dict
        pushover.send_url(rc_dict)


def monitor_files():
    new_files = drive_client.download_new_files()

    if len(new_files):
        print('Found new files: ' + str(len(new_files)))
        import_files(new_files)

    threading.Timer(30, monitor_files).start()


@app.route("/")
def index():
    receipt_id = request.args.get('receipt_id')

    url = c.url
    categories = receipt_model.get_categories()

    return render_template('index.html', base_url=url, cats=categories, rc_id=receipt_id)


@app.route("/get")
def get_orhpan_items():
    receipt_id = request.args.get('receipt_id')
    receipt_model.set_id(receipt_id)

    rows = receipt_model.get_items(True)
    result = json.dumps(rows)

    return result


@app.route("/update", methods=['POST'])
def attach_categories():
    receipt_id = request.args.get('receipt_id')
    post = request.get_data().decode("utf-8")

    patterns = json.loads(post)

    for p in patterns:
        receipt_model.attach_category(p['pattern'], p['cat_id'], p['id'])

    receipt_model.set_id(receipt_id)
    file = drebedengi.create_file(receipt_model)

    send_res = drebedengi.send_csv(file)

    msg = 'Чек добавлен' if send_res else 'Ошибка при добавлении чека'
    pushover.send_msg(None, 'Результат добавления', msg)

    return "OK"

monitor_files()
app.run()
