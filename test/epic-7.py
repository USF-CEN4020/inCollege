import pytest
import sys
import builtins
from unittest import mock
import sqlite3

from inCollege.manageDB import clearApplications, clearFriendships, clearJobs, clearUsers, getFriendsOf
from inCollege.states import loginNotifications, newAcct, requestFriends




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
	inputs = iter([' ',' ',' ',' ',' ','yes','accept', 'accept', 'yes', 'accept', 'yes', 'accept', 'yes', 'accept'])
	
	with mock.patch.object(builtins, 'input', lambda _: next(inputs)):

		requestFriends(1,'test2', 2)
		requestFriends(2, 'test3', 3)
		requestFriends(3, 'test4', 4)
		requestFriends(3, 'test1', 1)
		requestFriends(4, 'test1', 1)

		state, data = loginNotifications(1)
		state(*data)
		state, data = loginNotifications(2)
		state(*data)
		state, data = loginNotifications(3)
		state(*data)
		state, data = loginNotifications(4)
		state(*data)


@pytest.mark.friends
@pytest.mark.parametrize('userId, numFriends', [(1, 3), (2,2), (3,2), (4,2)])
def test_getFriendsOfCorrectNum(userId, numFriends):
	clearUsers()
	clearFriendships()
	clearJobs()
	clearApplications()

	initTestAccounts()
	initTestFriendships()
	
	assert len(getFriendsOf(userId)) == numFriends