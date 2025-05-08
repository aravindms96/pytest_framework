from utils.basePage import BasePage
from utils import webEl_Utit


class User_DetailsPage(BasePage):
    
    label_souscrivez = webEl_Utit.BaseElement(xpath="//p[text()='Souscrivez en quelques minutes']")
    mr_Checkbox = webEl_Utit.BaseElement(xpath="//label[@for='MR']")
    ms_Checkbox = webEl_Utit.BaseElement(xpath="//label[@for='MS']")
    firstname_Textbox = webEl_Utit.BaseElement(xpath="//input[@name='firstName']")
    lastname_Textbox = webEl_Utit.BaseElement(xpath="//input[@name='lastName']")
    dob_Textbox = webEl_Utit.BaseElement(xpath="//input[@name='fieldControl-input-dateOfBirth']")
    email_Textbox = webEl_Utit.BaseElement(xpath="//input[@name='email']")
    mobileNum_Textbox = webEl_Utit.BaseElement(xpath="//input[@name='mobilePhoneNumber']")
    submit_Button = webEl_Utit.BaseElement(xpath="//button[@type='submit']")
    birthname_Checkbox= webEl_Utit.BaseElement(xpath="//input[@name='birthNameCheck']")
    pob_Textbox= webEl_Utit.BaseElement(xpath="//input[@name='placeOfBirth']")
    deptob_Combobox= webEl_Utit.BaseElement(xpath="//select[@name='departmentOfBirth']")
    countryob_Combobox= webEl_Utit.BaseElement(xpath="//select[@name='countryOfBirth']")
    nationality_Combobox= webEl_Utit.BaseElement(xpath="//select[@name='nationality']")
    country_Combobox= webEl_Utit.BaseElement(xpath="//select[@name='country']")
    address_Textbox= webEl_Utit.BaseElement(xpath="//input[@name=residentialAddressLine2']")
    postalcode_Textbox= webEl_Utit.BaseElement(xpath="//input[@name='postcode']")
    town_Textbox= webEl_Utit.BaseElement(xpath="//input[@name='cityTown']")
    personalStatus_Combobox= webEl_Utit.BaseElement(xpath="//select[@name='personalResidentialStatus']")
    Checkbox_ErrMsg = webEl_Utit.BaseElement(xpath="//div[text()='Merci de préciser votre civilité.']")
    FN_ErrMsg = webEl_Utit.BaseElement(xpath="//div[text()='Prénom obligatoire.']")
    LN_ErrMsg = webEl_Utit.BaseElement(xpath="//div[text()='Nom obligatoire.']")
    DOB_ErrMsg = webEl_Utit.BaseElement(xpath="//div[text()='Vous devez avoir plus de 18 ans.']")
    email_ErrMsg = webEl_Utit.BaseElement(xpath="//div[contains(text(),'Merci de vérifier le format de votre adresse email (exemple : nom@domaine.fr).')]")
    mobile_ErrMsg = webEl_Utit.BaseElement(xpath="//div[contains(text(),'Téléphone mobile obligatoire en chiffres uniquement et sans espaces.')]")
    common_ErrMsg = webEl_Utit.BaseElement(xpath="//span[contains(text(),'Veuillez corriger les erreurs ci-dessus pour continuer.')]")
    addressInfo_form = webEl_Utit.BaseElement(xpath="//form[@name='JourneyForm']") 
    errorBtn = webEl_Utit.BaseElement(xpath="//button[text()='Revenir à la page d’accueil']")



    def validate_navto_userdetails_Page(self):
       assert self.label_souscrivez.IsVisible(), "label_souscrivez is not visible"
       self.logger.debug("User details page is loaded successfully")

    def enter_UserDetails(self):
        if self.getData('prefix') == "Mr":       
          self.mr_Checkbox.Click()
        else :
          self.ms_Checkbox.Click()
        self.firstname_Textbox.EnterText(self.getData('firstName')+self.getRandomString(2, True))
        self.lastname_Textbox.EnterText(self.getData('lastName')+self.getRandomString(2, True))
        self.dob_Textbox.EnterText(self.getData('dob'))
        self.email_Textbox.EnterText(self.getData('email'))
        self.mobileNum_Textbox.EnterText(self.getData('mobileNum'))
        self.logger.debug("User details are successfully")
        self.mr_Checkbox.IsVisible()

    def click_SubmitButton(self):
        assert self.submit_Button.IsVisible(), "Submit button is not visible"
        self.submit_Button.Click()
        self.logger.debug("Submit button clicked successfully")

    def validate_UserDetails_Field_ErrMsgs(self):
        assert self.Checkbox_ErrMsg.IsVisible(), "Checkbox error message is not visible"
        assert self.FN_ErrMsg.IsVisible(), "First name error message is not visible"
        assert self.LN_ErrMsg.IsVisible(), "Last name error message is not visible"
        assert self.DOB_ErrMsg.IsVisible(), "Date of birth error message is not visible"
        assert self.email_ErrMsg.IsVisible(), "Email error message is not visible"
        assert self.mobile_ErrMsg.IsVisible(), "Mobile number error message is not visible"
        assert self.common_ErrMsg.IsVisible(), "Common error message is not visible"
        self.logger.debug("User details field error messages are validated successfully")

    def validate_navto_AddressInfo(self):
      if self.addressInfo_form.IsVisible():
        self.logger.debug(f"Address info form is successfully loaded")
      else:
        self.logger.debug(f"Address info form is not visible")
        if self.errorBtn.IsVisible():
           self.logger.debug(f"Address info form could not be loaded, error button is visible")
        else:
           assert False, "Address info form or error button is not visible"
        