import pytest
import builtins
from unittest import mock
from inCollege.manageDB import clearFriendships, clearUsers, friendshipsCount
from inCollege.states import findFriends, findFriendsbyType, friendsList, mainInterface, newAcct, pendingRequest, requestFriends 
from inCollege.commons import *
from inCollege.testFunc import *

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


@pytest.mark.friends
@pytest.mark.parametrize('senderId, recieverUsername, lookupSelection, query, result', [
	(1, 'test4', '1', 'lname', requestFriends),
	(1, 'test2', '2', 'usf', requestFriends),
	(1, 'test3', '3', 'cs', requestFriends),
	(1, 'johnnynohit', '1', 'nohit', findFriendsbyType),
	(1, 'test1', '1', 'last', findFriendsbyType),
	(1, '0', '1', 'lname', findFriendsbyType)
])
def test_sendFriendRequestByLookup(senderId, recieverUsername, lookupSelection, query, result):
	clearUsers()
	clearFriendships()
	initTestAccounts()

	inputs = iter([query, recieverUsername, ' '])
	with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
		state, data = findFriends(senderId, lookupSelection)
		assert state == result


@pytest.mark.friends
@pytest.mark.parametrize('response, numFriendsInSystem', [
	('yes', 1),
	('no', 0)
])
def test_friendRequest(response, numFriendsInSystem):
	clearUsers()
	clearFriendships()
	initTestAccounts()

	inputs = iter([' ', response, ' '])

	with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
		requestFriends(1, 'test2', 2) # hard-coded friend request from test1 to test2
		pendingRequest(2)
		assert friendshipsCount() == numFriendsInSystem

	
@pytest.mark.friends
@pytest.mark.parametrize('disconnectChoice, numFriendsInSystem', [
	('test2', 0),
	('0', 1)
])
def test_disconnectFriend(disconnectChoice, numFriendsInSystem):
	clearUsers()
	clearFriendships()
	initTestAccounts()

	inputs = iter([' ', 'yes', ' ', disconnectChoice, ' '])

	with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
		requestFriends(1, 'test2', 2) # hard-coded friend request from test1 to test2
		pendingRequest(2)

		state, data = friendsList(1)
		if state != mainInterface:
			state, data = state(*data)
		
		assert friendshipsCount() == numFriendsInSystem
		
		
		
# Story: Total Accounts
#        As a developer, I want to increase the account limit so  
#        that InCollege can support 10 unique student accounts.   

@pytest.mark.accountNumber
def test_accountCount():
  assert accountCount(0) == True # counting the number of users in actual DB 



# Story: Friends
#		 As a developer, I want to add a friends list feature so that 
# 		 user’s can connect with people they know.
# Acceptance Criteria:
# 		 User will have a “show my network” option that will present 
#  		 the user with the list of people they’ve connected with (including none).

#@pytest.mark.friends
#@pytest.mark.parametrize('numFriendsInSystem',[
#	(0),(1)
#])
#def test_friendsList(numFriendsInSystem):
#	clearUsers()
#	clearFriendships()
#	initTestAccounts()
#
#	inputs = iter([' ', 'yes', ' '])
#
#	with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
#		requestFriends(1, 'test2', 2) # hard-coded friend request from test1 to test2
#		pendingRequest(2)
#		assert friendshipsCount() == numFriendsInSystem
