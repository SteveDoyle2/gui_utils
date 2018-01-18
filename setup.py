#!/usr/bin/env python
import os
import sys
from setuptools import setup, find_packages

PY2 = False
if sys.version_info < (3, 0):
    PY2 = True
if sys.version_info < (2, 7, 7):
    imajor, minor1, minor2 = sys.version_info[:3]
    # makes sure we don't get the following bug:
    #   Issue #19099: The struct module now supports Unicode format strings.
    sys.exit('Upgrade your Python to >= 2.7.7; version=(%s.%s.%s)' % (imajor, minor1, minor2))

import gui_utils
packages = find_packages()+['gui/icons/*.*']

# set up all icons
icon_files2 = []
if 0:
    icon_path = os.path.join('gui_utils', 'gui', 'icons')
    icon_files = os.listdir(icon_path)
    for icon_file in icon_files:
        if icon_file.endswith('.png'):
            icon_files2.append(os.path.join(icon_path, icon_file))

exclude_words = []
packages = find_packages(exclude=['ez_setup', 'examples', 'tests'] + exclude_words)
for exclude_word in exclude_words:
    packages = [package for package in packages if exclude_word not in package]
#print(packages, len(packages)) # 83

setup(
    name='gui_utils',
    version=gui_utils.__version__,
    description=gui_utils.__desc__,
    long_description="""\
""",
    classifiers=[
        'Natural Language :: English',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License (BSD-3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author=gui_utils.__author__,
    author_email=gui_utils.__email__,
    url=gui_utils.__website__,
    license=gui_utils.__license__,
    packages=packages,
    include_package_data=True,
    zip_safe=False,
    #{'': ['license.txt']}
    #package_data={'': ['*.png']},
    #data_files=[(icon_path, icon_files2)],
    package_data={
        # https://pythonhosted.org/setuptools/setuptools.html#including-data-files
        # If any package contains *.png files, include them:
        '': ['*.png'],
        #'mypkg': ['data/*.dat'],
    },
    entry_points={
        'console_scripts': [
            'mygui = gui_utils.gui.gui:cmd_line',
        ]
    },
    test_suite='pyNastran.all_tests',
)

