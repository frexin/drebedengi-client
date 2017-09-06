import onedrivesdk
import config as c
from onedrivesdk.helpers import GetAuthCodeServer

redirect_uri = 'http://localhost:8000/'
client_secret = c.ms_secret
client_id = c.ms_app_id
api_base_url = 'https://api.onedrive.com/v1.0/'
scopes = ['wl.signin', 'wl.offline_access', 'onedrive.readwrite']

http_provider = onedrivesdk.HttpProvider()
auth_provider = onedrivesdk.AuthProvider(
    http_provider=http_provider,
    client_id=client_id,
    scopes=scopes)

auth_provider.load_session()
auth_provider.refresh_token()

client = onedrivesdk.OneDriveClient(api_base_url, auth_provider, http_provider)

# print(client.item(id='root').subscriptions.request())

items = client.item(id='53E99255798DE9CE!1583').children.get()

for item in items:
    print(item.name, item.id)