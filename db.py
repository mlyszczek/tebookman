## ==========================================================================
#   Licensed under BSD 2clause license See LICENSE file for more information
#   Author: Michał Łyszczek <michal.lyszczek@bofc.pl>
## ==========================================================================

## ==========================================================================
#                   _                                 __
#                  (_)____ ___   ____   ____   _____ / /_ _____
#                 / // __ `__ \ / __ \ / __ \ / ___// __// ___/
#                / // / / / / // /_/ // /_/ // /   / /_ (__  )
#               /_//_/ /_/ /_// .___/ \____//_/    \__//____/
#                            /_/
## ==========================================================================


import	config
import	csv
import	errno
import	operator
import	os
import	pprint
import	shutil
import	sys


## ==========================================================================
#          __             __                     __   _
#     ____/ /___   _____ / /____ _ _____ ____ _ / /_ (_)____   ____   _____
#    / __  // _ \ / ___// // __ `// ___// __ `// __// // __ \ / __ \ / ___/
#   / /_/ //  __// /__ / // /_/ // /   / /_/ // /_ / // /_/ // / / /(__  )
#   \__,_/ \___/ \___//_/ \__,_//_/    \__,_/ \__//_/ \____//_/ /_//____/
#
## ==========================================================================


class book:
	title = None
	author = None
	series = None
	chapter = None
	formats = []

db_header = "author,series,chapter,title,formats"
db = []


## ==========================================================================
#                       __     __ _          ____
#        ____   __  __ / /_   / /(_)_____   / __/__  __ ____   _____ _____
#       / __ \ / / / // __ \ / // // ___/  / /_ / / / // __ \ / ___// ___/
#      / /_/ // /_/ // /_/ // // // /__   / __// /_/ // / / // /__ (__  )
#     / .___/ \__,_//_.___//_//_/ \___/  /_/   \__,_//_/ /_/ \___//____/
#    /_/
## ==========================================================================


## ==========================================================================
#   Returns list of all authors in database.
## ==========================================================================


def authors():
	a = []
	prev_author = ""

	for book in db:
		if prev_author == book.author:
			# author already in the list, avoid duplication
			continue

		a.append(book.author)
		prev_author = book.author

	return a


## ==========================================================================
#   Returns 0 when specified author does not exist in database or 1 if he
#   does.
## ==========================================================================


def author_exist(
	book
):
	for b in db:
		if book.author == b.author:
			return 1

	return 0


## ==========================================================================
#   Returns all series by given author.
## ==========================================================================


def series(
	author
):
	s = []
	author_found = 0
	prev_series = ""

	for book in db:
		if book.author != author:
			if author_found == 0:
				# we still didn't found author, keep looking
				continue
			# if author has been found and we end up here, it means we
			# have parsed all entries by that author and can return from
			# function
			return s

		author_found = 1

		if prev_series == book.series:
			# series already in the list
			continue

		s.append(book.series)
		prev_series = book.series

	return s


## ==========================================================================
#   Returns 1 when series exists for given author or 0 if not. If series is
#   empty 1 is returned, since we assume empty series always exist
## ==========================================================================


def series_exist(
	book
):
	if not book.series:
		return 1

	for b in db:
		if book.author == b.author and book.series == b.series:
			return 1

	return 0


## ==========================================================================
#   Returns all titles by given author for given series. If series is empty,
#   all titles for given author will be returned (with or without series).
## ==========================================================================


def titles(
	author,
	series
):
	t = []
	author_found = 0
	series_found = 0
	prev_title = ""

	for book in db:
		if book.author != author:
			if author_found == 0:
				# we still didn't found author, keep looking
				continue
			# if author has been found and we end up here, it means we
			# have parsed all entries by that author and can return from
			# function
			return t

		if series:
			# if series has been specified, show only titles for that
			# given series, otherwise we will return all titles for the
			# author
			if book.series != series:
				if series_found == 0:
					continue
				return t

		author_found = 1
		series_found = 1

		if prev_title == book.title:
			# title already in the list
			continue

		t.append(book.title)
		prev_title = book.title

	return t


## ==========================================================================
#   Returns 1 when title for given author and series exist or 0 if not. If
#   series is empty, it will check only titles that have no series.
## ==========================================================================


def title_exist(
	book
):
	for b in db:
		if book.author == b.author and book.series == b.series \
				and book.chapter == b.chapter and book.title == b.title:
			return 1

	return 0


## ==========================================================================
#   Returns 1 if book exists or 0. Book exists when author-series-title and
#   specific format of the book exists.
## ==========================================================================


def book_exist(
	book
):
	for b in db:
		if book.author == b.author and book.series == b.series \
				and book.title == b.title and book.formats[0] in b.formats:
			return 1

	return 0


## ==========================================================================
#   Initializes database module by reading ebook-dir/.db file into easy to
#   access array.
## ==========================================================================


