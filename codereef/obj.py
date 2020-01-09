#
# Copyright 2019-2020 CodeReef
# See CodeReef client LICENSE.txt for licensing details
#
# Developer(s): Grigori Fursin, https://fursin.net
#

from . import config
from . import comm

import ck.kernel as ck

import json
import zipfile
import os

skip_words_in_files=[
 'tmp',
 '.git',
 '.pyc',
 '__pycache__',
 '.cache'
]

##############################################################################
# Publish CK component to the CodeReef portal

def publish(i):

    """
    Input:  {
              cid [str] - CK CID of format (repo UOA:)module UOA:data UOA
                          (can use wildcards)
              (tags) [str] - search multiple CK components by these tags separated by comma
              (version) [str] - assign version
            }

    Output: {
              return  [int]    - return code = 0 if success or >0 if error
              (error) [str]    - error string if return>0 
            }
    """

    # Get current directory (since will be changing it to get info about Git repo)
    cur_dir=os.getcwd()

    # Get current configuration
    r=config.load({})
    if r['return']>0: return r
    cfg=r['dict']

    # Check commands
    # Username ##########################################################
    username=cfg.get('username','')
    if i.get('username')!=None: username=i['username']

    if username=='' or username==None: 
       return {'return':1, 'error':'Username is not defined'}

    cfg['username']=username

    # API key ###########################################################        
    api_key=cfg.get('api_key','')

    if i.get('api_key')!=None: api_key=i['api_key']

    if api_key=='' or api_key==None: 
       return {'return':1, 'error':'API key is not defined'}

    cfg['api_key']=api_key

    # CID ###########################################################        
    cid=i.get('cid')

    if cid=='' or cid==None: 
       return {'return':1, 'error':'CK entry (CID) is not defined'}

    tags=i.get('tags','')

    # Check if no module and use "cr-solution" by default
    if cid.find(':')<0:
       cid='cr-solution:'+cid

    # Version ###########################################################        
    version=i.get('version')
    if version=='' or version==None: 
       return {'return':1, 'error':'Version is not defined'}

    # Extra info about authors
    author=i.get('author','')
    if author==None: author=''

    author_codereef_id=i.get('author_codereef_id','')
    if author_codereef_id==None: author_codereef_id=''

    copyright=i.get('copyright','')
    if copyright==None: copyright=''

    license=i.get('license','')
    if license==None: license=''

    source=i.get('source','')
    if source==None: source=''

    quiet=i.get('quiet',False)
    force=i.get('force',False)

    # List CK components
    r=ck.access({'action':'search',
                 'cid':cid,
                 'tags':tags,
                 'add_info':'yes',
                 'add_meta':'yes',
                 'common_func':'yes'})
    if r['return']>0: return r

    lst=r['lst']
    llst=len(lst)

    if llst==0:
       ck.out('No CK objects found')

    num=0

    # Sort lst by modules and then data
    lst1=sorted(lst, key=lambda x: (x.get('repo_uoa',''), x.get('module_uoa',''), x.get('data_uoa','')))

    for obj in lst1:
        num+=1

        # Basic info about CK object
        repo_uoa=obj['repo_uoa']
        repo_uid=obj['repo_uid']

        module_uoa=obj['module_uoa']
        module_uid=obj['module_uid']

        data_uoa=obj['data_uoa']
        data_uid=obj['data_uid']

        # Print info
        ck.out(str(num)+' out of '+str(llst)+') '+repo_uoa+':'+module_uoa+':'+data_uoa)

        # Check name and date
        data_name=obj.get('info',{}).get('data_name','')
        if data_name==data_uoa: data_name=''

        data_meta=obj['meta']
        if data_name=='':
           if data_meta.get('misc',{}).get('title','')!='':
              data_name=data_meta['misc']['title']

        data_date=''
        if data_meta.get('misc',{}).get('date','')!='':
           data_date=data_meta['misc']['date']

        source2=data_meta.get('source','')
        if source2=='': source2=source

        # Specialize per specific modules
        not_digital_component=False
        extra_dict={}
        extra_tags={}

        if module_uoa=='module':
           extra_dict['last_module_actions']=[]
           actions=data_meta.get('actions',{})
           for a in actions:
               extra_dict['last_module_actions'].append(a+' '+data_uoa)

        elif module_uoa=='cr-lib':
           not_digital_component=True
           extra_tags=['codereef-library']

           if 'reproduced-papers' in data_meta.get('tags',[]):
              extra_tags.append('reproduced-papers')

           data_meta2=data_meta.get('meta',{})

           if data_name=='':
              data_name=data_meta2.get('title','')

           all_authors=data_meta2.get('authors','')
           if all_authors!='':
              extra_dict['all_authors']=[]
              for aa in all_authors.split(','):
                  if aa!='': aa=aa.strip()
                  if aa!='':
                     extra_dict['all_authors'].append(aa)

           for k in ['badge_acm_artifact_available', 'badge_acm_artifact_functional',
                     'badge_acm_artifact_reusable', 'badge_acm_results_replicated',
                     'badge_acm_results_reproduced']:
               if data_meta2.get(k,'')=='yes':
                  extra_tags.append(k)

        elif module_uoa=='cr-event' or module_uoa=='repo':
           not_digital_component=True

        # Get info of the first creation
        first_creation=obj['info'].get('control',{})

        # Load info about repo
        repo_dict={}

        if not force and repo_uoa=='local' and module_uoa!='repo': # Normally skip everything from local unless we publish repos themselves
           ck.out('     SKIPPED')
           continue 

        if module_uoa=='repo':
           if not force and data_uoa=='local':
              ck.out('     SKIPPED')
              continue 

           repo_dict=obj['meta']

        elif repo_uoa!='default' and repo_uoa!='local':
           r=ck.access({'action':'load',
                        'repo_uoa':config.CK_CFG_REPO_UOA,
                        'module_uoa':config.CK_CFG_MODULE_REPO_UOA,
                        'data_uoa':repo_uid,
                        'common_func':'yes'})
           if r['return']>0: return r
           repo_dict=r['dict']
           if 'path' in repo_dict:
              del(repo_dict['path'])

        # Generate temp file to pack
        r=ck.gen_tmp_file({'prefix':'cr-obj-', 'suffix':'.zip'})
        if r['return']>0: return r

        fn=r['file_name']

        # Pack component
        p=obj['path']

        zip_method=zipfile.ZIP_DEFLATED

        ii={'path':p, 'all':'yes'}

        # Prune files for cr-solution
        if module_uoa=='cr-solution':
           ii['ignore_names']=['CK','venv']

        r=ck.list_all_files(ii)
        if r['return']>0: return r

        fl=r['list']

        # Write archive
        try:
          f=open(fn, 'wb')
          z=zipfile.ZipFile(f, 'w', zip_method)
          for fx in fl:
              add=True
              for k in skip_words_in_files:
                  if k in fx:
                     add=False
                     break

              if add:
                 p1=os.path.join(p, fx)
                 z.write(p1, fx, zip_method)
          z.close()
          f.close()

        except Exception as e:
           return {'return':1, 'error':'failed to prepare archive ('+format(e)+')'}

        # Check size
        statinfo = os.stat(fn)
        pack_size=statinfo.st_size

        # Check problems with repository or components
        x=''
        if repo_dict.get('remote','')=='yes':
           x+='remote repo;'
        if repo_dict.get('private','')=='yes':
           x+='private repo;'
        if repo_dict.get('url','')=='' and repo_uoa!='default':
           x+='repo not shared;'
        if pack_size>config.PACK_SIZE_WARNING:
           x+='pack size ('+str(pack_size)+') > '+str(config.PACK_SIZE_WARNING)+';'

        skip_component=False
        if not force and x!='':
           if quiet:
              skip_component=True
           else:
              r=ck.inp({'text':'  This component has potential issues ('+x+'). Skip processing (Y/n)? '})
              if r['return']>0: return r
              s=r['string'].strip()
              if s=='' or s=='Y' or s=='y':
                 skip_component=True

        if skip_component:
           ck.out('    SKIPPED ('+x+')')

           if os.path.isfile(fn):
              os.remove(fn)

           continue

        # Convert to MIME to send over internet
        r=ck.convert_file_to_upload_string({'filename':fn})
        if r['return']>0: return r

        pack64=r['file_content_base64']

        if os.path.isfile(fn):
           os.remove(fn)

        # Check workspaces
        lworkspaces=[]
        workspaces=i.get('workspaces','')
        if workspaces!=None:
           lworkspaces=workspaces.strip().split(',')

        # Get extra info about repo
        os.chdir(p)

        repo_info={'publish_repo_uoa':repo_uoa,
                   'publish_repo_uid':repo_uid}

        # Get current Git URL
        r=ck.run_and_get_stdout({'cmd':['git','config','--get','remote.origin.url']})
        if r['return']==0 and r['return_code']==0: 
           x=r['stdout'].strip()
           if x!='': repo_info['remote_git_url']=x

        # Get current Git branch
        r=ck.run_and_get_stdout({'cmd':['git','rev-parse','--abbrev-ref','HEAD']})
        if r['return']==0 and r['return_code']==0: 
           x=r['stdout'].strip()
           if x!='': repo_info['remote_git_branch']=x

        # Get current Git checkout
        r=ck.run_and_get_stdout({'cmd':['git','rev-parse','--short','HEAD']})
        if r['return']==0 and r['return_code']==0: 
           x=r['stdout'].strip()
           if x!='': repo_info['remote_git_checkout']=x

        repo_info['dict']=repo_dict

        #TBD: owner, version, info about repo
        # Sending request
        r=comm.send({'config':cfg,
                     'action':'publish',
                     'ownership':{
                       'private':i.get('private', False),
                       'workspaces':lworkspaces
                     },
                     'dict':{
                       'publish_module_uoa':module_uoa,
                       'publish_module_uid':module_uid,
                       'publish_data_uoa':data_uoa,
                       'publish_data_uid':data_uid,
                       'publish_data_name':data_name,
                       'publish_data_date':data_date,
                       'publish_pack':pack64,
                       'publish_pack_size':pack_size,
                       'repo_info':repo_info,
                       'first_creation':first_creation,
                       'version':version,
                       'author':author,
                       'author_codereef_id':author_codereef_id,
                       'copyright':copyright,
                       'license':license,
                       'source':source2,
                       'not_digital_component':not_digital_component,
                       'extra_dict':extra_dict,
                       'extra_tags':extra_tags,
                     }
                    })
        if r['return']>0: 
           ck.out('    WARNING: CodeReef API returned error: '+r['error'])
        else:
           data_uid=r['data_uid']
           ck.out('    CodeReef component ID: '+data_uid)

    os.chdir(cur_dir)

    return {'return':0}

