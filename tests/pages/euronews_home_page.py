from selenium.webdriver.common.by import By
from framework.elements.label import Label
from framework.elements.button import Button
from framework.pages.base_page import BasePage


class EuronewsHomePage(BasePage):

    newsletters_lbl = Label(search_condition=By.XPATH,
                            locator="//a[@aria-label = 'Newsletters']//span[contains(@data-event, 'newsletter')]",
                            name="Newsletters label")

    accept_cookies_btn = Button(search_condition=By.XPATH,
                                locator="//button[@id = 'didomi-notice-agree-button']",
                                name="Accept cookies button")

    def __init__(self):
        super().__init__(search_condition=By.XPATH, locator="//main[@id = 'enw-main-content']",
                         page_name=self.__class__.__name__)
        super().wait_for_page_opened()

    def click_accept_cookies_button(self):
        self.accept_cookies_btn.wait_for_clickable()
        self.accept_cookies_btn.click()

    def click_newsletters_label(self):
        self.newsletters_lbl.wait_for_clickable()
        self.newsletters_lbl.click()
