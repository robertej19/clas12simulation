from __future__ import print_function
import argparse, sys, os, subprocess, socket
import file_struct

class scard_parser:
# Default Constructor: a = scard_parser();  a.parse_scard("scard.txt")
# Parametrized Constructor:  a = scard_parser("scard.txt")
    def __init__(self, scard_filename=None):
        self.type ='scard parser'
        self.data = {}
        if scard_filename != None:
            self.parse_scard(scard_filename)

# void function for saving line into a dictionary
    def parse_scard_line(self, linenum, line):
        self.validate_scard_line(linenum, line) # 1st validating
        pos_delimeter_colon = line.find(":")
        pos_delimeter_hash = line.find("#")
        key =   line[:pos_delimeter_colon].strip()
        value=  line[pos_delimeter_colon+1:pos_delimeter_hash].strip()
        if key != file_struct.scard_key[linenum]:
          print("ERROR: Line {} of the steering card has the key '{}''.".format(linenum+1,key))
          print("That line must have the key '{}'.".format(file_struct.scard_key[linenum]))
        self.data[key] = value

# void function for parsing scard.txt into a dictionary
    def parse_scard(self, filename, store=True):
        scard=open(filename, "r")
        for linenum, line in enumerate(scard):
            self.parse_scard_line(linenum,line)

#void function for validating s_card
    def validate_scard_line(self, linenum, line):
        if line.count("#") ==0:
            print("Warning: No comment in line {}.".format(linenum+1))
        elif line.count("#")>1:
            print("ERROR: number of hashes>1 in line {}".format(linenum+1))
            print("# can be used only as a delimeter and only once per line. Edit scard to fix.")
            exit()
        if line.count(":") ==0:
            print("ERROR: No colon in line {}".format(linenum+1))
            print("The data cannot be interpreted. Stopped.")
            exit()
        elif line.count(":")>1:
            print("ERROR: number of colons>1 at line {}".format(linenum+1))
            print("':' can be used only as a delimeter and only once per line. Edit scard to fix.")
            exit()
