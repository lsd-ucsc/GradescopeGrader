#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Copyright (c) 2023 Haofan Zheng
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
###


import itertools
import random
import sys
import unittest

from typing import List

from GradescopeGrader import Cmd
from GradescopeGrader import Grader
from GradescopeGrader.CmdAllOrNothingTest import CmdAllOrNothingTest


class TestCmdAllOrNothingTest(unittest.TestCase):

	def test_constructor(self):
		inst = CmdAllOrNothingTest(
			cmd=Cmd.Cmd(cmd=['echo' , '1']),
			maxScore=123,
			testId='test_inst',
			preCmd=Cmd.Cmd(cmd=['echo' , '2']),
			postCmd=Cmd.Cmd(cmd=['echo' , '3']),
		)
		self.assertEqual(inst.cmd.cmd, ['echo' , '1'])
		self.assertEqual(inst.maxScore, 123)
		self.assertEqual(inst.testId, 'test_inst')
		self.assertEqual(inst.preCmd.cmd, ['echo' , '2'])
		self.assertEqual(inst.postCmd.cmd, ['echo' , '3'])

	def test_all_ok_run(self):
		inst = CmdAllOrNothingTest(
			cmd=Cmd.Cmd(
				cmd=[
					sys.executable,
					'-c',
					'import sys; sys.stdout.write("|CMD_STDOUT|"); sys.stderr.write("|CMD_STDERR|")',
				]
			),
			maxScore=12345,
			testId='test_inst',
			preCmd=Cmd.Cmd(
				cmd=[
					sys.executable,
					'-c',
					'import sys; sys.stdout.write("|PRECMD_STDOUT|"); sys.stderr.write("|PRECMD_STDERR|")',
				]
			),
			postCmd=Cmd.Cmd(
				cmd=[
					sys.executable,
					'-c',
					'import sys; sys.stdout.write("|POSTCMD_STDOUT|"); sys.stderr.write("|POSTCMD_STDERR|")',
				]
			),
		)

		inst.Run()

		self.assertEqual(inst.returncode, 0)
		self.assertEqual(inst.stdout, b'|CMD_STDOUT|')
		self.assertEqual(inst.stderr, b'|CMD_STDERR|')
		self.assertGreaterEqual(inst.GetRunTimeNS(), 0)
		self.assertEqual(inst.score, 12345)
		self.assertEqual(inst.status, 'passed')

		res = inst.GetResult()
		self.assertEqual(res['score'], 12345)
		self.assertEqual(res['max_score'], 12345)
		self.assertEqual(res['status'], 'passed')
		self.assertEqual(res['name'], 'test_inst')
		self.assertEqual(res['name_format'], 'text')
		self.assertEqual(res['output_format'], 'md')
		self.assertNotEqual(res['output'].find('|CMD_STDOUT|'), -1)
		self.assertNotEqual(res['output'].find('|CMD_STDERR|'), -1)
		self.assertNotEqual(res['output'].find('Return Code: 0'), -1)

	def test_single_cmd_ok_run(self):
		inst = CmdAllOrNothingTest(
			cmd=Cmd.Cmd(
				cmd=[
					sys.executable,
					'-c',
					'import sys; sys.stdout.write("|CMD_STDOUT|"); sys.stderr.write("|CMD_STDERR|")',
				]
			),
			maxScore=12345,
			testId='test_inst',
		)

		inst.Run()

		self.assertEqual(inst.returncode, 0)
		self.assertEqual(inst.stdout, b'|CMD_STDOUT|')
		self.assertEqual(inst.stderr, b'|CMD_STDERR|')
		self.assertGreaterEqual(inst.GetRunTimeNS(), 0)
		self.assertEqual(inst.score, 12345)
		self.assertEqual(inst.status, 'passed')

		res = inst.GetResult()
		self.assertEqual(res['score'], 12345)
		self.assertEqual(res['max_score'], 12345)
		self.assertEqual(res['status'], 'passed')
		self.assertEqual(res['name'], 'test_inst')
		self.assertEqual(res['name_format'], 'text')
		self.assertEqual(res['output_format'], 'md')
		self.assertNotEqual(res['output'].find('|CMD_STDOUT|'), -1)
		self.assertNotEqual(res['output'].find('|CMD_STDERR|'), -1)
		self.assertNotEqual(res['output'].find('Return Code: 0'), -1)

	def test_precmd_fail_run(self):
		inst = CmdAllOrNothingTest(
			cmd=Cmd.Cmd(
				cmd=[
					sys.executable,
					'-c',
					'import sys; sys.stdout.write("|CMD_STDOUT|"); sys.stderr.write("|CMD_STDERR|")',
				]
			),
			maxScore=12345,
			testId='test_inst',
			preCmd=Cmd.Cmd(
				cmd=[
					sys.executable,
					'-c',
					'import sys; sys.stdout.write("|PRECMD_STDOUT|"); sys.stderr.write("|PRECMD_STDERR|"); sys.exit(23)',
				]
			),
			postCmd=Cmd.Cmd(
				cmd=[
					sys.executable,
					'-c',
					'import sys; sys.stdout.write("|POSTCMD_STDOUT|"); sys.stderr.write("|POSTCMD_STDERR|")',
				]
			),
		)

		inst.Run()

		self.assertEqual(inst.returncode, 23)
		self.assertEqual(inst.stdout, b'|PRECMD_STDOUT|')
		self.assertEqual(inst.stderr, b'|PRECMD_STDERR|')
		self.assertGreaterEqual(inst.GetRunTimeNS(), 0)
		self.assertEqual(inst.score, 0)
		self.assertEqual(inst.status, 'failed')

		res = inst.GetResult()
		self.assertEqual(res['score'], 0)
		self.assertEqual(res['max_score'], 12345)
		self.assertEqual(res['status'], 'failed')
		self.assertEqual(res['name'], 'test_inst')
		self.assertEqual(res['name_format'], 'text')
		self.assertEqual(res['output_format'], 'md')
		self.assertNotEqual(res['output'].find('|PRECMD_STDOUT|'), -1)
		self.assertNotEqual(res['output'].find('|PRECMD_STDERR|'), -1)
		self.assertNotEqual(res['output'].find('Return Code: 23'), -1)

	def test_cmd_fail_run(self):
		inst = CmdAllOrNothingTest(
			cmd=Cmd.Cmd(
				cmd=[
					sys.executable,
					'-c',
					'import sys; sys.stdout.write("|CMD_STDOUT|"); sys.stderr.write("|CMD_STDERR|"); sys.exit(34)',
				]
			),
			maxScore=12345,
			testId='test_inst',
			preCmd=Cmd.Cmd(
				cmd=[
					sys.executable,
					'-c',
					'import sys; sys.stdout.write("|PRECMD_STDOUT|"); sys.stderr.write("|PRECMD_STDERR|")',
				]
			),
			postCmd=Cmd.Cmd(
				cmd=[
					sys.executable,
					'-c',
					'import sys; sys.stdout.write("|POSTCMD_STDOUT|"); sys.stderr.write("|POSTCMD_STDERR|")',
				]
			),
		)

		inst.Run()

		self.assertEqual(inst.returncode, 34)
		self.assertEqual(inst.stdout, b'|CMD_STDOUT|')
		self.assertEqual(inst.stderr, b'|CMD_STDERR|')
		self.assertGreaterEqual(inst.GetRunTimeNS(), 0)
		self.assertEqual(inst.score, 0)
		self.assertEqual(inst.status, 'failed')

		res = inst.GetResult()
		self.assertEqual(res['score'], 0)
		self.assertEqual(res['max_score'], 12345)
		self.assertEqual(res['status'], 'failed')
		self.assertEqual(res['name'], 'test_inst')
		self.assertEqual(res['name_format'], 'text')
		self.assertEqual(res['output_format'], 'md')
		self.assertNotEqual(res['output'].find('|CMD_STDOUT|'), -1)
		self.assertNotEqual(res['output'].find('|CMD_STDERR|'), -1)
		self.assertNotEqual(res['output'].find('Return Code: 34'), -1)

	def test_postcmd_fail_run(self):
		inst = CmdAllOrNothingTest(
			cmd=Cmd.Cmd(
				cmd=[
					sys.executable,
					'-c',
					'import sys; sys.stdout.write("|CMD_STDOUT|"); sys.stderr.write("|CMD_STDERR|")',
				]
			),
			maxScore=12345,
			testId='test_inst',
			preCmd=Cmd.Cmd(
				cmd=[
					sys.executable,
					'-c',
					'import sys; sys.stdout.write("|PRECMD_STDOUT|"); sys.stderr.write("|PRECMD_STDERR|")',
				]
			),
			postCmd=Cmd.Cmd(
				cmd=[
					sys.executable,
					'-c',
					'import sys; sys.stdout.write("|POSTCMD_STDOUT|"); sys.stderr.write("|POSTCMD_STDERR|"); sys.exit(45)',
				]
			),
		)

		inst.Run()

		self.assertEqual(inst.returncode, 0)
		self.assertEqual(inst.stdout, b'|CMD_STDOUT|')
		self.assertEqual(inst.stderr, b'|CMD_STDERR|')
		self.assertGreaterEqual(inst.GetRunTimeNS(), 0)
		self.assertEqual(inst.score, 12345)
		self.assertEqual(inst.status, 'passed')

		res = inst.GetResult()
		self.assertEqual(res['score'], 12345)
		self.assertEqual(res['max_score'], 12345)
		self.assertEqual(res['status'], 'passed')
		self.assertEqual(res['name'], 'test_inst')
		self.assertEqual(res['name_format'], 'text')
		self.assertEqual(res['output_format'], 'md')
		self.assertNotEqual(res['output'].find('|CMD_STDOUT|'), -1)
		self.assertNotEqual(res['output'].find('|CMD_STDERR|'), -1)
		self.assertNotEqual(res['output'].find('Return Code: 0'), -1)