##############################################################################
# Download CK component from the CodeReef portal to the local repository

def download(i):

    """
    Input:  {
              cid [str] - CK CID of format (repo UOA:)module UOA:data UOA
                          (can use wildcards)
              (version) [str] - assign version
              (force) [bool] - if True, force download even if components already exists

              (tags) [str] - can search by tags (usually soft/package)

              (all) [bool] - if True, download dependencies (without force!)
            }

    Output: {
              return  [int]    - return code = 0 if success or >0 if error
              (error) [str]    - error string if return>0 
            }
    """

    # CID ###########################################################        
    cid=i.get('cid')

    if cid=='' or cid==None: 
       return {'return':1, 'error':'CK entry (CID) is not defined'}

    version=i.get('version')
    if version==None: version=''

    force=i.get('force')
    al=i.get('all')

    skip_module_check=i.get('skip_module_check',False)

    # Parse CID
    r=ck.parse_cid({'cid':cid})
    if r['return']>0: return r

    repo_uoa=r.get('repo_uoa','')
    data_uoa=r.get('data_uoa','')
    module_uoa=r.get('module_uoa','')

    tags=i.get('tags','')

    spaces=i.get('spaces','')

    # Get current configuration
    r=config.load({})
    if r['return']>0: return r
    cfg=r['dict']

    # Sending request to download
    r=comm.send({'config':cfg,
                 'action':'download',
                 'dict':{
                   'module_uoa':module_uoa,
                   'data_uoa':data_uoa,
                   'version':version,
                   'tags':tags
                 }
                })
    if r['return']>0: 
       return r

    lst=r['components']

    for l in lst:

        fpack64=l['file_base64']
        fmd5=l['file_md5']

        muoa=l['module_uoa']
        muid=l['module_uid']

        duoa=l['data_uoa']
        duid=l['data_uid']

        dependencies=l.get('dependencies',[])

        xcid=muoa+':'+duoa

        # Check if module exists
        if not skip_module_check:
           r=ck.access({'action':'find',
                        'module_uoa':'module',
                        'data_uoa':muoa,
                        'common_func':'yes'})
           if r['return']>0:
              if r['return']!=16: return r

              x='module:'+muoa
              if repo_uoa!='': x=repo_uoa+':'+x

