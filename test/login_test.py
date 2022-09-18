import pytest
import sqlite3
import inCollege.main
from inCollege.main import *

@pytest.fixture(scope='module')
def DB():
  print("-----setup-----\n")
  database = sqlite3.connect("inCollege.db")
  databaseCursor = database.cursor()
  sampleAccounts = [
        (1, 'test1', 'aaaaaaa!A1'),
        (2, 'test2', 'aaaaaaa!A1'),
        (3, 'test3', 'aaaaaaa!A1'),
    ]                         
  databaseCursor.executemany('''INSERT INTO users VALUES (?, ?, ?)''', sampleAccounts)
  database.commit()
  yield database
  print("-----teardown-----\n")
  database.close()

#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------

# Story: Account Creation
# 1. username is unique
@pytest.mark.accountCreation
@pytest.mark.parametrize('username, result',
                        [
                          ('test1', False), # exist
                          ('test2', False), # exist
                          ('test3', False), # exist
                          ('test', True) # not exist
                        ]
)
def test_usernameUnique(username, result):
  assert unique(username) == result

# 2. password valiation
@pytest.mark.accountCreation
@pytest.mark.parametrize('password, result',
                        [
                          ('abcdefgA!1', True),
                          ('abcdefg', False), # min 8 chars
                          ('abcdefghijklmno', False), # max 12 chars
                          ('abcdefgA!', False), # at least one digit
                          ('abcdefg!1', False), # at least one capital letter
                          ('abcdefgA1', False) # at least one special character
                        ]
                        )
def test_passwordValidation(password, result):
  assert passwordValidator(password) == result

# 3. username saved to a DB
@pytest.mark.accountCreation
@pytest.mark.parametrize('username, password, result',
                         [
                           ('test1', 'aaaaaaa!A1', True), # user exists
                           ('test2', 'aaaaaaa!A1', True), # user exists
                           ('test3', 'aaaaaaa!A1', True), # user exists
                           ('test', 'aaaaaaa!A1', False) # No such user
                         ]
)
def test_checkUsernameSaved(username, password, result):
  assert checkExistingAccts(username, password) == result

# Story: Login Status
@pytest.mark.loginStatus
@pytest.mark.parametrize('username, password, result',
                        [
                          ('test1', 'aaaaaaa!A1', True), # logged in
                          ('test2', 'aaaaaaa!A1', True), # logged in
                          ('test3', 'aaaaaaa!A1', True), # logged in
                          ('test', 'aaaaaaa!A1', False) # not logged in
                        ]
                        )
def test_loginStatus(username, password, result):
  assert loginStatus(username, password) == result

# Story: User Additional Options
@pytest.mark.userOptions
@pytest.mark.parametrize('username, password, result',
                        [
                          ('test1', 'aaaaaaa!A1', True), # logged in -> move to options
                          ('test2', 'aaaaaaa!A1', True), # logged in -> move to options
                          ('test3', 'aaaaaaa!A1', True), # logged in -> move to options
                          ('test', 'aaaaaaa!A1', False) # not logged in
                        ]     
                        )
def test_stateMainInterface(username, password, result):
  assert stateMainInterface(username, password) == result

@pytest.mark.userOptions
@pytest.mark.parametrize('sel, result',
                        [
                          ('1', True), # user option exists
                          ('2', True), # user option exists
                          ('3', True), # user option exists
                          ('4', False) # user option doesn't exist
                        ]     
                        )
def test_listOptions(sel, result):
  assert listOptions(sel) == result


# Story: Skills Options
@pytest.mark.skillsOptions
@pytest.mark.parametrize('sel, result',
                         [
                           ('1', True), # skill exists
                           ('2', True), # skill exists
                           ('3', True), # skill exists
                           ('4', True), # skill exists
                           ('5', True), # skill exists
                           ('6', True), # back to previous page exists
                           ('7', False) # No option exists
                         ]
)
def test_skillsOptions(sel, result):
   assert listSkillsOptions(sel) == result

# Story: Input Validation
@pytest.mark.inputValidation



# Story: Under Construction
@pytest.mark.underConstruction
@pytest.mark.parametrize('sel, result',
                        [
                          ('1', True), 
                          ('2', True), 
                          ('3', False),
                          ('4', True),
                          ('6', True), 
                          ('8', True),
                          ('10', True), 
                        ]
                        )
def test_underConstruction(sel, result):
  assert stateUnderConstruction(sel) == result

