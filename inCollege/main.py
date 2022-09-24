import sqlite3
import os
from functools import lru_cache
import random


MAX_USERS = 5
MAX_JOBS = 5



database = sqlite3.connect("inCollege.db")
databaseCursor = database.cursor()
databaseCursor.execute('''CREATE TABLE IF NOT EXISTS users(
														id INTEGER PRIMARY KEY ASC, 
														username TEXT, 
														password TEXT)''')
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

#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------

# test purpose

def loginStatus(username, password):
  check = checkExistingAccts(username, password)
  if check == -1:
    clear()
    return False
  else:
    clear()
    return True

def stateMainInterface(username, password):
  if loginStatus(username, password) == True:
    return True
  else:
    return False

def listOptions(sel):
  if sel == '1' or sel == '2' or sel == '3':
    return True
  else:
    return False

def accountCount(count):
  count = userCount()
  if count > 5 or count < 0:
    return False
  else:
    return True

def listSkillsOptions(sel):
  if sel == '1' or sel == '2' or sel == '3' or sel == '4' or sel == '5' or sel == '6':
    return True
  else:
    return False

def stateUnderConstruction(sel):
  if sel == '1' or sel == '2' or sel == '4' or sel == '6' or sel == '8' or sel == '10':
    return True
  else: 
    return False



#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------



def clearUsers():
	databaseCursor.execute('DELETE FROM users')
	database.commit()
 
def clearJobs():
	databaseCursor.execute('DELETE FROM jobs')
	database.commit() 

def listUsers():
	for row in databaseCursor.execute("SELECT * FROM users ORDER BY id"):
		print(row)
	


#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------


clear = lambda: os.system('clear') # A function f() that clears all text from the terminal
isEqual = lambda x, y: (x == y)
isZero = lambda x : (isEqual(x,0)) # A function f(x) = x == 0

byKey = lambda x, y: (x[y]) # A function f(x) = x[y]

def idLookup(uId):
    lookup = databaseCursor.execute("SELECT * FROM users WHERE id IS ?", uId)
    return lookup.fetchone()

def fieldById(field):
    '''
    Function generator for getting looking up an entries field by its id

    param field: a column field of the users table
    return: a function f(x) = (field of a user with id x)
    '''
    return lambda uId: (byKey(idLookup(uId), field))

usernameById = fieldById("username") # A function f(x) = (username of a user with id x)

def tableEntriesCount(table):
    '''
    Generates a function that returns the number of rows in a given table

    param table: a case-sensitive string of the name of a table that is to have its rows counted
    return: A lambda f() = number of rows in table
    '''
    return lambda: (databaseCursor.execute("SELECT Count(*) FROM " + table).fetchone()[0]) # Need to look into how much of a vulnerabilty this is

userCount = tableEntriesCount("users") # returns the number of total users in the system

jobsCount = tableEntriesCount("jobs") # returns the number of total jobs in the system

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

def numberValidator(number):
    try:
        float(number)
        return True
    except ValueError:
        return False

def passwordValidator(password):
  c, d, s = 0, 0, 0
  length = len(password)
  if length > 7 and length < 13:
    for i in password:
      if i.isupper():
        c += 1
      if i.isdigit():
        d += 1
      if i=='!' or i=='@' or i=='#' or i=='$' or i=='%' or i=='^' or i=='&' or i=='*':
        s += 1

  if c > 0 and d > 0 and s > 0:
    return True
  else:
    return False



@lru_cache
def menuValidatorBuilder(validOptions):
    '''
    Generates a validator from a list of valid options

    :param validOptions: A string consisting of every valid input from a menu
    :return a function f(x) that returns if x is in validOptions
    '''

    optionsList = list(validOptions)
    return lambda menuInput: (menuInput in optionsList and menuInput != '')

def gatherInput(prompt, failResponse, validator):
    '''
	Continuously prompts the user for input, validates the input it gets are returns it if its fine or gives an error message if its bad

    :param prompt: A string the user recieves when being prompted for input, used in an "input(prompt)" call
    :param failResponse: A message the user recieves if they give bad input
    :param validator: A function f(x) = (x is a valid string for a given prompt)
    :return validated user input
    '''
    
    userInput = input(prompt)
    while True:
        if len(userInput) == 0:
            clear()
            print("Please input a response.\n")
            userInput = input(prompt)
        elif not validator(userInput):
            clear()
            print(failResponse)
            userInput = input(prompt)
        else:
            return userInput


def exitState(asId):
  clear()
  if (asId == -1):
    print("Goodbye")
  else:
    print("Goodbye,", usernameById(asId))
  exit()


def jobPost(asId):
    title = gatherInput("Enter job title: ", "", vacuouslyTrue)
    description = gatherInput("Enter job description: ", "", vacuouslyTrue)
    employer = gatherInput("Enter employer: ", "", vacuouslyTrue)
    location = gatherInput("Enter job location: ", "", vacuouslyTrue)
    salary = float(gatherInput("Enter salary (no dollar sign): ", "PLease enter a valid number without a dollar sign", numberValidator))

    databaseCursor.execute("INSERT INTO jobs (title, description, employer, location, salary, posterID) VALUES (?,?,?,?,?,?)",
            (title, description, employer, location, salary, asId))

    database.commit()

    return jobInterface, (asId,)


