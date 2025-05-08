from utils.basePage import BasePage
from utils import webEl_Utit


class HomePage(BasePage):
    
   homepage_Title = webEl_Utit.BaseElement(xpath="//a[@title='Homepage']")
   loginButton = webEl_Utit.BaseElement(xpath="//a[@id='gnav_login']//span[contains(text(),'Connexion')]")
   devenirclientMenu = webEl_Utit.BaseElement(xpath="//label[@id='label-tab-open-cards' and contains(text(),'Devenir Client')]")
   lescartesAMButton = webEl_Utit.BaseElement(xpath="//span[contains(text(),'Les Cartes AMERICAN EXPRESS')][1]")
   cookies_acceptButton = webEl_Utit.BaseElement(xpath="//button[text()='Tout Accepter']")


   def validate_navto_homePage(self):
      try:
         self.cookies_acceptButton.Click()
      except Exception as e:
         self.logger.debug("Cookies accept button not found, continuing without clicking")
         self.logger.debug(e)
      self.sleep(5)
      # self.logger.debug("title get"+ self.getPageTitle())
      self.logger.debug(self.getData("page_title"))
      assert self.homepage_Title.IsVisible(), "Home page title is not visible"
      assert self.loginButton.IsVisible(), "Login button is not visible"
      self.logger.debug("Home page is loaded successfully")

   def click_lescartesAMButton(self):
      self.devenirclientMenu.Click()
      assert self.lescartesAMButton.IsVisible(), "Les Cartes AMERICAN EXPRESS button is not visible"
      self.lescartesAMButton.Click()
      self.logger.debug("Les Cartes AMERICAN EXPRESS button clicked successfully")

