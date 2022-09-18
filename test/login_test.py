import pytest
import sqlite3
import inCollege.main
from inCollege.main import *

@pytest.fixture(scope='module')
def DB():
  print("-----setup-----\n")
  database = sqlite3.connect("inCollege.db")
  databaseCursor = database.cursor()
  # databaseCursor.execute('''CREATE TABLE users(
  #                           id INTEGER PRIMARY KEY ASC, 
  #                           username TEXT, 
  #                           password TEXT)''')
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
# def test_checkUsernameSaved():


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

# Story: Under Construction
@pytest.mark.underConstruction
@pytest.mark.parametrize('sel, result',
                        [
                          ('3', False), 
                          ('1', True), 
                          ('2', True), 
                          ('4', True),
                          ('6', True), 
                          ('8', True),
                          ('10', True), 
                        ]
                        )
def test_underConstruction(sel, result):
  assert underConstructionState(sel) == result