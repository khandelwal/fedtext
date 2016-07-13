import scrapy
from bs4 import BeautifulSoup
from bs4.element import Comment

from fedtext.items import FedtextItem

class TutorialSpider(scrapy.Spider):
    name = "tutorialspider"
    allowed_domains = ['*.gov']
    start_urls = ['http://www.recreation.gov']

    def visible(self, element):
        """ Return True if the element text is visible (in the rendered sense),
        False otherwise. This returns False on empty strings """
        
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return False
        elif isinstance(element, Comment):
            return False
        else: 
            return element.strip()

    def parse(self, response):
        """ Callback method for parsing the response. Yields a FedtextItem.  """

        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
        texts = soup.findAll(text=True)
        visible_texts = [t.strip() for t in texts if self.visible(t)]
        item = FedtextItem()
        item['text_list'] = visible_texts
        yield item
