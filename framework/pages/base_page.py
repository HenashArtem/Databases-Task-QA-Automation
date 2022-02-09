from framework.browser.browser import Browser
from framework.elements.label import Label
from framework.utils.logger import Logger


class BasePage:
    def __init__(self, search_condition, locator, page_name):
        self.locator = locator
        self.page_name = page_name
        self.search_condition = search_condition

    def wait_page_to_load(self):
        Logger.info("Waiting for the page to load " + self.page_name + " using js")
        Browser.get_browser().wait_for_page_to_load()

    def is_opened(self):
        Logger.info("Checking if a page is open " + self.page_name)
        self.wait_page_to_load()
        return Browser.get_browser().is_wait_successful(
            Label(self.search_condition, self.locator, self.page_name).wait_for_is_visible)

    def wait_for_page_closed(self):
        self.wait_page_to_load()
        return Browser.get_browser().is_wait_successful(
            Label(self.search_condition, self.locator, self.page_name).wait_for_is_absent)

    def wait_for_page_opened(self):
        Logger.info("Waiting for the page to load " + self.page_name + "and the visibility of the element that "
                                                                       "identifies it")
        self.wait_page_to_load()
        Label(self.search_condition, self.locator, self.page_name).wait_for_is_visible()

    def refresh_page(self):
        Logger.info("Page refresh " + self.page_name)
        Browser.get_browser().refresh_page()
