#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Copyright (c) 2023 Haofan Zheng
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
###


import random

from typing import Union


class Test(object):

	def __init__(
		self,
		testId: Union[str, None] = None,
	) -> None:
		super(Test, self).__init__()

		self.testId = testId if testId is not None else (random.randbytes(16).hex())[:8]

	def Run(self) -> None:
		raise NotImplementedError("Test.Run() is not implemented.")

	def GetResult(self) -> dict:
		raise NotImplementedError("Test.GetResult() is not implemented.")

