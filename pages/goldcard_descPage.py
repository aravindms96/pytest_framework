from utils.basePage import BasePage
from utils import webEl_Utit


class GoldCard_DescPage(BasePage):
    
    breadcrumb_goldAMCard = webEl_Utit.BaseElement(xpath="//div[contains(@class,'breadcrumb')]//li[contains(text(),'Carte Gold American')]")
    demandezvc_Button = webEl_Utit.BaseElement(xpath="//a[@data-qe-id='Button' and text()='Demandez votre Carte'][1]")
    newMember_UIBanner = webEl_Utit.BaseElement(xpath="//div[@data-qe-id='NewMemberBanner']")


    def validate_navto_goldAM_desc_Page(self):
       assert self.breadcrumb_goldAMCard.IsVisible(), "Login button is not visible"
       assert self.newMember_UIBanner.IsVisible(), "New Member UI Banner is not visible"
       self.logger.debug("All cards page is loaded successfully")

    def click_Demandez_votre_carte_button(self):
       assert self.demandezvc_Button.IsVisible(), "Demandez votre carte button is not visible"
       self.demandezvc_Button.Click()
       self.logger.debug("Demandez votre carte button clicked successfully")

