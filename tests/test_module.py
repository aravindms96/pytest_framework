import pytest

@pytest.mark.app('FR_Credit')
def test_validate_user_is_in_Homepage(bootstrap):
    from pages.fr_homePage import HomePage
    
    homepage = HomePage(bootstrap)

    homepage.validate_navto_homePage()


@pytest.mark.app('FR_Credit')
def test_validate_user_navto_AllCards(bootstrap):
    from pages.fr_allcardsPage import AllCardsPage
    from pages.fr_homePage import HomePage

    allcards = AllCardsPage(bootstrap)
    homepage = HomePage(bootstrap)

    homepage.click_lescartesAMButton()
    allcards.validate_navto_lescartesAMPage()

@pytest.mark.app('FR_Credit')
def test_validate_user_clicks_EnSaviorPlus_Btn(bootstrap):
    from pages.fr_allcardsPage import AllCardsPage
    from pages.goldcard_descPage import GoldCard_DescPage

    allcards = AllCardsPage(bootstrap)
    goldcard = GoldCard_DescPage(bootstrap)

    allcards.click_ensavoirplusButton()
    goldcard.validate_navto_goldAM_desc_Page()

@pytest.mark.app('FR_Credit')
def test_validate_user_clicks_demandez_votre_carte_Btn(bootstrap):
    from pages.goldcard_descPage import GoldCard_DescPage
    from pages.user_detailsPage import User_DetailsPage

    goldcard = GoldCard_DescPage(bootstrap)
    userdtls = User_DetailsPage(bootstrap)

    goldcard.click_Demandez_votre_carte_button()
    userdtls.validate_navto_userdetails_Page()


@pytest.mark.app('FR_Credit')
def test_validate_user_details_Form_ErrMsgs(bootstrap):
    from pages.user_detailsPage import User_DetailsPage

    userdtls = User_DetailsPage(bootstrap)

    userdtls.click_SubmitButton()
    userdtls.validate_UserDetails_Field_ErrMsgs()

@pytest.mark.app('FR_Credit')
def test_validate_user_details_submit_ContactInfo(bootstrap):
    from pages.user_detailsPage import User_DetailsPage

    userdtls = User_DetailsPage(bootstrap)

    userdtls.refreshPage()
    userdtls.enter_UserDetails()
    userdtls.sleep(3)
    userdtls.click_SubmitButton()
    userdtls.sleep(5)
    userdtls.validate_navto_AddressInfo()