#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Copyright (c) 2023 Haofan Zheng
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
###


from typing import List

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
