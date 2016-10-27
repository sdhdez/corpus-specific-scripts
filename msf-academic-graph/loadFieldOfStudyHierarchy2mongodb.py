import sys
import pymongo

def load_to_mongodb(db, fields_of_study):
    collection = db.field_of_study_hierarchy
    collection.drop_indexes()
    collection.drop()
    collection.create_index([("child_id", pymongo.ASCENDING)])
    collection.create_index([("parent_id", pymongo.ASCENDING)])
    for field in fields_of_study:
        child_id, child_level, parent_id, parent_level, confidence = field.strip("\n").split("\t")
        child_level = int(child_level[1:])
        parent_level = int(parent_level[1:])
        confidence = float(confidence)
        #print child_id, child_level, parent_id, parent_level, confidence
        collection.insert_one({
                        'child_id': child_id,
                        'child_level': child_level,
                        'parent_id': parent_id,
                        'parent_level': parent_level,
                        'confidence': confidence
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


