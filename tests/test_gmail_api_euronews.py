from framework.browser.browser import Browser
from tests.config.urls import Urls
import allure
from tests.utils.gmail_api_utils import GmailApiUtils
from tests.test_data.gmail_test_data import email, password, endpoint_for_auth_page,\
                                            client_id, client_secret, redirect_uri
from tests.pages.auth_page import AuthPage
from tests.pages.euronews_home_page import EuronewsHomePage
from tests.pages.newsletters_page import NewslettersPage

from tests.pages.mail_confirmation_page import MailConfirmationPage
from tests.pages.unsubscribe_page import UnsubscribePage


class TestGmailApiEuronews(object):

    def test_get_auth_code(self, create_browser):
        with allure.MASTER_HELPER.step("First step"):
            Browser.get_browser().set_url(url=Urls.GOOGLE_URL_AUTH + endpoint_for_auth_page)

            auth_page = AuthPage()

            auth_page.enter_email(email)
            auth_page.click_next_block_auth_button()
            auth_page.enter_password(password)
            auth_page.click_next_block_auth_button()
            auth_page.click_additional_setting_label()
            auth_page.click_select_recommended_account()
            auth_page.click_continue_btn_in_terms_of_use()

            auth_code = auth_page.get_auth_code()

            gmail_api_util = GmailApiUtils()

            access_token = (gmail_api_util.get_access_token(auth_code,
                                                            client_id,
                                                            client_secret,
                                                            redirect_uri))

            params = {"code": f"{auth_code}",
                      "access_token": f"{access_token}",
                      "format": "full"}

            amount_of_messages_before_subscribe = gmail_api_util.get_amount_of_messages(params)

            Browser.get_browser().set_url(url=Urls.EURO_NEWS_URL)

            euronews_home_page = EuronewsHomePage()

            assert euronews_home_page.is_opened(), "EuronewsHomePage wasn't opened"

            euronews_home_page.click_accept_cookies_button()
            euronews_home_page.click_newsletters_label()

            newsletters_page = NewslettersPage()

            assert newsletters_page.is_opened(), "NewslettersPage wasn't opened"

            random_subscription_num = newsletters_page.get_random_newsletter_subscription_number()
            newsletters_page.click_random_newsletter_subscription(random_subscription_num)

            assert newsletters_page.is_email_fill_form_opened(), "Email fill form wasn't opened"

            newsletters_page.enter_email(email)
            newsletters_page.click_submit_btn()
            newsletters_page.click_close_additional_modal_window()
            amount_of_messages_after_subscribe = gmail_api_util.get_amount_of_messages(params)
            new_amount_of_messages_after_subscribe = gmail_api_util.get_amount_of_messages_with_wait_for_new_message(
                amount_of_messages_before_subscribe, amount_of_messages_after_subscribe, params)

            assert int(amount_of_messages_before_subscribe) != int(new_amount_of_messages_after_subscribe), \
                "The number of letters in the mail has not changed"

            last_message_id = gmail_api_util.get_id_from_last_message(email, params)
            confirm_url = gmail_api_util.get_confirm_email_link_from_last_message(email,
                                                                                  last_message_id,
                                                                                  params)

            Browser.get_browser().set_url(f"{confirm_url}")

            mail_confirmation_page = MailConfirmationPage()

            assert mail_confirmation_page.is_opened(), "MailConfirmationPage wasn't opened"

            mail_confirmation_page.click_back_to_site_btn()
            euronews_home_page.wait_for_page_opened()

            assert euronews_home_page.is_opened(), "EuronewsHomePage wasn't opened"

            euronews_home_page.click_newsletters_label()
            newsletters_page.wait_for_page_opened()
            newsletters_page.click_random_newsletter_subscription(random_subscription_num)
            newsletters_page.click_preview_is_selected_block()
            unsubscribe_link = newsletters_page.get_unsub_link()

            Browser.get_browser().set_url(f"{unsubscribe_link}")

            unsub_page = UnsubscribePage()

            unsub_page.wait_for_page_opened()

            assert unsub_page.is_opened(), "UnsubscribePage wasn't opened"

            unsub_page.enter_email(email)
            unsub_page.click_unsub_btn()

            assert unsub_page.is_successfully_unsub_text_presents(), "Successfully unsubscribe text isn't presents"

            amount_of_messages_after_unsubscribe = gmail_api_util.get_amount_of_messages(params)

            assert new_amount_of_messages_after_subscribe == amount_of_messages_after_unsubscribe, \
                "A new letter has arrived in the mail"
