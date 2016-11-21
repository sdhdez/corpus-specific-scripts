import sys 

def read_sentence_col_fmt(sentences_col_fmt):
    """ Recives read a POS tagged sentence in the format described below
    and returns a dictionary with two keys.

    Keyword arguments:
    sentences_col_fmt -- File stream of the data. 

    Return if there are tokens after a paper_id: 

    {
        'paper_id': "some_string", 
        'tokens': [("some_token", "some_pos_tag"), ("some_token", "some_pos_tag"), ... ]
    }
    
    If not returns None.


        
    --- START OF EXAMPLE ---
    7F0016FA
    Evolutionary-Neural JJ
    System NNP
    to TO
    Classify VB
    Infant NNP
    Cry NNP

    --- END OF EXAMPLE ---
    
    The above is an example of one block of the data, the first line 
    is the 'paper_id' and the following lines are the POS tagged tokens
    until the first empty line (An empty line may be the begining or 
    the ending of a tagged sentence)
    """
    #Get the first line (paper_id)
    paper_id = sentences_col_fmt.next().strip()
    tokens = []
    #Read line by line until the first empty line.
    for line in sentences_col_fmt:
        line = line.strip().split()
        if not line:
            break
        tokens.append((line[0], line[1]))
    return {'paper_id': paper_id, 'tokens': tokens}

def read_block(file_stream, read_formated_data, args = []): 
    """ Recives a file stream and reads and returns a block of data
    readed by the given fuction.

    Keyword arguments:
    file_stream -- File stream to data. 

    """
    returned_data = None
    try:
        if args:
            returned_data = read_formated_data(file_stream, args)
        else:
            returned_data = read_formated_data(file_stream)
    except:
        print >> sys.stderr, "Error in sentence:", returned_data, sys.exc_info()
    return returned_data
