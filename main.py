import sys

# pydedup imports
from pydedup.dedup_funcs import (unique_titles)
from pydedup.io import read_records, output_records
from pydedup.string_manip import truncate_surname, truncate_first_initial

def parse_arguments():
    '''Parse command line arguments.

    Cmd Parameters:
    ---------------
    -title_only: dedpup using title only
  
    Returns:
    -------
    Tuple (str, object, bool)
    
    0: the file name containing the references
    1: the function use to parse author names
    2: True = title only; False = mroe complex dedup!?
    '''
    if len(sys.argv) == 1:
        print("Please enter a filename to deduplicate")
        sys.exit()

    file_name = sys.argv[1]
    author_func = truncate_surname
    title_only = True

    for item in range(2, len(sys.argv)):
        if sys.argv[item] == '-initial':
            author_func = truncate_first_initial            
        elif sys.argv[item] == '-authorall':
            author_func == None
        else:
            print("Option {0} not recognised".format(sys.argv[item]))
            sys.exit()

    return file_name, author_func, title_only


if __name__ == '__main__':
    duplicates = []
    file_name, author_func, title_only = parse_arguments()

    print('Reading records...')
    all_records = read_records(file_name[:-4], author_func)
    print(str(len(all_records)) + ' records found')

    total_dups = 0

    if title_only:
        print('Excluding duplicate titles...')
        edited_records = unique_titles(all_records, lambda x: x[len(x)-1:][0])
        output_records(file_name[:-4], "edit", edited_records.edit)
        output_records(file_name[:-4], "dups", edited_records.duplicates)
        total_dups = len(edited_records.duplicates)
                    
    print('deduplication complete.')
    print('duplicates: {0}'.format(total_dups))
