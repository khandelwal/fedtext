import scrapy
from bs4 import BeautifulSoup
from bs4.element import Comment

from scrapy.http.request import Request

from fedtext.items import FedtextItem

class TutorialSpider(scrapy.Spider):
    name = "tutorialspider"
    allowed_domains = ['*.gov']
    start_urls = []

    # Overrride this function in the base class to populate start_urls dynamically 
    def start_requests(self):
        start_urls = ['http://www.recreation.gov']
        #from: http://stackoverflow.com/questions/9322219/how-to-generate-the-start-urls-dynamically-in-crawling
        #with open('urls.txt, 'rb') as urls:
        #    for url in urls:
        #        yield Request(url, self.parse)
        for url in start_urls:
            yield Request(url, self.parse)

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

        item['page_body'] = response.xpath('/html/body/text()').extract()
        yield item
