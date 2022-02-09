from bs4 import BeautifulSoup
from framework.utils.logger import Logger


def get_confirm_url_from_text(text: str):
    Logger.info("Getting confirm url from text")
    soup = BeautifulSoup(text, "lxml")
    return soup.find("div").find("a").get("href")


def get_unsub_link(text: str):
    Logger.info("Getting unsubscribe link")
    soup = BeautifulSoup(text, "lxml")
    list_of_a = list()
    for item in soup.find_all("a"):
        list_of_a .append(item.get("href"))
    for link in list_of_a:
        if "unsubscribe" in str(link):
            return link
