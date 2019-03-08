#from utils import utils
from __future__ import print_function
from parser import *
import sqlite3
import file_struct
import time

def dynamic_data_entry():
    conn = sqlite3.connect('CLAS12_OCRDB.db')
    c = conn.cursor()
    c.execute("ALTER TABLE Scards ADD COLUMN new_scard_val TEXT")
    conn.commit()
    print("Record added to DB from Scard")
    c.close()
    conn.close()

dynamic_data_entry()
