from unittest import TestCase
from altmetric_library import *
import json

__author__ = 'Lauren'


class TestAltmetric(TestCase):
    def setUp(self):
        self.alt = Altmetric()

    def test_article_from_doi_wrong(self):
        article = self.alt.article_from_doi('a')
        self.assertFalse(article)

    def test_article_from_doi_correct(self):
        article = self.alt.article_from_doi('10.1371/journal.pone.0000308')
        self.assertTrue(article)

        #should i write exceptions for if a key doesnt look like the correct type

    def test_article_from_pmid_wrong(self):
        article = self.alt.article_from_pmid('a')
        self.assertFalse(article)

    def test_article_from_pmid_correct(self):
        article = self.alt.article_from_pmid('21148220')
        self.assertTrue(article)

    def test_article_from_altmetric_wrong(self):
        article = self.alt.article_from_altmetric('a')
        self.assertFalse(article)

    def test_article_from_altmetric_correct(self):
        article = self.alt.article_from_altmetric('241939')
        self.assertTrue(article)

    def test_article_from_ads_wrong(self):
        article = self.alt.article_from_ads('a')
        self.assertFalse(article)

    def test_article_from_ads_correct(self):
        article = self.alt.article_from_ads('2012apphl.100y3104b')
        self.assertTrue(article)

    def test_article_from_arxiv_wrong(self):
        article = self.alt.article_from_arxiv('a')
        self.assertFalse(article)

    def test_article_from_arxiv_correct(self):
        article = self.alt.article_from_arxiv('1108.2455')
        self.assertTrue(article)

    def test_articles_from_timeframe_wrong(self):
        articles = self.alt.articles_from_timeframe('d')
        self.assertFalse(list(articles))

    def test_articles_from_timeframe_correct(self):
        articles = self.alt.articles_from_timeframe('1d')
        self.assertTrue(articles)

    def test_articles_from_timeframe_full(self):
        articles = self.alt.articles_from_timeframe('1d', num_results = 100,
        doi_prefix = '10.1038', nlmid = None, subjects = None, cited_in = None)
        self.assertTrue(articles)

        #use moking?
        #doesnt show full coverage because doenst go through the generator
        # unless i use it
        #should i check more more with what is happening using different kwargs?
        #I should check the formatting of the strings?

    def test__get_altmetrics_average(self):
        response = self.alt._get_altmetrics('doi','10.1038/nature.2014.14583')
        self.assertIsInstance(response, dict)

    def test__get_altmetrics_empty(self):
        response = self.alt._get_altmetrics('doi')
        self.assertFalse(response)

    def test__get_altmetrics_not_authorized(self):
        self.assertRaises(AltmetricHTTPException, self.alt._get_altmetrics,
            'fetch', 'doi','10.1038/nature.2014.14583')


        #should i check if the method is one of the correct methods
        #when i first run the program and throw an error there?
        #need to use mock for this for the json parse exception

    def test__create_article(self):
        article = self.alt._create_article(None)
        self.assertFalse(article)