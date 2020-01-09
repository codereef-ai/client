#
# Copyright 2019-2020 CodeReef
# See CodeReef client LICENSE.txt for licensing details
#
# Developer(s): Grigori Fursin, https://fursin.net
#               Herve Guillou, herve@codereef.ai
#

import click
import ck.kernel as ck

##############################################################################
@click.group()
def cli():
    return 0

# SETUP CLIENT #############################################################################
@cli.command()

@click.option('-u', '--username', 'username', required=False)
@click.option('-a', '--api_key', 'api_key', required=False)
@click.option('-s', '--server_url', 'server_url', required=False)
@click.option('-su', '--server_user', 'server_user', required=False)
@click.option('-sp', '--server_pass', 'server_pass', required=False)
@click.option('-ss', '--server_skip_validation', 'server_skip_validation', required=False)

def setup(username,
          api_key,
          server_url,
          server_user,
          server_pass,
          server_skip_validation):
    '''
     Setup CodeReef client.
    ''' 
    from . import setup
    return setup.setup({'username':username,
                        'api_key':api_key,
                        'server_url':server_url,
                        'server_user':server_user,
                        'server_pass':server_pass,
                        'server_skip_validation':server_skip_validation})

# LOGIN TEST #############################################################################
@cli.command()

@click.option('-u', '--username', 'username', required=False)
@click.option('-a', '--api_key', 'api_key', required=False)
@click.option('-s', '--server_url', 'server_url', required=False)
@click.option('-su', '--server_user', 'server_user', required=False)
@click.option('-sp', '--server_pass', 'server_pass', required=False)
@click.option('-ss', '--server_skip_validation', 'server_skip_validation', required=False)

def login(username,
          api_key,
          server_url,
          server_user,
          server_pass,
          server_skip_validation):
    '''
     Test login to CodeReef portal.
    '''
    from . import setup
    return setup.login({'username':username,
                        'api_key':api_key,
                        'server_url':server_url,
                        'server_user':server_user,
                        'server_pass':server_pass,
                        'server_skip_validation':server_skip_validation})

# PUBLISH COMPONENT #############################################################################
@cli.command()

@click.argument('cid')

@click.option('-t', '--tags', 'tags', required=False, default='')
@click.option('-u', '--username', 'username', required=False)
@click.option('-a', '--api_key', 'api_key', required=False)
@click.option('--quiet', 'quiet', required=False, is_flag=True)
@click.option('--force', 'force', required=False, is_flag=True)
@click.option('--private', is_flag=True)
@click.option('-w', '--workspaces', 'workspaces', required=False)
@click.option('-v', '--version', 'version', required=False)
@click.option('--author', 'author', required=False)
@click.option('--author_codereef_id', 'author_codereef_id', required=False)
@click.option('--copyright', 'copyright', required=False)
@click.option('--license', 'license', required=False)
@click.option('--source', 'source', required=False)

def publish(cid,
            tags,
            username,
            api_key,
            force,
            quiet,
            private,
            workspaces,
            version,
            author,
            author_codereef_id,
            copyright,
            license,
            source):
    '''
    Publish CK component to the CodeReef portal.

    CID: CK identifier ({repo UOA}:){module UOA}:{data UOA}.
    ''' 
    from . import obj
    r=obj.publish({'cid':cid,
                   'tags':tags,
                   'username':username,
                   'api_key':api_key,
                   'quiet':quiet,
                   'force':force,
                   'private':private,
                   'workspaces':workspaces,
                   'version':version,
                   'author':author,
                   'author_codereef_id':author_codereef_id,
                   'copyright':copyright,
                   'license':license,
                   'source':source})

    if r['return']>0: ck.err(r)
    return 0

# DOWNLOAD COMPONENT #############################################################################
@cli.command()

@click.argument('cid')

@click.option('-v', '--version', 'version', required=False)
@click.option('-f', '--force', 'force', required=False, is_flag=True)
@click.option('-t', '--tags', 'tags', required=False, default='')
@click.option('-a', '--all', 'all', required=False, is_flag=True)

def download(cid,
             version,
             force,
             tags,
             all):
    '''
    Download CK component from the CodeReef portal.

    CID: CK identifier {module UOA}:{data UOA}.
    ''' 
    from . import obj
    r=obj.download({'cid':cid,
                    'version':version,
                    'force':force,
                    'tags':tags,
                    'all':all})

    if r['return']>0: ck.err(r)
    return 0

# BOOSTRAP #############################################################################
@cli.command()

@click.option('-f', '--force', 'force', required=False, is_flag=True)

def update(force):
    '''
    Update/bootstrap CodeReef components.
    '''

    from . import config
    r=config.update({'force':force})

    if r['return']>0: ck.err(r)
    return 0

# INIT GRAPH #############################################################################
@cli.command()

@click.argument('uid', required=False)

