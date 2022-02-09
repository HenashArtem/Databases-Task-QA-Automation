from selenium.webdriver.common.by import By
from framework.elements.label import Label
from framework.elements.button import Button
from framework.elements.text_box import TextBox
from framework.pages.base_page import BasePage
from tests.utils.iframe_parse_util import IFrameParseUtil
import random
import time


class NewslettersPage(BasePage):
    newsletter_subscription_list = Label(search_condition=By.XPATH,
                                         locator="//label[contains(@class, 'unchecked-label cursor-pointer')]",
                                         name="Newsletter subscription list")

    email_fill_form = Label(search_condition=By.XPATH,
                            locator="//section[contains(@class, 'cta-newsletter-esturgeon')]",
                            name="Email fill form")

    email_textbox = TextBox(search_condition=By.XPATH,
                            locator="//input[@class = 'w-full']",
                            name="Email textbox")

    submit_btn = Button(search_condition=By.XPATH,
                        locator="//input[contains(@value, 'ubmit')]",
                        name="Submit button")

    additional_modal_window = Label(search_condition=By.XPATH,
                                    locator="//div[@id = 'additional-data-modal']",
                                    name="Additional modal window")

    close_additional_modal_window = Button(search_condition=By.XPATH,
                                           locator="//a[@class = 'close-modal ']",
                                           name="Close modal window")

    selected_block_preview_lbl = Label(search_condition=By.XPATH,
                                       locator="//label[@class='block w-full btn-tertiary-plain checked-label border "
                                               "border-transparent "
                                               "cursor-pointer']//parent::div//following-sibling::a[contains(@href, "
                                               "'previews')]",
                                       name="Selected block preview")

    previews_modal_window = Label(search_condition=By.XPATH,
                                  locator="//div[contains(@id, 'previews') and @class='modal']",
                                  name="Preview modal window")

    divs_list = Label(search_condition=By.XPATH,
                      locator="//div[contains(@class, 'current')]//div[contains(@id, 'previews')]",
                      name="Divs list")

    def __init__(self):
        super().__init__(search_condition=By.XPATH, locator="//form[@id = 'newsletters-form']",
                         page_name=self.__class__.__name__)
        super().wait_for_page_opened()

    def get_random_newsletter_subscription_number(self):
        self.newsletter_subscription_list.wait_for_is_present()
        list_of_newsletter_subscriptions = self.newsletter_subscription_list.get_elements()
        for item in range(len(list_of_newsletter_subscriptions)):
            num_of_sub = random.randint(0, len(list_of_newsletter_subscriptions))
            return num_of_sub

    def click_random_newsletter_subscription(self, random_sub_num):
        list_of_newsletter_subscriptions = self.newsletter_subscription_list.get_elements()
        list_of_newsletter_subscriptions[random_sub_num - 1].click()

    def is_email_fill_form_opened(self):
        self.email_fill_form.wait_for_is_present()
        return self.email_fill_form.is_displayed()

    def enter_email(self, email):
        self.email_textbox.wait_for_clickable()
        self.email_textbox.send_keys(email)

    def click_submit_btn(self):
        self.submit_btn.wait_for_clickable()
        self.submit_btn.click()

    def click_close_additional_modal_window(self):
        self.additional_modal_window.wait_for_is_present()
        self.close_additional_modal_window.wait_for_clickable()
        self.close_additional_modal_window.click()

    def click_preview_is_selected_block(self):
        self.selected_block_preview_lbl.wait_for_clickable()
        self.selected_block_preview_lbl.js_click()
        self.selected_block_preview_lbl.wait_for_invisibility()

    def get_iframe_preceding_sibling_div_id(self):
        time.sleep(3)
        if (self.divs_list.find_element()).is_displayed():
            return self.divs_list.find_element().get_attribute("id")

    def get_unsub_link(self):
        iframe_content_util = IFrameParseUtil()
        locator = f"//div[@id = '{self.get_iframe_preceding_sibling_div_id()}']//iframe"
        return iframe_content_util.get_unsubscribe_link(f"{locator}")
