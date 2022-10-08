from pickle import NONE
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
														password TEXT,
                            firstname TEXT,
                            lastname TEXT)''')
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


#firstnameById = fieldById("firstname") # A function f(x) = (username of a user with id x)
#lastnameById = fieldById("lastname") # A function f(x) = (username of a user with id x)



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


def checkExistingNames(firstname, lastname):
  '''
  Looks up a name from firstname and lastname

  param firstname:
  param lastname:
  return the id of the specified user or -1 if the user does not exist

  '''

  databaseCursor.execute("SELECT * FROM users WHERE firstname= ? and lastname= ?",(firstname, lastname))
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
          "\t4. InCollege navigation links\n"\
          "\t5. log Out\n"\
          "Selection: "
  sel = int(
        gatherInput(prompt, "Invalid input. Please try again.\n",
                    menuValidatorBuilder('1234')))

  if sel == 1:
    clear()
    return jobInterface, (asId,)
  elif sel == 2:
    clear()
    return findPpl, (asId,)
  elif sel == 3:
    clear()
    return listSkills, (asId,)
  elif sel == 4:
    clear()
    return inCollegeGroups, (asId,)
  else:
    clear()
    return applicationEntry, None

def login():
  if dbEmpty():
    print("\n\nNo existing accounts. Please create a new account.\n")
    return applicationEntry, None
  else:
    username = input("Username: ")
    password = input("Password: ")
  
    id = checkExistingAccts(username, password)
    if (id != -1):
      clear()
      print("\n\nYou have successfully logged in\n")
      return mainInterface, (id,)
    else:
      clear()
      print("\n\nIncorrect username/password. Please try again.\n")
      return applicationEntry, None


def newAcct():
    '''
    Creates a new account based on user input. Ensures there is room in the database and username and passwords are valid.

    :sideeffect Adds a new user to the users table in the database
    :return mainInterface state function
    '''
    if dbFull():
      print("\n\nAll permitted accounts have been created, please come back later.\n")
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

    firstname = gatherInput("\nEnter your first name:\n", "", vacuouslyTrue)

    lastname = gatherInput("\nEnter your last name: \n", "", vacuouslyTrue)


    databaseCursor.execute("""
                  INSERT INTO users (username, password, firstname, lastname) VALUES
                      (?, ?, ?, ?)
                  """, (username, password, firstname, lastname))
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
           "\t4. Find someone you know\n"\
           "\t5. InCollege navigation links\n"\
           "Selection: "
  sel = int(gatherInput(prompt, "Invalid input. Please try again.\n",
                    menuValidatorBuilder('123456')))

  if sel == 1:
    clear()
    return login, None
  elif sel == 2:
    clear()
    return newAcct, None
  elif sel == 3:
    clear()
    return videoPlayer, None
  elif sel == 4:
    clear()
    return findPpl, (-1,)
  elif sel == 5:
    clear()
    return inCollegeGroups, (-1,)




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




def findPpl(asId):
      findFirstname = gatherInput("Enter first name: ", "", vacuouslyTrue)
      findLastname = gatherInput("Enter last name: ", "", vacuouslyTrue)


      findId = checkExistingNames(findFirstname, findLastname)
      if (findId != -1):
        clear()
        print("\n\nThey are a part of the InCollege system\n")
        
      else:
        clear()
        print("\n\nThey are not yet a part of the InCollege system yet. Please try again.\n")
      
      if asId == -1:
        return applicationEntry, None
      else: 
        return mainInterface, (asId,)



def inCollegeGroups(asId):
    prompt = "Please select an Incollege Group:\n"\
             "\t1. Useful Links\n"\
             "\t2. Incollege Important Links\n"\
            "Selection: "
    sel = int(gatherInput(prompt, "Invalid Input. Please try again.\n", menuValidatorBuilder('12')))

    if sel == 1:
        clear()

        return usefulLinks, (asId,)

    elif sel == 2:
        clear()

        return importantLinks, (asId,)

    if asId == -1:
        return applicationEntry, None
    else: 
        return mainInterface, (asId,)



def usefulLinks(asId):
    prompt = "Please select an option: \n"\
             "\t1. General \n"\
             "\t2. Browser Incollege\n"\
             "\t3. Business Solutions\n"\
             "\t4. Directories\n"\
             "\t5. Go Back\n"\
            "Selection: "
    sel = int(gatherInput(prompt, "Invalid Input. Please try again.\n", menuValidatorBuilder('12345')))

    if sel == 1:
        clear()
        return generalLinks, (asId,)

    elif sel == 2:
        clear()

        return underConstruction(asId, usefulLinks)

    elif sel == 3:
        clear()
        
        return underConstruction(asId, usefulLinks)

    elif sel == 4:
        clear()
        
        return underConstruction(asId, usefulLinks) 
    elif sel == 5:
        clear()

        return inCollegeGroups, (asId,)



def importantLinks(asId):
      prompt = "Please select a option below:\n"\
              "\t1. A Copyright Notice\n"\
              "\t2. About\n"\
              "\t3. Accessibility\n"\
              "\t4. User Agreement\n"\
              "\t5. Privacy Policy\n"\
              "\t6. Cookie Policy\n"\
              "\t7. Copyright Policy\n"\
              "\t8. Brand Policy\n"\
              "\t9. Languages\n"\
              "\t10. Go Back\n"\
              "Selection: "
      sel = int(gatherInput(prompt, "Invalid input. Please try again.\n", menuValidatorBuilder(('1','2','3','4','5','6','7','8','9','10'))))

      if sel == 1:
            clear()
            return copyRightNotice, (asId,)
      
      elif sel == 2:
            clear()
            return about, (asId,)

      elif sel == 3:
            clear()
            return accessbility, (asId,)

      elif sel == 4:
            clear()
            return userAgreement, (asId,)

      elif sel == 5:
            clear()
            return privacyPolicy, (asId,)
      
      elif sel == 6:
            clear()
            return cookiePolicy, (asId,)

      elif sel == 7:
            clear()
            return copyRightPolicy, (asId,)
        
      elif sel == 8:
            clear()
            return brandPolicy, (asId,)
      
      elif sel == 9:
            clear()
            return languages, (asId,)
      
      elif sel == 10:
            clear()
            return inCollegeGroups, (asId,)



def copyRightNotice(asId):
      print("\n\nCopyright © 2022, InColeege, All rights reserved.\n\n\n")
      return importantLinks, (asId,)



def about(asId):
     print("\n\nWelcome to InCollege, the best professional network for college students\n\n\n")
     return importantLinks, (asId,)



def accessbility(asId):
      print("\n\nHere at InCollege we commit to do everything we can to ensure that\n" + 
            "the products and services we deliver are accessible to everyone\n\n\n")
      return importantLinks, (asId,)
    


def userAgreement(asId):
      print("\n\nWhen you use our Services you agree to all of these terms. Your use of\n" + 
            "our Services is also subject to our Cookie Policy and our Privacy Policy,\n" + 
            "which covers how we collect, use, share, and store your personal information.\n\n\n")
      return importantLinks, (asId,)



def privacyPolicy(asId):
      print("\n\nThis Privacy Policy describes Our policies and procedures on the collection,\n" +
            "use and disclosure of Your information when You use the Service and tells You\n" +
            "about Your privacy rights and how the law protects You.\n\n\n")

      prompt = "Please select an option: \n"\
              "\t1. Guest Control\n"\
              "\t2. Go Back\n"\
              "selection: "
      sel = int(gatherInput(prompt, "Invalid Input. Please try again.\n", menuValidatorBuilder('12'))) 

      if sel == 1:
            clear()
            return guestControls, (asId,)

      elif sel == 2:
            return importantLinks, (asId,)



def guestControls(asId):
      #if asId == -1:
      #      print("\n\tYou are not signed in\n\n")
      #      return privacyPolicy, (asId,)
      #else: 
            prompt = "You can turn off Email, SMS, aand Advertising here: \n"\
                    "\t1. Email\n"\
                    "\t2. SMS\n"\
                    "\t3. Targeted Advertising\n"\
                    "\t4. Go Back\n"\
                    "Selection: "
            sel = int(gatherInput(prompt, "Invalid Input. Please try again.\n", menuValidatorBuilder('1234')))

            if sel == 1:
                  clear()
                  return email, (asId,)
            
            elif sel == 2:
                  clear()
                  return sms, (asId,)

            elif sel == 3:
                  clear()
                  return targetedAdvertising, (asId,)
            
            elif sel == 4:
                  return privacyPolicy, (asId,)



def email(asId):
      prompt = "Please select an option: \n"\
             "\t1. Turn on Email \n"\
             "\t2. Turn of Email \n"\
             "\t3. Go Back\n"\
             "Selection: "
      sel = int(gatherInput(prompt, "Invalid Input. Please try again.\n", menuValidatorBuilder('123')))

      if sel == 1:
            clear()
            print("\n\nEamil turned on\n")
            return guestControls, (asId,)
      elif sel == 2:
            clear()
            print("\n\nEmail turned off\n")
            return guestControls, (asId,)
      elif sel == 3:
            clear()
          
            return guestControls, (asId,)      



def sms(asId):
      prompt = "Please select an option: \n"\
             "\t1. Turn on SMS \n"\
             "\t2. Turn of SMS \n"\
             "\t3. Go Back\n"\
             "Selection: "
      sel = int(gatherInput(prompt, "Invalid Input. Please try again.\n", menuValidatorBuilder('123')))

      if sel == 1:
            clear()
            print("\n\nSMS turned on\n")
            return guestControls, (asId,)
      elif sel == 2:
            clear()
            print("\n\nSMS turned off\n")
            return guestControls, (asId,)
      elif sel == 3:
            clear()
          
            return guestControls, (asId,)   



def targetedAdvertising(asId):
      prompt = "Please select an option: \n"\
             "\t1. Turn on Targeted Advertising \n"\
             "\t2. Turn of Targeted Advertising \n"\
             "\t3. Go Back\n"\
             "Selection: "
      sel = int(gatherInput(prompt, "Invalid Input. Please try again.\n", menuValidatorBuilder('123')))

      if sel == 1:
            clear()
            print("\n\nAdvertising turned on\n")
            return guestControls, (asId,)
      elif sel == 2:
            clear()
            print("\n\nAdvertising turned off\n")
            return guestControls, (asId,)
      elif sel == 3:
            clear()
          
            return guestControls, (asId,)   



def cookiePolicy(asId):
      print("\n\nThis Cookies Policy explains what Cookies are and how We use them.\n"+ 
            "You should read this policy so You can understand what type of cookies\n" + 
            "We use, or the information We collect using Cookies and how that information is used.\n\n\n")
      return importantLinks, (asId,)



def copyRightPolicy(asId):
      print("\n\nCopyright Policy. You may not post, distribute, or reproduce in any way any\n" +
            "copyrighted material, trademarks, or other proprietary information without \n" +
            "obtaining the prior written consent of the owner of such proprietary rights.\n" +
            "If you believe that your work has been copied and posted on the Websites in\n" +
            "a way that constitutes copyright infringement, please provide us with the \n" +
            "following information: \n\n\n")
      return importantLinks, (asId,)



def brandPolicy(asId):
      print("\n\nOur trademarks and other brand features are protected by law.\n" +  
            "You wll need our permission in order to use them.\n" +
            "For permission requests, please contact TrademarkRequest@InCollege.com\n\n\n")
      return importantLinks, (asId,)



def languages(asId):
      #if asId == -1:
      #      print("\tYou are not signed in\n\n")
      #      return privacyPolicy, (asId,)
      #else:
            prompt = "Please select a language: \n"\
                    "\t1. English\n"\
                    "\t2. Spanish\n"\
                    "\t3. Go Back\n"\
                    "Selection: "
            sel = int(gatherInput(prompt, "Invalid Input. Please try again.\n", menuValidatorBuilder('123')))      

            if sel == 1:
              clear()
              print("\n\nLanguage now is English\n\n")
              return importantLinks, (asId,)
            
            elif sel == 2:
                  clear()
                  print("\n\nLanguage now is Spanish\n\n")
                  return importantLinks, (asId,)
            
            elif sel == 3:
                  clear()
                  return importantLinks, (asId,)


        
def generalLinks(asId):
    prompt = "Please select an option: \n"\
             "\t1. Sign Up \n"\
             "\t2. Help Center\n"\
             "\t3. About\n"\
             "\t4. Press\n"\
             "\t5. Blog\n"\
             "\t6. Careers\n"\
             "\t7. Developers\n"\
             "\t8. Go Back \n"\
            "Selection: "
    sel = int(gatherInput(prompt, "Invalid Input. Please try again.\n", menuValidatorBuilder('12345678')))

    if sel == 1:
       clear()
       return newAcct, None

    elif sel == 2:
       clear()

       print("\n\nWe're here to help\n\n")
       return generalLinks, (asId,)

    elif sel == 3:
        clear()

        print("\n\nIn College: Welcome to In College, the world's largest college student network with many users in many countries and territories worldwide\n\n")
        return generalLinks, (asId,)
 
    elif sel == 4:
        clear()

        print("\n\nIn College Pressroom: Stay on top of the latest news, updates, and reports\n\n")
        return generalLinks, (asId,)

    elif sel == 5:
        clear()
        
        return underConstruction(asId, generalLinks)

    elif sel == 6:
        clear()
        
        return underConstruction(asId, generalLinks)

    elif sel == 7:
        clear()

        return underConstruction(asId, generalLinks)

    elif sel == 8:
        clear()

        return usefulLinks, (asId,)






      

def underConstruction(asId, prevState):
      print("\n\nUnder construction.\n")
      input("\nPress ENTER to continue.\n")
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
