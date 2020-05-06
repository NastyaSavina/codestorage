import json
import base64
import requests

DOMAIN = 'https://burberry-databricks.cloud.databricks.com/'
TOKEN = b'dapid20bcb8163b4be2a97c23734b7f09462'
BASE_URL = 'https://%s/api/2.0/dbfs/' % (DOMAIN)

def dbfs_rpc(action, body):
  """ A helper function to make the DBFS API request, request/response is encoded/decoded as JSON """
  response = requests.post(
    BASE_URL + action,
    headers={"Authorization: Bearer %s" % TOKEN },
    json=body
  )
  return response.json()

handle = dbfs_rpc("workspace/delete", {"path": "/Users/aliaksandr.zaparozhtsau@burberry.com/test_backups", "recursive": "false"})

