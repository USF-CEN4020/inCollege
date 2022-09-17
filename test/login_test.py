import pytest
import sqlite3
from inCollege.main import *

@pytest.fixture(scope='module')
def setupDatabase():
  print("-----INSERT TO A DB-----\n")
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
  database.close()

# Story: Account Creation

# 1. username is unique
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



