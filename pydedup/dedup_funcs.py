#--------------------------------------------------------------------
#
#   Module:         dedupFuncs
#   Description:    Simple script for removing duplicate EndNote entries
#   Author:         T.Monks
#   Python ver:     3.9.15 (upgraded from 2.7.3 on 03/03/23)
#
#   Logic:          1. Strip punctuation/whitespace from titles
#                   2. Remove all matching titles (pass 1)
#                   3. Flag all entries with matching:
#                       a. author surnames (concatonated, lowercase, no whitespace)
#                       b. Year of pub
#                       c. Volumn of pub
#                       d. journal title (no puct/whitespace)
#--------------------------------------------------------------------

from pydedup.string_manip import truncate_surname

class Results:
    def __init__(self):
        self.duplicates = []
        self.edit = []
        
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
            

class DedupFuncContainer():
    """Container for deduplication preferences"""
    def __init__(self):
        self.authorFunc = truncate_surname
    
