import pytest
import sys
import builtins
from unittest import mock
import sqlite3

from inCollege.manageDB import *
from inCollege.testFunc import *
from inCollege.manageDB import *
from inCollege.states import mainInterface, jobInterface, jobViewQuery, jobDetails, applyForJob, jobPost


# ==================================================================================
# ==================================================================================
      
      
      
      
      
# EPIC #6 Test Cases
      




# ==================================================================================
# ==================================================================================

def initTestJobs():
	jobs = [
		('SWE', 'Software Engineer', 'Google', 'Tampa, FL', '100000.0', 1),
        ('DevOps', 'Dev Ops', 'Google', 'Tampa, FL', '100000.0', 1),
        ('Frontend', 'Frontend Engineer', 'Google', 'Tampa, FL', '100000.0', 1),
	]
	for job in jobs:
		inputs = iter(job)
		with mock.patch.object(builtins, 'input', lambda _: next(inputs)):
			jobPost()


# the maximum number of jobs is 10
@pytest.mark.jobCount
def test_jobCount():
    assert jobCount(0) == True 


# view Jobs and Internships option on the mainInterface
# Once the option is selected, show jobInteface state
@pytest.mark.jobStates
@pytest.mark.parametrize('select', [('1')])
def test_viewJobInteface(select):
    state = jobInterface
    with mock.patch.object(builtins, 'input', lambda _: select):
        output, dataOut = mainInterface(-1)
        assert output == state


# view a list of job that student have applied 
# and have not yet applied for
@pytest.mark.jobStates
@pytest.mark.parametrize('select', [('2')])
def test_viewAppliedJobs(select):
    state = queryAppliedJobs
    with mock.patch.object(builtins, 'input', lambda _: select):
        output, dataOut = jobViewQuery(-1)
        assert output == state

@pytest.mark.jobStates
@pytest.mark.parametrize('select', [('3')])
def test_viewNotAppliedJobs(select):
    state = queryNotAppliedJobs
    with mock.patch.object(builtins, 'input', lambda _: select):
        output, dataOut = jobViewQuery(-1)
        assert output == state


# entered information be stored and associates with job has been applied for 
# so that when List of jobs displayed, applied job will be indicated



# mark a job as "saved" when I am interested in a job 
# so that I can see a list of jobs I marked 
# and I also can unmark a job when I want.



# once applied for a job, they cannot apply it again.
