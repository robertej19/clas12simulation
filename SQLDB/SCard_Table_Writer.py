#from utils import utils
from parser import *
import sqlite3

filename = "scard.txt"
sarray = []

# Fix the below so that it works with a dictionary
# Collecting info from scard
# If scard is not in a proper format, the class scard_parser should stop the script.
scard = scard_parser(filename) # parse scard. scard is called only once at this line.

scard_key = ['group','user','nevents','generator', 'genOptions',  'gcards', 'jobs',  'project', 'luminosity', 'tcurrent',  'pcurrent']

for key in scard_key:
  sarray.append(scard.data[key])

def create_bank_account_details(bank_type):
  fields = {
    "UserID": {"type": "string", "required": True},
    "Group_name": {"type": "string", "required": True},
    "User": {"type": "string", "required": True},
    "Nevents": {"type": "integer", "required": True}
  }

  # this is only for the order we want the information in
  field_names = [ "UserID", "Group_name", "User", "Nevents"]

  bankaccount_obj = {'bank_type': bank_type}


UID = "robertEJ"
CReq = 1
MReq = 2

def dynamic_data_entry(UID,scard_array,CReq,MReq):
    conn = sqlite3.connect('CLAS12_OCRDB.db')
    c = conn.cursor()
    ta = scard_array
    c.execute("INSERT INTO Scards(UserID, Group_name, User, Nevents, Generator, GenOptions, Gcards, Jobs, Project, Luminosity, Tcurrent, Pcurrent, Cores_Req, Mem_Req) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
              (UID,ta[0],ta[1],ta[2],ta[3],ta[4],ta[5],ta[6],ta[7],ta[8],ta[9],ta[10],CReq,MReq))
    conn.commit()
    print("Record added to DB from Scard")
    c.close()
    conn.close()

dynamic_data_entry(UID,sarray,CReq,MReq)
"""
scard_fields = (('UserID','TEXT'),('Group_name','TEXT'),('User','TEXT'),('Nevents','INT')
                ('Generator','TEXT'),('GenOptions','TEXT'),('Gcards','TEXT'),('Jobs','INT'),
                ('Project','TEXT'),('Luminosity','INT'),('Tcurrent','INT'),('Pcurrent','INT'),
                  ('Cores_Req','INT'),('Mem_Req','INT'))
"""

"""
  print("If you would like to cancel at any time type: \"cancel\"")
  for key in field_names:
    value = utils.get_scard_value(key, fields[key])
    if value is None:
      continue
    elif value == "cancel":
      return "ERROR PARSING"#cancel_creation()
    else:
      bankaccount_obj[key] = value

  return bankaccount_obj #RequestHelper.send_post_request("/bank/create", {}, bankaccount_obj)

def create_bankaccount(request):
  #Django sends the request in a byte string, json needs a unicode string
  body_unicode = request.body.decode('utf-8')
  body = json.loads(body_unicode)
  if not isinstance(body, dict):
    return Response("Invalid Request JSON Object expected", 400)

  required_parameters = ["username", "password","account_number", "display_name", "bank_type"]

  optional_parameters = ["direct_deposits", "transactions"]

  response = utils.verify_parameters(required_parameters, body)

  if response:
    return response

  # Set all optional parameters to None if they are not set
  for parameter in optional_parameters:
    if parameter not in body:
      body[parameter] = None
  return controller.create_bankaccount(body["username"],body["password"], body["account_number"],
                                       body["display_name"],body["direct_deposits"],
                                       body["transactions"], request.user, body["bank_type"])
"""

"""
def create_bankaccount(username, password, account_number, display_name,
                       direct_deposits, transactions, user, bank_type):

  try:
    bank_account = BankAccount(username=username, password=password,
                               account_number=account_number, display_name=display_name,
                               direct_deposits=direct_deposits, transactions=transactions,
                               user=user,
                               bank_type= SupportedBank.objects.get(pk=bank_type))

    bank_account.save()
    print("Saving account")
    """
