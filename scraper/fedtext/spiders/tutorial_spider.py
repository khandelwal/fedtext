import scrapy
import csv
from bs4 import BeautifulSoup
from bs4.element import Comment

from scrapy.http.request import Request

from fedtext.items import FedtextItem

class TutorialSpider(scrapy.Spider):
    name = "tutorialspider"
    allowed_domains = ['*.gov']
    start_urls = []

    def __init__(self, *args, **kwargs):
        super(TutorialSpider, self).__init__(*args, **kwargs)

        #Get the file containing a list of URLs from the command line.
        self.file_with_urls = kwargs.get('url_file')
        

    def start_requests(self):
        """ Populate start_urls dynamically """
        #start_urls = ['http://www.recreation.gov']
        #from: http://stackoverflow.com/questions/9322219/how-to-generate-the-start-urls-dynamically-in-crawling
        with open(self.file_with_urls, 'r') as data_file:
            url_reader = csv.DictReader(data_file)
            for row in url_reader:
                url = "".join([ "http://", row['Domain Name']])
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
        item['word_list'] = []
        item['word_frequency'] = []
        item['link'] = response.url
        item['title'] = soup.title.text
        yield item
