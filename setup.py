#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Copyright (c) 2023 Haofan Zheng
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
###


from setuptools import setup
from setuptools import find_packages

import GradescopeGrader._Meta


setup(
	name        = GradescopeGrader._Meta.PKG_NAME,
	version     = GradescopeGrader._Meta.__version__,
	packages    = find_packages(where='.', exclude=['tests*']),
	url         = 'https://github.com/lsd-ucsc/GradescopeGrader',
	license     = GradescopeGrader._Meta.PKG_LICENSE,
	author      = GradescopeGrader._Meta.PKG_AUTHOR,
	description = GradescopeGrader._Meta.PKG_DESCRIPTION,
	entry_points= {
		'console_scripts': [
			'GradescopeGrader=GradescopeGrader.__main__:main',
		]
	},
	install_requires=[
	],
)
