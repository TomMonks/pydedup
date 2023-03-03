"""
Functions for manipulating strings within the reference files 
and individual records
"""
import string

def remove_punct(title):
    """ Strip white space and punctuation from string return edited string"""
    # python 2.7 code s = title.translate(string.maketrans("",""), string.punctuation)
    # python 3.9 updatetype
    # adds in '\u2013' (long dash from unicode) to the punc as this sometimes appears in ris.
    s = title.translate(str.maketrans('', '', string.punctuation + '\u2013'))
    return s.replace(' ', '')

def truncate_first_initial(author):
    """truncates author name to surname+ 1st intial only + strips punct snd whitespace returns string"""
    return remove_punct(author[:author.find(' ')+2]).lower()

def truncate_surname(author):
    """truncates author to surname only return string"""
    return author[3:author.find(',')].lower()