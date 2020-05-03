import json

json_str = '{"host":"ftp1.medallia.eu","user":"burberry","pass":"eUE0cnVwcl8=-"}'
parsed = json.loads(json_str)
print(parsed['pass'])