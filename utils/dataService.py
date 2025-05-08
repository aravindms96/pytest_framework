import dynaconf
from dynaconf import Dynaconf
import toml

class DataService(object):
    """Class used to read and store data from data file"""
    _testCache = None

    @classmethod
    def Init(cls, obj):
        cls._testCache = obj.testCache

    def __init__(self):  
        self.__readTestData()

    def __readTestData(self):
        filePath = self._testCache.config_service.get('testdatapath')
        logger = self._testCache.logger_service.logger
        logger.debug(f"Reading test data from - {filePath}")
        try:
            self._defaultdata = dynaconf.LazySettings(SETTINGS_FILE_FOR_DYNACONF=filePath)
        except Exception as e:
            logger.exception(f"Failed to read test data: {e}")
            self._defaultdata = None

    def switchTestData(self, testCaseId):
        logger = self._testCache.logger_service.logger
        logger.debug(f"Switching current test case data to - {testCaseId}")
        if not self._defaultdata:
            logger.exception("Data will not be read from test data file, as it is not initialized")
            self._testdata = None
            return

        self.testCaseId = testCaseId
        try:
            self._testdata = self._defaultdata.from_env(env=self.testCaseId)
            self.datadict = self._testdata.as_dict()
        except Exception as e:
            logger.exception(f"Switching test data failed: {e}")
            self._testdata = None

    def get(self, dataName):
        logger = self._testCache.logger_service.logger
        if not self._testdata:
            logger.debug("Test data is not initialized")
            return None

        try:
            logger.debug(f"Trying to get test data: {dataName}")
            # return self._testdata.get(dataName)
            try:
                reqdata = self.datadict[self.testCaseId.upper()]
                try: return reqdata[dataName]
                except KeyError: 
                    logger.debug(f"Test data not found for {dataName}, trying to get from default")
                    try:
                        return self.datadict["DEFAULT"][dataName]
                    except KeyError:
                        logger.debug(f"Test data not found for {dataName}, in default also, hence returning None")
                        return None
            except KeyError:
                logger.debug(f"Test data not found for {self.testCaseId}, trying to get from default")
                try:
                    return self.datadict["DEFAULT"][dataName]
                except KeyError:
                    logger.debug(f"Test data not found for {dataName}, in default also, hence returning None")
                    return None
        except Exception as e:
            logger.exception(f"Getting test data failed: {dataName}, Error: {e}")
            return None