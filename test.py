import mysql.connector
import os
import config as c
from receipt_model import ReceiptModel
from push import PushoverClient
from receipt import ReceiptProcessor
from driveclient import DriveClient

conn = mysql.connector.connect(host=c.host, database=c.database, user=c.user, password=c.password)
receipt_model = ReceiptModel(conn)

# drive = DriveClient(c, receipt_model)
# print(drive.download_new_files())

# pushover = PushoverClient(c.push_ukey, c.push_token)
# print(pushover.send_msg('http://ya.ru', 'Обработка чека', 'Пожалуйста, обработайте чек'))

# receipt_file = '06_09_2017_02_39_371104604864.json'
# receipt_path = c.download_path + os.sep + receipt_file
#
# rc_processor = ReceiptProcessor(receipt_path, conn)
# rc_processor.process_file()
#
# rc_id = rc_processor.rc_id
