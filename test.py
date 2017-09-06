import mysql.connector
import config as c
from receipt_model import ReceiptModel
from driveclient import DriveClient

conn = mysql.connector.connect(host=c.host, database=c.database, user=c.user, password=c.password)
receipt_model = ReceiptModel(conn)

drive = DriveClient(c, receipt_model)
print(drive.download_new_files())
