import sys 

def read_sentence_col_fmt(file_stream):
    """ Recives read a POS tagged sentence in the format described below
    and returns a dictionary with the paper_id, tokens and POS tags.

    Keyword arguments:
    file_stream -- File stream of the data. 

    Return if there are tokens after a paper_id: 

    {
        'paper_id': "some_string", 
        'tokens': ["some_token", "some_token", ... ],
        'pos_tags': ["some_tag", "some_tag", ... ]
    }
    
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
    try:
        first_line = file_stream.next()
    except:
        first_line = ""
    data_block = {}
    data_block['paper_id'] = first_line.strip()
    data_block['tokens'] = []
    data_block['pos_tags'] = []
    #Read line by line until the first empty line.
    for line in file_stream:
        line = line.strip()
        if not line:
            break
        line = line.split()
        data_block['tokens'].append(line[0])
        data_block['pos_tags'].append(line[1])
    return data_block

def read_sentence_col_raw(file_stream):
    """ Recives read a POS tagged sentence in the format described below
    and returns a dictionary with the paper_id and the block of data as an unique string.

    Keyword arguments:
    file_stream -- File stream of the data. 

    Return if there are tokens after a paper_id: 

    {
        'paper_id': "some_string", 
        'data_block': "data block in a string"
    }
    
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
    try:
        first_line = file_stream.next()
    except:
        first_line = ""
    data_block = {}
    data_block['paper_id'] = first_line.strip()
    data_block['data_block'] = ""
    #Read line by line until the first empty line.
    for line in file_stream:
        if not line.strip():
            break
        data_block['data_block'] += line
    return data_block


def read_block(file_stream, read_formated_data, args = []): 
    """ Recives a file stream and reads and returns a block of data
    readed by the given fuction.

    Keyword arguments:
    file_stream -- File stream to data. 
    read_formated_data -- Function to read a block of data
    args -- Extra arguments to the function

    Returned data is defined by the function 'read_formated_data'.
    """
    returned_data = None
    try:
        if args:
            returned_data = read_formated_data(file_stream, args)
        else:
            returned_data = read_formated_data(file_stream)
    except:
        print >> sys.stderr, "Error at reading data:", returned_data, sys.exc_info()
    return returned_data
