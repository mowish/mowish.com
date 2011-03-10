import urllib2
import json

def getjsonfromurl(url):
    raw = urllib2.urlopen(url).read()
    jsondata = json.loads(unicode(raw, errors='ignore'))
    return jsondata