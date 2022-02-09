import lxml.html as lh
from framework.utils.api_util import APIUtil
from tests.config.urls import Urls
import requests
from tests.utils.get_confirm_url_with_bs4 import get_unsub_link
from framework.utils.logger import Logger


class IFrameParseUtil:

    iframe_parse_util = APIUtil(f"{Urls.EURO_NEWS_URL_NEWSLETTERS}")

    def get_content(self):
        Logger.info("Getting content")
        resp = self.iframe_parse_util.send_get_req("")
        return resp.content

    def get_unsubscribe_link(self, iframe_locator):
        Logger.info("Getting unsubscribe link")
        resp_content = self.get_content()
        doc = lh.fromstring(resp_content)
        for i, elt in enumerate(doc.xpath(f"{iframe_locator}")):
            url_data = elt.attrib.get('src')
            content = requests.get(url_data).content
            return get_unsub_link(str(content))


