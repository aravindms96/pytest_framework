import sys,os 
import pytest               
# import importlib
from .sessionCache import SessionCache
from .loggerService import LoggerService
from .configService import ConfigService
from .dataService import DataService
from .driverService import DriverService
# from .databaseService import DatabaseService

class Bootstrapper(): 
    """Bootstrapper class use to control the setup and teardown activities.
    Initializes new instance of :class:`SessionCache` and all the services used by the framework.

    """
    def __init__(self):
        # self._testCaseId = None
        self.testCache = SessionCache()
        #Config service
        if self.testCache.config_service is None:            
            self.testCache.config_service = ConfigService()
        
        
        
    #Initialize all services for TestCache

    def InitServices(self):
        #Logger service
        try:
            if self.testCache.logger_service is None:            
                self.testCache.logger_service = LoggerService(self.testCache.config_service.get('loglevel'))
            self.testCache.logger_service.logger.info("Bootstrap Master Initialize...")
        except:
            logger_service = LoggerService("DEBUG")
            logger_service.logger.exception("Logger Service Initialize Failed:")
        
        # #Database service
        # try:
        #     if self.testCache.database_service is None and (self.testCache.config_service.get('framework')=="pytest"): 
        #         DatabaseService.Init(self)           
        #         self.testCache.data_service = DatabaseService()
        # except:
        #     self.testCache.logger_service.logger.exception("Data Service Initialize Failed:")

        #Data service
        try:
            if self.testCache.data_service is None and (self.testCache.config_service.get('framework')=="pytest"): 
                DataService.Init(self)           
                self.testCache.data_service = DataService()
        except:
            self.testCache.logger_service.logger.exception("Data Service Initialize Failed:")
        
        
        #Driver service
        try:
            if self.testCache.driver_service is None and (self.testCache.config_service.get('framework')=="pytest"):  
                DriverService.Init(self)          
                self.testCache.driver_service = DriverService()
        except:
            self.testCache.logger_service.logger.exception("Driver Service Initialize Failed:")


    # def DatabaseInitialize(self,databaseName):    
    #     if (self.testCache.config_service.get('framework')=="pytest"):    
    #         self.testCache.database_service.initializeDbConnection(databaseName)

    def DriverInitialize(self,driverName):    
        if (self.testCache.config_service.get('framework')=="pytest"):    
            self.testCache.driver_service.initializeDriver(driverName)
        
    def SwitchTestCase(self,testCase):
        self._testCaseId = testCase
        if (self.testCache.config_service.get('framework')=="pytest"):
            self.testCache.data_service.switchTestData(self._testCaseId)
            self.testCache.logger_service.logger.info("test data is mapped")
        # self.testCache.testcase_service.currentTestCase = testCase
        # self.testCache.testcase_service.StartTestCase()

    def DriverCleanup(self):   
        if self.testCache is not None:   
            if (self.testCache.config_service.get('framework')=="pytest"):            
                self.testCache.driver_service.killDriver()

    def SessionCleanup(self):         
        if (self.testCache.config_service.get('framework')=="pytest"):            
            self.testCache.driver_service.cleanupAllDrivers()
        self.testCache.logger_service.logger.info("Bootstrap Master Cleanup...")
        self.testCache = None

        
        


     

           

        

    
    




        
