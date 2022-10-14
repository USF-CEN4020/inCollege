from main import *
from manageDB import *


# initial state
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


# main state
def mainInterface(asId):
  prompt = "Please select an option below:\n"\
          "\t1. Search for a job\n"\
          "\t2. Find your network\n"\
          "\t3. Show my network\n"\
          "\t4. Learn a new skill\n"\
          "\t5. InCollege navigation links\n"\
          "\t6. log Out\n"\
          "Selection: "
  sel = int(
          gatherInput(prompt, "Invalid input. Please try again.\n",
                      menuValidatorBuilder('123456')))

  if sel == 1:
      clear()
      return jobInterface, (asId,)

  elif sel == 2:
      clear()
      return findFriendsbyType, (asId,)

  elif sel == 3:
      clear()
      return friendsList, (asId,)

  elif sel == 4:
      clear()
      return listSkills, (asId,)

  elif sel == 5:
      clear()
      return inCollegeGroups, (asId,)

  elif sel == 6:
      clear()
      return applicationEntry, None


# login
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
      return pendingRequest, (id,)

    else:
      clear()
      print("\n\nIncorrect username/password. Please try again.\n")
      return applicationEntry, None


# create a new account
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
  university = gatherInput("\nEnter your university (if no, enter NONE): \n", "", vacuouslyTrue)
  major = gatherInput("\nEnter your major (if no, enter NONE): \n", "", vacuouslyTrue)

  databaseCursor.execute("""
                INSERT INTO users (username, password, firstname, lastname, university, major) VALUES
                    (?, ?, ?, ?, ?, ?)
                """, (username, password, firstname, lastname, university, major))
  database.commit()

  clear()
  return mainInterface, (databaseCursor.lastrowid,)


# job
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


# learn skills
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


# ads video
def videoPlayer():
  print("Video is now playing\n\n")
  enterToContinue()
  return applicationEntry, None


# find InCollege existing user
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


# friends network
def pendingRequest(asId):
  pendingRequest = checkExistingPendingRequest(asId)
  
  if pendingRequest == -1:
    return mainInterface, (asId,)

  else: 
    usernameList = []
    for row in pendingRequest:
      requesterId = row[1]
      requesterUsername = usernameLookup(requesterId)
      usernameList.append(requesterUsername)
      print("\nYou have a pending request from <", requesterUsername, ">.\n")

    print("Would you like to be connected with them?\n")
    acceptedUsername = gatherInput("Please enter the username to accept the request: ", "", vacuouslyTrue)

    for username in usernameList:
      if acceptedUsername == username:
        databaseCursor.execute('''UPDATE friendships 
                                    SET
                                      acceptRequest= 1
                                    WHERE
                                      receiverId= ?''', (asId,)) 
        database.commit()
        
    usernameList.remove(acceptedUsername)

    return acceptRequestDone, (asId, acceptedUsername, usernameList)


def acceptRequestDone(asId, acceptedUsername, usernameList):
  print("\nYou have accepted the request from <", acceptedUsername, "> successfully.")

  if usernameList:
    addMore = gatherInput("Would you like to accept more requests? (yes / no) ",
                      "Please enter either \"yes\" or \"no\".",
                      binaryOptionValidatorBuilder("yes", "no"))
    if addMore == 'yes':
      clear()
      return pendingRequest, (asId,)
  else:
    enterToContinue()
    return mainInterface, (asId,)
    

def findFriendsbyType(asId):
  prompt = "Search by below options:\n"\
        "\t1. Last name\n"\
        "\t2. University\n"\
        "\t3. Major\n"\
        "\t4. Go Back\n"\
        "Selection: "
  sel = gatherInput(prompt, "Invalid input. Please try again.\n",
                menuValidatorBuilder('1234'))

  if sel == '1':
    clear()
    return findFriends, (asId, sel)

  elif sel == '2':
    clear()
    return findFriends, (asId, sel)

  elif sel == '3':
    clear()
    return findFriends, (asId, sel)

  elif sel == '4': 
    clear()
    return mainInterface, (asId,)


