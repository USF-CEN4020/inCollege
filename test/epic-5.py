import pytest
import builtins
from unittest import mock
from inCollege.manageDB import *
from inCollege.states import *
from inCollege.commons import *
from inCollege.testFunc import *



# ==================================================================================
# ==================================================================================
      
      
      
      
      
# EPIC #5 Test Cases
      




# ==================================================================================
# ==================================================================================

#Story:As a student, I want to be able to create a profile
#      so that other students can learn about me.
#A profile should contain fields:
#       Title (1 line)
#       Major (title case)
#       University (title case)
#       About me (paragraph)


@pytest.mark.profiles
@pytest.mark.parametrize('choice, title, major, university, aboutme, result',
                        [
                          (1, 'test1', 'cs', 'USF', 'student', 0),
                          (2, 'test2', 'ee', 'USF', 'student', 0),
                          (3, 'test3', 'cs', 'USF', 'student', 0),
                          (4, 'test4', 'ee', 'USF', 'student', 0)
                        ]
                        )



def test_profileCreation(choice, title, major, university, aboutme, result):
    clearProfiles()

    inputs = iter(['1', ' ', title, ' ', '2', ' ', major, ' ', '3', ' ', university, ' ', '4', ' ', aboutme, ' ']
    )
    with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
        
        updateProfileSimple(1, choice)
        assert profilesCount() == result



# Story: View my own profile



@pytest.mark.profiles
@pytest.mark.parametrize('select',
                        [('6')]
)

def test_viewMyProfile(select):
    state = myProfile
    with mock.patch.object(builtins, 'input', lambda _: select):
        output, dataOut = mainInterface(-1)
        assert output == state



# Story: Convert text to title case.



@pytest.mark.profiles

def test_convertTitle(testTitleCase):
    assert testTitleCase == True
