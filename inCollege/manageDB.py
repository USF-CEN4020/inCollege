from .commons import *
import sqlite3



database = sqlite3.connect("inCollege.db")
databaseCursor = database.cursor()


databaseCursor.execute('''CREATE TABLE IF NOT EXISTS users(
														id INTEGER PRIMARY KEY ASC, 
														username TEXT, 
														password TEXT,
                            firstname TEXT,
                            lastname TEXT,
                            university TEXT,
                            major TEXT)''')
database.commit()


databaseCursor.execute('''Create TABLE IF NOT EXISTS jobs(
                                                        jobId INTEGER PRIMARY KEY ASC,
                                                        title TEXT,
                                                        description TEXT,
                                                        employer TEXT,
                                                        location TEXT,
                                                        salary REAL,
                                                        posterId INTEGER,
                                                        FOREIGN KEY(posterId)
                                                            REFERENCES users(id))''')
database.commit()


databaseCursor.execute('''CREATE TABLE IF NOT EXISTS userSettings(
                            userId INTEGER,
                            receiveEmail INTEGER,
                            receiveSMS INTEGER,
                            targetedAds INTEGER,
                            language TEXT,
                            FOREIGN KEY(userId)
                                REFERENCES users(id))''')
database.commit()


databaseCursor.execute('''CREATE TABLE IF NOT EXISTS friendships(
                            acceptRequest INTEGER,
                            senderId INTEGER,
                            receiverId INTEGER,
                            FOREIGN KEY(senderId) REFERENCES users(id),
                            FOREIGN KEY(receiverId) REFERENCES users(id))''')
database.commit()


databaseCursor.execute('''CREATE TABLE IF NOT EXISTS profiles(
														userId INTEGER,
														title TEXT, 
														major TEXT,
                            university TEXT,
                            about TEXT,
                            experience TEXT,
                            school TEXT,
                            degree TEXT,
                            years TEXT)''')
database.commit()


# databaseCursor.execute('''CREATE TABLE IF NOT EXISTS experience(
# 														userId INTEGER,
# 														title TEXT, 
# 														major TEXT,
#                             university TEXT,
#                             about TEXT,
#                             experience TEXT,
#                             education TEXT)''')
# database.commit()



#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------



def clearUsers():
	databaseCursor.execute('DELETE FROM users')
	database.commit()
 

def clearJobs():
	databaseCursor.execute('DELETE FROM jobs')
	database.commit() 


def clearFriendships():
  databaseCursor.execute('DELETE FROM friendships')
  database.commit()


def listUsers():
	for row in databaseCursor.execute("SELECT * FROM users ORDER BY id"):
		print(row)


def listFriendships():
  for row in databaseCursor.execute("SELECT * FROM friendships ORDER BY senderId"):
    print(row)


def clearUserSetting(uId):
  databaseCursor.execute("DELETE FROM userSettings WHERE userId = ?", (uId,))
  database.commit()
	

def idLookup(uId):
  lookup = databaseCursor.execute("SELECT * FROM users WHERE id IS ?", (uId,))
  return lookup.fetchone()


def usernameLookup(uId):
  lookup = databaseCursor.execute("SELECT * FROM users WHERE id IS ?", (uId,))
  user = lookup.fetchone()
  return user[1]


def deleteFromPendingList(userId, friendId):
  databaseCursor.execute("DELETE FROM friendships WHERE (acceptRequest = 0 AND senderId = ? AND receiverId = ?)", (friendId, userId))
  database.commit()


def deleteFromFriendList(userId, friendId):
  databaseCursor.execute("DELETE FROM friendships WHERE (acceptRequest = 1 AND senderId = ? AND receiverId = ?) OR (acceptRequest = 1 AND receiverId = ? AND senderId = ?)", (userId, friendId, userId, friendId))
  database.commit()



#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------



def fieldById(field):
    '''
    Function generator for getting looking up an entries field by its id

    param field: a column field of the users table
    return: a function f(x) = (field of a user with id x)
    '''
    return lambda uId: (byKey(idLookup(uId), field))


usernameById = fieldById("username") # A function f(x) = (username of a user with id x)
#firstnameById = fieldById("firstname") # A function f(x) = (username of a user with id x)
lastnameById = fieldById("lastname") # A function f(x) = (username of a user with id x)


