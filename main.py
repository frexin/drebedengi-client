import argparse
import config as c
import mysql.connector
from receipt import ReceiptProcessor
from receipt_model import ReceiptModel
from drebedengi import Drebedengi

parser = argparse.ArgumentParser(description='Импорт чеков в домашнюю бухгалтерию')
parser.add_argument('path', help='Путь к JSON файлу чека')
args = parser.parse_args()

conn = mysql.connector.connect(host=c.host, database=c.database, user=c.user, password=c.password)

# receipt_processor = ReceiptProcessor(args.path, conn)
# receipt_processor.process_file()

receipt_model = ReceiptModel(conn)
receipt_model.set_id(7)

client = Drebedengi(c.duser, c.dpassword)
# client.create_file(receipt_model)
client.send_csv('06_09_2017_02_39_371104604864.txt')