@click.option('-v', '--version', 'version', required=False)
@click.option('-d', '--desc_file', 'desc_file', required=False)

def init_graph(uid,
               version,
               desc_file):
    '''
    Init graph at the CodeReef portal.

    UID: CodeReef graph identifier.
    ''' 
    from . import graph
    r=graph.init({'uid':uid,
                  'version':version,
                  'desc_file':desc_file})

    if r['return']>0: ck.err(r)
    return 0

# PUSH RESULT #############################################################################
@cli.command()

@click.argument('uid', required=True)

@click.option('-v', '--version', 'version', required=False, default='')
@click.option('-f', '--filename', 'filename', required=False, default='')
@click.option('-j', '--json', 'json_string', required=False, default='')
@click.option('-p', '--point', 'point', required=False, default='')

def push_result(uid,
                version,
                filename,
                json_string,
                point):
    '''
    Push result to a graph at the CodeReef portal.

    UID: CodeReef graph identifier.
    ''' 
    from . import graph
    r=graph.push({'uid':uid,
                  'version':version,
                  'filename':filename,
                  'json':json_string,
                  'point':point})

    if r['return']>0: ck.err(r)
    return 0

# ACCESS API #############################################################################
@cli.command()

@click.option('-f', '--filename', 'filename', required=False, default='')
@click.option('-j', '--json', 'json_string', required=False, default='')

def access(filename,
           json_string):
    '''
    Access CodeReef Portal via JSON API.
    ''' 
    from . import comm
    r=comm.access({'filename':filename,
                   'json':json_string})

    if r['return']>0: ck.err(r)
    return 0

# INIT SOLUTION #############################################################################
@cli.command()

@click.argument('uid', required=False)

@click.option('-u', '--username', 'username', required=False, default='')
@click.option('-a', '--api_key', 'api_key', required=False, default='')
@click.option('-n', '--name', 'name', required=False, default='')
@click.option('-t', '--tags', 'tags', required=False, default='')
@click.option('-pp', '--python_path', required=False, default='')
@click.option('-pv', '--python_version', required=False, default='')
@click.option('-pvf', '--python_version_from', required=False, default='')
@click.option('-pvt', '--python_version_to', required=False, default='')
@click.option('-pl', '--python_localenv', 'python_localenv', is_flag=True, default=True)
@click.option('-ho', '--host_os', 'host_os', required=False, default='')
@click.option('-to', '--target_os', 'target_os', required=False, default='')
@click.option('-di', '--device_id', 'device_id', required=False, default='')
@click.option('-h', '--hostname', 'hostname', required=False, default='')
@click.option('-w', '--workflow', 'workflow', required=False, default='')
@click.option('-wr', '--workflow_repo_url', 'workflow_repo_url', required=False, default='')
@click.option('-wc', '--workflow_cmd', 'workflow_cmd', required=False, default='')
@click.option('-wce', '--workflow_cmd_extra', 'workflow_cmd_extra', required=False, default='')
@click.option('-wi', '--workflow_input', 'workflow_input', required=False, default='') # Input source (stream, webcam, etc)
@click.option('-wid', '--workflow_input_dir', 'workflow_input_dir', required=False, default='') # Input directory (will be cleaned)
@click.option('-wod', '--workflow_output_dir', 'workflow_output_dir', required=False, default='') # Output directory (will be cleaned)
@click.option('-d', '--desc_prereq', 'desc_prereq', required=False, default='')
@click.option('-dp', '--desc_prepare', 'desc_prepare', required=False, default='')
@click.option('-dr', '--desc_run', 'desc_run', required=False, default='')
@click.option('-s', '--add_extra_scripts', 'add_extra_scripts', required=False, default='')
@click.option('-e', '--add_extra_meta_from_file', 'add_extra_meta_from_file', required=False, default='')
@click.option('-rf', '--result_file', 'result_file', required=False, default='')
@click.option('--update_meta_and_stop', 'update_meta_and_stop', is_flag=True, default=False)
@click.option('--skip_graph_init', 'skip_graph_init', is_flag=True, default=False)
@click.option('-r', '--resume', 'resume', is_flag=True, default=False)
@click.option('-ss', '--skip_stop', 'skip_stop', is_flag=True, default=False)
@click.option('-g', '--graphs', 'graphs', required=False, default='')
@click.option('-dg', '--desc_graph', 'desc_graph', required=False, default='')
@click.option('-gc', '--graph_convertor', 'graph_convertor', required=False, default='')

