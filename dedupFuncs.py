#--------------------------------------------------------------------
#
#   Module:         dedupFuncs
#   Description:    Simple script for removing duplicate EndNote entries
#   Author:         T.Monks
#   Python ver:     2.7.2
#
#   Logic:          1. Strip punctuation/whitespace from titles
#                   2. Remove all matching titles (pass 1)
#                   3. Flag all entries with matching:
#                       a. author surnames (concatonated, lowercase, no whitespace)
#                       b. Year of pub
#                       c. Volumn of pub
#                       d. journal title (no puct/whitespace)
#--------------------------------------------------------------------

import string
import sys

class Results:
    def __init__(self):
        self.duplicates = []
        self.edit = []
        
def remove_punct(title):
    """ Strip white space and punctuation from string return edited string"""
    s = title.translate(string.maketrans("",""), string.punctuation)
    return s.replace(' ', '')


def unique_titles(seq, idfun=None):
    """ Dedup using title field return Results object """
    if idfun is None:
        def idfun(x): return x
    seen = {}
    unique = Results()
   
    for item in seq:
        marker = idfun(item)
        if marker in seen:
            unique.duplicates.append(item)
            continue
        seen[marker] = 1
        unique.edit.append(item)

    return unique



def uniquify(all_records):
    """ Uniquify a reference list using a iterative approach return list of Result objects """
    results = []
    original = Results()
    original.edit = all_records
    results.append(original)
    
    for i in range(6, 1, -1):
        results.append(remove_by_criteria(results[len(results) - 1].edit, i))

    return results


def remove_by_criteria(records, c_index):
    """ Remove duplicates using criteria list return Results object"""
    found = set()
    likely_dups = []
    unique = Results()
    
    for item in records:
        li = item[len(item)-c_index]  # this looks at a specific item...
        if li not in found:
            found.add(li)
            unique.edit.append(item)
        else:
            unique.duplicates.append(item)
            
    return unique
            

def read_records(fileName, authorFunc = None):
    """ Read references from a file Return list of references """

    if authorFunc == None:
        def authorFunc(x): return x
    
    try:
        f = open(fileName + '.ris', 'r')
    except IOError as e:
        print("Error accessing file.  Please make sure that filename is correct.")
        sys.exit()

    

    curr_record = []
    likely_details = ()
    all_records = []
    title = ''
    journal = ''
    authors = ''
    year = 0
    vol = 0
    pages = ''
    
    for line in f:
        
        # used to be %0
        if line[0:2] == 'ER':

            likely_details_it1 = authors, title, year, journal, pages
            likely_details_it2 = authors, title, year, pages
            likely_details_it3 = title, year, pages
            likely_details_it4 = authors, title, year
            likely_details_it5 = title, journal
            
            curr_record.append(likely_details_it1)
            curr_record.append(likely_details_it2)
            curr_record.append(likely_details_it3)
            curr_record.append(likely_details_it4)
            curr_record.append(likely_details_it5)
            
            curr_record.append(title)
            authors = ''
            all_records.append(curr_record)
            curr_record = []
                        
        elif line[0:2] == 'TI':
            
            title = remove_punct(line[3:len(line)-1].lower())

        elif line[0:2] == 'T2':
            
            journal = remove_punct(line[3:len(line)-1].lower())

        elif line[0:2] == 'PY':
           
            year = line[3:len(line)-1]

        elif line[0:2] == '%V':
            
            year = line[3:len(line)-1]

        elif line[0:2] == 'AU':
            
            #authors = ''.join([authors, line[3:line.find(',')].lower()])
            authors = ''.join([authors, authorFunc(line[3:])])

        elif line[0:2] == '%P':

            pages = line[3:len(line)-1]
            
        curr_record.append(line)
        
    all_records.append(curr_record)
    f.close()
    return all_records


def output_records(fileName, postFix, all_records):
    newFileName = fileName + '_' + postFix + '.ris'
    f = open(newFileName, 'w')

    for record in all_records:
        for line in record[0:len(record)-7]:
            f.write(str(line))
            

    f.close()    
    


def truncate_first_initial(author):
    """truncates author name to surname+ 1st intial only + strips punct snd whitespace returns string"""
    return remove_punct(author[:author.find(' ')+2]).lower()


def truncate_surname(author):
    """truncates author to surname only return string"""
    return author[3:author.find(',')].lower()
    

class DedupFuncContainer():
    """Container for deduplication preferences"""
    def __init__(self):
        self.authorFunc = truncate_surname
    
