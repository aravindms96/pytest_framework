import pytest
import os
import sys
import time
from utils.sessionCache import SessionCache
from utils.Bootstrapper import Bootstrapper
import pytest_html

global testCount
testCount = 0 

def pytest_load_initial_conftests(args):
    global BOOTSTRAP
    BOOTSTRAP = Bootstrapper()

def pytest_configure(config):
    # register an additional marker
    config.addinivalue_line(
        "markers", "app(name): mark application type used for this test"
    )   
    if not os.path.exists('Reports'):
        os.makedirs('Reports')
    config.option.htmlpath = 'Reports/TestReport_' + time.strftime("%d%m%Y_%H%M%S") + ".html"
    config.option.self_contained_html = True    


def pytest_sessionstart(session):
    global BOOTSTRAP
    collect_only = session.config.getoption("--collect-only")
    if not collect_only:
        BOOTSTRAP = Bootstrapper()
        # BOOTSTRAP.testCache.config_service.set('framework',session.config.getoption("--framework"))
        # BOOTSTRAP.testCache.config_service.set('bootstrapscope',session.config.getoption("--bootstrapscope"))
        # BOOTSTRAP.testCache.config_service.set('loglevel',session.config.getoption("--loglevel"))
        # BOOTSTRAP.testCache.config_service.set('testdatapath',session.config.getoption("--testdatapath"))
        BOOTSTRAP.InitServices()
        # BOOTSTRAP.testCache.logger_service.logger.debug("test print")
        # if session.config.getoption("--projectid"): BOOTSTRAP.testCache.logger_service.logger.debug(session.config.getoption("--projectid"))
        BOOTSTRAP.testCache.logger_service.logger.debug("pytest_sessionstart hook ended")

def determine_scope(fixture_name,config):  
    global BOOTSTRAP
    bootstrapscope = "session"
    collect_only = config.getoption("--collect-only")
    if not collect_only:
        bootstrapscope = BOOTSTRAP.testCache.config_service.get("bootstrapscope")
    return bootstrapscope

@pytest.fixture(scope=determine_scope,autouse=False)
def bootstrap(request):    
    global BOOTSTRAP
    current_scope = BOOTSTRAP.testCache.config_service.get("bootstrapscope")
    BOOTSTRAP.testCache.logger_service.logger.debug(current_scope +" bootstrap start")         
    yield BOOTSTRAP
    BOOTSTRAP.DriverCleanup()
    BOOTSTRAP.testCache.logger_service.logger.debug(current_scope +" bootstrap end")

def _get_test_case(request):
    global BOOTSTRAP
    fnName = request.node.name
    currentTc = fnName
    BOOTSTRAP.testCache.logger_service.logger.debug(currentTc) 
    return currentTc

@pytest.fixture(scope="function",autouse=True)
def function_initialize(request):
    global BOOTSTRAP
    BOOTSTRAP.testCache.logger_service.logger.debug("function initialize")
    testCase = _get_test_case(request)
    if testCase is None:
        BOOTSTRAP.testCache.logger_service.logger.warning("Skipping test as it is not available in mapper file")
        pytest.skip("Skipping test as it is not available in mapper file")
    else:
        BOOTSTRAP.testCache.logger_service.logger.info("Initiating test case - "+testCase)
        appname = "Default"
        mark = request.node.get_closest_marker('app')   
        if BOOTSTRAP is not None and testCase is not None:
            BOOTSTRAP.SwitchTestCase(testCase)        
            if mark is not None:
                appname = mark.args[0]            
            BOOTSTRAP.DriverInitialize(appname)
            global testCount
            testCount = testCount + 1
            BOOTSTRAP.testCache.logger_service.logger.info(f"{testCount} count in initialize")
    yield
    if BOOTSTRAP.testCache.config_service.get("customDriverClean"):
        killCount = BOOTSTRAP.testCache.config_service.get("driverKillCount")
        if (testCount%killCount)==0:
            BOOTSTRAP.testCache.logger_service.logger.info("Initiating yield")  
            BOOTSTRAP.testCache.logger_service.logger.info(testCount)  
            BOOTSTRAP.DriverCleanup()

def pytest_sessionfinish(session, exitstatus):
    global BOOTSTRAP
    collect_only = session.config.getoption("--collect-only")
    if not collect_only:
        BOOTSTRAP.testCache.logger_service.logger.debug("pytest_sessionfinish hook")
        BOOTSTRAP.SessionCleanup()