def init(uid,
         username,
         api_key,
         name,
         tags,
         python_path,
         python_version,
         python_version_from,
         python_version_to,
         python_localenv,
         host_os,
         target_os,
         device_id,
         hostname,
         workflow,
         workflow_repo_url,
         workflow_cmd,
         workflow_cmd_extra,
         workflow_input,
         workflow_input_dir,
         workflow_output_dir,
         desc_prereq,
         desc_prepare,
         desc_run,
         add_extra_scripts,
         add_extra_meta_from_file,
         result_file,
         update_meta_and_stop,
         skip_graph_init,
         resume,
         skip_stop,
         graphs,
         desc_graph,
         graph_convertor):
    '''
    Init CodeReef portable solution.

    UID: CodeReef solution identifier.
    ''' 
    from . import solution
    r=solution.init({'uid':uid,
                     'username':username,
                     'api_key':api_key,
                     'name':name,
                     'tags':tags,
                     'python_path':python_path,
                     'python_version':python_version,
                     'python_version_from':python_version_from,
                     'python_version_to':python_version_to,
                     'python_localenv':python_localenv,
                     'host_os':host_os,
                     'target_os':target_os,
                     'device_id':device_id,
                     'hostname':hostname,
                     'workflow_repo_url':workflow_repo_url,
                     'workflow':workflow,
                     'workflow_cmd':workflow_cmd,
                     'workflow_cmd_extra':workflow_cmd_extra,
                     'workflow_input':workflow_input,
                     'workflow_input_dir':workflow_input_dir,
                     'workflow_output_dir':workflow_output_dir,
                     'desc_prereq':desc_prereq,
                     'desc_prepare':desc_prepare,
                     'desc_run':desc_run,
                     'add_extra_meta_from_file':add_extra_meta_from_file,
                     'result_file':result_file,
                     'add_extra_scripts':add_extra_scripts,
                     'update_meta_and_stop':update_meta_and_stop,
                     'skip_graph_init':skip_graph_init,
                     'resume':resume,
                     'skip_stop':skip_stop,
                     'graphs':graphs,
                     'desc_graph':desc_graph,
                     'graph_convertor':graph_convertor})

    if r['return']>0: ck.err(r)
    return 0

# ACTIVATE SOLUTION #############################################################################
@cli.command()

@click.argument('uid')

def activate(uid):
    '''
     Activate virtual environment from the prepared solution.

     UID - CodeReef solution identifier.
    ''' 
    from . import solution
    r=solution.activate({'uid':uid})

    if r['return']>0: ck.err(r)
    return 0

# RUN SOLUTION #############################################################################
@cli.command()

@click.argument('uid')

@click.option('-c', '--cmd', 'cmd', required=False, default='')

def benchmark(uid, 
        cmd):
    '''
    Benchmark CodeReef solution.

    UID: CodeReef solution identifier.
    ''' 
    from . import solution
    r=solution.benchmark({'uid':uid,
                    'cmd':cmd})

    if r['return']>0: ck.err(r)
    return 0

# RUN SOLUTION #############################################################################
@cli.command()

@click.argument('uid')

@click.option('-c', '--cmd', 'cmd', required=False, default='')

def run(uid, 
        cmd):
    '''
    Run CodeReef portable solution.

    UID: CodeReef solution identifier.
    ''' 
    from . import solution
    r=solution.run({'uid':uid,
                    'cmd':cmd})

    if r['return']>0: ck.err(r)
    return 0

# LIST SOLUTIONS #############################################################################
@cli.command()

@click.argument('uid', required=False)

def ls(uid):
    '''
    List CodeReef portable solutions.

    UID: CodeReef solution identifier (can use wildcards)..
    ''' 
    from . import solution
    r=solution.ls({'uid':uid})

    if r['return']>0: ck.err(r)
    return 0

# FIND SOLUTION #############################################################################
@cli.command()

@click.argument('uid')

def find(uid):
    '''
    Find CodeReef portable solution.

    UID: CodeReef solution identifier.
    ''' 
    from . import solution
    r=solution.find({'uid':uid})

    if r['return']>0: ck.err(r)
    return 0

# DELETE SOLUTION #############################################################################
@cli.command()

@click.argument('uid')

def rm(uid):
    '''
    Delete CodeReef portable solution.

    UID: CodeReef solution identifier (can use wildcards).
    ''' 
    from . import solution
    r=solution.rm({'uid':uid})

    if r['return']>0: ck.err(r)
    return 0

# START SERVICE TO COMMUNICATE WITH CODEREEF PORTAL #############################################################################
@cli.command()

@click.option('-h', '--host', 'host', required=False)
@click.option('-p', '--port', 'port', required=False)
@click.option('-t', '--tunnel', 'tunnel', required=False)


def start(host,
          port,
          tunnel):
    '''
    Start CodeReef server.
    ''' 

    from . import client
    return client.start({'host':host,
                         'port':port,
                         'tunnel':tunnel})

# START SERVICE TO COMMUNICATE WITH CODEREEF PORTAL #############################################################################
@cli.command()

def version():
    '''
    Show CodeReef client version.
    '''

    from . import __version__

    print (__version__)

    return 0

##############################################################################
if __name__ == "__main__":
   cli()
