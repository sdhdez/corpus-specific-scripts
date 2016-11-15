import sys
import pymongo

def load_to_mongodb(db, fields_of_study):
    collection = db.fields_of_study
    collection.drop_indexes()
    collection.drop()
    collection.create_index([("field_name", pymongo.ASCENDING)])
    for field in fields_of_study:
        field_key, field_name = field.strip("\n").split("\t")
        collection.insert_one({
                        '_id': field_key, 
                        'field_name': field_name
                        })

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


