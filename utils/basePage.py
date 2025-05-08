from .Bootstrapper import Bootstrapper
import time
import os
import string
import random

class BasePage(object):
    """Base Page for all pages.
    
    """
    def __init__(self,bootstrap:Bootstrapper):
        self.testCache = bootstrap.testCache
        self.logger = self.testCache.logger_service.logger  
        self.wrapper_driver = self.testCache.driver_service.driver

    def getData(self,dataName):
        """Fetch test data based on field name.
        Data will be fetched from key-value test data file based on the test case

        :param dataName: Key value used to fetch the data
        :type dataName: str
        :return: Returns a string if Key is present. Returns None otherwise

        """
        data = 1
        try:
            data = self.testCache.data_service.get(dataName)
        except:
            self.testCache.logger_service.logger.exception("DataFailure-getData:")        
        return data

    def getRandomString(self,size, alphaonly = False, splChars = False):
        """Get a random string value with a specified str length.
       
        :param size: string length
        :type size: int
        :param alphaonly: to include only alphabets in random string
        :type alphaonly: boolean
        :param splChars: to include special characters in random string
        :type splChars: boolean
        :return: Returns a random string with spl chars if splChars is true. Returns random string without spl chars otherwise

        """
        if splChars:
            data = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k = size))
        elif alphaonly:
            data = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k = size))
        else:
            data = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase + string.punctuation, k = size))
        #data +="!"
        return data

    def sleep(self,seconds):
        """Used to sleep/wait for the specified time.
       
        :param seconds: Seconds to sleep
        :type seconds: int

        """
        time.sleep(seconds)   

    def navigateToUrl(self,url):
        """Navigate to the specified URL.
       
        :param url: URL to be navigated
        :type url: str

        """
        try:
            self.testCache.driver_service.driver.get(url)
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-navigateToUrl:")

    def refreshPage(self):
        """Refresh the web page.

        """
        try:
            self.testCache.driver_service.driver.refresh()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-refreshPage:")

    def navigatePage(self, action):
        """Navigate forward or backward from current web page.
       
        :param action: URL to be navigated - back or forward
        :type action: char

        """
        try:
            if action is 'b': self.testCache.driver_service.driver.back()
            elif action is 'f': self.testCache.driver_service.driver.forward()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-navigatePage:")
    
    def switchToFrame(self,frameReference):
        """Switch to the specified frame.
       
        :param frameReference: Name of the frame to be switched to
        :type frameReference: str

        """
        try:
            self.testCache.driver_service.driver.switch_to.frame(frameReference)
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-switchToFrame:")

    def switchToDefaultWindow(self):
        """Switch to the specified window.

        """
        try:
            self.testCache.driver_service.driver.switch_to.default_content()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-switchToDefaultWindow:")

    def getWindowNames(self):
        """To get all open tabs in a browser session.

        """
        windows = None
        try:
            windows = self.testCache.driver_service.driver.window_handles
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-switchToWindow:")
        return windows

    def switchToWindow(self,windowName = "new"):
        """Switch to the specified window.
       
        :param windowName: Name of the window to be switched to
        :type windowName: str

        """
        if windowName == "new":
            wins = self.getWindowNames()
            self.testCache.driver_service.driver.switch_to.window(self.testCache.driver_service.driver.window_handles[len(wins)-1])
        else:
            try:
                self.testCache.driver_service.driver.switch_to.window(windowName)
            except:
                self.testCache.logger_service.logger.exception("ActionFailure-switchToWindow:")

    def handleAlert(self,accept=True,text=None):
        """Handle alerts produced by the Window.
        Alerts can be accepted or dismissed. Text can be entered incase alert has textbox

        :param accept: (Optional) True to Accept, False to Dismiss. Defaults to True
        :type accept: boolean
        :param text: (Optional) Text to be entered in the alert
        :type text: str

        """
        try:
            if text: self.testCache.driver_service.driver.switch_to.alert.send_keys(text)
            if accept:
                self.testCache.driver_service.driver.switch_to.alert.accept()
            else:
                self.testCache.driver_service.driver.switch_to.alert.dismiss()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-handleAlert:")

    def saveScreenshot(self,fileName):
        """Saves current web screen shot as PNG file in Screenshots Folder.
        
        :param fileName: File name
        :type fileName: str
       
        """
        
        try:            
            directory = os.getcwd()
            destDirectory = os.path.join(directory,'Screenshots\\Website')
            if not os.path.exists(destDirectory):os.makedirs(destDirectory)
            file_name = fileName + ".png"
            found = self.testCache.driver_service.driver.get_screenshot_as_file(os.path.join(destDirectory,file_name))
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-saveScreenshot:")

    def getPageTitle(self):
        """Get the title of current Web Page.

        """
        text = None
        try:
            self.testCache.driver_service.driver.title
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-getPageTitle:")
        return text

    def pageClose(self):
        """Close the current Web Page.

        """
        try:
            self.testCache.driver_service.driver.close()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-pageClose:")

    def pageQuit(self):
        """Quit the current and all opened pages or tabs.

        """
        try:
            self.testCache.driver_service.driver.quit()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-pageQuit:")
