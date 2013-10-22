import base64
import json
import requests
import ConfigParser
import os
import sys

try:
    config = ConfigParser.ConfigParser()
    config.read([os.path.expanduser('~/.imgur.conf')])
except:
    import traceback
    traceback.print_exc()
    print "Couldn't find configuration file: ~/.imgur.conf"
    sys.exit(1)
CLIENT_ID = config.get('imgur', 'client_id')
IMGUR_API = "https://api.imgur.com/3/"

def upload_image(filename):
    img = base64.b64encode(open(filename, 'rb').read())
    headers = {"Authorization": "Client-ID %s" % CLIENT_ID}
    data = {
        'key': CLIENT_ID,
        'image': img,
        'type': 'base64',
        'name': filename,
        'title': filename
    }
    response = requests.post(IMGUR_API + "upload.json", data=data, headers=headers)
    return response.json()

if __name__ == "__main__":
    for root, dirs, files in os.walk(sys.argv[1]):
        for f in files:
            filename = os.path.join(root, f)
            print "Uploading %s" % filename
            response = upload_image(filename)
            print "Filename: %s\t\tURL: %s\t\tDeleteHash: %s" % (filename, response['data']['link'], response['data']['deletehash'])
