from selenium.webdriver.common.by import By
from framework.elements.label import Label
from framework.elements.button import Button
from framework.elements.text_box import TextBox
from framework.pages.base_page import BasePage


class UnsubscribePage(BasePage):
    enter_email_txb = TextBox(search_condition=By.XPATH,
                              locator="//input[@id = 'email']",
                              name="Enter email textbox")

    unsub_btn = Button(search_condition=By.XPATH,
                       locator="//button[@type='submit']",
                       name="Back to site button")

    successful_unsub_lbl = Label(search_condition=By.XPATH,
                                 locator="//div//p",
                                 name="Successful unsub label")

    def __init__(self):
        super().__init__(search_condition=By.XPATH, locator="//form[contains(@action,'unsubscribe')]",
                         page_name=self.__class__.__name__)
        super().wait_for_page_opened()

    def enter_email(self, email):
        self.enter_email_txb.wait_for_clickable()
        self.enter_email_txb.clear_field()
        self.enter_email_txb.send_keys(f"{email}")

    def click_unsub_btn(self):
        self.unsub_btn.wait_for_clickable()
        self.unsub_btn.click()

    def is_successfully_unsub_text_presents(self):
        self.successful_unsub_lbl.wait_for_is_present()
        return self.successful_unsub_lbl.is_displayed()
