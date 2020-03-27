#
# Copyright 2019-2020 CodeReef
# See CodeReef client LICENSE.txt for licensing details
#
# Developer(s): Grigori Fursin, https://fursin.net
#               Herve Guillou, herve@codereef.ai
#

import os
import sys
import imp

import codereef.comm

############################################################
from setuptools import find_packages, setup, convert_path

try:
    from setuptools.command.install import install
except ImportError:
    from distutils.command.install import install

############################################################
# Version
version = imp.load_source(
    'codereef.__init__', os.path.join('codereef', '__init__.py')).__version__

# Default portal
portal_url='https://dev.codereef.ai/portal'

# Read description (TBD: should add short description!)
with open(convert_path('./README.md')) as f:
    long_readme = f.read()

############################################################
class custom_install(install):
    def run(self):
        # Run original installer
        install.run(self)

        # Get release notes 
        r=codereef.comm.send({'action':'get_client_release_notes', 
                              'config':{'server_url':portal_url+'/api/v1/?'},
                              'dict':{'version': version}})
        if r['return']==0:
           notes=r.get('notes','')
           if notes!='':
              print ('*********************************************************************')
              print ('Release notes:')
              print ('')
              print (notes)
              print ('*********************************************************************')

# Package description
setup(
    name='codereef',
    author="CodeReef",

    version=version,

    description="CodeReef client to deal with portable workflows",

    license="Apache Software License (Apache 2.0)",

    long_description=long_readme,
    long_description_content_type="text/markdown",

    cmdclass={'install': custom_install}, 

    url=portal_url,

    python_requires=">=2.7",

    packages=find_packages(exclude=["tests*", "docs*"]),
    package_data={"codereef":['static/*']},

    include_package_data=True,

    install_requires=[
      'click>=7.0',
      'ck',
      'requests',
      'virtualenv'
    ],

    entry_points={
      "console_scripts": 
        [
         "cr = codereef.main:cli",
         "codereef = codereef.main:cli"
        ]
    },

    zip_safe=False,

    keywords="portable workflows, reproducibility, collaborative experiments, portability, dependencies, workflows, automation, pipelines, data pipelines, computer systems, data science",

    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research"
       ],
)
