#!/usr/bin/python

import os
import sys

#

# command line call example: python -c 'import parser ; parser.commonFilenameRoot("/Users/ungaro/list.txt")'
def commonFilenameRoot(filename = ''):
	print "Importing list of files from: ", filename
	f = open(filename, 'r')
	files = f.readlines()
	f.close()
	common = os.path.commonprefix(files)
	print "Common path: ", common


# command line call example: python -c 'import parser ; parser.getOption("scard.txt")'
def getOption(filename = 'scard.txt'):
	print "Importing list of files from: ", filename



# arguments: filename and string to find
filename = sys.argv[1]
toFind   = sys.argv[2]

lines = []             # Declare an empty list named "lines"

if not "output" in toFind:
	with open (filename, 'rt') as in_file:  # Open file
		in_file.seek(0)
		for line in in_file:      # For each line of text in in_file, where the data is named "line",
			if toFind in line:     # match toFInd string
				lines.append(line)  # add that line to our list of lines.

	for element in lines:                 # For each element in our list
		start = element.find(":") + 1      # after the :
		end   = element.find("#")          # before #
		found = element[start:end].strip() # stripping whitespaces
		print(found)

if "genOutput" in toFind:
	with open (filename, 'rt') as in_file:  # Open file
		for line in in_file:          # For each line of text in in_file, where the data is named "line",
			if "generator:" in line:  # match generator to find type
				lines.append(line)     # add that line to our list of lines.
	for element in lines:                 # For each element in our list
		start = element.find(":") + 1      # after the :
		end   = element.find("#")          # before #
		found = element[start:end].strip() # stripping whitespaces
	if "clasdis" in found != -1:
		print "sidis.dat"
	elif "dvcs" in found != -1:
		print "dvcs.dat"
	elif "disrad" in found != -1:
		print "dis-rad.dat"

if "genExecutable" in toFind:
	with open (filename, 'rt') as in_file:  # Open file
		for line in in_file:          # For each line of text in in_file, where the data is named "line",
			if "generator:" in line:  # match generator to find type
				lines.append(line)     # add that line to our list of lines.
	for element in lines:                 # For each element in our list
		start = element.find(":") + 1      # after the :
		end   = element.find("#")          # before #
		found = element[start:end].strip() # stripping whitespaces
	if "clasdis" in found != -1:
		print "clasdis"
	elif "dvcs" in found != -1:
		print "dvcsgen"
	elif "disrad" in found != -1:
		print "generate-dis"
