import sys
from copy import copy as copy_list 
import msag_common_lib as msagcl

def test_reading(file_stream):
    """ Test to read data with msagcl.read_block

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
    while True:
        readed_block = msagcl.read_block(file_stream, msagcl.read_sentence_col_fmt)
        print readed_block
        if readed_block['tokens']:
            pass
        else:
            break

if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
        file_stream = open(file_name, "rU")
        test_reading(file_stream)
        file_stream.close()
    except:
      print >> sys.stderr, "Error:", sys.exc_info()