def findFriends(asId, sel):
  rows = ()

  if sel == '1':
    findLastname = gatherInput("Enter last name: ", "", vacuouslyTrue)
    findLastname.lower()
    print("\n")
    lastnameCursor =  databaseCursor.execute("SELECT * FROM users WHERE lastname IS ?", (findLastname,))
    lastnameRows = lastnameCursor.fetchall()
    rows = lastnameRows

  elif sel == '2':
    findUniversity = gatherInput("Enter the University: ", "", vacuouslyTrue)
    findUniversity.lower()
    print("\n")
    universityCursor =  databaseCursor.execute("SELECT * FROM users WHERE university IS ?", (findUniversity,))
    universityRows = universityCursor.fetchall()
    rows = universityRows

  elif sel == '3':
    findMajor = gatherInput("Enter the major: ", "", vacuouslyTrue)
    findMajor.lower()
    print("\n")
    majorCursor = databaseCursor.execute("SELECT * FROM users WHERE major IS ?", (findMajor,))
    majorRows = majorCursor.fetchall()
    rows = majorRows

  if not rows:
    print("No such data in inCollege. Please find other options.\n")
    enterToGoBack()
    return findFriendsbyType, (asId,)

  count = 0
  currentUsername = ""
  selectedFriendId = 0

  for row in rows:
    if row[0] == asId:
      currentUsername = row[1]

    else:
      selectedFriendId = row[0]
      count += 1
      print(count)
      print("Username  : ", row[1])
      print("Firstname : ", row[3])
      print("Lastname  : ", row[4])
      print("University: ", row[5])
      print("Major     : ", row[6])
      print("\n")

  selectedUsername = gatherInput("Enter the username of friend you would like to connect with (or enter 0 to go back): ", "", vacuouslyTrue)

  if selectedUsername == '0':
    clear()
    return findFriendsbyType, (asId,)

  elif selectedUsername == currentUsername:
    print("You are not allowed to add your account to the network list.\n\n\n")
    enterToContinue()
    return findFriendsbyType, (asId,)

  else:
    clear()
    return requestFriends, (asId, selectedUsername, selectedFriendId)
    

def requestFriends(asId, selectedUsername, selectedFriendId):
  # check the entered username exists
  exist = checkExistingUsername(selectedUsername)

  if exist == -1:
    print("Username not found. Please enter the correct username in the list.\n\n\n")
    enterToGoBack()
    return findFriendsbyType, (asId,)

  # check the selected friend is already under a network list
  isAccepted = checkExistingFriend(asId, selectedFriendId)
  if isAccepted == -1:
    isAccepted = checkExistingFriend(selectedFriendId, asId) 

  if isAccepted == 0: # pending
    print("You have a pending request to <", selectedUsername, ">.\n")
    print("Please wait for <", selectedUsername, "> to accept your request and choose other friends.\n\n\n")
    enterToGoBack()
    return findFriendsbyType, (asId,)

  elif isAccepted == 1: # already a friend
    print("You already have <", selectedUsername, "> in your network list.\n\n\n")
    print("Please choose other friends.")
    enterToGoBack()
    return findFriendsbyType, (asId,)

  elif isAccepted == -1: # not added to the network list
    databaseCursor.execute("INSERT INTO friendships (acceptRequest, senderId, receiverId) VALUES (?, ?, ?)", (0, asId, selectedFriendId))
    database.commit() 

    print("Your network request to <", selectedUsername, "> has been sent succesfully.\n")
    print("<", selectedUsername, "> will be added to your network list as soon as they accept your request.\n\n\n")
    enterToContinue()
    return findFriendsbyType, (asId,)


