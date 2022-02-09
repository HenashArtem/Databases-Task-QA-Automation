from framework.utils.api_util import APIUtil
from tests.utils.message_model import MessageModel
from tests.config.urls import Urls
from framework.utils.logger import Logger
from tests.utils.base64_util import base64_decode
from tests.utils.get_confirm_url_with_bs4 import get_confirm_url_from_text
import time


class GmailApiUtils:
    gmail_api_util_token = APIUtil(f"{Urls.GOOGLE_URL_TOKEN}")
    gmail_api_util = APIUtil(f"{Urls.GMAIL_API_URL}")

    def get_access_token(self, code, client_id, client_secret, redirect_uri):
        self.gmail_api_util_token.send_post_req(endpoint="",
                                                post_data={
                                                    "code": f"{code}",
                                                    "client_id": f"{client_id}",
                                                    "client_secret": f"{client_secret}",
                                                    "redirect_uri": f"{redirect_uri}",
                                                    "grant_type": "authorization_code"
                                                })
        resp = self.gmail_api_util_token.response_to_json()
        model_of_resp = MessageModel(**resp)
        Logger.info("Getting access_token")
        return model_of_resp.get_data("access_token")

    def get_amount_of_messages(self, params):
        self.gmail_api_util.send_get_req(f"/gmail/v1/users/me/messages", params)
        resp = self.gmail_api_util.response_to_json()
        list_of_messages = list(resp["messages"])
        return len(list_of_messages)

    def get_amount_of_messages_with_wait_for_new_message(self, amount_before_subscribe, amount_after_subscribe, params):
        while amount_before_subscribe == amount_after_subscribe:
            current_amount_of_messages = self.get_amount_of_messages(params)
            time.sleep(1)
            if current_amount_of_messages != amount_before_subscribe:
                return current_amount_of_messages

    def get_id_from_last_message(self, email, params):
        self.gmail_api_util.send_get_req(f"/gmail/v1/users/{email}/messages", params)
        resp = self.gmail_api_util.response_to_json()
        last_message = resp["messages"][0]
        return last_message.get("id")

    def get_confirm_email_link_from_last_message(self, email, message_id, params):
        self.gmail_api_util.send_get_req(f"/gmail/v1/users/{email}/messages/{message_id}", params)
        resp = self.gmail_api_util.response_to_json()
        base64_text = base64_decode((resp['payload']['parts'][0]['body']['data']))
        return get_confirm_url_from_text(base64_text)
