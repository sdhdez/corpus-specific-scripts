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
    qr = mdbcl.QueryResources()
    qr.set_domain(domain)
    while True:
        readed_block = msagcl.read_block(file_stream, msagcl.read_sentence_col_raw)
        if readed_block and readed_block['paper_id']:
            paper_id = readed_block['paper_id']
            paper = qr.is_there(paper_id)
            if paper:
                print readed_block['paper_id']
                print readed_block['data_block']
                #qr.is_there_debug(paper_id)
        else:
            break

if __name__ == "__main__":
    try:
        domain = sys.argv[1]
        file_name = sys.argv[2]
        file_stream = open(file_name, "rU")
        iterate_data(file_stream, domain)
        file_stream.close()
    except:
      print >> sys.stderr, "Error:", sys.exc_info()
