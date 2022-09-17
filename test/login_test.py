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
        (4, 'test4', 'aaaaaaa!A1'),
    ]                         
  databaseCursor.executemany('''INSERT INTO users VALUES (?, ?, ?)''', sampleAccounts)
  database.commit()
  yield database
  database.close()

# Story: Account Creation

# 1. username is unique
def test_usernameUnique():
  assert unique('test1') == False
  assert unique('test2') == False
  assert unique('test3') == False
  assert unique('test4') == False
  assert unique('test') == True

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

