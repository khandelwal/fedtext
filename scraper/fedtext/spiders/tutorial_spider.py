from urllib.parse import urlparse
import csv
import sys

import scrapy
from scrapy import Request

from bs4 import BeautifulSoup
from bs4.element import Comment, Doctype


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

def add_www(original_url):
    """ Take a URL such as http://18f.gov and return http://www.18f.gov """

    o = urlparse(original_url)
    return "http://www.{}".format(o.netloc)


class TutorialSpider(scrapy.Spider):
    name = "tutorialspider"
    start_urls = []
    handle_httpstatus_list = [404]

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

        if response.status == 404:
            original_url = response.url
            url = add_www(original_url)
            yield Request(url)
        else:
            soup = BeautifulSoup(response.body_as_unicode(), 'lxml')
            texts = soup.findAll(text=True)

            if soup.title:
                item = FedtextItem()
                # Some pages, like safetyact.gov don't have well-formed markup without 
                # JavaScript. 
                item['title'] = soup.title.text
                item['text_list'] = [t.strip() for t in texts if visible(t)]
                item['word_list'] = []
                item['word_frequency'] = []
                item['response_url'] = response.url

                if 'request_url' in response.request.meta:
                    item['request_url'] = response.request.meta['redirect_urls'][0]
                else:
                    item['request_url'] = response.url
                yield item
