import sys
import pymongo

def load_to_mongodb(db, papers_keywords):
    collection = db.papers_keywords
    collection.drop_indexes()
    collection.drop()
    bulk = collection.initialize_ordered_bulk_op()
    bulk_size = 50000
    documents_count = 0
    for paper_keyword in papers_keywords:
        paper_id, keyword_name, field_id = paper_keyword.strip("\n").split("\t")
        #print paper_id, keyword_name, field_id
        bulk.insert({
                            'paper_id': paper_id,
                            'keyword_name': keyword_name,
                            'field_id': field_id
                        })
        documents_count += 1
        if documents_count >= bulk_size:
            print bulk.execute()
            documents_count = 0
            bulk = collection.initialize_ordered_bulk_op()
    if documents_count > 0:
        print bulk.execute()
    collection.create_index([("paper_id", pymongo.ASCENDING)])
    collection.create_index([("keyword_name", pymongo.ASCENDING)])
    collection.create_index([("field_id", pymongo.ASCENDING)])

if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
        fields_of_study = open(file_name, "rU")
        client = pymongo.MongoClient("localhost", 27017)
        db = client.msag
        load_to_mongodb(db, fields_of_study)
        fields_of_study.close()
    except:
      print >> sys.stderr, "Error:", sys.exc_info()


