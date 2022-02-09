# coding=utf-8
import json

from selenium.common.exceptions import NoSuchWindowException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from tests.config.waits import Waits
from tests.config.browser import BrowserConfig
from framework.browser.browser_factory import BrowserFactory
from framework.utils.logger import Logger
from framework.waits.wait_for_custom_event import WaitForCustomEvent
from framework.waits.wait_for_ready_state_complete import WaitForReadyStateComplete
from framework.waits.wait_for_true_with_action import WaitForTrueWithAction
from framework.singleton import Singleton


class Browser(metaclass=Singleton):
    def __init__(self):
        self.__web_driver = {}
        self.__main_window_handle = None
        self.__selected_browser = BrowserConfig.BROWSER

    @staticmethod
    def get_browser():
        return Browser()

    def get_selected_browser_key(self):
        return self.__selected_browser

    def get_browser_keys(self):
        return self.__web_driver.keys()

    def get_driver(self):
        return self.__web_driver[self.__selected_browser]

    def set_up_driver(self, browser_key=BrowserConfig.BROWSER, capabilities=None, is_incognito=False,
                      enable_performance_logging=False, test_name=None, grid_port=None):
        Logger.info('Browser driver initialization ' + BrowserConfig.BROWSER)
        with open("test_results.json", "r") as file:
            file_data = dict(json.load(file))
        with open("test_results.json", "w") as f:
            data_to_update = {"browser": f"{BrowserConfig.BROWSER}"}
            file_data.update(data_to_update)
            json.dump(file_data, f)
        if browser_key in self.__web_driver:
            raise ValueError("Browser with key '{}' has already been created.".format(browser_key))
        self.__web_driver[browser_key] = \
            BrowserFactory.get_browser_driver(capabilities=capabilities,
                                              is_incognito=is_incognito,
                                              enable_performance_logging=enable_performance_logging,
                                              test_name=test_name, grid_port=grid_port)
        self.__web_driver[browser_key].implicitly_wait(Waits.IMPLICITLY_WAIT_SEC)
        self.__web_driver[browser_key].set_page_load_timeout(Waits.PAGE_LOAD_TIMEOUT_SEC)
        self.__web_driver[browser_key].set_script_timeout(Waits.SCRIPT_TIMEOUT_SEC)
        self.__main_window_handle = self.__web_driver[browser_key].current_window_handle
        self.select_browser(browser_key)

    def select_browser(self, browser_key=BrowserConfig.BROWSER):
        if browser_key not in self.__web_driver:
            raise KeyError("Browser with key '{}' does not exist.".format(browser_key))
        self.__selected_browser = browser_key

    def quit(self, browser_key=BrowserConfig.BROWSER):
        browser_inst = self.__web_driver.get(browser_key)
        if browser_inst is not None:
            Logger.info("Shutting down the driver")
            browser_inst.quit()
            self.__web_driver.pop(browser_key, None)

    def get_driver_names(self):
        return self.__web_driver.keys()

    def close(self, page_name=""):
        if self.get_driver() is not None:
            Logger.info("Closing page %s" % page_name)
            self.get_driver().close()

    def refresh_page(self):
        Logger.info("Page reload")
        self.get_driver().refresh()

    def maximize(self, browser_key=BrowserConfig.BROWSER):
        self.__web_driver[browser_key].maximize_window()

    def set_url(self, url):
        Logger.info("Change page url to" + url)
        self.get_driver().get(url)

    def execute_script(self, script, arguments=None):
        if arguments is None:
            arguments = []
        return self.get_driver().execute_script(script, arguments)

    def get_cookies(self):
        Logger.info("Getting all cookies")
        return self.get_driver().get_cookies()

    def get_cookie(self, name):
        Logger.info("Getting a cookie with a name:" + name)
        return self.get_driver().get_cookie(name=name)

    def get_current_url(self):
        return self.get_driver().current_url

    def back_page(self):
        self.get_driver().back()

    def switch_to_window(self, window_handle=None):
        if window_handle is None:
            window_handle = self.__main_window_handle
        Logger.info("Switch to window named %s" % window_handle)
        try:
            self.get_driver().switch_to_window(window_handle)
        except NoSuchWindowException:
            Logger.error("No matching window found named %s" % window_handle)

    def get_count_windows(self):
        count = len(self.get_driver().window_handles)
        Logger.info("Number of browser windows open: %d" % count)
        return count

    def switch_new_window(self, logged_page_name=""):
        Logger.info("Switch to new window %s" % logged_page_name)
        handles = self.get_driver().window_handles
        if len(handles) <= 1:
            raise NoSuchWindowException("There is no new window. The number of windows is %s" % len(handles))
        self.get_driver().switch_to_window(handles[-1])

    def switch_to_frame_by_name(self, frame_name):
        Logger.info("Switch to frame named %s" % frame_name)
        self.get_driver().switch_to_frame(frame_name)

    def switch_to_frame_by_locator(self, search_condition, locator):
        Logger.info("Switching to frame by locator {}".format(locator))
        self.get_driver().switch_to.frame(self.get_driver().find_element(search_condition, locator))

    def switch_to_default_content(self):
        Logger.info("Switch to main frame")
        self.get_driver().switch_to_default_content()

    def wait_for_page_to_load(self):
        WebDriverWait(self.get_driver(), Waits.PAGE_LOAD_TIMEOUT_SEC).until(WaitForReadyStateComplete(browser=self))

    def wait_for_custom_event(self, event, expected_result, *args, time_in_seconds=Waits.IMPLICITLY_WAIT_SEC, msg=""):
        waiter = WaitForCustomEvent(event, expected_result, *args)
        self.wait_for_check_by_condition(waiter=waiter, time_in_seconds=time_in_seconds, message=msg)

    def wait_for_true(self, expression, time_in_seconds=Waits.IMPLICITLY_WAIT_SEC, msg=""):
        self.wait_for_custom_event(expression, True, time_in_seconds=time_in_seconds, msg=msg)

    def wait_for_true_with_action(self, expression, event, expression_args=None, action_args=None,
                                  time_in_seconds=Waits.IMPLICITLY_WAIT_SEC, msg=""):
        waiter = WaitForTrueWithAction(self.get_driver(), expression, event, expression_args=expression_args,
                                       action_args=action_args)
        self.wait_for_check_by_condition(waiter=waiter, time_in_seconds=time_in_seconds, message=msg)

    def wait_for_check_by_condition(self, waiter, time_in_seconds=Waits.IMPLICITLY_WAIT_SEC, message=""):
        try:
            WebDriverWait(self.get_driver(), time_in_seconds).until(waiter)
        except TimeoutException:
            error_msg = "Event failed after {time} seconds elapsed: {msg}".format(time=time_in_seconds,
                                                                                        msg=message)
            Logger.warning(error_msg)
            raise TimeoutException(error_msg)

    def is_wait_successful(self, wait_function, *args):
        try:
            wait_function(*args)
        except TimeoutException:
            return False
        return True
