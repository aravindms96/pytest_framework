from selenium import webdriver as seleniumWebDriver
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager, EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service
# from appium import webdriver as appiumDriver
import sys, os
from datetime import datetime,timedelta


from utils.configService import ConfigService
from utils.loggerService import LoggerService
# from .databaseService import DatabaseService

class DriverService(object):
    """Class used to create and maintain drivers
    """
    _testCache = None

    @classmethod
    def Init(cls,obj):
        cls._testCache = obj.testCache

    def __init__(self):
        self._configService = self._testCache.config_service
        self.driver = None
        self.drivers = list()
        
        _driverType = self._configService.get("drivertype") 
        if isinstance(_driverType,list):
            #create multi drivers         
            for item in _driverType:
                self.drivers.append({'driverName':item[0],'driverType':item[1],'driver':None})
        else:
            #create single driver
            self.drivers.append({'driverName':"Default",'driverType':_driverType,'driver':None})  


    def __create_driver(self,driverName,driverType): 
        dr = None

        if (driverType == "selenium"):
            # import logging
            # selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
            # selenium_logger.setLevel(logging.WARNING)    

            self.selenium_options = None
            seleniumSettings = self._configService.getCustomSettings('seleniumsettings-'+driverName)
            self._testCache.logger_service.logger.debug(seleniumSettings.as_dict())
            self._testCache.logger_service.logger.debug("Launching selenium driver")
            dr:WebDriver = self.__create_selenium_driver(seleniumSettings.get('browser'))
           
            dr.maximize_window()
            dr.implicitly_wait(30)
            dr.get(seleniumSettings.get('appurl'))           
      
            # dr = seleniumWebDriver.Remote(self._configService.get('remoteUrl'), desired_caps)            


        else:
            pass
        #Add driver to dict
        self.__addToDriverCache(driverName,driverType,dr)
        return dr
    

    def __addToDriverCache(self,driverName,driverType,driver):
        self._testCache.logger_service.logger.debug("Adding driver to cache")
        next(filter((lambda d: d['driverName']==driverName),self.drivers))['driver'] = driver

    def removeFromDriverCache(self,driverName):
        self._testCache.logger_service.logger.debug("Adding driver to cache")
        next(filter((lambda d: d['driverName']==driverName),self.drivers))['driver'] = None           

    def initializeDriver(self,driverName):
        self._testCache.logger_service.logger.debug("Switching current driver to - "+driverName)
        try:
            drDict = next(filter((lambda d: d['driverName']==driverName),self.drivers))
            self._testCache.logger_service.logger.debug(f"driver dict is {drDict}")
            if(drDict['driver'] == None):
                self.__create_driver(drDict['driverName'],drDict['driverType'])
            
            self.driver = next(filter((lambda d: d['driverName']==driverName),self.drivers))['driver']
            self._testCache.logger_service.logger.debug(f"drivers list is {self.drivers}")
        except:                    
            self._testCache.logger_service.logger.exception("Failed while switching driver:")

    def getDriver(self,driverName):
        self._testCache.logger_service.logger.debug("Switching current driver to - "+driverName)
        dr = None
        try:
            drDict = next(filter((lambda d: d['driverName']==driverName),self.drivers))
            if(drDict['driver'] == None):
                self.__create_driver(drDict['driverName'],drDict['driverType'])
            dr = next(filter((lambda d: d['driverName']==driverName),self.drivers))['driver']
        except:                    
            self._testCache.logger_service.logger.exception("Failed while switching driver:")
        return dr

    def killDriver(self): 
        dr = next(filter((lambda d: d['driver']==self.driver),self.drivers))  
        driverName = dr['driverName']     
        driverType = dr['driverType']
        driver = dr['driver']     
           
        if driver is not None:       
            self._testCache.logger_service.logger.debug("Killing current driver - "+driverName) 
            try:    
                if (driverType == "selenium"):
                    driver.close()
                    driver.quit()

                elif (driverType == "appium"): 
                    driver.close()
                    driver.quit()
            except:                    
                self._testCache.logger_service.logger.exception("Failed while killing driver:")

            self.driver = None
            next(filter((lambda d: d['driverName']==driverName),self.drivers))['driver'] = None

    def cleanupAllDrivers(self):
        for dr in self.drivers:
            driverName = dr['driverName']
            driverType = dr['driverType']
            driver = dr['driver']
            if driver is not None:       
                self._testCache.logger_service.logger.debug("Killing driver - "+driverName)  
                try:
                    if (driverType == "selenium"):
                        driver.close()
                        driver.quit()
                    elif (driverType == "appium"): 
                        try:
                            driver.close()
                        except:
                            pass
                        driver.quit()  
                except:
                    pass
                    # self._testCache.logger_service.logger.exception("Failed while killing driver:")   
                





    #---------------------------------------------------------------------------------------------------------------------------#
    #---------------------------------------Selenium driver Private functions---------------------------------------------------#
    #---------------------------------------------------------------------------------------------------------------------------#
    __browser_names = {
        'googlechrome': "chrome",
        'gc': "chrome",
        'chrome': "chrome",
        'headlesschrome': 'headless_chrome',
        'ff': 'firefox',
        'firefox': 'firefox',
        'headlessfirefox': 'headless_firefox',
        'ie': 'ie',
        'internetexplorer': 'ie',
        'edge': 'edge',
        'opera': 'opera',
        'safari': 'safari',
        'phantomjs': 'phantomjs',
        'htmlunit': 'htmlunit',
        'htmlunitwithjs': 'htmlunit_with_js',
        'android': 'android',
        'iphone': 'iphone'
    }

    def __create_selenium_driver(self, browser, desired_capabilities=None, remote_url=None,
                      profile_dir=None, options=None, service_log_path=None):
        browser = self.__normalise_browser_name(browser)
        creation_method = self.__get_creator_method(browser)
        # desired_capabilities = self._parse_capabilities(desired_capabilities, browser)
        # service_log_path = self._get_log_path(service_log_path)
        #options = self.selenium_options.create(self.__browser_names.get(browser), options)
        # if service_log_path:
        #     logger.info('Browser driver log file created to: %s' % service_log_path)
        #     self._create_directory(service_log_path)
        if (creation_method == self.__create_firefox
                or creation_method == self.__create_headless_firefox):
            return creation_method(desired_capabilities, remote_url, profile_dir,
                                   options=options, service_log_path=service_log_path)
        return creation_method(desired_capabilities, remote_url, options=options,
                               service_log_path=service_log_path)

    def __normalise_browser_name(self, browser):
        return browser.lower().replace(' ', '')

    def __get_creator_method(self, browser):
        if browser in self.__browser_names:
            return getattr(self, '_DriverService__create_{}'.format(self.__browser_names[browser]))
        raise ValueError('{} is not a supported browser.'.format(browser))
    
    def __remote_capabilities_resolver(self, set_capabilities, default_capabilities):
        if not set_capabilities:
            return {'desired_capabilities': default_capabilities}
        if 'capabilities' in set_capabilities:
            caps = set_capabilities['capabilities']
        else:
            caps = set_capabilities['desired_capabilities']
        if 'browserName' not in caps:
            caps['browserName'] = default_capabilities['browserName']
        return {'desired_capabilities': caps}

    def __create_chrome(self, desired_capabilities, remote_url, options=None, service_log_path=None):
        if not options:
            options = seleniumWebDriver.ChromeOptions()
        # options.add_argument("--log-level=3")  
        options.add_experimental_option('excludeSwitches',['enable-logging'])
        options.add_experimental_option("prefs", {"profile.default_content_setting_values.media_stream_mic": 1,
        "profile.default_content_setting_values.media_stream_camera": 1,
        "profile.default_content_setting_values.geolocation": 2,
        "profile.default_content_setting_values.notifications": 2}) 
        if (remote_url):
            defaul_caps = seleniumWebDriver.DesiredCapabilities.CHROME.copy()
            desired_capabilities = self.__remote_capabilities_resolver(desired_capabilities, defaul_caps)
            return self.__remote(desired_capabilities, remote_url, options=options)
        #return seleniumWebDriver.Chrome(options=options, service_log_path=service_log_path, **desired_capabilities)
        base_dir = os.path.dirname(__file__)
        chromedriver_path = os.path.join(base_dir, "chromedriver-win64\chromedriver.exe")
        self._testCache.logger_service.logger.debug("chromedriver path is "+chromedriver_path)
        service = Service(executable_path=chromedriver_path)
        return seleniumWebDriver.Chrome(service=service,options=options)

    def __create_headless_chrome(self, desired_capabilities, remote_url, options=None, service_log_path=None):
        if not options:
            options = seleniumWebDriver.ChromeOptions()
        options.headless = True
        return self.__create_chrome(desired_capabilities, remote_url, options, service_log_path)

    def __create_firefox(self, desired_capabilities, remote_url, ff_profile_dir, options=None, service_log_path=None):
        profile = self.__get_ff_profile(ff_profile_dir)
        if not options:
            options = seleniumWebDriver.FirefoxOptions()
        options.set_preference("media.getusermedia.browser.enabled", True)
        if (remote_url):
            default_caps = seleniumWebDriver.DesiredCapabilities.FIREFOX.copy()
            desired_capabilities = self.__remote_capabilities_resolver(desired_capabilities, default_caps)
            return self.__remote(desired_capabilities, remote_url,
                                profile, options)
        # service_log_path = service_log_path if service_log_path else self._geckodriver_log
        #return seleniumWebDriver.Firefox(options=options, firefox_profile=profile,service_log_path=service_log_path, **desired_capabilities)
        return seleniumWebDriver.Firefox(executable_path=GeckoDriverManager().install(),options=options, firefox_profile=profile)

    def __get_ff_profile(self, ff_profile_dir):
        if isinstance(ff_profile_dir,seleniumWebDriver.FirefoxProfile):
            return ff_profile_dir
        if not (ff_profile_dir):
            return seleniumWebDriver.FirefoxProfile()
        try:
            return seleniumWebDriver.FirefoxProfile(ff_profile_dir)
        except (OSError, FileNotFoundError):
            ff_options = self.selenium_options._parse(ff_profile_dir)
            ff_profile = seleniumWebDriver.FirefoxProfile()
            for option in ff_options:
                for key in option:
                    attr = getattr(ff_profile, key)
                    if callable(attr):
                        attr(*option[key])
                    else:
                        setattr(ff_profile, key, *option[key])
            return ff_profile

    # @property
    # def _geckodriver_log(self):
    #     log_file = self._get_log_path(os.path.join(self.log_dir, 'geckodriver-{index}.log'))
    #     logger.info('Firefox driver log is always forced to to: %s' % log_file)
    #     return log_file

    def __create_headless_firefox(self, desired_capabilities, remote_url,
                                ff_profile_dir, options=None, service_log_path=None):
        if not options:
            options = seleniumWebDriver.FirefoxOptions()
        options.headless = True
        return self.__create_firefox(desired_capabilities, remote_url, ff_profile_dir, options, service_log_path)

    def __create_ie(self, desired_capabilities, remote_url, options=None, service_log_path=None):
        if not options : 
            options = seleniumWebDriver.IeOptions()
            options.ignore_protected_mode_settings = True
            options.ignore_zoom_level = True
        if (remote_url):
            defaul_caps = seleniumWebDriver.DesiredCapabilities.INTERNETEXPLORER.copy()
            desired_capabilities = self.__remote_capabilities_resolver(desired_capabilities, defaul_caps)
            return self.__remote(desired_capabilities, remote_url, options=options)
        #return seleniumWebDriver.Ie(options=options, service_log_path=service_log_path, **desired_capabilities)
        # return seleniumWebDriver.Ie(executable_path=IEDriverManager().install(),options=options)
        return seleniumWebDriver.Ie(options=options)
    
    # def _has_options(self, web_driver):
    #     signature = inspect.getargspec(web_driver.__init__)
    #     return 'options' in signature.args

    def __create_edge(self, desired_capabilities, remote_url, options=None, service_log_path=None):
        if (remote_url):
            defaul_caps = seleniumWebDriver.DesiredCapabilities.EDGE.copy()
            desired_capabilities = self.__remote_capabilities_resolver(desired_capabilities, defaul_caps)
            return self.__remote(desired_capabilities, remote_url)
        # if self._has_options(seleniumWebDriver.Edge):
        #     # options is supported from Selenium 4.0 onwards
        #     # If can be removed when minimum Selenium version is 4.0 or greater
            # return seleniumWebDriver.Edge(options=options, service_log_path=service_log_path, **desired_capabilities)
        # return seleniumWebDriver.Edge(service_log_path=service_log_path, **desired_capabilities)
        return seleniumWebDriver.Edge(executable_path=EdgeChromiumDriverManager().install())


    def __remote(self, desired_capabilities, remote_url,
                profile_dir=None, options=None):
        remote_url = str(remote_url)
        # file_detector = self._get_sl_file_detector()
        file_detector = None
        return seleniumWebDriver.Remote(command_executor=remote_url,
                                browser_profile=profile_dir, options=options,
                                file_detector=file_detector,
                                **desired_capabilities)



