import pytest
import sys
import builtins
from unittest import mock
import sqlite3
from inCollege.main import *
from inCollege.states import newAcct

# ==================================================================================
# ==================================================================================
      
      
      
      
      
# EPIC #4 Test Cases
      




# ==================================================================================
# ==================================================================================


def initTestAccounts():
	accounts = [
		('test1', 'aaaaaaa!A1', 'first', 'last', 'usf', 'cs'),
        ('test2', 'aaaaaaa!A1', 'fname', 'lname', 'usf', 'ce'),
        ('test3', 'aaaaaaa!A1', 'f', 'l', 'hcc', 'cs'),
        ('test4', 'aaaaaaa!A1', 'fff', 'lll', 'NONE', 'NONE')
	]
	for account in accounts:
		inputs = iter(account)
		with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
			newAcct()



