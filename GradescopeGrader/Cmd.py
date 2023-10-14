#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Copyright (c) 2023 Haofan Zheng
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
###


import os
import subprocess
import time

from typing import Union


class Cmd(object):

	def __init__(
		self,
		cmd: Union[str, list],
		workDir: str = os.getcwd(),
		env: dict = os.environ,
	) -> None:
		super(Cmd, self).__init__()

		self.workDir = workDir
		self.cmd = cmd
		self.env = env

		self.stdout = None
		self.stderr = None
		self.returncode = None
		self.runtimeNS = None

	def Run(self) -> None:
		startTime = time.time_ns()
		with subprocess.Popen(
			self.cmd,
			cwd=self.workDir,
			env=self.env,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
		) as proc:
			self.stdout, self.stderr = proc.communicate()
			self.returncode = proc.returncode
		endTime = time.time_ns()
		self.runtimeNS = endTime - startTime

	def __str__(self) -> str:
		if isinstance(self.cmd, str):
			return self.cmd
		else:
			return ' '.join(self.cmd)

