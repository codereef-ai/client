#
# Copyright 2019 CodeReef
# See CodeReef client LICENSE.txt for licensing details
#
# Developer(s): Grigori Fursin, https://fursin.net
#               Herve Guillou, herve@codereef.ai
#

# CK entry to keep CodeReef client configuration info
CK_CFG_REPO_UOA="local"
CK_CFG_DATA_UOA="codereef-client"
CK_CFG_MODULE_UID="b34231a3467566f8" # ck info module:cfg

CK_CFG_MODULE_REPO_UOA="befd7892b0d469e9" # CK module UOA for REPO

CR_DEFAULT_SERVER_URL="https://codereef.ai/portal/api/v1/?"
CR_DEFAULT_SERVER_USER="codereef-crowd-user"
CR_DEFAULT_SERVER_API_KEY="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozOCwidXNlcm5hbWUiOiJjb2RlcmVlZi1jcm93ZC11c2VyIiwiZXhwIjoxNTc2ODQ5MzM4LCJlbWFpbCI6ImNvZGVyZWVmLmNyb3dkLnVzZXJAZ21haWwuY29tIn0.WrxyFZakw3daBmhbQ74W8VzC_buJP1zbpAmmH2jiADU"

PACK_SIZE_WARNING=5000000

CR_WORK_DIR='CR'
CR_SOLUTIONS_DIR='solutions'

CR_MODULE_UOA='cr-solution'

PACK_FILE='pack.zip'

CR_ENV_USERNAME='CR_USER'
CR_ENV_API_KEY='CR_KEY'

CR_LINE='**************************************************************************'

CR_SOLUTION_CK_COMPONENTS=[
 {'cid':'module:device', 'version':'1.0.0'},
 {'cid':'module:env', 'version':'1.1.0'},
 {'cid':'module:machine', 'version':'1.0.0'},
 {'cid':'module:misc', 'version':'1.0.0'},
 {'cid':'module:os', 'version':'1.0.0'},
 {'cid':'module:package', 'version':'1.1.0'},
 {'cid':'module:platform*', 'version':'1.0.0'},
 {'cid':'module:script', 'version':'1.0.0'},
 {'cid':'module:soft', 'version':'1.1.0'},
 {'cid':'module:docker', 'version':'1.0.0'},
 {'cid':'module:cr-event', 'version':'1.0.0'},
 {'cid':'module:cr-lib', 'version':'1.0.0'},
 {'cid':'module:cr-result', 'version':'1.0.0'},
 {'cid':'module:cr-solution', 'version':'1.0.0'},
 {'cid':'os:*', 'version':'1.0.0'},
 {'cid':'platform.init:*', 'version':'1.0.0'},
 {'cid':'script:download-and-install-package', 'version':'1.0.0'},
 {'cid':'soft:compiler.python', 'version':'1.0.0'},
 {'cid':'soft:tool.adb', 'version':'1.0.0'},
]

import ck.kernel as ck

bootstrapping=False

##############################################################################
# Load CodeReef client configuration

def load(i):
    """
    Input:  {
            }

    Output: {
              return  [int]    - return code = 0 if success or >0 if error
              (error) [str]    - error string if return>0 

              dict    [dict]   - configuration dictionary
              path    [str]    - path to CK cfg entry
            }
    """

    global bootstrapping

    import os

    # Get current configuration
    cfg={
          'server_url':CR_DEFAULT_SERVER_URL   # Default
        }
    path=''

    ii={'action':'load',
        'repo_uoa':CK_CFG_REPO_UOA,
        'module_uoa':CK_CFG_MODULE_UID,
        'data_uoa':CK_CFG_DATA_UOA}

    r=ck.access(ii)
    if (r['return']>0 and r['return']!=16): return r

    if r['return']==0: 
       cfg=r['dict']
       path=r['path']

    if not bootstrapping and (r['return']==16 or cfg.get('bootstrapped','')!='yes'):
       rx=update({'cfg':cfg})
       if rx['return']>0: return rx

    # Check overriding by env
    v=os.environ.get(CR_ENV_USERNAME,'')
    if v!='': cfg['username']=v
    v=os.environ.get(CR_ENV_API_KEY,'')
    if v!='': cfg['api_key']=v

    return {'return':0, 'dict':cfg, 'path':path}

##############################################################################
# Update CK modules and configuration

def update(i):
    """
    Input:  {
              (force) [bool] - if True, force update
            }

    Output: {
              return  [int]    - return code = 0 if success or >0 if error
              (error) [str]    - error string if return>0 
            }
    """

    global bootstrapping
    bootstrapping=True

    force=i.get('force')
    cfg=i.get('cfg',{})

    from . import obj

    title='Bootstrapping'
    if cfg.get('bootstrapped','')=='yes': title='Updating'

    ck.out(title+' CodeReef client:')
    ck.out('')

    for x in CR_SOLUTION_CK_COMPONENTS:
        r=obj.download({'cid':x['cid'], 'version':x.get('version',''), 'force':force})
        if r['return']>0: 
           if r['return']!=8: return r
           else: ck.out(r['error'])

    ck.out('')

    # Update cfg
    cfg['bootstrapped']='yes'

    ii={'action':'update',
        'repo_uoa':CK_CFG_REPO_UOA,
        'module_uoa':CK_CFG_MODULE_UID,
        'data_uoa':CK_CFG_DATA_UOA,
        'dict':cfg,
        'sort_keys':'yes'}

    r=ck.access(ii)

    ck.out(title+' finished!')
    ck.out('')

    return r

##############################################################################
# Get path to work directory in a USER space

def get_work_dir(i):
    """
    Input:  {
            }

    Output: {
              return  [int]    - return code = 0 if success or >0 if error
              (error) [str]    - error string if return>0 

              path    [str]    - path to work dir
            }
    """

    import os

    # Get home user directory
    from os.path import expanduser
    home = expanduser("~")

    work_dir=os.path.join(home, CR_WORK_DIR)
    if not os.path.isdir(work_dir):
       os.makedirs(work_dir)

    return {'return':0, 'path':work_dir}
