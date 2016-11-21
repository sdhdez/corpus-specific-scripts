""" 
This script needs the information loaded in mongodb, 
see the scripts under load_data_mongodb/ 
"""
import sys
import msag_common_lib as msagcl
import mdb_common_lib as mdbcl

def iterate_data(file_stream, domain):
    """ Iterate data with msagcl.read_block
    --- START FILE EXAMPLE ---
    0B00AFD8
    Towards IN
    the DT
    creation NN
    of IN
    semantic JJ
    models NNS
    based VBN
    on IN
    computer-aided JJ
    designs NNS
    --- END FILE EXAMPLE
    """
    db = mdbcl.get_db()
    while True:
        readed_block = msagcl.read_block(file_stream, msagcl.read_sentence_col_raw)
        if readed_block and readed_block['paper_id']:
            paper_id = readed_block['paper_id']
            paper = db.paper_domains.find_one({'_id': paper_id, domain: True})
            if paper:
                print readed_block['paper_id']
                print readed_block['data_block']
                #debug_information(db, readed_block['paper_id'])
        else:
            break

def debug_information(db, paper_id):
    """ Debug information, print keywords and fields """
    keywords = db.papers_keywords.aggregate([
            {'$match': {'paper_id': paper_id}},
            {'$group': {'_id': {'paper_id': '$paper_id', 'field_id': '$field_id'}, 'keywords': {'$push': '$keyword_name'}}}
        ])
    for kws in keywords:
        field_id = kws['_id']['field_id']
        for k in kws['keywords']:
            field = db.fields_of_study.find_one({'_id': field_id})
            if field:
                field = field['field_name']
            domains = db.keywords.find_one({'_id': k})
            if domains:
                domains.pop('_id', None)
            print 'Field:', field, ', Keyword:', k, ', Target domains:', domains
    print


if __name__ == "__main__":
    try:
        domain = sys.argv[1]
        file_name = sys.argv[2]
        file_stream = open(file_name, "rU")
        iterate_data(file_stream, domain)
        file_stream.close()
    except:
      print >> sys.stderr, "Error:", sys.exc_info()
