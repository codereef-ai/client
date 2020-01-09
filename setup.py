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

############################################################
from setuptools import find_packages, setup, convert_path

# Version
version = imp.load_source(
    'codereef.__init__', os.path.join('codereef', '__init__.py')).__version__

# Read description (TBD: should add short description!)
with open(convert_path('./README.md')) as f:
    long_readme = f.read()

# Package description
setup(
    name='codereef',
    author="CodeReef",

    version=version,

    description="CodeReef client to deal with portable workflows",

    license="Apache Software License (Apache 2.0)",

    long_description=long_readme,
    long_description_content_type="text/markdown",

    url="https://codereef.ai/portal",

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
