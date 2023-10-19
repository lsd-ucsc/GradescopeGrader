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

	def test_timeout_run_sleep(self):
		cmd = [ sys.executable, '-c', 'import time; print("before sleep"); time.sleep(10); print("after sleep")' ]
		inst = Cmd.Cmd(
			workDir='/tmp',
			cmd=cmd,
			env={},
			timeout=1.0,
		)
		inst.Run()
		#self.assertEqual(inst.stdout, b'')
		self.assertEqual(inst.stderr, b'')
		self.assertEqual(inst.returncode, -9)
		self.assertGreater(inst.GetRunTime(), 0.500) # 0.5s
		self.assertLess(inst.GetRunTime(), 2.0) # 2s
		self.assertGreater(inst.GetRunTimeMS(), 500.0) # 500ms
		self.assertLess(inst.GetRunTimeMS(), 2000.0) # 2000ms
		self.assertEqual(inst.hasTimedOut, True)

	def test_timeout_run_loop(self):
		cmd = [ sys.executable, '-c', 'i = 1\nwhile True:\n\ti += 1' ]
		inst = Cmd.Cmd(
			workDir='/tmp',
			cmd=cmd,
			env={},
			timeout=1.0,
		)
		inst.Run()
		self.assertEqual(inst.stdout, b'')
		self.assertEqual(inst.stderr, b'')
		self.assertEqual(inst.returncode, -9)
		self.assertGreater(inst.GetRunTime(), 0.500) # 0.5s
		self.assertLess(inst.GetRunTime(), 2.0) # 2s
		self.assertGreater(inst.GetRunTimeMS(), 500.0) # 500ms
		self.assertLess(inst.GetRunTimeMS(), 2000.0) # 2000ms
		self.assertEqual(inst.hasTimedOut, True)

	def test_runtime_500ms(self):
		inst = Cmd.Cmd(
			cmd=[sys.executable, '-c', 'import time; time.sleep(0.5); exit(123)']
		)
		inst.Run()
		self.assertGreaterEqual(inst.returncode, 123)
		self.assertGreater(inst.GetRunTimeNS(), 400000000)
		self.assertLess(   inst.GetRunTimeNS(), 600000000)
		self.assertGreater(inst.GetRunTimeMS(), 400.0)
		self.assertLess(   inst.GetRunTimeMS(), 600.0)
		self.assertGreater(inst.GetRunTime(),   0.4)
		self.assertLess(   inst.GetRunTime(),   0.6)

	def test_runtime_2s(self):
		inst = Cmd.Cmd(
			cmd=[sys.executable, '-c', 'import time; time.sleep(2.0); exit(132)']
		)
		inst.Run()
		self.assertGreaterEqual(inst.returncode, 132)
		self.assertGreater(inst.GetRunTimeNS(), 1500000000)
		self.assertLess(   inst.GetRunTimeNS(), 2500000000)
		self.assertGreater(inst.GetRunTimeMS(), 1500.0)
		self.assertLess(   inst.GetRunTimeMS(), 2500.0)
		self.assertGreater(inst.GetRunTime(),   1.5)
		self.assertLess(   inst.GetRunTime(),   2.5)
