#!/usr/bin/env python3
## ==========================================================================
#   Licensed under BSD 2clause license See LICENSE file for more information
#   Author: Michał Łyszczek <michal.lyszczek@bofc.pl>
## ==========================================================================
#                   _                                 __
#                  (_)____ ___   ____   ____   _____ / /_ _____
#                 / // __ `__ \ / __ \ / __ \ / ___// __// ___/
#                / // / / / / // /_/ // /_/ // /   / /_ (__  )
#               /_//_/ /_/ /_// .___/ \____//_/    \__//____/
#                            /_/
## ==========================================================================


import	errno
import	os
import	readline


## ==========================================================================
#               ____                     __   _
#              / __/__  __ ____   _____ / /_ (_)____   ____   _____
#             / /_ / / / // __ \ / ___// __// // __ \ / __ \ / ___/
#            / __// /_/ // / / // /__ / /_ / // /_/ // / / /(__  )
#           /_/   \__,_//_/ /_/ \___/ \__//_/ \____//_/ /_//____/
#
## ==========================================================================


## ==========================================================================
#   Prints message to standard error
## ==========================================================================


def eprint(
	*args,
	**kwargs
):
	print(*args, file=sys.stderr, **kwargs)


## ==========================================================================
#   Creates new directory, but does not return error when directory already
#   exists.
## ==========================================================================


def mkdir(
	path  # path where to create new directory
):
	# create outdir, but don't crash if it already exists
	try:
		os.mkdir(path)
	except OSError as e:
		if e.errno != errno.EEXIST:
			raise
		pass


## ==========================================================================
#
## ==========================================================================


def readline_input(
	prompt,
	lst
):
	def completer(
		text,
		state
	):
		line = readline.get_line_buffer()
		if not line:
			return [c + " " for c in lst][state]
		else:
			return [c + " " for c in lst if c.startswith(line)][state]
	
	readline.set_completer_delims('\t')
	readline.parse_and_bind("tab: complete")
	readline.set_completer(completer)
	return input(prompt).rstrip()


## ==========================================================================
#
## ==========================================================================


def detect_format(
	file
):
	root, ext = os.path.splitext(file)
	return ext[1:]
