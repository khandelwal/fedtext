# fedtext
A text analysis of Federal websites

## Installation

See requirements.txt for the libraries this uses. 

For nltk, you'll need to download the stopwords copora. Open a Python 
console and do the following: 

>>> import nltk
>>> nltk.download("stopwords")

## Sample Run Commands
* `scrapy crawl tutorialspider`
* `scrapy crawl tutorialspider -o items.json`
https://github.com/GSA/data/tree/gh-pages/dotgov-domains

## Current Federal Data optained from:
* https://raw.githubusercontent.com/GSA/data/gh-pages/dotgov-domains/current-federal.csv