# FGG: we should not add "version" for dependencies or related components since it's not the same!
#              r=download({'cid':x, 'force':force, 'version':version, 'skip_module_check':True, 'all':al})
              r=download({'cid':x, 'force':force, 'skip_module_check':True, 'all':al})
              if r['return']>0: return r

        # Check if entry already exists
        path=''
        r=ck.access({'action':'find',
                     'common_func':'yes',
                     'repo_uoa':repo_uoa,
                     'module_uoa':muid,
                     'data_uoa':duid})
        if r['return']==0:
           path=r['path']

           if not force:
              return {'return':8, 'error':'local entry for "'+xcid+'" already exists'}

        # Find/create entry (as a placeholder for pack.zip)
        r=ck.access({'action':'find',
                     'common_func':'yes',
                     'repo_uoa':repo_uoa,
                     'module_uoa':muid,
                     'data_uoa':duid})
        if r['return']>0:
           if r['return']!=16: return r

           r=ck.access({'action':'add',
                        'common_func':'yes',
                        'repo_uoa':repo_uoa,
                        'module_uoa':muid,
                        'data_uoa':duoa,
                        'data_uid':duid,
                        'ignore_update':'yes'})
           if r['return']>0: return r

        path=r['path']

        # Prepare pack
        ppz=os.path.join(path, config.PACK_FILE)

        if os.path.isfile(ppz):
           if not force:
              return {'return':1, 'error':'pack file already exists ('+ppz+')'}
           os.remove(ppz)

        # Save pack to file
        rx=ck.convert_upload_string_to_file({'file_content_base64':fpack64, 'filename':ppz})
        if rx['return']>0: return rx

        # MD5 of the pack
        rx=ck.load_text_file({'text_file':ppz, 'keep_as_bin':'yes'})
        if rx['return']>0: return rx
        bpack=rx['bin']

        import hashlib
        md5=hashlib.md5(bpack).hexdigest()

        if md5!=fmd5:
           return {'return':1, 'error':'MD5 of the newly created pack ('+md5+') did not match the one from CodeReef server ('+fmd5+')'}

        # Unpack to src subdirectory
        import zipfile

        f=open(ppz,'rb')
        z=zipfile.ZipFile(f)
        for d in z.namelist():
            if d!='.' and d!='..' and not d.startswith('/') and not d.startswith('\\'):
               pp=os.path.join(path,d)
               if d.endswith('/'):
                  # create directory
                  if not os.path.exists(pp): os.makedirs(pp)
               else:
                  ppd=os.path.dirname(pp)
                  if not os.path.exists(ppd): os.makedirs(ppd)

                  # extract file
                  fo=open(pp, 'wb')
                  fo.write(z.read(d))
                  fo.close()
        f.close()

        # Remove pack file
        os.remove(ppz)

        # Note
        ck.out(spaces+'Successfully downloaded "'+xcid+'" to '+path)

        # Check deps
        if al:
           if len(dependencies)>0:
              ck.out(spaces+'  Checking dependencies ...')

#           import json
#           print (json.dumps(dependencies))
#           input('xyz')

           for dep in dependencies:
               muoa=dep.get('module_uid','')
               duoa=dep.get('data_uid','')

               tags=dep.get('tags',[])
               xtags=''
               if len(tags)>0:
                  xtags=','.join(tags)
                  muoa='package'
                  duoa=''

               cid=muoa+':'+duoa
               rx=download({'cid':cid,
                            'all':al,
                            'tags':xtags,
                            'spaces':spaces+'    '})
               if rx['return']>0 and rx['return']!=8 and rx['return']!=16: return rx
               if rx['return']==16:
                  if xtags=='': return rx
                  rx=download({'cid':'soft:',
                               'all':al,
                               'tags':xtags,
                               'spaces':spaces+'    '})
                  if rx['return']>0 and rx['return']!=8: return rx

    return r
