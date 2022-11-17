from inCollege.states import stateLoop, applicationEntry
from inCollege.api import *

if (__name__ == "__main__"):
  print("Welcome to InCollege!\n")
  
  studentAccountsAPI()
  profilesAPI()
  usersAPI()

  stateLoop(applicationEntry)