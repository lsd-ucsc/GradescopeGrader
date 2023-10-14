#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Copyright (c) 2023 Haofan Zheng
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
###



import sys
import unittest

from GradescopeGrader import Cmd


class TestCmd(unittest.TestCase):

	def test_constructor(self):
		cmd = [ sys.executable, '-c', 'import os\nprint(os.getcwd())' ]
		inst = Cmd.Cmd(
			workDir='/tmp',
			cmd=cmd,
			env={},
		)
		self.assertEqual(inst.workDir, '/tmp')
		self.assertEqual(inst.cmd, cmd)
		self.assertEqual(inst.env, {})
		self.assertEqual(
			str(inst),
			' '.join(cmd),
		)

	def test_ok_run(self):
		cmd = [
			sys.executable,
			'-c',
			'import os\nimport sys\nprint(os.getcwd())\nsys.stderr.write("test stderr")'
		]
		inst = Cmd.Cmd(
			workDir='/tmp',
			cmd=cmd,
			env={},
		)
		inst.Run()
		self.assertEqual(inst.stdout, b'/tmp\n')
		self.assertEqual(inst.stderr, b'test stderr')
		self.assertEqual(inst.returncode, 0)
		self.assertGreater(inst.runtimeNS, 0)

	def test_fail_run(self):
		cmd = [ sys.executable, '-c', 'exit(12)' ]
		inst = Cmd.Cmd(
			workDir='/tmp',
			cmd=cmd,
			env={},
		)
		inst.Run()
		self.assertEqual(inst.stdout, b'')
		self.assertEqual(inst.stderr, b'')
		self.assertEqual(inst.returncode, 12)
		self.assertGreater(inst.runtimeNS, 0)
