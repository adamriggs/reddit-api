import urllib2
import urllib
import json
from base64 import b64encode

def sideLoad(filepath):
    req = urllib2.Request('https://api.imgur.com/3/image', 'image=' + urllib.quote(b64encode(open(filepath,'rb').read())))
    req.add_header('Authorization', 'Client-ID ' + '89861848efdc33c')
    response = urllib2.urlopen(req)
    response = json.loads(response.read())
    return str(response[u'data'][u'link'])


print sideLoad('postgres.png')