def friendsList(asId):
  print("Your Network List: \n")

  friendsCursor =  databaseCursor.execute("SELECT * FROM friendships WHERE (acceptRequest = 1 AND senderId = ?) OR (acceptRequest = 1 AND receiverId = ?)", (asId, asId))
  friendsRows = friendsCursor.fetchall()

  friendsList = []

  for row in friendsRows:
    if row[1] != asId and row[2] != asId and row not in friendsList:
      friendsList.append(row)

  if not friendsList:
    print("NONE\n\n\n")
    enterToContinue()
    return mainInterface, (asId,)
  
  else:
    count = 0
    for friendKey in friendsList:
      friendsListCursor =  databaseCursor.execute("SELECT * FROM users WHERE id = ?", (friendKey,))
      friendsListRows = friendsListCursor.fetchall()
      count += 1
      print(count)
      print("Username  : ", row[1])
      print("Firstname : ", row[3])
      print("Lastname  : ", row[4])
      print("University: ", row[5])
      print("Major     : ", row[6])
      print("\n")

  print("\n")
  enterToContinue()
  return mainInterface, (asId,)


# InCollege navigation links
def inCollegeGroups(asId):
  prompt = "Please select an Incollege Group:\n"\
            "\t1. Useful Links\n"\
            "\t2. Incollege Important Links\n"\
            "\t3. Go Back\n"\
          "Selection: "
  sel = int(gatherInput(prompt, "Invalid Input. Please try again.\n", menuValidatorBuilder('123')))

  if sel == 1:
    clear()
    return usefulLinks, (asId,)

  elif sel == 2:
    clear()
    return importantLinks, (asId,)
  else:
    clear()
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

  elif sel == 2 or sel == 3 or sel == 4:
    clear()
    return underConstruction, (asId, usefulLinks)
  
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
  enterToContinue()
  return importantLinks, (asId,)


def about(asId):
  print("\n\nWelcome to InCollege, the best professional network for college students\n\n\n")
  enterToContinue()
  return importantLinks, (asId,)


def accessbility(asId):
  print("\n\nHere at InCollege we commit to do everything we can to ensure that\n" + 
        "the products and services we deliver are accessible to everyone\n\n\n")
  enterToContinue()
  return importantLinks, (asId,)
    

def userAgreement(asId):
  print("\n\nWhen you use our Services you agree to all of these terms. Your use of\n" + 
        "our Services is also subject to our Cookie Policy and our Privacy Policy,\n" + 
        "which covers how we collect, use, share, and store your personal information.\n\n\n")
  enterToContinue()
  return importantLinks, (asId,)


def privacyPolicy(asId):
  print("\n\nThis Privacy Policy describes Our policies and procedures on the collection,\n" +
        "use and disclosure of Your information when You use the Service and tells You\n" +
        "about Your privacy rights and how the law protects You.\n\n\n")

  if (asId == -1):
    return importantLinks, (asId,)

  controls = checkUserGuestControls(asId)

  print("Your current privacy settings:")
  
  if (controls[0] == 1):
    print("\tInCollege Emails: ENABLED")
  else:
    print("\tInCollege Emails: DISABLED")

  if (controls[1] == 1):
    print("\tInCollege SMS: ENABLED")
  else:
    print("\tInCollege SMS: DISABLED")

  if (controls[2] == 1):
    print("\tTargeted Emails : ENABLED")
  else:
    print("\tTargeted Emails : DISABLED")

  print()

  prompt = "Please select an option: \n"\
          "\t1. Edit Guest Controls\n"\
          "\t2. Go Back\n"\
          "selection: "
  sel = int(gatherInput(prompt, "Invalid Input. Please try again.\n", menuValidatorBuilder('12'))) 

  if sel == 1:
    clear()
    return guestControls, (asId,)

  elif sel == 2:
    clear()
    return importantLinks, (asId,)


