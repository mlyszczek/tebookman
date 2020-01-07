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


import	argparse
import	config
import	db
import	os
import	sys
import	util
import	version

from	pprint    import pprint


## ==========================================================================
#          __             __                     __   _
#     ____/ /___   _____ / /____ _ _____ ____ _ / /_ (_)____   ____   _____
#    / __  // _ \ / ___// // __ `// ___// __ `// __// // __ \ / __ \ / ___/
#   / /_/ //  __// /__ / // /_/ // /   / /_/ // /_ / // /_/ // / / /(__  )
#   \__,_/ \___/ \___//_/ \__,_//_/    \__,_/ \__//_/ \____//_/ /_//____/
#
## ==========================================================================


def_config = "~/.tebookman"

ebook_formats = [ "cbr", "cbz", "cb7", "cbt", "cba", "djvu", "doc", "docx",
		"epub", "fb2", "html", "ibook", "inf", "azw", "lit", "prc", "mobi",
		"pkg", "pdb", "txt", "pdb", "pdf", "ps", "tr2", "tr3", "oxps", "xps" ]


## ==========================================================================
#               ____                     __   _
#              / __/__  __ ____   _____ / /_ (_)____   ____   _____
#             / /_ / / / // __ \ / ___// __// // __ \ / __ \ / ___/
#            / __// /_/ // / / // /__ / /_ / // /_/ // / / /(__  )
#           /_/   \__,_//_/ /_/ \___/ \__//_/ \____//_/ /_//____/
#
## ==========================================================================


def do_add(
	args
):
	book = db.book()

	# gather info about book we shall add
	book.author = args.author if args.author else \
			util.readline_input("> Author of the book: ", db.authors())
	book.series = args.series if args.series else \
			util.readline_input("> Book series: ", db.series(book.author))
	book.title = args.title if args.title else \
			util.readline_input("> Book title: ",
					db.titles(book.author, book.series))
	book.chapter = args.chapter if args.chapter else input("> Chapter/Tome: ")
	default_format = util.detect_format(args.book)
	book.formats.append(args.format if args.format else \
			util.readline_input("> Book format[{}]: ".format(default_format),
					ebook_formats))
	if not book.formats[0]:
		book.formats[0] = default_format

	book_file = os.path.abspath(args.book)

	# print info about what we are about to add, for confirmation
	print("")
	print("\tAuthor: {}{}".format(book.author,
			"" if db.author_exist(book) else " (new)"))
	if book.series:
		print("\tSeries: {}{}".format(book.series,
			"" if db.series_exist(book) else " (new)"))
	else:
		print("\tSeries: (none)")
	print("\tTitle: {}{}".format(book.title,
			"" if db.title_exist(book) else " (new)"))
	print("\tChapter: {}".format(book.chapter if book.chapter else "(none)"))
	print("\tFormat: {}{}".format(book.formats[0],
			"" if db.book_exist(book) else " (new)"))
	print("")

	# getting consent
	if db.book_exist(book):
		answer = input("Book already exists. Overwrite? [N/y]: ")
		answer = answer.lower() if answer else "n"
	else:
		answer = input("Add that book? [n/Y]: ")
		answer = answer.lower() if answer else "y"

	if answer == "n":
		sys.exit(0)

	return db.add_book(book, book_file)


## ==========================================================================
#                                 __                __
#                          _____ / /_ ____ _ _____ / /_
#                         / ___// __// __ `// ___// __/
#                        (__  )/ /_ / /_/ // /   / /_
#                       /____/ \__/ \__,_//_/    \__/
#
## ==========================================================================


vstr = "tebookman v" + version.tebookman_version
parser = argparse.ArgumentParser(description="manager for ebook collection")
parser.add_argument("-v", "--version", action='version', version=vstr)
parser.add_argument("-C", "--config", required=0, metavar="path",
		default=def_config, help="path to config file, default: ~/.tebookman")
subparsers = parser.add_subparsers(dest="command")
add_parser = subparsers.add_parser("add", help="add book to database")
add_parser.add_argument("book", metavar="path", help="file to add to database")
add_parser.add_argument("-a", "--author", required=0, metavar="name",
		help="author of the book")
add_parser.add_argument("-t", "--title", required=0, metavar="name",
		help="title of the book")
add_parser.add_argument("-s", "--series", required=0, metavar="name",
		help="series to which book belongs to")
add_parser.add_argument("-c", "--chapter", required=0, metavar="num",
		help="book series chapter/tome")
add_parser.add_argument("-f", "--format", required=0, metavar="extension",
		help="book format (extension)")

del_parser = subparsers.add_parser("del")

args = parser.parse_args()
config.init(args.config)
db.init()

if args.command == "add":
	do_add(args)
