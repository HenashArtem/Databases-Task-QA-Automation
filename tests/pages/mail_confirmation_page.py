from selenium.webdriver.common.by import By
from framework.elements.button import Button
from framework.pages.base_page import BasePage


class MailConfirmationPage(BasePage):
    back_to_site_btn = Button(search_condition=By.XPATH,
                              locator="//a[contains(@class, 'btn__confirmation')]",
                              name="Back to site button")

    def __init__(self):
        super().__init__(search_condition=By.XPATH, locator="//div[contains(@class, 'block-confirmation')]//img["
                                                            "contains(@class, 'block-confirmation')]",
                         page_name=self.__class__.__name__)
        super().wait_for_page_opened()

    def click_back_to_site_btn(self):
        self.back_to_site_btn.wait_for_clickable()
        self.back_to_site_btn.click()
