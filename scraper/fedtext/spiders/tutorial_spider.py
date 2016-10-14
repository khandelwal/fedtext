import scrapy
import csv
from bs4 import BeautifulSoup
from bs4.element import Comment, Doctype

from scrapy.http.request import Request

from fedtext.items import FedtextItem

def visible(element):
    """ Return True if the element text is visible (in the rendered sense),
    False otherwise. This returns False on empty strings """

    not_visible = ['style', 'script', '[document]', 'head', 'title']

    if element.parent.name in not_visible:
        return False
    elif isinstance(element, Comment) or isinstance(element, Doctype):
        return False
    else:
        return element.strip()


class TutorialSpider(scrapy.Spider):
    name = "tutorialspider"
    allowed_domains = ['*.gov']
    start_urls = []

    def __init__(self, *args, **kwargs):
        super(TutorialSpider, self).__init__(*args, **kwargs)

        # Get the file containing a list of URLs from the command line.
        self.file_with_urls = kwargs.get('url_file')

    def start_requests(self):
        """ Populate start_urls dynamically """
        # start_urls = ['http://www.recreation.gov']
        # from: http://stackoverflow.com/questions/9322219/how-to-generate-the-start-urls-dynamically-in-crawling
        with open(self.file_with_urls, 'r') as data_file:
            url_reader = csv.DictReader(data_file)
            for row in url_reader:
                url = "".join(["http://", row['Domain Name']])
                yield Request(url, self.parse)

    def parse(self, response):
        """
            Callback method for parsing the response. Yields a FedtextItem.
        """

        soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
        texts = soup.findAll(text=True)

        # Remove duplicate statements, only grab what's visible
        visible_texts = list(set([t.strip() for t in texts if visible(t)]))
        
        item = FedtextItem()
        item['text_list'] = visible_texts
        item['word_list'] = []
        item['word_frequency'] = []
        item['link'] = response.url
        item['title'] = soup.title.text

        yield item
