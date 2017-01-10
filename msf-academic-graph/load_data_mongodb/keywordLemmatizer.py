import sys
import pymongo
from nltk.tokenize import TreebankWordTokenizer as Tokenizer
from nltk.stem import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords

def lemmatize_keywords(db):
    tokenizer = Tokenizer()
    lemmatizer = WordNetLemmatizer()
    stemmer = LancasterStemmer()
    keyword_collections = ['keywords', 'keywords_not_of_interest']
    for kw_collection in keyword_collections:
        keywords = db[kw_collection].find({})
        for kw in keywords:
            tokens = [t for t in tokenizer.tokenize(kw['_id']) if t not in stopwords.words('english')]
            lemma_keywords_str = " ".join([lemmatizer.lemmatize(token) for token in tokens])
            stem_keywords_str = " ".join([stemmer.stem(token) for token in tokens])
            db[kw_collection].update({'_id': kw['_id']}, 
                    {
                        '$set': {'lemma': lemma_keywords_str, 'stem': stem_keywords_str}
                    }
                )
        db[kw_collection].create_index([("lemma", pymongo.ASCENDING)])
        db[kw_collection].create_index([("stem", pymongo.ASCENDING)])

if __name__ == "__main__":
    try:
        client = pymongo.MongoClient("localhost", 27017)
        db = client.msag
        lemmatize_keywords(db)
    except:
      print >> sys.stderr, "Error:", sys.exc_info()


