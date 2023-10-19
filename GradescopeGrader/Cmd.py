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
import threading
import time

from typing import Union


class Cmd(object):

	def __init__(
		self,
		cmd: Union[str, list],
		workDir: str = os.getcwd(),
		env: dict = os.environ,
		timeout: Union[None, float] = None,
	) -> None:
		super(Cmd, self).__init__()

		self.workDir = workDir
		self.cmd = cmd
		self.env = env
		self.timeout = timeout

		self.proc = None
		self.stdout = None
		self.stderr = None
		self.returncode = None # None value by default
		self.runtimeNS = None
		self.hasTimedOut = False
		self.timer = None

	def Kill(self) -> None:
		if self.proc:
			self.proc.kill()
			self.hasTimedOut = True

	def StartKillTimer(self) -> None:
		if self.timer is not None:
			self.CancelKillTimer()

		if self.timeout is not None:
			self.hasTimedOut = False # reset
			self.timer = threading.Timer(
				interval=self.timeout,
				function=self.Kill
			)
			self.timer.start()

	def CancelKillTimer(self) -> None:
		if self.timer:
			self.timer.cancel()
			self.timer = None

	def Run(self) -> None:
		startTime = time.time_ns()

		try:
			with subprocess.Popen(
				self.cmd,
				cwd=self.workDir,
				env=self.env,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE,
			) as proc:
				self.proc = proc
				self.StartKillTimer()
				self.stdout, self.stderr = proc.communicate()
				# update return code based on the process return code
				# or -9 if the process is killed by timeout
				self.returncode = proc.returncode if not self.hasTimedOut else -9
		finally:
			self.CancelKillTimer()
			self.proc = None

		endTime = time.time_ns()
		self.runtimeNS = endTime - startTime

	def GetRunTimeNS(self) -> int:
		return self.runtimeNS

	def GetRunTimeMS(self) -> float:
		return self.GetRunTimeNS() / 1000 / 1000

	def GetRunTime(self) -> float:
		return self.GetRunTimeMS() / 1000

	def __str__(self) -> str:
		if isinstance(self.cmd, str):
			return self.cmd
		else:
			return ' '.join(self.cmd)

