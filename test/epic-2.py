import pytest
import builtins
from unittest import mock
import sqlite3
from commons import *
from inCollege.states.baseStates import *
from inCollege.manageDB import *


# ==================================================================================
# ==================================================================================
      
      
      
      
      
# EPIC #2 Test Cases
      




# ==================================================================================
# ==================================================================================

# Testing whether the sub-menu's that list additional options are returning the
# the correct previous state if the specific option is selected

@pytest.mark.backtracking
def test_mainInterfaceTrue():
  state = applicationEntry
  with mock.patch.object(builtins, 'input', lambda _: '4'):
    output, dataOut = mainInterface(-1)
    assert output == state
    
@pytest.mark.backtracking
def test_mainInterfaceFalse():
  state = applicationEntry
  with mock.patch.object(builtins, 'input', lambda _: '1'):
    output, dataOut = mainInterface(-1)
    assert output != state

@pytest.mark.backtracking
def test_jobInterfaceTrue():
  state = mainInterface
  with mock.patch.object(builtins, 'input', lambda _: '3'):
    output, dataOut = jobInterface(-1)
    assert output == state
    
@pytest.mark.backtracking    
def test_jobInterfaceFalse():
  state = mainInterface
  with mock.patch.object(builtins, 'input', lambda _: '2'):
    output, dataOut = jobInterface(-1)
    assert output != state
    
@pytest.mark.backtracking   
def test_listSkillsTrue():
  state = mainInterface
  with mock.patch.object(builtins, 'input', lambda _: '6'):
    output, dataOut = listSkills(-1)
    assert output == state
    
@pytest.mark.backtracking
def test_listSkillsFalse():
  state = mainInterface
  with mock.patch.object(builtins, 'input', lambda _: '4'):
    output, dataOut = listSkills(-1)
    assert output != state
      
      
      
# ==================================================================================
# ==================================================================================

# Ensuring the user can add jobs and when five jobs are in the database, it reads full

clearJobs()
  
@pytest.mark.jobPosting
@pytest.mark.parametrize('title, description, employer, location, salary, posterID, result',
                         [
                           ('CPE', 'stuff', 'Company4', 'Tampa, FL', '100000', '1', False),
                           ('CS', 'stuff', 'Company4', 'Tampa, FL', '100000', '2', False),
                           ('ME', 'stuff', 'Company4', 'Tampa, FL', '100000', '3', False),
                           ('EE', 'stuff', 'Company4', 'Tampa, FL', '100000', '4', False),
                           ('BIO', 'stuff', 'Company4', 'Tampa, FL', '100000', '5', True)
                         ]
)
def test_jobPost(title, description, employer, location, salary, posterID, result):
  inputs = iter([title, description, employer, location, salary, posterID])
  with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
    state, data = jobPost(-1) 
    assert jobsFull() == result

# testing whether the user can look up the existing first and last name
# and the extended account creation function

clearUsers()

@pytest.mark.extendedAccountCreation
@pytest.mark.parametrize('username, password, firstname, lastname, result',
                        [
                          ('test1', 'aaaaaaa!A1', 'first', 'last', 1),
                          ('test2', 'aaaaaaa!A1', 'fname', 'lname', 2),
                          ('test3', 'aaaaaaa!A1', 'f', 'l', 3),
                          ('test4', 'aaaaaaa!A1', 'fff', 'lll', 4)
                        ]
                        )
def test_extendedAccountCreation(username, password, firstname, lastname, result):
  inputs = iter([username, password, firstname, lastname])
  with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
    state, data = newAcct() 
    assert checkExistingAccts(username, password) == result

@pytest.mark.userLookup
@pytest.mark.parametrize('firstname, lastname, result',
                        [
                          ('first', 'last', 1),
                          ('fname', 'lname', 2),
                          ('f', 'l', 3),
                          ('fff', 'lll', 4),
                          ('ffff', 'llll', -1)
                        ]
                        )
def test_userLookup(firstname, lastname, result):
  assert checkExistingNames(firstname, lastname) == result


# testing if the user can see a success story and have the option to play a related video
@pytest.mark.successStory
def test_successStoryState():
  state = applicationEntry
  with mock.patch.object(builtins, 'input', lambda _: '3'):
    output, dataOut = videoPlayer()
    assert output == state