class TestGrader(unittest.TestCase):

	def test_constructor(self):
		inst = Grader.Grader()
		self.assertEqual(inst.tests, [])

	def _run_some_tests(
		self,
		isFailedList: List[bool],
	) -> None:
		okCmd = Cmd.Cmd(cmd=[sys.executable, '-c', 'exit(0)'])
		failCmd = Cmd.Cmd(cmd=[sys.executable, '-c', 'exit(1)'])

		scoreList = [ random.randint(1, 1000) for _ in range(len(isFailedList))]

		inst = Grader.Grader()

		for isFailed, maxScore, i in zip(isFailedList, scoreList, range(len(isFailedList))):
			inst.AddTest(
				CmdAllOrNothingTest(
					testId='test_{}'.format(i),
					cmd=failCmd if isFailed else okCmd,
					maxScore=maxScore,
				)
			)

		inst.RunTests()

		res = inst.GetResults()

		self.assertTrue('tests' in res)
		self.assertEqual(len(res['tests']), len(isFailedList))

		for isFailed, maxScore, testRes, i in zip(
			isFailedList,
			scoreList,
			res['tests'],
			range(len(isFailedList))
		):
			self.assertEqual(testRes['max_score'], maxScore)
			self.assertEqual(testRes['score'], 0 if isFailed else maxScore)
			self.assertEqual(testRes['status'], 'failed' if isFailed else 'passed')
			self.assertEqual(testRes['name'], 'test_{}'.format(i))
			self.assertEqual(testRes['name_format'], 'text')
			self.assertEqual(testRes['output_format'], 'md')
			# print(testRes)

	def test_2_tests(self):
		self._run_some_tests(isFailedList=[False, False])
		self._run_some_tests(isFailedList=[False, True])
		self._run_some_tests(isFailedList=[True, False])
		self._run_some_tests(isFailedList=[True, True])

	def test_10_tests(self):
		for failList in itertools.product([False,True], repeat=5):
			self._run_some_tests(isFailedList=failList)
