#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# $Id: setup.py,v 0.2.3.4 2013-02-27 09:56:56 gaelL Exp $
#
# Copyright (C) 2010-2013  Gaël Lambert (gaelL) <gael@gael-lambert.org>
#
# Numeter is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from distutils.core import setup


if __name__ == '__main__':

    setup(name='numeter-backuppc-module',
          version='0.0.0.0',
          description='Numeter Backuppc Poller module',
          long_description="""A Backuppc module for Numeter poller. This module\
          make backup statistics with the backuppc server log.
	  Documentation is available here: https://github.com/talset/numeter-backuppc-module""",
          author='Florian Lambert (talset)',
          author_email='florian.lambert@enovance.com',
          maintainer='Florian Lambert (talset)',
          maintainer_email='florian.lambert@enovance.com',
          keywords=['numeter','graphing','poller','backuppc'],
	  url='https://github.com/talset/numeter-backuppc-module',
          license='GNU Affero General Public License v3',
          packages = [''],
          package_data={'': ['backuppcModule.py']},
          classifiers=[
              'Development Status :: 4 - Beta',
              'Environment :: Console',
              'Intended Audience :: Advanced End Users',
              'Intended Audience :: System Administrators',
              'License :: OSI Approved :: GNU Affero General Public License v3',
              'Operating System :: POSIX',
              'Programming Language :: Python',
              'Topic :: System :: Monitoring'
          ],
         )
