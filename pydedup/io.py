'''
Functions for reading and writing RIS files into pydedup
'''

import sys

# function to remove all punctuation and whitespace.
from pydedup.string_manip import remove_punct

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
    start_page = ''
    pages = ''
    
    for line in f:
        
        # End of record
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
                        
        # title of article                  
        elif line[0:2] == 'TI':
            
            title = remove_punct(line[3:len(line)-1].lower())

        # journal name
        elif line[0:2] == 'T2':
            
            journal = remove_punct(line[3:len(line)-1].lower())

        # publication year
        elif line[0:2] == 'PY':
           
            year = line[3:len(line)-1]

        # authors - there may be multiple - concat
        elif line[0:2] == 'AU':
            
            #authors = ''.join([authors, line[3:line.find(',')].lower()])
            authors = ''.join([authors, authorFunc(line[3:])])

        # start page
        elif line[0:2] == 'SP':

            start_page = line[3:len(line)-1]

        # concat end page with start page
        elif line[0:2] == 'EP':
            pages = start_page + '-' + line[3:len(line)-1]
            
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