def init():
	dbpath = os.path.expanduser(config.config['db']['location'])

	if not os.path.isdir(dbpath):
		print("Cannot access database dir " + dbpath)
		sys.exit(1)

	try:
		fd = open(dbpath + "/.db")
		dbcsv = csv.DictReader(fd)
	except IOError as e0:
		if e0.errno == errno.ENOENT:
			# db does not exist, try to create new empty one
			try:
				fd = open(dbpath + "/.db", "w")
				fd.write(db_header + "\n")
				dbcsv = []
			except IOError as e1:
				print("Cannot create empty database in " + dbpath + "/.db")
				print(e1.strerror)
				sys.exit(1)
		else:
			print("Cannot open database file "  + dbpath + "/.db")
			print(e0.strerror)
			sys.exit(1)

	for row in dbcsv:
		b = book()
		b.title = row['title']
		b.author = row['author']
		b.series = row['series']
		b.chapter = row['chapter']
		b.formats = row['formats'].split(";")
		db.append(b)


def add_format(
	book,
	format
):
	i = 0
	for b in db:
		if book.author == b.author and book.series == b.series \
				and book.chapter == b.chapter and book.title == b.title:
			db[i].formats.append(format)
		i += 1


## ==========================================================================
#   Removes conditionals from specified path string. Conditionals are in
#   format {<field>|<string to print}. Field is a single character that
#   represents author, title, chapter etc. For example:
#
#       {a|some text}
#
#   for that, when author of the book is set, 'some text' will be returned,
#   otherwise nothing. Another - more - real life example.
#
#       %a/{s|%s/}{c|%c - }%t/%a - {s|%s - }{c|%c - }%t.%f
#
#   Assuming series is NOT set and chapter IS set we will have
#
#       %a/%c - %t/%a - %c - %t.%f
#
#   And if both series and chapter are not set, we will have
#
#       %a/%t/%a - %t.%f
## ==========================================================================


def remove_conditionals(
	book,
	path
):
	ret = ""
	i = 0
	cond_true = -1

	while i < len(path):
		if path[i] != "{":
			# not a conditional part of format
			ret += path[i]
			i += 1
			continue

		# in conditional part now, skip conditional opening '{'
		i += 1

		# check if field is set, if so - use what is inside conditional
		# as part of path, otherwise skip it
		field = path[i]
		i += 1
		if path[i] != "|":
			print("Syntax error, missing '|' in conditional")
			return ""
		i += 1

		if field == 'a':
			cond_true = book.author != ""
		elif field == 's':
			cond_true = book.series != ""
		elif field == "c":
			cond_true = book.chapter != ""
		elif field == 't':
			cond_true = book.title != ""
		elif field == 'f':
			cond_true = book.title != ""
		else:
			print("Unknown field specified in conditional: " + field)
			return ""

		while True:
			if path[i] == "}":
				i += 1
				break

			if cond_true:
				ret += path[i]
			i += 1

	return ret


## ==========================================================================
#   Replaces all specifiers with specific value. Specifier consists of one
#   percent (%) character and a single letter ie. `%a'.
#
#   for `path':
#     %a/%c - my text - %t
#
#   function will return (assuming it's sir Terry's book):
#     Terry Pratchett/1 - my text - Guards! Guards!
## ==========================================================================


def replace_specifiers(
	book,
	path
):
	ret = ""
	i = 0

	while i < len(path):
		if path[i] != "%":
			ret += path[i]
			i += 1
			continue

		# skip '%' specifier begin marker
		i += 1

		# replace specifier with a value from book
		field = path[i]
		i += 1

		if field == 'a':
			ret += book.author
		elif field == 's':
			ret  += book.series
		elif field == "c":
			ret  += book.chapter
		elif field == 't':
			ret  += book.title
		elif field == 'f':
			ret += book.formats[0]
		else:
			print("Unknown field specified in database format: " + field)
			return ""

	return ret


## ==========================================================================
#   Adds new book to database. `file' is copied to directory that is set
#   in config [db]format. After that book is added to database file, which
#   later is sorted.
## ==========================================================================


def add_book(
	book,
	file
):
	dbpath = os.path.expanduser(config.config['db']['location']) + "/.db"
	newdbpath= dbpath + "~"

	path = remove_conditionals(book, config.config['db']['format'])
	if not path:
		print("Error processing conditionals in database format")
		print("Book has not been added")
		return -1

	path = "/" + replace_specifiers(book, path)
	filename = os.path.basename(path)
	full_path_dir = os.path.expanduser(config.config['db']['location']) + path
	full_path_dir = os.path.dirname(full_path_dir)

	print(filename)
	os.makedirs(full_path_dir, exist_ok=True)
	shutil.copyfile(file, full_path_dir + "/" + filename)

	if book_exist(book):
		# book already exists, file has been replaces, no need to
		# alter database
		return 0

	# update database

	if title_exist(book):
		# title exist, we are adding new format
		add_format(book, book.formats[0])
	else:
		db.append(book)

	with open(newdbpath, "w") as fd:
		fd.write(db_header + "\n")
		for b in sorted(db, key=operator.attrgetter('author', \
				'series', 'chapter', 'title')):
			fd.write('"' + b.author + '","' + b.series + '","' + b.chapter + \
					'","' + b.title + '",' + ";".join(b.formats) + "\n")

	os.rename(newdbpath, dbpath)

	return 0
