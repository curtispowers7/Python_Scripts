import hashlib
import requests
import sys
import json

VirusTotalKey = '8852e4a928620098fe0a2333dd4e9d58fa6c5b67d000eb785bbe544968c9f0aa'
url = 'https://www.virustotal.com/api/v3/search'

FileName = sys.argv[1]
md5 = hashlib.md5()

with open(FileName, 'rb') as file:
    contents = file.read()
    md5.update(contents)

digest = md5.hexdigest()
print(digest)

params = {
    'query': digest
}

headers = {
    'x-apikey': VirusTotalKey
}

response = requests.get(url, headers=headers, params=params)

results = json.loads(response.text)

if not results['data']:
    print('{0} is not malicious'.format(FileName))
    
else:
    attributes = results['data'][0]['attributes']

    malwaretype = attributes['popular_threat_classification']['popular_threat_category'][0]['value']
    malwarevotes = attributes['popular_threat_classification']['popular_threat_category'][0]['count']

    print('''{0} is voted as malicious by {1} source(s) with the following classification:
    {2}
    '''.format(FileName, malwarevotes, malwaretype))
