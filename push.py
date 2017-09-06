from pushover import Client


class PushoverClient:

    client = None
    base_url = None

    def __init__(self, key, token, url):
        self.client = Client(key, api_token=token)
        self.base_url = url

    def send_msg(self, url, title, msg):
        res = self.client.send_message(msg, url=url, title=title)

        return res

    def send_url(self, rc_dict):
        title = "Обработка чека №{}".format(rc_dict['fiscalDocumentNumber'])
        url = "{0}/?receipt_id={1}".format(self.base_url, rc_dict['id'])
        msg = "Магазин: {0}\nСумма: {1}".format(rc_dict['user'], rc_dict['totalSum'])

        return self.send_msg(url, title, msg)