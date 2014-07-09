from unittest import TestCase
from altmetric_library import *
import json
import datetime
from mock import Mock

__author__ = 'Lauren Revere'

class TestArticle(TestCase):
    def setUp(self):
        with open('full.json') as raw_json:
            raw_dict = json.load(raw_json)
            self.art = Article(raw_dict)

    def test__parse_raw_empty(self):
        #An empty dictionary would never actually be passed to this
        self.art._raw = {}
        self.art._parse_raw()

        self.assertFalse(self.art.title)
        self.assertFalse(self.art.abstract)
        self.assertFalse(self.art.abstract_source)
        self.assertFalse(self.art.journal)
        self.assertFalse(self.art.subjects)
        self.assertIsInstance(self.art.subjects, list)
        self.assertFalse(self.art.added_on)
        self.assertFalse(self.art.published_on)
        self.assertFalse(self.art.url)
        self.assertFalse(self.art.is_open_access)
        self.assertFalse(self.art.scopus_subjects)
        self.assertIsInstance(self.art.scopus_subjects, list)
        self.assertFalse(self.art.publisher_subjects)
        self.assertIsInstance(self.art.publisher_subjects, list)
        self.assertFalse(self.art.taglines)
        self.assertIsInstance(self.art.taglines, list)

        self.assertFalse(self.art.doi)
        self.assertFalse(self.art.nlmid)
        self.assertFalse(self.art.pmid)
        self.assertFalse(self.art.altmetric_id)
        self.assertFalse(self.art.arxiv_id)
        self.assertFalse(self.art.ads_id)
        self.assertFalse(self.art.issns)
        self.assertIsInstance(self.art.issns, list)

        self.assertFalse(self.art.score)
        self.assertFalse(self.art.score_history)
        self.assertIsInstance(self.art.score_history, dict)
        self.assertFalse(self.art.score_context)
        self.assertIsInstance(self.art.score_context, dict)
        self.assertFalse(self.art.last_updated)
        self.assertFalse(self.art.schema)
        self.assertFalse(self.art.cited_by_facebook_walls_count)
        self.assertFalse(self.art.cited_by_redits_count)
        self.assertFalse(self.art.cited_by_tweeters_count)
        self.assertFalse(self.art.cited_by_google_plus_count)
        self.assertFalse(self.art.cited_by_msm_count)
        self.assertFalse(self.art.cited_by_delicious_count)
        self.assertFalse(self.art.cited_by_qs_count)
        self.assertFalse(self.art.cited_by_posts_count)
        self.assertFalse(self.art.cited_by_accounts_count)
        self.assertFalse(self.art.cited_by_forums_count)
        self.assertFalse(self.art.cited_by_peer_review_sites_count)
        self.assertFalse(self.art.cited_by_feeds_count)
        self.assertFalse(self.art.cited_by_videos_count)
        self.assertFalse(self.art.cohorts)
        self.assertFalse(self.art.readers_count)
        self.assertFalse(self.art.readers)
        self.assertIsInstance(self.art.readers, dict)
        self.assertFalse(self.art.altmetric_details_url)
        self.assertFalse(self.art.altmetric_images)
        self.assertIsInstance(self.art.altmetric_images, dict)


    def test__parse_raw_average(self):
        with open('average.json') as raw_json:
            raw_dict = json.load(raw_json)
            self.art._raw = raw_dict
            self.art._parse_raw()

        self.assertTrue(self.art.title)
        self.assertFalse(self.art.abstract)
        self.assertFalse(self.art.abstract_source)
        self.assertTrue(self.art.journal)
        self.assertTrue(self.art.subjects)
        self.assertIsInstance(self.art.subjects, list)

        self.assertTrue(self.art.added_on)
        self.assertIsInstance(self.art.added_on, datetime.datetime)

        self.assertTrue(self.art.published_on)
        self.assertIsInstance(self.art.published_on, datetime.datetime)

        self.assertTrue(self.art.url)
        self.assertFalse(self.art.is_open_access)
        self.assertIsInstance(self.art.is_open_access, bool)

        self.assertTrue(self.art.scopus_subjects)
        self.assertIsInstance(self.art.scopus_subjects, list)

        self.assertFalse(self.art.publisher_subjects)
        self.assertTrue(self.art.taglines)
        self.assertIsInstance(self.art.taglines, list)

        self.assertTrue(self.art.doi)
        self.assertTrue(self.art.nlmid)
        self.assertFalse(self.art.pmid)
        self.assertTrue(self.art.altmetric_id)
        self.assertFalse(self.art.arxiv_id)
        self.assertFalse(self.art.ads_id)
        self.assertTrue(self.art.issns)
        self.assertIsInstance(self.art.taglines, list)

        self.assertTrue(self.art.score)
        self.assertIsInstance(self.art.score, float)

        self.assertTrue(self.art.score_history)
        self.assertIsInstance(self.art.score_history, dict)

        self.assertTrue(self.art.score_context)
        self.assertIsInstance(self.art.score_context, dict)

        self.assertTrue(self.art.last_updated)
        self.assertIsInstance(self.art.last_updated, datetime.datetime)

        self.assertTrue(self.art.schema)
        self.assertTrue(self.art.cited_by_facebook_walls_count)
        self.assertIsInstance(self.art.cited_by_facebook_walls_count, int)

        self.assertTrue(self.art.cited_by_redits_count)
        self.assertIsInstance(self.art.cited_by_redits_count, int)

        self.assertTrue(self.art.cited_by_tweeters_count)
        self.assertIsInstance(self.art.cited_by_tweeters_count, int)

        self.assertFalse(self.art.cited_by_google_plus_count)

        self.assertTrue(self.art.cited_by_msm_count)
        self.assertIsInstance(self.art.cited_by_msm_count, int)

        self.assertFalse(self.art.cited_by_delicious_count)
        self.assertFalse(self.art.cited_by_qs_count)

        self.assertTrue(self.art.cited_by_posts_count)
        self.assertIsInstance(self.art.cited_by_posts_count, int)

        self.assertTrue(self.art.cited_by_accounts_count)
        self.assertIsInstance(self.art.cited_by_accounts_count, int)

        self.assertFalse(self.art.cited_by_forums_count)

        self.assertFalse(self.art.cited_by_peer_review_sites_count)

        self.assertTrue(self.art.cited_by_feeds_count)
        self.assertIsInstance(self.art.cited_by_feeds_count, int)

        self.assertFalse(self.art.cited_by_videos_count)

        self.assertTrue(self.art.cohorts)
        self.assertIsInstance(self.art.cohorts, dict)

        self.assertTrue(self.art.readers_count)
        self.assertIsInstance(self.art.readers_count, int)

        self.assertTrue(self.art.readers)
        self.assertIsInstance(self.art.readers, dict)

        self.assertTrue(self.art.altmetric_details_url)
        self.assertTrue(self.art.altmetric_images)
        self.assertIsInstance(self.art.altmetric_images, dict)

    def test__parse_raw_full(self):
        self.assertTrue(self.art.title)
        self.assertTrue(self.art.abstract)
        self.assertTrue(self.art.abstract_source)
        self.assertTrue(self.art.journal)
        self.assertTrue(self.art.subjects)
        self.assertTrue(self.art.added_on)
        self.assertTrue(self.art.published_on)
        self.assertTrue(self.art.url)
        self.assertTrue(self.art.is_open_access)
        self.assertTrue(self.art.scopus_subjects)
        self.assertTrue(self.art.publisher_subjects)
        self.assertTrue(self.art.taglines)

        self.assertEquals("10.1038/news.2011.490", self.art.doi)
        self.assertEquals("0410462", self.art.nlmid)
        self.assertEquals("21148220", self.art.pmid)
        self.assertEquals("241939", self.art.altmetric_id)
        self.assertEquals("1108.2455", self.art.arxiv_id)
        self.assertEquals("2011arxiv1108.2455l", self.art.ads_id)

        self.assertTrue(self.art.issns)
        self.assertTrue(self.art.score)
        self.assertTrue(self.art.score_history)
        self.assertTrue(self.art.score_context)
        self.assertTrue(self.art.last_updated)
        self.assertTrue(self.art.schema)

        self.assertEquals(5, self.art.cited_by_facebook_walls_count)
        self.assertEquals(1, self.art.cited_by_redits_count)
        self.assertEquals(176, self.art.cited_by_tweeters_count)
        self.assertEquals(3, self.art.cited_by_google_plus_count)
        self.assertEquals(1, self.art.cited_by_msm_count)
        self.assertEquals(1, self.art.cited_by_delicious_count)
        self.assertEquals(1, self.art.cited_by_qs_count)
        self.assertEquals(196, self.art.cited_by_posts_count)
        self.assertEquals(186, self.art.cited_by_accounts_count)
        self.assertEquals(6, self.art.cited_by_forums_count)
        self.assertEquals(1, self.art.cited_by_peer_review_sites_count)
        self.assertEquals(3, self.art.cited_by_feeds_count)
        self.assertEquals(1, self.art.cited_by_videos_count)


        self.assertTrue(self.art.cohorts)
        self.assertTrue(self.art.readers_count)
        self.assertTrue(self.art.readers)
        self.assertTrue(self.art.altmetric_details_url)
        self.assertTrue(self.art.altmetric_images)

    def test_from_json_file_empty(self):
        self.assertRaises(AttributeError, Article.from_json_file,'empty.json')

    def test_from_json_file_wrong(self):
        self.assertRaises(JSONParseException, Article.from_json_file,'wrong.txt')

    def test_from_json_file_correct(self):
        a = Article.from_json_file('full.json')
        self.assertIsInstance(a, Article)

    def test_from_file_empty(self):
        with open('empty.json') as raw_json:
            self.assertRaises(AttributeError, Article.from_json,raw_json)

    def test_from_file_wrong(self):
        with open('wrong.txt') as raw_json:
            self.assertRaises(JSONParseException, Article.from_json, raw_json)

    def test_from_file_correct(self):
        with open('full.json') as raw_json:
            a = Article.from_json(raw_json)
            self.assertIsInstance(a, Article)

    def test__parse_score_history_average(self):
        old_history = self.art.raw_dictionary.get("history")
        correct_history = {
            "all time":164.966, "past day":0,"past 2 days":0,"past 3 days":0,
            "past 4 days":0,"past 5 days":0,"past 6 days":0,"past week":0,
            "past month":0,"past 3 months":0,"past 6 months":0,"past year":0
            }
        new_history = self.art._parse_score_history(old_history)
        for key in correct_history:
            self.assertEquals(correct_history[key], new_history.get(key))

    def test__parse_score_history_empty(self):
        self.assertEqual(self.art._parse_score_history({}), {})

    def test__convert_to_datetime_average(self):
        time = self.art._convert_to_datetime(0)
        self.assertIsInstance(time, datetime.datetime)

    def test__convert_to_datetime_empty(self):
        time = self.art._convert_to_datetime(None)
        self.assertFalse(time)

    def test__parse_publisher_subjects_average(self):
        old_subjects  = self.art.raw_dictionary.get("publisher_subjects")
        correct_subjects = ["Public Health And Health Services"]
        new_subjects = self.art._parse_publisher_subjects(old_subjects)
        self.assertEquals(correct_subjects, new_subjects)

    def test__parse_publisher_subjects_empty(self):
        self.assertEquals(self.art._parse_publisher_subjects({}),[])

    def test__parse_score_context_average(self):
        old_context = self.art.raw_dictionary.get("context")
        correct_context = {
            "all":
                {"count":2162451,"mean":4.7684323457198,"rank":4979,"pct":99,
                 "higher_than":2157568},
            "journal":
                {"count":25073,"mean":38.781049218251,"rank":1332,"pct":94,
                 "higher_than":23741},
            "context age":
                {"count":54719,"mean":4.231628860704,"rank":98,"pct":99,
                 "higher_than":54621},
            "journal age":
                {"count":869,"mean":41.477870967742,"rank":41,"pct":95,
                 "higher_than":828}
            }

        new_context = self.art._parse_score_context(old_context)

        for key in correct_context:
            self.assertEquals(correct_context[key], new_context.get(key))

    def test__parse_score_context_empty(self):
        self.assertEquals(self.art._parse_score_context({}),{})