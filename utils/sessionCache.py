from logging import RootLogger
from utils.loggerService import LoggerService
from utils.configService import ConfigService
from utils.dataService import DataService
from utils.driverService import DriverService


class SessionCache(object):
     """Test Cache object to store all the services used by the framework. 
    Test Cache object will be initialized and controlled by Bootstrapper 
    
    :param config_service: Config service used to store all configurations
    :type config_service: :class:`ConfigService`
    :param driver_service: Driver service used to create and maintain all the drivers
    :type driver_service: :class:`DriverService`
    :param data_service: Data service used to fetch data from different data sources
    :type data_service: :class:`DataService`
    :param logger_service: Logger service used for logging
    :type logger_service: :class:`LoggerService`

    """
     
     def __init__(self, config_service: ConfigService=None, driver_service: DriverService=None, data_service: DataService=None, logger_service: LoggerService=None):
            self.config_service = config_service
            self.driver_service = driver_service
            self.data_service = data_service
            self.logger_service = logger_service
            self.cache = dict()