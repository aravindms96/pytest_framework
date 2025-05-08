 #from elementService import ElementService
# import selenium
# from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from .sessionCache import SessionCache
import time
        
# def _locatorSwitcher(searchBy):
#     switcher ={
#         "id":lambda:webdriver.Remote.find_element_by_id,
#         "class_name":lambda:webdriver.Remote.find_elements_by_class_name,
#     }
#     return switcher.get(searchBy,lambda: "expression")()

def _locatorSwitcher(searchBy):
    switcher ={
        "id":By.ID,
        "class_name":By.CLASS_NAME,
        "css_selector":By.CSS_SELECTOR,
        "name":By.NAME,
        "tag_name":By.TAG_NAME,
        "link_text":By.LINK_TEXT,
        "partial_link_text":By.PARTIAL_LINK_TEXT,
        "xpath":By.XPATH,
    }
    return switcher.get(searchBy,"Locator type not supported")

class BaseElement(object):    
    """Base class with all Common actions. 

    .. note::
        Use only when not sure about the control type. Otherwise use custom classes

    :param locators: Key-Value pair of identifier used to locate the element. Available locators- id,class_name,css_selector,name,tag_name,link_text,partial_link_text,xpath
    :type locators: kwargs

    """
    def __init__(self, **kwargs):   
        self._currentElement:WebElement = None     
        self.criteria = kwargs 
   
    def __get__(self, obj, owner):
        self.testCache:SessionCache = obj.testCache
        return self
   
    # def __set__(self, obj, value): 
    #     raise Exception('Cannot set value')    
    
    def _searchElement(self,parentElement=None,timeoutInSeconds=15):
        try:
            self._webdriver:WebDriver = self.testCache.driver_service.driver
            if not parentElement:
                parentElement = self._webdriver            
            # if self._currentElement is None:
            if self.criteria.__len__() == 1:
                locator,val = list(self.criteria.items())[0]
                if locator == "current_element" and isinstance(val,WebElement):
                    self._currentElement = val
                else:
                    # self._currentElement = parentElement.find_element(by=_locatorSwitcher(locator),value=val)      
                    wait = WebDriverWait(self._webdriver, timeoutInSeconds)
                    self._currentElement = wait.until(ec.presence_of_element_located((_locatorSwitcher(locator),val)))
                    try:
                        self._webdriver.execute_script("arguments[0].scrollIntoView();", self._currentElement)
                    except:
                        self.testCache.logger_service.logger.exception("scrollIntoView Failure:")
                  
        except:
            self.testCache.logger_service.logger.exception("SearchFailure:")
            
    # def FindElement(self,**searchCriteria):  
    #     self._searchElement()   
    #     el = self._currentElement.find_element()
    #     return el
    
    def FindElement(self,elementType,**searchCriteria):
        """Returns a child element as a Wrapped element based on Element type.

        :param elementType: Type of element to be returned
        :type elementType: Type of WebElement
        :param locators: Key-Value pair of identifier used to locate the element. Available locators- id,class_name,css_selector,name,tag_name,link_text,partial_link_text,xpath
        :type locators: kwargs
        :returns: Returns element of the type specified
        """
        el = None
        self._searchElement()
        try:           
            locator,val = list(searchCriteria.items())[0]
            cell:WebElement = self._currentElement.find_element(by=_locatorSwitcher(locator),value=val)
            el = elementType(current_element=cell)
            el.testCache = self.testCache
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-FindElement:")        
        return el

    def FindElements(self,elementType,**searchCriteria):
        """Returns a list of child elements as a Wrapped element based on Element type.

        :param elementType: Type of element to be returned
        :type elementType: Type of WebElement
        :param locators: Key-Value pair of identifier used to locate the element. Available locators- id,class_name,css_selector,name,tag_name,link_text,partial_link_text,xpath
        :type locators: kwargs
        :returns: Returns list of elements of the type specified
        """
        els = None
        self._searchElement()
        try:           
            locator,val = list(searchCriteria.items())[0]
            elements:list(WebElement) = self._currentElement.find_elements(by=_locatorSwitcher(locator),value=val)
            els = [elementType(current_element=element) for element in elements] 
            for el in els:
                el.testCache = self.testCache
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-FindElements:")        
        return els

    def findShadowElement(self,elementType,*searchCriteria):
        """Returns a Shadow element from shadow DOM based on Element type.

        :param elementType: Type of element to be returned
        :type elementType: Type of WebElement
        :param locators: Arguments to be passed based on the element selector or query selector
        :type locators: args
        :returns: Returns element of the type specified
        """
        el = None
        if searchCriteria.__len__()>1:
            self._searchElement()
        try:
            driver = self.testCache.driver_service.driver
            cell:WebElement = driver.execute_script(searchCriteria)           
            el = elementType(current_element=cell)
            el.testCache = self.testCache
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-FindElement:")        
        return el

    def ExecuteScript(self, action):
        """Used to execute Java script commands...   

        :param action: Type of action to be performed
        :type action: str
        """
        self._searchElement()
        try:
            self._webdriver.execute_script(action, self._currentElement)
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-ExecuteScript:")

    def SetFocus(self):
        """Set focus on the specified element.   

        """
        self._searchElement()
        try:
            self._webdriver.execute_script("arguments[0].focus();", self._currentElement)
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-SetFocus:")

    def Click(self):
        """Click on the specified element.   

        """
        self._searchElement()
        try:
            try:
                self._currentElement.click()
            except:
                self._webdriver.execute_script("arguments[0].click();", self._currentElement)            
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-Click:")
    
    def ClickMultiple(self):
        """Control click on elements when multiple elements are to be selected.   

        """
        self._searchElement()
        try:
            ActionChains(self._webdriver).key_down(Keys.CONTROL).click(self._currentElement).key_up(Keys.CONTROL).perform()          
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-ClickMultiple:")
        return self

    def ClickElementAtCoordinates(self, xoffset, yoffset):
        """Click the element at ``xoffset/yoffset``.
        The Cursor is moved from the center of the element and x/y coordinates are
        calculated from that point.

        :param xoffset: Distance on the x coordinate
        :type xoffset: int
        :param yoffset: Distance on the y coordinate
        :type yoffset: int

        """
        # self.info("Clicking element '%s' at coordinates x=%s, y=%s."
        #           % (locator, xoffset, yoffset))
        self._searchElement()        
        try:
            action = ActionChains(self._webdriver)        
            action.move_to_element(self._currentElement)        
            action.move_by_offset(xoffset, yoffset)
            action.click()
            action.perform()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-ClickElementAtCoordinates:")

    def DoubleClick(self):
        """Double Click on the specified element.   

        """       
        self._searchElement()        
        try:
            action = ActionChains(self._webdriver)        
            action.double_click(self._currentElement).perform()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-DoubleClick:")

    def IsEnabled(self):
        """Check if the specified element is enabled.   

        :rtype: boolean
        """
        self._searchElement()
        found = False
        try:
            found = self._currentElement.is_enabled()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-IsEnabled:")
        return found

    def IsVisible(self):
        """Check if the specified element is visible on the screen.   

        :rtype: boolean
        """
        self._searchElement()
        found = False
        try:
            found = self._currentElement.is_displayed()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-IsVisible:")
        return found

    def ScrollIntoView(self):
        """Scroll the specified element into viewable area on the screen.   

        """
        self._searchElement()
        try:
            ActionChains(self._webdriver).move_to_element(self._currentElement).perform()           
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-ScrollIntoView:")
        return self
    
    def WaitForExists(self,timeoutInSeconds=30):
        """Wait for the specified element to be visible on the screen.   

        """
        try:
            self._searchElement(timeoutInSeconds)
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-WaitForExists:")
        return self
    
    def WaitForVisible(self,timeoutInSeconds=30):
        """Wait for the specified element to be visible on the screen.   

        """
        self._searchElement()
        wait = WebDriverWait(self._webdriver, timeoutInSeconds)
        try:
            wait.until(ec.visibility_of(self._currentElement))
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-WaitForVisible:")
        return self
    
    def WaitForInVisible(self,timeoutInSeconds=30):
        """Wait for the specified element to be visible on the screen.   

        """
        self._searchElement()
        wait = WebDriverWait(self._webdriver, timeoutInSeconds)
        try:
            wait.until(ec.invisibility_of_element(self._currentElement))
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-WaitForInVisible:")

    def GetAttribute(self,attributeName:str):
        """Fetch the attribute value from the specified element.   

        :rtype: str
        """
        self._searchElement()
        text = None
        try:
            text = self._currentElement.get_attribute(attributeName)
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-GetAttribute:")
        return text

    def EnterText(self,text): 
            """Enter the given text in the specified element.   

            :param text: Text to be entered
            :type text: str
            """          
            self._searchElement()        
            try:            
                self._currentElement.send_keys(text)
            except:
                self.testCache.logger_service.logger.exception("ActionFailure-EnterText:")

    def ClearText(self):    
        """Clear all the text in the specified element.  

        """      
        self._searchElement()        
        try:            
            self._currentElement.clear()
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-ClearText:")

    def GetText(self):
        """Fetch the text from the specified element.   

        :rtype: str
        """
        self._searchElement()
        text = None
        try:
            text = self._currentElement.text
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-GetText:")
        return text

    def SetValue(self,text): 
        """Set the value attribute in the specified element.   

        :param text: Text to be entered
        :type text: str
        """          
        self._searchElement()        
        try:            
            self._webdriver.execute_script("arguments[0].setAttribute('value', '" + text +"')", self._currentElement)
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-SetValue:")
                
    def GetValue(self):
        """Fetch the value attribute from the specified element.(For cases where GetText doesn't work)   

        :rtype: str
        """
        self._searchElement()
        text = None
        try:
            text = self._currentElement.get_attribute("value")
        except:
            self.testCache.logger_service.logger.exception("ActionFailure-GetValue:")
        return text
