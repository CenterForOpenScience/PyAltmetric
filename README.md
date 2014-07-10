===========
PyAltmetric
===========

PyAltmetric provides an easy python wrapper for the Altmetric API.

Typical usage often looks like this:

    from pyaltmetric import Altmetric

Create an Altmetric object:

    altmetric_object = Altmetric()

Creating an Altmetric object caches api version number and key. The 
object is then used to make calls to the Altmetric API. From here you can
easily create article objects filled with Altmetric information simply by
giving an id for the article you want information on:

    article1 = altmetric_object.article_from_doi("doi_of_article")

There are various id's to choose from including: bibcode, pmid, and arxiv id.

After you have an article you can easily extract altmetric information
using the built in attributes such as:

    article1.title
    article1.abstract
    article1.score

If you want to gather multiple article metrics at once you can use the
articles_from_timeframe method. This will give you articles with internet
mentions within a given time period (past 3 days, past month, ect):

    articles = altmetric_object.articles_from_timeframe("1 day")

It returns an article gerator which can easily be iterated through.

If you already have a json from the Altmetric API you can create an
article directly.

First you need to import article:

    from pyaltmetric import Article

Then you can simply create atricles. There are three ways to do so.

1. Using supplying a properly constructed dictionary stright into the constructor:
        
        article2 = Article(json_dict)
        
2. Supplying the filename of a properly formatted json and using the class method from_json_file:
       
        article3 = Article.from_json_file(file)
        
3. Supplying an alreay open file of properly formatted json and using the class method from_json_file:
        
        article3 = Article.from_json_file("filename.json")

