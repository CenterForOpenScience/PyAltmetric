from unittest import TestCase
from altmetric_library import Article
import json

__author__ = 'Lauren'

class TestArticle(TestCase):
    def setUp(self):
        raw_json = open('average.json')
        raw_dict = json.load(raw_json)
        print(raw_dict)
        self.art = Article(raw_dict)

    def test__parse_raw_empty(self):
        #An empty dictionary would never actually be passed to this
        self.art._raw = {}
        self.art._parse_raw()

        self.assertFalse(self.art._title)
        self.assertFalse(self.art._abstract)
        self.assertFalse(self.art._abstract_source)
        self.assertFalse(self.art._journal)
        self.assertFalse(self.art._subjects)
        self.assertFalse(self.art._added_on)
        self.assertFalse(self.art._published_on)
        self.assertFalse(self.art._url)
        self.assertFalse(self.art._is_open_access)
        self.assertFalse(self.art._scopus_subjects)
        self.assertFalse(self.art._publisher_subjects)
        self.assertFalse(self.art._taglines)

        self.assertFalse(self.art._doi)
        self.assertFalse(self.art._nlmid)
        self.assertFalse(self.art._pmid)
        self.assertFalse(self.art._altmetric_id)
        self.assertFalse(self.art._arxiv_id)
        self.assertFalse(self.art._ads_id)
        self.assertFalse(self.art._issns)

        self.assertFalse(self.art._score)
        self.assertFalse(self.art._score_history)
        self.assertFalse(self.art._score_context)
        self.assertFalse(self.art._last_updated)
        self.assertFalse(self.art._schema)
        self.assertFalse(self.art._cited_by_facebook_walls_count)
        self.assertFalse(self.art._cited_by_redits_count)
        self.assertFalse(self.art._cited_by_tweeters_count)
        self.assertFalse(self.art._cited_by_google_plus_count)
        self.assertFalse(self.art._cited_by_msm_count)
        self.assertFalse(self.art._cited_by_delicious_count)
        self.assertFalse(self.art._cited_by_qs_count)
        self.assertFalse(self.art._cited_by_posts_count)
        self.assertFalse(self.art._cited_by_accounts_count)
        self.assertFalse(self.art._cited_by_forums_count)
        self.assertFalse(self.art._cited_by_peer_review_sites_count)
        self.assertFalse(self.art._cited_by_feeds_count)
        self.assertFalse(self.art._cited_by_videos_count)
        self.assertFalse(self.art._cohorts)
        self.assertFalse(self.art._readers_count)
        self.assertFalse(self.art._readers)
        self.assertFalse(self.art._altmetric_details_url)
        self.assertFalse(self.art._altmetric_images)


    def test__parse_raw_average(self):
        self.assertTrue(self.art._title)
        self.assertFalse(self.art._abstract)
        self.assertFalse(self.art._abstract_source)
        self.assertTrue(self.art._journal)
        self.assertTrue(self.art._subjects)
        print(self.art._raw.get("added_on"))
        self.assertTrue(self.art._added_on)
        self.assertTrue(self.art._published_on)
        self.assertTrue(self.art._url)
        self.assertFalse(self.art._is_open_access)
        #its false because its a boolean not because it doesnt exits hmmmm
        self.assertTrue(self.art._scopus_subjects)
        self.assertFalse(self.art._publisher_subjects)
        self.assertTrue(self.art._taglines)

        self.assertTrue(self.art._doi)
        self.assertTrue(self.art._nlmid)
        self.assertFalse(self.art._pmid)
        self.assertTrue(self.art._altmetric_id)
        self.assertFalse(self.art._arxiv_id)
        self.assertFalse(self.art._ads_id)
        self.assertTrue(self.art._issns)

        self.assertTrue(self.art._score)
        self.assertTrue(self.art._score_history)
        self.assertTrue(self.art._score_context)
        self.assertTrue(self.art._last_updated)
        self.assertTrue(self.art._schema)
        self.assertTrue(self.art._cited_by_facebook_walls_count)
        self.assertTrue(self.art._cited_by_redits_count)
        self.assertTrue(self.art._cited_by_tweeters_count)
        self.assertFalse(self.art._cited_by_google_plus_count)
        self.assertTrue(self.art._cited_by_msm_count)
        self.assertFalse(self.art._cited_by_delicious_count)
        self.assertFalse(self.art._cited_by_qs_count)
        self.assertTrue(self.art._cited_by_posts_count)
        self.assertTrue(self.art._cited_by_accounts_count)
        self.assertFalse(self.art._cited_by_forums_count)
        self.assertFalse(self.art._cited_by_peer_review_sites_count)
        self.assertTrue(self.art._cited_by_feeds_count)
        self.assertFalse(self.art._cited_by_videos_count)
        self.assertTrue(self.art._cohorts)
        self.assertTrue(self.art._readers_count)
        self.assertTrue(self.art._readers)
        self.assertTrue(self.art._altmetric_details_url)
        self.assertTrue(self.art._altmetric_images)


    def test__parse_raw_full(self):
        raw_json = open('full.json')
        raw_dict = json.load(raw_json)
        self.art._raw = raw_dict
        self.art._parse_raw()

        self.assertTrue(self.art._title)
        self.assertTrue(self.art._abstract)
        self.assertTrue(self.art._abstract_source)
        self.assertTrue(self.art._journal)
        self.assertTrue(self.art._subjects)
        self.assertTrue(self.art._added_on)
        self.assertTrue(self.art._published_on)
        self.assertTrue(self.art._url)
        self.assertTrue(self.art._is_open_access)
        self.assertTrue(self.art._scopus_subjects)
        self.assertTrue(self.art._publisher_subjects)
        self.assertTrue(self.art._taglines)

        self.assertTrue(self.art._doi)
        self.assertTrue(self.art._nlmid)
        self.assertTrue(self.art._pmid)
        self.assertTrue(self.art._altmetric_id)
        self.assertTrue(self.art._arxiv_id)
        self.assertTrue(self.art._ads_id)
        self.assertTrue(self.art._issns)

        self.assertTrue(self.art._score)
        self.assertTrue(self.art._score_history)
        self.assertTrue(self.art._score_context)
        self.assertTrue(self.art._last_updated)
        self.assertTrue(self.art._schema)
        self.assertTrue(self.art._cited_by_facebook_walls_count)
        self.assertTrue(self.art._cited_by_redits_count)
        self.assertTrue(self.art._cited_by_tweeters_count)
        self.assertTrue(self.art._cited_by_google_plus_count)
        self.assertTrue(self.art._cited_by_msm_count)
        self.assertTrue(self.art._cited_by_delicious_count)
        self.assertTrue(self.art._cited_by_qs_count)
        self.assertTrue(self.art._cited_by_posts_count)
        self.assertTrue(self.art._cited_by_accounts_count)
        self.assertTrue(self.art._cited_by_forums_count)
        self.assertTrue(self.art._cited_by_peer_review_sites_count)
        self.assertTrue(self.art._cited_by_feeds_count)
        self.assertTrue(self.art._cited_by_videos_count)
        self.assertTrue(self.art._cohorts)
        self.assertTrue(self.art._readers_count)
        self.assertTrue(self.art._readers)
        self.assertTrue(self.art._altmetric_details_url)
        self.assertTrue(self.art._altmetric_images)

    def test__properties(self):
        raw_json = open('full.json')
        raw_dict = json.load(raw_json)
        self.art._raw = raw_dict
        self.art._parse_raw()

        self.assertTrue(self.art.raw_dictionary)
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

        self.assertTrue(self.art.doi)
        self.assertTrue(self.art.nlmid)
        self.assertTrue(self.art.pmid)
        self.assertTrue(self.art.altmetric_id)
        self.assertTrue(self.art.arxiv_id)
        self.assertTrue(self.art.ads_id)
        self.assertTrue(self.art.issns)

        self.assertTrue(self.art.score)
        self.assertTrue(self.art.score_history)
        self.assertTrue(self.art.score_context)
        self.assertTrue(self.art.last_updated)
        self.assertTrue(self.art.schema)
        self.assertTrue(self.art.cited_by_facebook_walls_count)
        self.assertTrue(self.art.cited_by_redits_count)
        self.assertTrue(self.art.cited_by_tweeters_count)
        self.assertTrue(self.art.cited_by_google_plus_count)
        self.assertTrue(self.art.cited_by_msm_count)
        self.assertTrue(self.art.cited_by_delicious_count)
        self.assertTrue(self.art.cited_by_qs_count)
        self.assertTrue(self.art.cited_by_posts_count)
        self.assertTrue(self.art.cited_by_accounts_count)
        self.assertTrue(self.art.cited_by_forums_count)
        self.assertTrue(self.art.cited_by_peer_review_sites_count)
        self.assertTrue(self.art.cited_by_feeds_count)
        self.assertTrue(self.art.cited_by_videos_count)
        self.assertTrue(self.art.cohorts)
        self.assertTrue(self.art.readers_count)
        self.assertTrue(self.art.readers)
        self.assertTrue(self.art.altmetric_details_url)
        self.assertTrue(self.art.altmetric_images)

    def test__parse_score_history_average(self):
        old_history = {
            "at":164.966, "1d":0,"2d":0,"3d":0,
            "4d":0,"5d":0,"6d":0,"1w":0,
            "1m":0,"3m":0,"6m":0,"1y":0
            }
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

    def test__convert_to_utc_average(self):
        time = self.art._convert_to_utc(0)
        self.assertEquals(time, "1970-01-01T00:00:00Z") #hmmmm ? day off

    def test__convert_to_utc_empty(self):
        time = self.art._convert_to_utc(None)
        self.assertFalse(time)

    def test__parse_publisher_subjects_average(self):
        old_subjects  = [{"name":"Public Health And Health Services","scheme":"era"}]
        correct_subjects = ["Public Health And Health Services"]
        new_subjects = self.art._parse_publisher_subjects(old_subjects)
        self.assertEquals(correct_subjects, new_subjects)


    def test__parse_publisher_subjects_empty(self):
        self.assertEquals(self.art._parse_publisher_subjects({}),[])

    def test__parse_score_context_average(self):
        old_context = {
            "all":
                {"count":2162451,"mean":4.7684323457198,"rank":4979,"pct":99,
                 "higher_than":2157568},
            "journal":
                {"count":25073,"mean":38.781049218251,"rank":1332,"pct":94,
                 "higher_than":23741},
            "similar_age_3m":
                {"count":54719,"mean":4.231628860704,"rank":98,"pct":99,
                 "higher_than":54621},
            "similar_age_journal_3m":
                {"count":869,"mean":41.477870967742,"rank":41,"pct":95,
                 "higher_than":828}
            }

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