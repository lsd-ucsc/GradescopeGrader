#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Copyright (c) 2023 Haofan Zheng
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
###


import logging

from typing import Tuple, Union

from . import Test
from . import Cmd


class CmdAllOrNothingTest(Test.Test):

	def __init__(
		self,
		cmd: Cmd.Cmd,
		maxScore: int,
		testId:  Union[str,     None] = None,
		preCmd:  Union[Cmd.Cmd, None] = None,
		postCmd: Union[Cmd.Cmd, None] = None,
	) -> None:
		super(CmdAllOrNothingTest, self).__init__(
			testId=testId,
		)

		self.cmd = cmd
		self.maxScore = maxScore
		self.preCmd = preCmd
		self.postCmd = postCmd

		self.score = 0
		self.status = 'failed'

		self.returncode = None
		self.stdout = None
		self.stderr = None
		self.runtimeNS = None

		self.logger = logging.getLogger(
			__name__ + '.' + self.__class__.__name__ + f'[{self.testId}]'
		)

	def Run(self) -> None:
		if self.preCmd is not None:
			self.logger.info('Running pre-command {}'.format(self.preCmd))
			self.preCmd.Run()
			if self.preCmd.returncode != 0:
				self.returncode = self.preCmd.returncode
				self.stdout     = self.preCmd.stdout
				self.stderr     = self.preCmd.stderr
				self.runtimeNS  = self.preCmd.runtimeNS
				return

		self.logger.info('Running command {}'.format(self.cmd))
		self.cmd.Run()
		self.returncode = self.cmd.returncode
		self.stdout     = self.cmd.stdout
		self.stderr     = self.cmd.stderr
		self.runtimeNS  = self.cmd.runtimeNS

		if self.cmd.returncode == 0:
			self.score = self.maxScore
			self.status = 'passed'

		if self.postCmd is not None:
			self.logger.info('Running post-command {}'.format(self.postCmd))
			self.postCmd.Run()

	def _GenOutput(self) -> Tuple[str, str]:
		output = ''
		output += 'Execution Time: {:.2f} ms\n'.format(self.runtimeNS / 1000000)
		output += 'Return Code: {}\n'.format(self.returncode)
		output += '\n'

		if len(self.stdout) > 0:
			output += 'stdout:\n'
			output += '```\n'
			output += self.stdout.decode('utf-8', errors='replace')
			output += '```\n'
			output += '\n'

		if len(self.stderr) > 0:
			output += 'stderr:\n'
			output += '```\n'
			output += self.stderr.decode('utf-8', errors='replace')
			output += '```\n'

		return 'md', output

	def GetRunTimeNS(self) -> int:
		return self.runtimeNS

	def GetRunTime(self) -> float:
		return self.GetRunTimeNS() / 1000000

	def GetResult(self) -> dict:
		'''
		the output format specs can be found at:
		https://gradescope-autograders.readthedocs.io/en/latest/specs/
		'''
		outputFormat, output = self._GenOutput()
		return {
			'score': self.score,
			'max_score': self.maxScore,
			'status': self.status,
			'name': self.testId,
			'name_format': 'text',
			'output': output,
			'output_format': outputFormat,
		}
