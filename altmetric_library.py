"""
This is a python library for the Altmetric API.

For more information on the Altmetric API visit http://api.altmetric.com/.

Some pieces of this library were inspired by or derived from the altmetric api
wrapper altmetric.py which is licensed under the MIT open source license.
"""

#raise exceptions
#fix timeframe to have everything
#altmetric jid?

import requests
import datetime
import warnings
import json

class AltmetricException(Exception):
    """Base class for any altmetric_library error."""
    pass

class JSONParseException(AltmetricException):
    """
    Failed to turn HTTP Response into JSON.
    Site is probably in the wrong format.
    """
    pass

class IDTypeMismatch(AltmetricException):
    """
    The ID entered does not match the type you selected.
    """
    pass

class AltmetricHTTPException(AltmetricException):
    """A query argument or setting was formatted incorrectly."""
    def __init__(self, status_code):
        response_codes = {
            403:"You are not authorized for this call.",
            420:"Rate Limit Reached",
            502:"API is down.",
        }
        super(AltmetricHTTPException, self).__init__(
            response_codes.get(status_code, status_code)
        )

class Altmetric(object):
    def __init__(self, api_key = None, api_version = 'v1'):
        """Cache API key and version."""
        self._api_version = api_version
        if self._api_version != 'v1':
            warnings.warn("This library has only been tested with API v1.\
                If you try another version it will probably break.")

        self._api_url = "http://api.altmetric.com/%s/" % self.api_version

        self._api_key = {}
        if api_key:
            self._api_key = {'key': api_key}

    #Make articles
    def article_from_doi(self, doi):
        """Create an Article object using DOI."""
        raw_json = self._get_altmetrics('doi', doi)
        return self._create_article(raw_json)

    def article_from_pmid(self, pmid):
        """Create an Article object using PMID."""
        raw_json = self._get_altmetrics('pmid', pmid)
        return self._create_article(raw_json)
    
    def article_from_altmetric(self, altmetric_id):
        """Create an Article object using Altmetric ID."""
        warnings.warn("Altmetric ID's are subject to change.")
        raw_json = self._get_altmetrics('id', altmetric_id)
        return self._create_article(raw_json)

    def article_from_ads(self, ads_bibcode):
        """Create an Article object using ADS Bibcode."""
        raw_json = self._get_altmetrics('ads', ads_bibcode)
        return self._create_article(raw_json)
    
    def article_from_arxiv(self, arxiv_id):
        """Create an Article object using arXiv ID."""
        raw_json = self._get_altmetrics('arxiv', arxiv_id)
        return self._create_article(raw_json)

    def articles_from_timeframe(self, timeframe, page = 1, num_results = 100,
        doi_prefix = None, nlmid = None, subjects = None, cited_in = None):

        #timeframe = self._check_timeframe(timeframe)
        #should I collect metadata about the query? where do i store that?

        while(1):
            raw_json = self._get_altmetrics('citations', timeframe,
                page = page, num_results = num_results,
                doi_prefix = doi_prefix, nlmid = nlmid,
                subjects = subjects, cited_in = cited_in)
            page += 1
            if not raw_json:
                break
            for result in raw_json.get('results', []):
                yield self._create_article(result)

    def _convert_to_dict(self, raw):
        try:
            if isinstance(raw, file):
                return json.load(raw)
            elif isinstance(raw, requests.Response):
                return raw.json()

        except ValueError as e:
            raise JSONParseException(e.message)

    def _get_altmetrics(self, method, *args, **kwargs):
        """
        Request information from Altmetric. Return a dictionary.
        """
        request_url = self.api_url + method + "/" + "/".join([a for a in args])
        params = kwargs or {}
        params.update(self.api_key)
        response = requests.get(request_url, params = params)
        if response.status_code == 200:
            return self._convert_to_dict(response)
        elif response.status_code in (404, 400): #should i handle this differently
            return {}
        else:
            raise AltmetricHTTPException(response.status_code)

    def _create_article(self, json):
        try:
            return Article(json)
        except AttributeError:
            return None

    @property
    def api_version(self):
        return self._api_version

    @property
    def api_url(self):
        return self._api_url

    @property
    def api_key(self):
        return self._api_key


