"""
This is a python library for the altmetrics API.
It allows a user to access information about a specific
article by supplying DOI,  arXiv ID, PMID, ADS bibcode,
or Altmetric ID. Users should avoid Altmetric ID's because
they are subject to change. 
"""

import requests
import datetime
import warnings


class AltmetricException(Exception):
    """Base class for any altmetric_library error."""
    pass

class AltmetricParseException(AltmetricException):
    """A query argument or setting was formatted incorrectly."""
    def __init__(self):
        self.msg = "Something was formatted incorrectly."

class AltmetricHTTPException(AltmetricException):
    """A query argument or setting was formatted incorrectly."""
    def __init__(self, status_code):
            response_codes = {403:"You are not authorized for this call.",
                          420:"Rate Limit Reached",
                          502:"API is down."}
            self.status_code = status_code
            self.msg = response_codes[status_code]


class Altmetric():
    def __init__(self, api_key = None, api_version = 'v1'):
        """Cache API key and version."""
        self._api_key = api_key
        self._api_version = api_version
        if self._api_version != 'v1':
            warnings.warn("This library has only been tested with API v1.\
                If you try another version it will probably break.")

        if self._api_key:
            self._params = {'key': api_key}

        self._api_url = "http://api.altmetric.com/%s/" % self.api_version

    #Make articles
    def from_doi(self, doi):
        """Create an Article object using DOI"""
        return Article(self, doi, 'doi')

    def from_pmid(self, pmid):
        """Create an Article object using PMID"""
        return Article(self, pmid, 'pmid')
    
    def from_altmetric(self, altmetric_id):
        """Create an Article object using Altmetric ID"""
        return Article(self. altmetric_id, 'id')

    def from_ads(self, ads_bibcode):
        """Create an Article object using ADS Bibcode"""
        return Article(self, ads_bibcode, 'ads')
    
    def from_arxiv(self, arxiv_id):
        """Create an Article object using arXiv ID"""
        return Article(self, arxiv_id, 'arxiv')

    @property
    def api_version(self):
        return self._api_version

    @property
    def api_url(self):
        return self._api_url

    @property
    def key(self):
        return self._params


