from commons import *
from manageDB import *



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

