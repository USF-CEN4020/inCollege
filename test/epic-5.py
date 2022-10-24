import pytest
import sys
import builtins
from unittest import mock
import sqlite3
# from commons import *
#from states import myWorkExperience
from inCollege.manageDB import *
from inCollege.testFunc import *
from inCollege.manageDB import clearFriendships, clearUsers, friendshipsCount
from inCollege.states import friendsList, mainInterface, myEducation, newAcct, friendsProfileView, myProfile, findFriends, requestFriends, pendingRequest, myWorkExperience, updateProfileSimple


# ==================================================================================
# ==================================================================================
      
      
      
      
      
# EPIC #5 Test Cases
      




# ==================================================================================
# ==================================================================================
def initTestAccounts():
    accounts = [
        ('test1', 'aaaaaaa!A1', 'first', 'last', 'usf', 'cs'),
        ('test2', 'aaaaaaa!A1', 'fname', 'lname', 'usf', 'ce'),
        ('test3', 'aaaaaaa!A1', 'f', 'l', 'hcc', 'cs'),
        ('test4', 'aaaaaaa!A1', 'fff', 'lll', 'NONE', 'NONE'),
        ('test5', 'aaaaaaa!A1', 'firstname', 'lastname', 'usf', 'cse')
	]
    for account in accounts:
        inputs = iter(account)
        with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
        
            newAcct()

@pytest.mark.jobExperience
@pytest.mark.parametrize('asId, title, employer, dateStarted, dateEnded, location, workDescription, result', 
                          [
                            (1, 'CS', 'Company', 'January 2022', 'May 2022','Tampa, FL', 'description', True),
                            (1, 'softwareDeveloper', 'Company1', 'January 2022', 'May 2022', 'Tampa, FL', 'description', True),
                            (1, 'BME', 'Company2', 'January 2022', 'May 2022','Tampa, FL', 'description', True),
                            (1, 'tester', 'Company3', 'January 2022', 'May 2022', 'Tampa, FL', 'description', False),
                            

                         ]
 )


def test_jobExperience(asId, title, employer, dateStarted, dateEnded, location, workDescription, result):
    removeWorkExperience()
    inputs = iter([title, employer, dateStarted, dateEnded, location, workDescription])
    with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
        state, data = myWorkExperience(asId)
        assert getExperienceCount(asId) == 1



@pytest.mark.parametrize('select, result', 

                        [
                        ('1', updateProfileSimple),
                        ('2', updateProfileSimple),
                        ('3', updateProfileSimple),
                        ('4', updateProfileSimple),
                        ('5', myWorkExperience),
                        ('6', myEducation)])

def test_myProfile(select, result):

    clearUsers()

    initTestAccounts()


    state = result
    with mock.patch.object(builtins, 'input', lambda _: select):
        output, dataOut = myProfile(1)
        assert output == state





# @pytest.mark.friends
# @pytest.mark.parametrize('senderId, recieverUsername, lookupSelection, query, result', [
# 	(1, 'test4', '1', 'lname', requestFriends),
# 	(1, 'test2', '2', 'usf', requestFriends),
# 	(1, 'test3', '3', 'cs', requestFriends),
	
# ])
# def test_sendFriendRequestByLookup(senderId, recieverUsername, lookupSelection, query, result):
# 	clearUsers()
# 	clearFriendships()
# 	initTestAccounts()

# 	inputs = iter([query, recieverUsername, ' '])
# 	with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
# 		state, data = findFriends(senderId, lookupSelection)
# 		assert state == result


# @pytest.mark.friends
# @pytest.mark.parametrize('response, numFriendsInSystem', [
# 	('yes', 1),
# 	('no', 0)
# ])
# def test_friendRequest(response, numFriendsInSystem):
# 	clearUsers()
# 	clearFriendships()
# 	initTestAccounts()

# 	inputs = iter([' ', response, ' '])

# 	with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
# 		requestFriends(1, 'test2', 2) # hard-coded friend request from test1 to test2
# 		pendingRequest(2)
# 		assert friendshipsCount() == numFriendsInSystem


def initDummyProfile(asId):
    with mock.patch.object(builtins, 'input', lambda _: '7'):
        myProfile(asId)


@pytest.mark.profileView
@pytest.mark.parametrize('shouldHaveProfile, result',
                            [
                                (True, friendsProfileView),
                                (False, mainInterface)
                            ]
)

def test_friendsProfileView(shouldHaveProfile, result):

    clearUsers()
    clearFriendships()
    clearProfiles()

    initTestAccounts()



    if (shouldHaveProfile):
        initDummyProfile(2)

    inputs = iter([' ','yes',' ', '1','test2',' '])
    with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
        requestFriends(1, 'test2', 2) # hard-coded friend request from test1 to test2
        pendingRequest(2)
        state, data = friendsList(1)
        assert state == result




  

