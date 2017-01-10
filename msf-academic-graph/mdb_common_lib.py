import sys 
import pymongo
import re

class QueryResources:
    domain = None

    def __init__(self):
        self.db = self.get_db()

    def get_db(self):
        return pymongo.MongoClient('mongodb://localhost:27017/').msag

    def set_domain(self, name):
        self.domain = name

    def is_there(self, paper_id, domain = None):
        query = {'_id': paper_id}
        if domain:
            query[domain] = True
        elif self.domain:
            query[self.domain] = True
        result = self.db.paper_domains.find_one(query)
        return result

    def is_there_debug(self, paper_id):
        """ Debug information, print keywords and fields """
        keywords = self.db.papers_keywords.aggregate([
                {'$match': {'paper_id': paper_id}},
                {'$group': {'_id': {'paper_id': '$paper_id', 'field_id': '$field_id'}, 'keywords': {'$push': '$keyword_name'}}}
            ])
        for kws in keywords:
            field_id = kws['_id']['field_id']
            for k in kws['keywords']:
                field = self.db.fields_of_study.find_one({'_id': field_id})
                if field:
                    field = field['field_name']
                domains = self.db.keywords.find_one({'_id': k})
                if domains:
                    domains.pop('_id', None)
                print >> sys.stderr, 'Field:', field, ', Keyword:', k, ', Target domains:', domains
        print >> sys.stderr

    def is_keyword(self, text, domain = None, exact = True, of_interest = True, not_by_keyword = '_id'):
        if exact:
            start, end = "^", "$"
        else:
            start, end = "", ""
        text = re.compile(start + re.escape(text) + end, re.IGNORECASE)
        query = {not_by_keyword: text}
        if domain:
            query[domain] = True
        elif self.domain:
            query[self.domain] = True
        if of_interest:
            result = self.db.keywords.find_one(query)
        else:
            result = self.db.keywords_not_of_interest.find_one(query)
        return result

