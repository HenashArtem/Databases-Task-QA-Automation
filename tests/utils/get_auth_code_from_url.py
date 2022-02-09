from framework.browser.browser import Browser
from framework.utils.logger import Logger


def get_auth_code_form_url():
    Logger.info("Getting authorization code from current url")
    current_url = Browser.get_browser().get_current_url()

    mark_1 = current_url.find('code=')
    new_s = current_url[mark_1 + 5:]
    mark_2 = new_s.find('&')

    auth_code = new_s[:mark_2]
    return auth_code
