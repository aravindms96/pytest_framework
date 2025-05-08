from utils.basePage import BasePage
from utils import webEl_Utit


class AllCardsPage(BasePage):
    
    breadcrumb_lescartesAM = webEl_Utit.BaseElement(xpath="//section//*[@class='breadcrumb']//span[contains(text(),'Cartes American Express')]")
    header_cardList = webEl_Utit.BaseElement(xpath="//section//a[@id='LesCartesAmericanExpress']")
    ensavoirplusBtn_GoldCard = webEl_Utit.BaseElement(xpath="//a[contains(@href,'gold-card-americanexpress')]/span[contains(text(),'En savoir plus')]")


    def validate_navto_lescartesAMPage(self):
       assert self.breadcrumb_lescartesAM.IsVisible(), "Login button is not visible"
       self.logger.debug("All cards page is loaded successfully")

    def click_ensavoirplusButton(self):
       self.sleep(3)
       assert self.ensavoirplusBtn_GoldCard.IsVisible(), "Carte Gold American Express ensavoirplus button is not visible"
       self.ensavoirplusBtn_GoldCard.Click()
       self.logger.debug("En Savoir Plus button clicked successfully")