def tableEntriesCount(table):
    '''
    Generates a function that returns the number of rows in a given table

    param table: a case-sensitive string of the name of a table that is to have its rows counted
    return: A lambda f() = number of rows in table
    '''
    return lambda: (databaseCursor.execute("SELECT Count(*) FROM " + table).fetchone()[0]) # Need to look into how much of a vulnerabilty this is


userCount = tableEntriesCount("users") # returns the number of total users in the system
jobsCount = tableEntriesCount("jobs") # returns the number of total jobs in the system
friendshipsCount = tableEntriesCount("friendships")


def dbEmpty():
	if (userCount() == 0):
		return True
	else:
		return False


def dbFull():
	if (userCount() == MAX_USERS):
		return True
	else:
		return False


def jobsFull():
    return (jobsCount() == MAX_JOBS)


def vacuouslyTrue(string):
    return True


def unique(username):
    lookup = databaseCursor.execute("SELECT COUNT(*) FROM users where username IS ?", (username,))
    return lookup.fetchone()[0] == 0


def acctSettingsInitilized(userId):
  lookup = databaseCursor.execute("SELECT COUNT(*) FROM userSettings WHERE userId IS ?", (userId,))
  return lookup.fetchone()[0] == 1



#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------



def checkExistingAccts(username, password):
  '''
  Looks up an account from a username and password

  param username: the username of the target user
  param password: the password of the target user
  return: the id of the specified user or -1 if the user does not exist
  '''

  databaseCursor.execute("SELECT * FROM users WHERE username= ? and password= ?",
    (username, password))
  found = databaseCursor.fetchone()
  if found:
    return found[0]
  else:
    return -1


def checkExistingUsername(username):
  databaseCursor.execute("SELECT * FROM users WHERE username= ?",
    (username,))
  found = databaseCursor.fetchone()
  if found:
    return found[0]
  else:
    return -1


def checkUserGuestControls(userId):
  databaseCursor.execute("SELECT receiveEmail, receiveSMS, targetedAds FROM userSettings WHERE userId = ?", (userId,))
  found = databaseCursor.fetchone()

  if found:
    return found
  else:
    return DEFAULT_GUEST_CONTROLS


def checkUserLanguage(userId):
  databaseCursor.execute("SELECT language FROM userSettings where userId = ?", (userId,))
  found = databaseCursor.fetchone()

  if found:
    return found[0]
  else:
    return DEFAULT_LANGUAGE_SETTINGS


def checkExistingNames(firstname, lastname):
  '''
  Looks up a name from firstname and lastname

  param firstname:
  param lastname:
  return the id of the specified user or -1 if the user does not exist

  '''
  databaseCursor.execute("SELECT * FROM users WHERE firstname= ? and lastname= ?", (firstname, lastname))
  found = databaseCursor.fetchone()
  if found:
    return found[0]
  else:
    return -1


def checkExistingFriend(userId, friendId):
  databaseCursor.execute("SELECT * FROM friendships WHERE (senderId= ? AND receiverId= ?) OR (senderId= ? AND receiverId= ?)", (userId, friendId, friendId, userId))
  found = databaseCursor.fetchone()
  if found: # return 0 if the request is not accepted or 1 if the request is accepted
    return found[0]
  else:
    return -1


def checkUserId(username):
  databaseCursor.execute("SELECT * FROM users WHERE username= ?", (username,))
  found = databaseCursor.fetchone()
  if found: # return user id
    return found[0]
  else:
    return -1


def checkExistingPendingRequest(userId):
  databaseCursor.execute("SELECT * FROM friendships WHERE acceptRequest= ? AND receiverId= ?", (0, userId))
  found = databaseCursor.fetchall()
  if found: 
    return found
  else:
    return -1
  
  
def checkProfileExists(userId):
  '''
  Looks up an account from a username and password

  param username: the username of the target user
  param password: the password of the target user
  return: the id of the specified user or -1 if the user does not exist
  '''

  databaseCursor.execute("SELECT * FROM profiles WHERE userId= ?",
    (userId,))
  found = databaseCursor.fetchone()
  if found:
    return found[0]
  else:
    return -1
  

def updateDB(table, field, userId, value):
    databaseCursor.execute("UPDATE " + table +  " SET " + field + " = ? WHERE userId = ?", (value, userId))
    database.commit()