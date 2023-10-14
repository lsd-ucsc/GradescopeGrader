#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Copyright (c) 2023 Haofan Zheng
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
###


import json
import os

from typing import List, Union

from . import Test


class Grader(object):

	def __init__(self) -> None:
		super(Grader, self).__init__()

		self.tests: List[Test.Test] = []

	def AddTest(self, test: Test.Test) -> None:
		self.tests.append(test)

	def RunTests(self) -> None:
		for test in self.tests:
			test.Run()

	def GetResults(self) -> dict:
		resultFromTests = []
		for test in self.tests:
			resultFromTests.append(test.GetResult())

		return {
			'tests': resultFromTests
		}

	def GenResultsJson(self) -> str:
		return json.dumps(self.GetResults(), indent='\t', sort_keys=True)

	def WriteResultsJson(
		self,
		path: Union[str, os.PathLike] = '/autograder/results/results.json',
	) -> None:
		with open(path, 'w') as f:
			f.write(self.GenResultsJson())
