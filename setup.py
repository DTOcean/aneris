# -*- coding: utf-8 -*-

import os
import sys
from distutils.cmd import Command

import yaml
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

# Test for correct python
python = sys.version_info

if python.major == 3:
    print "Sorry, Python 3 is not supported (yet)"
    sys.exit(1)
elif python.minor < 7 or (python.minor == 7 and python.micro < 3):
    print "Python version must be at least 2.7.3"
    sys.exit(1)


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


class CleanPyc(Command):

    description = 'clean *.pyc'
    user_options = []
    exclude_list = ['.egg', '.git', '.idea', '__pycache__']
     
    def initialize_options(self):
        pass
     
    def finalize_options(self):
        pass
     
    def run(self):
        print "start cleanup pyc files."
        for pyc_path in self.pickup_pyc():
            print "remove pyc: {0}".format(pyc_path)
            os.remove(pyc_path)
        print "the end."
     
    def is_exclude(self, path):
        for item in CleanPyc.exclude_list:
            if path.find(item) != -1:
                return True
        return False
     
    def is_pyc(self, path):
        return path.endswith('.pyc')
     
    def pickup_pyc(self):
        for root, dirs, files in os.walk(os.getcwd()):
            for fname in files:
                if self.is_exclude(root):
                    continue
                if not self.is_pyc(fname):
                    continue
                yield os.path.join(root, fname)


def read_yaml(rel_path):
    with open(rel_path, 'r') as stream:
        data_loaded = yaml.safe_load(stream)
    return data_loaded


def get_appveyor_version():
    
    data = read_yaml("appveyor.yml")
    
    if "version" not in data:
        raise RuntimeError("Unable to find version string.")
    
    appveyor_version = data["version"]
    last_dot_idx = appveyor_version.rindex(".")
    
    return appveyor_version[:last_dot_idx]


setup(name='aneris',
      version=get_appveyor_version(),
      description='aneris.py: data management, coupling and execution',
      author='Mathew Toppper',
      author_email='mathew.topper@dataonlygreater.com',
      license = "MIT",
      packages=find_packages(),
      setup_requires=['pyyaml'],
      install_requires=['attrdict',
                        'numpy',
                        'openpyxl<3',
                        'pandas>=0.20',
                        'polite>=0.9',
                        'pywin32',
                        'pyyaml',
                        'sqlalchemy',
                        'xlrd<2',
                        'xlwt'
                        ],
      entry_points={
          'console_scripts':
              [
               'bootstrap-dds = aneris.utilities.files:bootstrap_dds_interface',
               'xl-merge = aneris.utilities.files:xl_merge_interface',
               ]},
      tests_require=['pytest',
                     ],
      cmdclass = {'test': PyTest,
                  'cleanpyc': CleanPyc,
                  },
      )
