from flask import Flask, request, render_template
import mysql.connector
import json
import config as c
from receipt_model import ReceiptModel

conn = mysql.connector.connect(host=c.host, database=c.database, user=c.user, password=c.password)
receipt_model = ReceiptModel(conn)
app = Flask(__name__)

@app.route("/")
def index():
    receipt_id = request.args.get('receipt_id')

    url = c.url + '/get?receipt_id=' + receipt_id
    categories = receipt_model.get_categories()

    return render_template('index.html', base_url=url, cats=categories)


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

app.run()