def guestControls(asId):
  email = gatherInput("Would you like to receive emails from InCollege? (yes / no) ",
                      "Please enter either \"yes\" or \"no\".",
                      binaryOptionValidatorBuilder("yes", "no"))

  sms = gatherInput("Would you like to receive text messages from InCollege? (yes / no) ",
                      "Please enter either \"yes\" or \"no\".",
                      binaryOptionValidatorBuilder("yes", "no"))

  targetedAds = gatherInput("Would you like personalized advertising from InCollege? (yes / no) ",
                      "Please enter either \"yes\" or \"no\".",
                      binaryOptionValidatorBuilder("yes", "no"))

  if (not acctSettingsInitilized(asId)):
    databaseCursor.execute("INSERT INTO userSettings (userId, receiveEmail, receiveSMS, targetedAds,language) VALUES (?, ?, ?, ?, ?)", (asId, isYes(email), isYes(sms), isYes(targetedAds), "english"))
    
  else:
    databaseCursor.execute('''UPDATE userSettings SET
                                                    receiveEmail = ?,
                                                    receiveSMS = ?,
                                                    targetedAds = ?
                                                  WHERE
                                                    userId = ?''', (isYes(email), isYes(sms), isYes(targetedAds), asId)) 

  database.commit()

  clear()
  return privacyPolicy, (asId,)

def cookiePolicy(asId):
  print("\n\nThis Cookies Policy explains what Cookies are and how We use them.\n"+ 
        "You should read this policy so You can understand what type of cookies\n" + 
        "We use, or the information We collect using Cookies and how that information is used.\n\n\n")
  enterToContinue()
  return importantLinks, (asId,)


def copyRightPolicy(asId):
  print("\n\nCopyright Policy. You may not post, distribute, or reproduce in any way any\n" +
        "copyrighted material, trademarks, or other proprietary information without \n" +
        "obtaining the prior written consent of the owner of such proprietary rights.\n" +
        "If you believe that your work has been copied and posted on the Websites in\n" +
        "a way that constitutes copyright infringement, please provide us with the \n" +
        "following information: \n\n\n")
  enterToContinue()
  return importantLinks, (asId,)


def brandPolicy(asId):
  print("\n\nOur trademarks and other brand features are protected by law.\n" +  
        "You wll need our permission in order to use them.\n" +
        "For permission requests, please contact TrademarkRequest@InCollege.com\n\n\n")
  enterToContinue()
  return importantLinks, (asId,)


def languages(asId):
  print("InCollege is available in ENGLISH and SPANISH.\n")

  if (asId == -1):
    return importantLinks, (asId,)

  currLanguage = checkUserLanguage(asId).upper()

  print("Your current language is: " + currLanguage)

  prompt = "Please select an option: \n"\
          "\t1. Change Language\n"\
          "\t2. Go Back\n"\
          "Selection: "
  sel = int(gatherInput(prompt, "Invalid Input. Please try again.\n", menuValidatorBuilder('12')))      

  if sel == 1:
    clear()
    return setLanguage, (asId,)
  
  elif sel == 2:
    clear()
    return importantLinks, (asId,)


def setLanguage(asId):
  lang = gatherInput("Please select a language. (English or Spanish) ",
                      "Only English and Spanish are available at this time.",
                      binaryOptionValidatorBuilder("english", "spanish")).lower()

  if (not acctSettingsInitilized(asId)):
    databaseCursor.execute("INSERT INTO userSettings (userId, receiveEmail, receiveSMS, targetedAds,language) VALUES (?, ?, ?, ?, ?)", (asId, 1, 1, 1, lang))
  else:
    databaseCursor.execute("UPDATE userSettings SET language = ? WHERE userId = ?", (lang, asId))
  
  database.commit()

  clear()
  return languages, (asId,)


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

  elif sel == 5 or sel == 6 or sel == 7:
    clear()
    
    return underConstruction(asId, generalLinks)

  elif sel == 8:
    clear()

    return usefulLinks, (asId,)



#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------



def underConstruction(asId, prevState):
  print("\n\nUnder construction.\n")
  enterToContinue()
  return prevState, (asId, )


def exitState(asId):
  clear()
  if (asId == -1):
    print("Goodbye")
  else:
    print("Goodbye,", usernameById(asId))
  exit()


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