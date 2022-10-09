import pytest
import sys
import builtins
from unittest import mock
import sqlite3
from inCollege.main import *

# ==================================================================================
# ==================================================================================
      
      
      
      
      
# EPIC #3 Test Cases
      




# ==================================================================================
# ==================================================================================


# Test whether Browse InCollege, Business Solution, and Directories return the 
# underConstruction to be displayed

@pytest.mark.parametrize('select',
                        [('2'), ('3'), ('4')]
)
def test_usefulLinks(select):
  state = underConstruction
  with mock.patch.object(builtins, 'input', lambda _: select):
    output, dataOut = usefulLinks(-1)
    assert output == state
    
    


# Tests the General state links

@pytest.mark.parametrize('select, result',
                        [('1', None), 
                         ('2', "\n\nWe're here to help\n\n\n"),
                         ('3', "\n\nIn College: Welcome to In College, the world's largest college student network with many users in many countries and territories worldwide\n\n\n"), 
                         ('4', "\n\nIn College Pressroom: Stay on top of the latest news, updates, and reports\n\n\n"),
                         ('5', "\n\nUnder construction.\n\n"),
                         ('6', "\n\nUnder construction.\n\n"),
                         ('7', "\n\nUnder construction.\n\n")
                         ]
)
def test_generalLinks(capfd, select, result):
  
  state = newAcct
  if select == '1':
    with mock.patch.object(builtins, 'input', lambda _: select):
        output, dataOut = generalLinks(-1)
        assert output == state
  else:
    with mock.patch.object(builtins, 'input', lambda _: select):
        output, dataOut = generalLinks(-1)
        out, err = capfd.readouterr()
        assert out == result
        
        
# Testing Important Links besides Guest Controls and Languages

@pytest.mark.parametrize('select, result',
                        [('1', copyRightNotice),
                         ('2', about), 
                         ('3', accessbility),
                         ('4', userAgreement),
                         ('5', privacyPolicy), 
                         ('6', cookiePolicy),
                         ('7', copyRightPolicy),
                         ('8', brandPolicy)
                         ]
)
def test_importantLinks(select, result):
  state = result
  with mock.patch.object(builtins, 'input', lambda _: select):
    output, dataOut = importantLinks(-1)
    assert output == state