class Article():
    def __init__(self, raw_json):
        """
        Create an article object. Get raw dictionary from
        Altmetrics JSON. Parse dictionary into attributes.
        """
        if raw_json:
            self._raw  = raw_json
            self._parse_raw()
        else:
            raise AttributeError
       
    def _parse_raw(self):
        """Extract all attributes from raw dictionary"""
        #Article Info
        self._title = self._raw.get('title')
        self._abstract = self._raw.get('abstract')
        self._abstract_source = self._raw.get('abstract_source')
        self._journal = self._raw.get('journal')
        self._subjects = self._raw.get('subjects', [])
        self._added_on = self._convert_to_utc(self._raw.get('added_on'))
        self._published_on = self._convert_to_utc(
            self._raw.get('published_on'))
        self._url = self._raw.get('url')
        self._is_open_access = self._raw.get('is_oa')

        self._scopus_subjects = self._raw.get('scopus_subjects', [])
        self._publisher_subjects = self._parse_publisher_subjects\
        (self._raw.get('publisher_subjects',[])) #FIX? am i losing info

        self._taglines = self._raw.get('tq', [])
        
        #Various ID's
        self._doi = self._raw.get('doi')
        self._nlmid = self._raw.get('nlmid')
        self._pmid = self._raw.get('pmid')
        self._altmetric_id = self._raw.get('altmetric_id')
        self._arxiv_id = self._raw.get('arxiv_id')
        self._ads_id = self._raw.get('ads_id')
        self._issns = self._raw.get('issns', [])
        
        #Altmetrics
        self._score = self._raw.get('score')
        self._score_history = self._parse_score_history(
            self._raw.get('history', {}))
        self._score_context = self._parse_score_context(
            self._raw.get('context', {}))  
        self._last_updated = self._convert_to_utc(
            self._raw.get('last_updated'))
        #self._downloads = self._raw.get('downloads', 0)
        self._schema  = self._raw.get('schema') #FIX schema for what
        
        self._cited_by_facebook_walls_count = self._raw.get(
            'cited_by_fbwalls_count', 0)
        self._cited_by_redits_count = self._raw.get('cited_by_rdts_count', 0)
        self._cited_by_tweeters_count = self._raw.get(
            'cited_by_tweeters_count', 0)
        self._cited_by_google_plus_count = self._raw.get(
            'cited_by_gplus_count', 0)
        self._cited_by_msm_count = self._raw.get('cited_by_msm_count', 0)
        self._cited_by_delicious_count = self._raw.get('cited_by_delicious_count', 0)
        self._cited_by_qs_count = self._raw.get('cited_by_qs_count', 0)
        self._cited_by_posts_count = self._raw.get('cited_by_posts_count', 0)
        self._cited_by_accounts_count = (
            self._raw.get('cited_by_accounts_count', 0)
            or self._raw.get('by_accounts_count', 0)
        )

        self._cited_by_forums_count = self._raw.get('cited_by_forums_count', 0)
        self._cited_by_peer_review_sites_count = self._raw.get(
            'cited_by_peer_review_sites_count', 0)
        self._cited_by_feeds_count = self._raw.get('cited_by_feeds_count', 0)
        self._cited_by_videos_count = self._raw.get('cited_by_videos_count', 0)


        self._cohorts = self._raw.get('cohorts', {})
        
        self._readers_count = self._raw.get('readers_count', 0)
        self._readers = self._raw.get('readers', {})
        
        self._altmetric_details_url = self._raw.get('details_url',)

        self._altmetric_images = self._raw.get('images', {})


    #Specific methods for reformatting dictionaries/lists that are difficult to read.        
    def _parse_score_history(self, history):
        """Make the score_history dictionary a little more readable."""
        new_dictionary = {}
        if history:
            change = {'d':'day','m':'month','w':'week','y':'year'}
            for item in history:
                if item == 'at':
                    date = "all time"
                else:
                    if item[0] == '1':
                        date = "past " + change[item[1]]
                    else:
                        date = "past " + item[0]+ " " + change[item[1]]+"s" 
                new_dictionary[date] = history[item]
        return new_dictionary

    def _convert_to_utc(self, unix_time):
        """Convert UNIX timestamp to UTC."""
        if isinstance(unix_time, int): #this line could cause us to lose data
            return datetime.datetime.fromtimestamp(unix_time).strftime(
                '%Y-%m-%dT%H:%M:%SZ')

    def _parse_publisher_subjects(self, subjects):
        """
        Turns the publisher_subjects list of dictionaries into a list of 
        subjects.
        """
        new_subjects = []
        if subjects:
            for item in subjects:
                new_subjects.append(item['name'])
        return new_subjects

    def _parse_score_context(self, context): #FIX possibally change the word percent
        """
        Change the names of the dictionaries in context to make more sense.
        """
        new_context = {}
        if context:
            new_context['all'] = context.get(
                'all', {})
            new_context['journal age'] = context.get(
                'similar_age_journal_3m', {})
            new_context['context age'] = context.get(
                'similar_age_3m', {})
            new_context['journal'] = context.get('journal', {})
        return new_context

    def __repr__(self): #FIX unicode problems
        return self.title[:12].encode('UTF-8')

    def __str__(self): #FIX unicode problems
        string = u""
        for item in self._raw:
            string += unicode(item) + u": " + unicode(self._raw[item]) + u'\n'
        return unicode(string).encode('UTF-8')
    
    #Basic info

    @property
    def raw_dictionary(self):
        return self._raw

    @property
    def title(self):
        return self._title
    
    @property
    def abstract(self):
        return self._abstract
    
    @property
    def abstract_source(self):
        return self._abstract_source
    
    @property
    def journal(self):
        return self._journal
    
    @property
    def subjects(self):
        """Return a list of realted subjects"""
        return self._subjects
    
    @property
    def scopus_subjects(self):
        """Return a list of Scopus subjects"""
        return self._scopus_subjects
    
    @property
    def publisher_subjects(self):
        """Return a list of related subjects."""
        return self._publisher_subjects
    
    @property
    def added_on(self):
        return self._added_on
    
    @property
    def published_on(self):
        return self._published_on
    
    @property
    def url(self):
        return self._url
    
    @property
    def is_open_access(self):
        return self._is_open_access 
    
    @property
    def taglines(self):
        """Return a list of related phrases"""
        return self._taglines
    
    #Various ID's
    @property
    def doi(self):
        return self._doi
    
    @property
    def nlmid(self):
        return self._nlmid
    
    @property
    def pmid(self):
        return self._pmid
    
    @property
    def altmetric_id(self):
        return self._altmetric_id
    
    @property
    def arxiv_id(self):
        return self._arxiv_id
    
    @property
    def ads_id(self):
        return self._ads_id
    
    @property
    def issns(self):
        """A list of issns."""
        return self._issns
    
    #Altmetrics
    @property
    def score(self):
        return self._score
    
    @property
    def score_history(self):
        """
        Return dictionry of Altmetric scores for time periods
        such as 'past day', 'past 3 days', 'past month', 'past year',
        and 'all time' looking only at that time period.
        """
        return self._score_history
    
    @property
    def last_updated(self):
        """Return when the Altmetrics were last updated."""
        return self._last_updated
    
    @property
    def score_context(self):
        """
        Return a dictionary that allows you to compare an article's popularity
        to articles of a 'similar age'(published within 6 weeks on either
        side), articles in journals of a 'similar age', and other articles in
        the same 'journal'.
        """
        return self._score_context
    
    
    #Cited by
    #Returns count of unique authors for posts cited on various medias.

    @property
    def cited_by_facebook_walls_count(self):
        """
        Return number of posts made on public facebook walls mentioning chozen
        article.
        """
        return  self._cited_by_facebook_walls_count 
    
    @property
    def cited_by_redits_count(self):
        return self._cited_by_redits_count
    @property
    def cited_by_tweeters_count(self):
        return self._cited_by_tweeters_count
    
    @property
    def cited_by_google_plus_count(self):
        return self._cited_by_google_plus_count
    
    @property
    def cited_by_msm_count(self):
        """Return number of citations from articles in science news outlets."""
        return self._cited_by_msm_count
    
    @property
    def cited_by_delicious_count(self):
        return self._cited_by_delicious_count

    @property
    def cited_by_qs_count(self):
        """
        Return number of citations from questions, answers or comments on Stack
        Exchange sites (inc. Biostar).
        """
        return self._cited_by_qs_count

    @property
    def cited_by_posts_count(self):
        return self._cited_by_posts_count

    @property
    def cited_by_forums_count(self):
        return self._cited_by_forums_count

    @property
    def cited_by_feeds_count(self):
        return self._cited_by_feeds_count

    @property
    def cited_by_peer_review_sites_count(self):
        return self._cited_by_peer_review_sites_count
    
    @property
    def cited_by_accounts_count(self):
        return self._cited_by_accounts_count
    
    @property
    def cited_by_videos_count(self):
        return self._cited_by_videos_count


    @property
    def readers_count(self):
        return self._readers_count
        
    @property
    def readers(self):
        """
        Return a  dictionary that contains information about the numbers of
        readers on various reference manager websites. The website name is the
        key and the number of readers is the value.
        Ex. {'mendeley': 11, , 'citeulike': 0, 'connotea' : 4}
        """
        return self._readers

    @property
    def cohorts(self): #FIX maybe change so more clear
        """
        Return a dictionary with the number of people mentioning this article
        who are members of the public (pub), practitioners (doc), research
        scientists (sci) or science communicators (com)
        (This is an experimental Altmetric feature).
        """
        return self._cohorts

    @property
    def schema(self):
        return self._schema

    @property
    def altmetric_details_url(self):
        return self._altmetric_details_url
    
    #Altmetric Score Images
    @property
    def altmetric_images(self):
        """
        Return a dictionary of the altmetric score image in
        'small', 'medium', and 'large'.
        """
        return self._altmetric_images


if __name__ == "__main__": #for mini tests

    api_key = ''
    with open("altmetric_api_key.txt", "r") as f:
        api_key = f.read()

    metric_object = Altmetric(api_key)
    #articles = metric_object.articles_from_timeframe("1d")
    article = metric_object.article_from_doi("10.1371/journal.pone.0000308")
    print article
    #for list_ in articles:
        #print list_

