import pytest
import sys
import builtins
from unittest import mock
import sqlite3

from manageDB import clearFriendships, clearUsers
from states import newAcct




# ==================================================================================
# ==================================================================================





# EPIC #7 Test Cases





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


def initTestFriendships():
	inputs = [' ',' ',' ',' ',' ','yes',' ']

def test_getFriendsOf():
	clearUsers()
	clearFriendships()
	initTestAccounts()

