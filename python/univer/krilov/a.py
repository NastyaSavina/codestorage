import tempfile
from oauth2client import file
from googleapiclient import discovery
from pathlib import Path
import httplib2
from airflow.contrib.operators.databricks_operator import DatabricksSubmitRunOperator

API_SERVICE_NAME = 'webmasters'
API_VERSION = 'v3'
with tempfile.NamedTemporaryFile() as tmp:
    tmp.write(str.encode('{"_module": "oauth2client.client", "scopes": ["https://www.googleapis.com/auth/webmasters.readonly"], "token_expiry": "2018-09-10T13:58:19Z", "id_token": null, "user_agent": null, "access_token": "ya29.GlsUBt4GD-bZZgOQZyOxMo28F14c4dGb4fqBP-zwoqGtCf1JNGC_u_F6Ya7WzIq9A8dGH_w3cOotGocTG2YyqWUV2Zn8oDr7TdH0ukh6PLqbww1bqhD7dlHvucq4", "token_uri": "https://www.googleapis.com/oauth2/v3/token", "invalid": false, "token_response": {"access_token": "ya29.GlsUBt4GD-bZZgOQZyOxMo28F14c4dGb4fqBP-zwoqGtCf1JNGC_u_F6Ya7WzIq9A8dGH_w3cOotGocTG2YyqWUV2Zn8oDr7TdH0ukh6PLqbww1bqhD7dlHvucq4", "scope": "https://www.googleapis.com/auth/webmasters.readonly", "expires_in": 3600, "token_type": "Bearer"}, "client_id": "551103279375-v7dc84rm7ba3hr7gr9h477ag1q20pm77.apps.googleusercontent.com", "token_info_uri": "https://www.googleapis.com/oauth2/v3/tokeninfo", "client_secret": "oGrW2HJ4jiJ-ttsu-Ij-_OPd", "revoke_uri": "https://accounts.google.com/o/oauth2/revoke", "_class": "OAuth2Credentials", "refresh_token": "1/q8xG064hS-vnIFKhmZpyjM_HtCdrJ9Q7SckX8fbsgZM", "id_token_jwt": null}'))
    tmp.flush()
    print(tmp.name)
    storage = file.Storage(tmp.name)
    credentials = storage.get()
    http = credentials.authorize(http=httplib2.Http())
    service = discovery.build(API_SERVICE_NAME, API_VERSION, http=http, cache_discovery=False)
    print(credentials)
    print(http)
    print(service)

    task = DatabricksSubmitRunOperator(
        task
    )