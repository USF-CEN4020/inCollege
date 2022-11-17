from os.path import exists
import os.path


# studentAccounts.txt api

# If a file named "studentAccounts.txt" exists, then it will be opened. 
# In this file the information needed to create new student accounts will be contained. 
# This information will consist of a user name, first name and last name on one line, and a password on the next line. 
# If the maximum number of student accounts, 10 is reached, then no more student accounts will be created. 
# Each student account information will be separated by a line with "=====".
def studentAccountsAPI(username, firstname, lastname, password):
    absPath = os.path.abspath(os.path.dirname(__file__))
    textPath = os.path.join(absPath, "api", "studentAccounts.txt")
    fileExists = exists(textPath)

    if fileExists:
        with open(textPath, 'a') as f:
            f.write("%s, %s, %s\n%s\n=====\n" % (username, firstname, lastname, password))
    else:
        with open(textPath, 'w') as f:
            f.write("%s,%s,%s\n%s\n=====\n" % (username, firstname, lastname, password))



# MyCollege_profiles.txt api

# A file called MyCollege_profiles.txt" will be created. 
# For each of the profiles in the InCollege system, the following information will be placed in the file: 
# title, major, university name, about, experience, education.
# When a new user joins the system, their profile information will be added to this file. 
# Each user's profile information will be separated by a line with "=====".
def profilesAPI():
    pass


# MyCollege_users.txt api

# A file called "MyCollege_users.txt" will be created that contains the username of all of the user accounts that have been created in the MyCollege system. 
# After each user name, a "standard" or "plus" will be included depending on the type of the account. 
# If a new user account is created, then the user account will be added to the list.
def usersAPI():
    pass