import onedrivesdk
import os


class DriveClient:

    client = None
    config = None
    rc_model = None

    def __init__(self, c, rc_model):
        self.config = c
        self.rc_model = rc_model

        http_provider = onedrivesdk.HttpProvider()
        auth_provider = onedrivesdk.AuthProvider(
            http_provider=http_provider,
            client_id=c.ms_app_id,
            scopes=['wl.signin', 'wl.offline_access', 'onedrive.readwrite'])

        auth_provider.load_session()
        auth_provider.refresh_token()

        self.client = onedrivesdk.OneDriveClient('https://api.onedrive.com/v1.0/', auth_provider, http_provider)

    def download_new_files(self):
        new_files = []

        old_rc_list = [orc['filename'] for orc in self.rc_model.get_receipts()]
        all_rc_list = self.client.item(id=self.config.folder_id).children.get()

        for rc in all_rc_list:
            if rc.name not in old_rc_list:
                if not self.is_already_downloaded(rc.name):
                    new_files.append(rc.name)
                    path = self.config.download_path + os.sep + rc.name
                    self.client.item(id=rc.id).download(path)

        return new_files

    def get_local_files(self):
        local_files = []

        for file in os.listdir(self.config.download_path):
            if file.endswith('.json'):
                local_files.append(file)

        return local_files

    def is_already_downloaded(self, filename):
        return filename in self.get_local_files()

