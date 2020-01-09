#
# Communication with CodeReef server
# Based on "perform_remote_action" function from the CK kernel
#
# Copyright 2019 CodeReef
# See CodeReef client LICENSE.txt for licensing details
#
# Developer(s): Grigori Fursin, https://fursin.net
#


from . import config

import ck.kernel as ck

import json
import sys

##############################################################################
# Send JSON request to CodeReef portal

def send(i):
    """
    Input:  {
              action [str]     - remote API action name
              config [dict]    - configuration for remote server
              dict [dict]      - dict to send to remote server
              ownership [dict] - info about user ownership
            }

    Output: {
              return  [int]    - return code = 0 if success or >0 if error
              (error) [str]    - error string if return>0 
            }
    """

    # Get server and user config
    config=i.get('config',{})

    username=config.get('username')
#    if username=='' or username==None: 
#       return {'return':1, 'error':'Username is not defined'}

    api_key=config.get('api_key')
#    if api_key=='' or api_key==None: 
#       return {'return':1, 'error': 'API key is not defined'}

    url=config.get('server_url')
    if url=='' or url==None:
       return {'return':1, 'error': 'CodeReef API URL is not defined'}

    remote_server_user=config.get('server_user')
    if remote_server_user==None: remote_server_user=''

    remote_server_password=config.get('server_pass')
    if remote_server_password==None: remote_server_password=''

    remote_skip_certificate_validation=config.get('server_skip_validation')
    if remote_skip_certificate_validation==None: remote_skip_certificate_validation=''

    # Import modules compatible with Python 2.x and 3.x
    import urllib

    try:    import urllib.request as urllib2
    except: import urllib2

    try:    from urllib.parse import urlencode
    except: from urllib import urlencode

    # Prepare dict to send to remote server
    ii={}
    ii['action']=i.get('action','')
    ii['dict']=i.get('dict',{})
    ii['ownership']=i.get('ownership',{})
    ii['username']=username
    ii['api_key']=api_key

    # Prepare post variables
    r=ck.dumps_json({'dict':ii, 'skip_indent':'yes'})
    if r['return']>0: return r

    s=r['string']
    if sys.version_info[0]>2: s=s.encode('utf8')

    post=urlencode({'cr_json':s}) # We have to send JSON as string
    if sys.version_info[0]>2: post=post.encode('utf8')

    # Check if skip SSL certificate
    ctx=None
    add_ctx=False

    if remote_skip_certificate_validation=='yes':

       import ssl

       ctx = ssl.create_default_context()
       ctx.check_hostname = False
       ctx.verify_mode = ssl.CERT_NONE

       add_ctx=True

    # If auth
    auth=None
    add_auth=False

    if remote_server_user!='' and remote_server_user!=None: 
       if remote_server_password==None: remote_server_password=''

       auth = urllib2.HTTPPasswordMgrWithDefaultRealm()
       auth.add_password(None, url, remote_server_user, remote_server_password)

       add_auth=True

    # Prepare handler (TBD: maybe there is another, more elegant way?)
    if add_auth and add_ctx:
       urllib2.install_opener(urllib2.build_opener(urllib2.HTTPBasicAuthHandler(auth), urllib2.HTTPSHandler(context=ctx)))
    elif add_auth:
       urllib2.install_opener(urllib2.build_opener(urllib2.HTTPBasicAuthHandler(auth)))
    elif add_ctx:
       urllib2.install_opener(urllib2.build_opener(urllib2.HTTPSHandler(context=ctx)))

    # Prepare request
    request = urllib2.Request(url, post)

    # Connect
    try:
       f=urllib2.urlopen(request)
    except Exception as e:
       return {'return':1, 'error':'Access to the CodeReef portal failed ('+format(e)+')'}

    # Read from Internet
    try:
       s=f.read()
       f.close()
    except Exception as e:
       return {'return':1, 'error':'Failed reading stream from the CodeReef portal ('+format(e)+')'}

    # Check output
    try: s=s.decode('utf8')
    except Exception as e: pass

    # Try to convert output to dictionary
    r=ck.convert_json_str_to_dict({'str':s, 'skip_quote_replacement':'yes'})
    if r['return']>0: 
       return {'return':1, 'error':'can\'t parse output from the CodeReef portal ('+r['error']+'):\n'+s[:256]+'\n\n...)'}

    d=r['dict']

    if 'return' in d: d['return']=int(d['return']) # Fix for some strange behavior when 'return' is not integer - should check why ...
    else:
       d['return']=99
       d['error']='repsonse doesn\'t follow the CodeReef standard'

    return d

##############################################################################
# Low-level access to CodeReef portal

def access(i):

    """
    Input:  {
              (filename) [str] - load JSON from this file
              (json) [str] - parse JSON string from command line (use ' instead of ")
            }

    Output: {
              return  [int]    - return code = 0 if success or >0 if error
              (error) [str]    - error string if return>0 
            }
    """

    filename=i.get('filename','')
    json_string=i.get('json','')

    if filename=='' and json_string=='':
       return {'return':1, 'error':'either "filename" or "json" should define results to be pushed'}

    # Prepare data
    data={}

    if filename!='':
       r=ck.load_json_file({'json_file':filename})
       if r['return']>0: return r

       data2=r['dict']
       data.update(data2)

    if json_string!='':
       import json

       json_string=json_string.replace("'", '"')

       data2=json.loads(json_string)

       data.update(data2)

    # Get current configuration
    r=config.load({})
    if r['return']>0: return r
    cfg=r['dict']

    # Prepare request
    ii={'config':cfg}
    ii.update(data)

    # Sending request to download
    r=send(ii)
    if r['return']>0: return r

    ck.out('Output:')
    ck.out('')

    ck.out(json.dumps(r, indent=2))

    return r
