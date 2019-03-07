"""
SCard Utilities
"""
genOutput= {'clasdis': 'sidis.dat', 'dvcs': 'dvcs.dat','disrad':'dis-rad.dat'}
genExecutable =  {'clasdis': 'clasdis', 'dvcs': 'dvcsgen','disrad':'generate-dis'}
"""
get number of lines in scard
if number of non-empty lines larger than scard_proper return error

for line in scard:
  get_scard_value(line)

get_scard_value(line):
  grab first word in line
    find if line is in proper scard format
      if no, error message
      if yes, grab all text between : and #
        validate that data is of the right form
          if yes, return scard format word, value


group:  rgaDIS     #
project description
user:  mungaro

def get_scard_value(field_name, field_obj):

  value = input("Please enter the desired field, %s: " %(bold(field_name)))
  if value == "cancel!":
    return value
  if not field_obj["required"] and not value:
    return None
  elif not is_valid_type(value, field_obj["type"]):
    print("Invalid Type for %s it should be of type: %s" %(bold(field_name), field_obj["type"]))
    return get_field_value(field_name, field_obj)

import argparse, sys, os, subprocess, socket

# declare a global dictionary to match genOutput and genExecutable to generator row

# Proper configuration of scard:
scard_key = ['group','user','nevents','generator', 'genOptions',  'gcards', 'jobs',  'project', 'luminosity', 'tcurrent',  'pcurrent']

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
        if key != scard_key[linenum]:
            print "ERROR: The " + ordinal(linenum+1) +" line of steering card starts with "+ key +"."
            print "That line must have the key " + scard_key[linenum] +"."
        self.data[key] = value

# voild function for parsing scard.txt into a dictionary
    def parse_scard(self, filename, store=True):
        scard=open(filename, "r")
        for linenum, line in enumerate(scard):
            self.parse_scard_line(linenum,line)
        if store == True:
            self.store()

#void function for validating s_card
    def validate_scard_line(self, linenum, line):
        if line.count("#") ==0:
            print "Warning: No comment in "+ ordinal(linenum+1) + " line."
        elif line.count("#")>1:
            print "ERROR: number of hashes>1 at "+ordinal(linenum+1)+" line."
            print "# can be only used for a delimeter and for once. Stopped."
            exit()
        if line.count(":") ==0:
            print "ERROR: No colon in "+ ordinal(linenum+1) + " line."
            print "The data cannot be interpreted. Stopped."
            exit()
        elif line.count(":")>1:
            print "ERROR: number of colons>1 at "+ordinal(linenum+1)+" line."
            print "\':\' can be only used for a delimeter and for once. Stopped."
            exit()

# store info's in dictionary into single variables
    def store(self):
        self.group = self.data.get("group")
        self.user = self.data.get("user")
        self.nevents = self.data.get("nevents")
        self.generator = self.data.get("generator")
        self.genOptions = self.data.get("genOptions")
        self.gcards = self.data.get("gcards")
        self.jobs = self.data.get("jobs")
        self.project = self.data.get("project")
        self.luminosity = self.data.get("luminosity")
        self.tcurrent = self.data.get("tcurrent")
        self.pcurrent = self.data.get("pcurrent")
        self.genOutput = genOutput.get(self.data.get("generator"))
        self.genExecutable = genExecutable.get(self.data.get("generator"))

  return value
"""
  """
  Prompts user for input and verifies that it is correct

  param field_name: String of what the field should be called for the user
  param field_obj: Dict with type field and required field
  returns: String of value input by user or None if optional and no argument
  """
"""
  value = input("Please enter the desired field, %s: " %(bold(field_name)))
  if value == "cancel!":
    return value
  if not field_obj["required"] and not value:
    return None
  elif not is_valid_type(value, field_obj["type"]):
    print("Invalid Type for %s it should be of type: %s" %(bold(field_name), field_obj["type"]))
    return get_field_value(field_name, field_obj)

  return value
"""
def is_valid_type(value, desired_type):
  """
  Checks the input string for if it is of desired type

  param value: String of what the user typed in
  param desired_type: String of what type you want the input to be
  returns: True/False where True signifies type is valid
  """

  # should already be a string
  if desired_type == "string" and value:
    return True
  if desired_type == "integer":
    return value.isdigit()
  if desired_type == "money":
    return is_number(value)
  #if unknown type return false
  return False

def bold(input_str):
  """
  Makes input string bold formatted

  param input_str: string you would like to be bold
  returns: bold string
  """

  return '\033[1m' + input_str + '\033[0m'

def error(input_str):
  """
  Makes input string error formatted

  param input_str: string you would like to be error text (red)
  returns: error string
  """

  return '\033[91m' + input_str + '\033[0m'

def is_number(s):
  try:
    float(s)
    return True
  except ValueError:
    return False