class Article():

    
    def __init__(self, altmetric, id_key, id_type="doi"):
        """
        Create an article object. Get raw dictionary from
        Altmetrics JSON. Parse dictionary into attributes.
        """
        self._raw  = self.get_altmetrics(altmetric, id_key,id_type)
        if self._raw:
            self._parse_raw()
       
    def _parse_raw(self):
        """Extract all attributes from raw dictionary"""
        #Article Info
        self._title = self._raw.get('title')
        self._abstract = self._raw.get('abstract')
        self._abstract_scource = self._raw.get('abstract_source')
        self._journal = self._raw.get('journal')
        self._subjects = self._raw.get('subjects', [])
        self._added_on = self._convert_to_utc(self._raw.get('added_on'))
        self._published_on = self._convert_to_utc(self._raw.get('published_on'))
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
        self._score_history = self._parse_score_history(self._raw.get('history', {}))
        self._score_context = self._parse_score_context(self._raw.get('context', {}))  
        self._last_updated = self._convert_to_utc(self._raw.get('last_updated'))
        self._downloads = self._raw.get('downloads', 0)
        
        self._schema  = self._raw.get('schema') #FIX schema for what
        
        self._cited_by_facebook_walls_count = self._raw.get('cited_by_fbwalls_count', 0)
        self._cited_by_redits_count = self._raw.get('cited_by_rdts_count', 0)
        self._cited_by_tweeters_count = self._raw.get('cited_by_tweeters_count', 0)
        self._cited_by_google_plus_count = self._raw.get('cited_by_gplus_count', 0)
        self._cited_by_msm_count = ('cited_by_msm_count', 0)
        self._cited_by_delicious_count = ('cited_by_delicious _count', 0)
        self._cited_by_qs_count = self._raw.get('cited_by_qs_count', 0)
        self._cited_by_posts_count = self._raw.get('cited_by_posts_count', 0)
        self._cited_by_accounts_count = self._raw.get('cited_by_accounts_count', 0) or \
        self._raw.get('by_accounts_count', 0)
        self._cited_by_forums_count = ('cited_by_forum_count', 0)
        self._peer_review_sites_count = ('cited_by_peer_review_sites_count', 0)
        self._cited_by_feeds_count = ('cited_by_feeds_count', 0)
        self._cited_by_videos_count = ('cited_by_videos_count', 0)


        self._cohorts = self._raw.get('cohorts', {}) #FIX what is this
        
        self._readers_count = ('readers_count', 0)
        self._readers = self._raw.get('readers', {})
        
        self._altmetric_details_url = self._raw.get('details_url',)

        self._altmetric_images = self._raw.get('images', {})
    
    def get_altmetrics(self, altmetric, id_key_, id_type_):
        """Check server response. Return dictionary from JSON if possible."""
        request_url = "{base_url}{id_type}/{id_key}".format\
                (base_url = altmetric.api_url, id_type = id_type_, id_key = id_key_)
        response = requests.get(request_url, params = altmetric.key)
        if response.status_code == 200:
            try:
                return response.json()
            except ValueError as e:
                raise ParseException(e.message)
        elif response.status_code == 404:
            return {}
        else:
            raise AltmetricHTTPException(response_codes)
        
    def _convert_to_utc(self,unix_time):
        """Convert UNIX timestamp to UTC."""
        if unix_time:
            return datetime.datetime.fromtimestamp(unix_time).strftime('%Y-%m-%dT%H:%M:%Sz')

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


    def _parse_publisher_subjects(self, subjects):
        """Turns the publisher_subjects list of dictionaries into a list of subjects."""
        new_subjects = []
        if subjects:
            for item in subjects:
                new_subjects.append(item['name'])
        return new_subjects

    def _parse_score_context(self, context): #FIX possibally change the word percent
        """Change the names of the dictionaries in context to make more sense."""
        new_context = {}
        if context:
            new_context['journal age'] = context.get('similar_age_journal_3m', {})
            new_context['context age'] = context.get('similar_age_3m', {})
            new_context['journal'] = context.get('journal', {})
        return new_context
        
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
        return self._tq
    
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
    def downloads(self):
        return self._downloads
    
    @property
    def score_context(self):
        """
        Return a dictionary that allows you to compare an article's popularity to
        articles of a 'similar age'(published within 6 weeks on either side), articles
        in journals of a 'similar age', and other articles in the same 'journal'.
        """
        return self._score_context
    
    
    #Cited by - Returns count of unique authors for posts cited on various medias.
    @property
    def cited_by_facebook_walls_count(self):
        """Return number of posts made on public facebook walls mentioning chozen article."""
        return  self._cited_by_facebook_walls_count 
    
    @property
    def cited_by_redits_count(self):
        return self._redit_mentions
    @property
    def cited_by_tweeters_count(self):
        return scited_by_tweeters_count
    
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
    def cited_by_peer_review_count(self):
        return self._cited_by_peer_review_count
    
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
        Return a  dictionary that contains information about the numbers of readers on
        various reference manager websites. The website name is the key and the number of
        readers is the value. Ex. {'mendeley': 11, , 'citeulike': 0, 'connotea' : 4}
        """
        return self._readers

    @property
    def cohorts(self): #FIX maybe change so more clear
        """
        Return a dictionary with the number of people mentioning this article who are
        members of the public (pub), practitioners (doc), research scientists (sci) or
        science communicators (com) (This is an experimental Altmetric feature).
        """
        return self._cohorts
    
    @property
    def altmetric_details_url(self):
        return self._altmetric_details_url
    
    #Altmetric Score Images
    @property
    def altmetric_images(self):
        """
        Return a dictionary of the altmetric score image in 'small', 'medium', and 'large'
        """
        return self._altmetric_images


if __name__ == "__main__": #for mini tests
    api_key = ''
    with open("altmetric_api_key.txt", "r") as f:
        api_key = f.read()

    metric_object = Altmetric(api_key)
    arxiv = metric_object.from_arxiv("1108.2455")
    
    print arxiv

