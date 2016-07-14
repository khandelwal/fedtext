# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

### OVERALL PIPELINE PLAN:
    # Take page_body, which should be webpage body content
    # PreProcess and Clean Data
    # Split words by: SPACE, PUNCTUATION
    # Filter out: STOP_WORDS, 
    # Make Frequency Count
#
# This could be done by a single processer but is implemented in / as
#   multiple stages for simplicity / experimentation / maintainability
#
### Note see ../settings.py to ensure ITEM_PIPELINES matches ideal order
### Examples: http://doc.scrapy.org/en/latest/topics/item-pipeline.html#topics-item-pipeline
###

from collections import Counter

from nltk.corpus import stopwords
english_stops = set(stopwords.words('english'))
from nltk.tokenize import RegexpTokenizer
## PreLoading so the pickle import cost isn't paid by every item
tokenizer = RegexpTokenizer("[\w']+") 

########## Random Thoughts ###############
## Might want to expand for word Coallitions another time
####    http://techbus.safaribooksonline.com/book/programming/python/9781849513609/firstchapter#X2ludGVybmFsX0h0bWxWaWV3P3htbGlkPTk3ODE4NDk1MTM2MDklMkZjaDAxbHZsMXNlYzE1JnF1ZXJ5PQ==
### Also Lemmatizing in place of (any future) Stemming: http://techbus.safaribooksonline.com/book/programming/python/9781849513609/firstchapter#X2ludGVybmFsX0h0bWxWaWV3P3htbGlkPTk3ODE4NDk1MTM2MDklMkZjaDAybHZsMXNlYzE4JnF1ZXJ5PQ==
####
########## Useful ##################
###
### http://www.nltk.org/book/ch03.html
###


class Clean(object):
    ''' Used in pipeline processing to split words '''
    def process_item(self, item, spider):
        ### Note: as of now this removes some signal from "word frequency" because repeated phrases will be lost
        ###         however repeated words in different phrases won't be lost
        item['text_list'] = list(set(item['text_list']))
        return item

### Maybe Clean and Remove should be combined ?
class Remove(object):
    ''' Used in pipeline processing to remove any particularly non-words '''
    ##this may have to become a regexp e.g. "starts with" or something in the future
    dead_text = [u'html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"', u'|']

    def process_item(self, item, spider):
        item['text_list'] = [word for word in item['text_list'] if word not in self.dead_text]
        return item

class Split(object):
    ''' Used in pipeline processing to split words '''
    def process_item(self, item, spider):
        item['word_list'] = tokenizer.tokenize( "".join( item['text_list'] ) )
        return item

class Filter(object):
    ''' Used in pipeline processing to filter common words '''
    def process_item(self, item, spider):
        item['text_list'] = [word for word in item['text_list'] if word not in english_stops]
        return item

class FrequencyCount(object):
    ''' Used in pipeline processing to remove non-words '''
    def process_item(self, item, spider):
        item['word_frequency'] = Counter( item['word_list'] )
        return item

class Final(object):
    ''' Used in pipeline for any final processing | debugging '''
    def process_item(self, item, spider):
        return item
