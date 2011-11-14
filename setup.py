# -*- encoding: utf-8 -*-
from distutils.core import setup
import py2exe

setup(
    name='frostbite_server_info',
    version='1.0',
    description="query a frostbite game server for basic info",
    console=['frostbite_server_info.py'],
    zipfile=None,
    options={
        'py2exe': {
            'compressed': True,
            'bundle_files': 1,
        }
    }
)