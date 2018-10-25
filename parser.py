#!/usr/bin/python

import os
import sys

# command line call example: python -c 'import parser ; parser.commonFilenameRoot("/Users/ungaro/list.txt")'
def commonFilenameRoot(filename = ''):
	print "Importing list of files from: ", filename
	f = open(filename, 'r')
	files = f.readlines()
	f.close()
	common = os.path.commonprefix(files)
	print "Common path: ", common