def jobInterface(asId):
    prompt = "Please select an option below:\n"\
        "\t1. Post a job\n"\
        "\t2. Search for a job\n"\
        "\t3. Go back\n"\
        "Selection: "
    sel = int(gatherInput(prompt, "Invalid input. Please try again\n", menuValidatorBuilder('123')))

    if sel == 1:
        clear()
        return jobPost, (asId,)
    elif sel == 2:
        clear()
        return underConstruction, (asId, jobInterface)
    else:
        clear()
        return mainInterface, (asId,)

def mainInterface(asId):
  prompt = "Please select an option below:\n"\
          "\t1. Search for a job\n"\
          "\t2. Find someone you know\n"\
          "\t3. Learn a new skill\n"\
          "\t4. Log Out\n"\
          "Selection: "
  sel = int(
        gatherInput(prompt, "Invalid input. Please try again.\n",
                    menuValidatorBuilder('1234')))

  if sel == 1:
    clear()
    return jobInterface, (asId,)
  elif sel == 2:
    clear()
    return underConstruction, (asId, mainInterface)
  elif sel == 3:
    clear()
    return listSkills, (asId,)
  else:
    clear()
    return applicationEntry, None

def login():
  if dbEmpty():
    print("No existing accounts. Please create a new account.\n")
    return applicationEntry, None
  else:
    username = input("Username: ")
    password = input("Password: ")
  
    id = checkExistingAccts(username, password)
    if (id != -1):
      clear()
      print("You have successfully logged in\n")
      return mainInterface, (id,)
    else:
      clear()
      print("Incorrect username/password. Please try again.\n")
      return applicationEntry, None


def newAcct():
	'''
 	Creates a new account based on user input. Ensures there is room in the database and username and passwords are valid.

	:sideeffect Adds a new user to the users table in the database
	:return mainInterface state function
'''
	if dbFull():
		print("\nAll permitted accounts have been created, please come back later.\n")
		return exitState, -1
	username = gatherInput(
            "Enter a username: ",
            "Username already exists. Please try again.",
            unique)

	password = gatherInput(
            "\nPassword must meet the following requirements:\n"\
            "\t-Length of 8-12 characters\n"\
            "\t-Contain one capital letter\n"\
            "\t-Contain one digit\n"\
            "\t-Contain one of the following special characters: !, @, #, $, %, ^, &, *\n"\
            "\nPassword: ",
            "Password does not meet security requirements",
            passwordValidator)

	databaseCursor.execute("""
                 INSERT INTO users (username, password) VALUES
                     (?, ?)
                 """, (username, password))
	database.commit()

	clear()
	return mainInterface, (databaseCursor.lastrowid,)

def videoPlayer():

    print("Video is now playing\n\n")

    input("Press ENTER to continue.\n")
    clear()

    return applicationEntry, None


testimonials = ["""InCollege helped me develop the skills I needed to land a job!
                \t-Ron Willson""",
                """My normal resume wasn't getting noticed by employers. InCollege allowed my to market my skills and begin my carrer.
                \t-Henry Close""",
                """This program made finding an internship really easy.
                \t-Taylor Oak"""]

def applicationEntry():

  print(random.choice(testimonials))
  print()

  prompt = "Please select an option below:\n"\
           "\t1. Log in to an existing account\n"\
           "\t2. Create a new account\n"\
           "\t3. Why you should join InCollege\n"\
           "Selection: "
  sel = int(gatherInput(prompt, "Invalid input. Please try again.\n",
                    menuValidatorBuilder('123')))

  if sel == 1:
    clear()
    return login, None
  elif sel == 2:
    clear()
    return newAcct, None
  elif sel == 3:
    clear()
    return videoPlayer, None




def listSkills(asId):
  prompt = "Please select a skill below:\n"\
          "\t1. Setup a database\n"\
          "\t2. Setup access roles\n"\
          "\t3. Use a microservice from the marketplace\n"\
          "\t4. Create budget alerts\n"\
          "\t5. Calculate OPEX costs\n"\
          "\t6. Go Back\n"\
          "Selection: "
  sel = gatherInput(prompt, "Invalid input. Please try again.\n",
                  menuValidatorBuilder('123456'))
  if sel == '6':
    clear()
    return mainInterface, (asId,)
  clear()
  return underConstruction, (asId, listSkills)


def underConstruction(asId, prevState):
  print("Under construction.\n")
  input("Press ENTER to continue.\n")
  clear()
  return prevState, (asId, )
    




def stateLoop(state):
    data = None
    while (state is not exitState):
        if data is None:
            state, data = state()
        else:
            state, data = state(*data)

#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------

if (__name__ == "__main__"):
	print("Welcome to InCollege!\n")
	
	stateLoop(applicationEntry)
