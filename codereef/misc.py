#
# Low-level API
# Developer: Grigori Fursin
#

import urllib
import json
import sys

try:
  import urllib.request as urllib2
except: 
  import urllib2

try:
  from urllib.parse import urlencode
  from urllib.parse import quote_plus
except: 
  from urllib import urlencode
  from urllib import quote_plus


def request(i):
    """
    Input:  {
              url - URL
              get - get parameters
              post - post parameters
            }

    Output: {
              return  - return code = 0 if success or >0 if error
              (error) - error string if return>0 
            }
    """

    url=i['url']

    # Prepare dict to send to remote server
    ii=i.get('get',{})

    started=False
    for k in ii:
        v=ii[k]
        if started: 
           url+='&'
        started=True 
        url+=k+'='+quote_plus(v)

    # Request
    request = urllib2.Request(url)

    # Connect
    try:
       f=urllib2.urlopen(request)
    except Exception as e:
       return {'return':1, 'error':'Access failed ('+format(e)+')'}

    # Read
    try:
       s=f.read()
    except Exception as e:
       return {'return':1, 'error':'Failed to read stream ('+format(e)+')'}

    # CLose
    try:
       f.close()
    except Exception as e:
       return {'return':1, 'error':'Failed to close stream ('+format(e)+')'}

    # Check UTF
    try: 
       s=s.decode('utf8')
    except Exception as e: 
       pass

    # Check output
    d={}

    # Try to convert output to dictionary
    try:
      d=json.loads(s)
    except Exception as e: 
       pass

    return {'return':0, 'string':s, 'dict':d}
