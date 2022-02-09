from framework.pages.base_page import BasePage
from selenium.webdriver.common.by import By
from framework.elements.button import Button
from framework.elements.text_box import TextBox
from framework.elements.label import Label
from tests.utils.get_auth_code_from_url import get_auth_code_form_url


class AuthPage(BasePage):
    email_input = TextBox(search_condition=By.XPATH,
                          locator="//input[@type = 'email']",
                          name="Email textbox")

    password_input = TextBox(search_condition=By.XPATH,
                             locator="//input[@type = 'password']",
                             name="Password textbox")

    next_auth_block_btn = Button(search_condition=By.XPATH,
                                 locator="//button[contains(@class, 'VfPpkd-LgbsSe-OWXEXe-k8QpJ')]",
                                 name="Next auth block button")

    additional_settings_lbl = Label(search_condition=By.XPATH,
                                    locator="//a[@jsname = 'BO4nrb']",
                                    name="Additional settings label")

    select_recommended_account_lbl = Label(search_condition=By.XPATH,
                                           locator="//a[@jsname = 'ehL7e']",
                                           name="Select recommended account label")

    continue_btn_in_terms_of_use = Button(search_condition=By.XPATH,
                                          locator="//div[@jsname = 'uRHG6']//button[@jsname = 'LgbsSe']",
                                          name="Continue button in terms of use")

    def __init__(self):
        super().__init__(search_condition=By.XPATH, locator="//div[@class = 'xkfVF']",
                         page_name=self.__class__.__name__)
        super().wait_for_page_opened()

    def enter_email(self, email):
        self.email_input.wait_for_clickable()
        self.email_input.send_keys(f"{email}")

    def click_next_block_auth_button(self):
        self.next_auth_block_btn.wait_for_clickable()
        self.next_auth_block_btn.click()

    def enter_password(self, password):
        self.password_input.wait_for_clickable()
        self.password_input.send_keys(f"{password}")

    def click_additional_setting_label(self):
        self.additional_settings_lbl.wait_for_clickable()
        self.additional_settings_lbl.click()

    def click_select_recommended_account(self):
        self.select_recommended_account_lbl.wait_for_clickable()
        self.select_recommended_account_lbl.click()

    def click_continue_btn_in_terms_of_use(self):
        self.continue_btn_in_terms_of_use.wait_for_clickable()
        self.continue_btn_in_terms_of_use.click()
        self.continue_btn_in_terms_of_use.wait_for_invisibility()

    def get_auth_code(self):
        return get_auth_code_form_url()
