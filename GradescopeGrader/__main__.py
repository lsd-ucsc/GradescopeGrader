#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Copyright (c) 2023 Haofan Zheng
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
###


import argparse
import logging


def main():
	argParser = argparse.ArgumentParser(
		description='Gradescope Grader',
	)
	argParser.add_argument(
		'--verbose', '-v',
		action='store_true',
		help='verbose mode',
	)

	opParser = argParser.add_subparsers(
		dest='operation',
		help='operation to perform',
		required=True,
	)
	opParser.add_parser(
		'version',
		help='print version and exit',
	)

	args = argParser.parse_args()

	logLvl = logging.DEBUG if args.verbose else logging.INFO
	logging.basicConfig(
		level=logLvl,
		format='%(asctime)s %(name)s[%(levelname)s]: %(message)s',
	)

	if args.operation == 'version':
		from ._Meta import __version__
		print(__version__)
	else:
		raise NotImplementedError('unknown operation {}'.format(args.operation))


if __name__ == '__main__':
	main()
