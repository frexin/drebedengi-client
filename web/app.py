from flask import Flask, request, render_template
import mysql.connector
import json
import threading
import config as c
from receipt_model import ReceiptModel
from driveclient import DriveClient

conn = mysql.connector.connect(host=c.host, database=c.database, user=c.user, password=c.password)
receipt_model = ReceiptModel(conn)
drive_client = DriveClient(c, receipt_model)

app = Flask(__name__)


def monitor_files():
    new_files = drive_client.download_new_files()
    print(new_files)

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
    post = request.get_data().decode("utf-8")

    patterns = json.loads(post)
    param_count = len(patterns)

    if param_count:
        for p in patterns:
            receipt_model.attach_category(p['pattern'], p['cat_id'], p['id'])

    return "OK"

monitor_files()
app.run()
