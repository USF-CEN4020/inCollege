from os.path import exists
import os.path

from inCollege.manageDB import *


# INPUT: studentAccounts.txt api

# If a file named "studentAccounts.txt" exists, then it will be opened. 
# In this file the information needed to create new student accounts will be contained. 
# This information will consist of a user name, first name and last name on one line, and a password on the next line. 
# If the maximum number of student accounts, 10 is reached, then no more student accounts will be created. 
# Each student account information will be separated by a line with "=====".
def studentAccountsAPI():
    absPath = os.path.abspath(os.path.dirname(__file__))
    txtFilePath = os.path.join(absPath, "api", "studentAccounts.txt")
    fileExists = exists(txtFilePath)

    if fileExists: 
        with open(txtFilePath) as f:
            initFlag = 1

            lines = f.readlines()
            for line in lines:
                if dbFull():
                    print("INPUT API WARNING: All permitted accounts have been created")
                    break   
                
                # initialize data to the empty string
                if initFlag == 1:
                    username = ''
                    password = ''
                    firstname = ''
                    lastname = ''
                    university = ''
                    major = ''
                    membership = ''

                if line == "=====\n" or line == "=====":
                    if username == '' or password == '' or firstname == '' or lastname == '' or university == '' or major == '' or membership == '':
                        # all information from input txt file should have the value, if not the user is not created
                        initFlag = 0
                    else:
                        initAcct(username, password, firstname, lastname, university, major, membership)
                        initFlag = 1

                elif ' ' in line:
                    accountInfo = line.split()
                    if unique(accountInfo[0]): # check if username is unique
                        username = accountInfo[0]
                        firstname = accountInfo[1]
                        lastname = accountInfo[2]
                        university = accountInfo[3]
                        major = accountInfo[4]
                        membership = accountInfo[5]
                        initFlag = 0
                    else:
                        initFlag = 1
                        continue
                else:
                    if passwordValidator(line):
                        password = line
                        initFlag = 0
                    else: 
                        initFlag = 1
                        continue


# OUTPUT: MyCollege_profiles.txt api

# A file called MyCollege_profiles.txt" will be created. 
# For each of the profiles in the InCollege system, the following information will be placed in the file: 
# title, major, university name, about, experience, education.
# When a new user joins the system, their profile information will be added to this file. 
# Each user's profile information will be separated by a line with "=====".
def profilesAPI():
    absPath = os.path.abspath(os.path.dirname(__file__))
    txtFilePath = os.path.join(absPath, "api", "MyCollege_profiles.txt")

    f = open(txtFilePath, 'w')

    databaseCursor.execute("SELECT * FROM profiles")
    profiles = databaseCursor.fetchall()

    for profile in profiles:
        userId = profile[0]
        title = profile[1]
        major = profile[2]
        university = profile[3]
        about = profile[4]
        education = profile[5]

        databaseCursor.execute("SELECT * FROM workExperience WHERE userId = ?", (userId,))
        experiences = databaseCursor.fetchone()
        jobTitle = experiences[2]
        employer = experiences[3]
        startDate = experiences[4]
        endDate = experiences[5]
        location = experiences[6]
        description = experiences[7]

        f.write("%s\n%s\n%s\n%s\n%s %s %s %s %s %s\n%s\n=====\n" % (title, major, university, about, jobTitle, employer, startDate, endDate, location, description, education))

    f.close()

# OUTPUT: MyCollege_users.txt api

# A file called "MyCollege_users.txt" will be created 
# that contains the username of all of the user accounts that have been created in the MyCollege system. 
# After each username, a "standard" or "plus" will be included depending on the type of the account. 
# If a new user account is created, then the user account will be added to the list.
def usersAPI():
    absPath = os.path.abspath(os.path.dirname(__file__))
    txtFilePath = os.path.join(absPath, "api", "MyCollege_users.txt")
    
    f = open(txtFilePath, 'w')

    databaseCursor.execute("SELECT * FROM users")
    users = databaseCursor.fetchall()

    for user in users:
        username = user[1]
        membership = user[7]

        f.write("%s %s\n" % (username, membership))

    f.close()