from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)


def get_title(html_content):
    title = ""
    try:
        bs = BeautifulSoup(html_content, 'html.parser')
        title = bs.title.string

    except Exception as error:
        logger.error("Couldn't get the title from html content")
    return title
