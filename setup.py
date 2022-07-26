#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# This file is part of Tatyana.
#
# Copyright (C) 2022  Dialogue Movement contributors.  See AUTHORS.
#
# Tatyana is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Tatyana is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

# Install packages as defined in this file into the Python environment
from setuptools import setup, find_packages

# Get version number from source tree
import sys
sys.path.append( '.' )
from tatyana import VERSION

modname = distname = 'tatyana'

setup(
    name=distname,
    version=VERSION,
    description='Bot for interaction with the local government bodies',
    author='Mikhail Podivilov',
    author_email='mikhail@podivilov.com',
    packages=[ 'tatyana', 'tatyana.examples' ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: Russian",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ],
    license='GPLv3+',
    install_requires=[
        "setuptools>=61.0",
        "gspread==5.4.0",
        "pyTelegramBotAPI==4.6.0",
        "python-dotenv==0.20.0",
    ],
    scripts=scripts,
)
