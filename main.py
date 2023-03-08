import sys
import argparse

# pydedup imports
from pydedup.dedup_funcs import (unique_titles, merge_unique)
from pydedup.io import read_records, output_records
from pydedup.string_manip import truncate_surname, truncate_first_initial
from pydedup import __version__

def adv_parse_arguments():
    '''Parse command line arguments.

    match options:
    ---------------
    default: dedpup using title only
    -tj: (title, journal)
    -atj: (author, title, journal)
    -i: use 1st author initial only
    -a: use all authors in match

    Returns:
    -------
    Tuple (str, object, bool, str)
    
    0: the file name containing the references
    1: the function use to parse author names
    2: the function used to match the duplicates.
    3: the file name containing references to MERGE.
    '''
    # Construct the argument parser and parse the arguments
    arg_desc = '''\
            Deduplicate academic references easily!
            --------------------------------
                Deduplicate combined searches or 
                return update a search and only return
                new unique references.
            
            '''
    parser = argparse.ArgumentParser(formatter_class = argparse.RawDescriptionHelpFormatter,
                                     description= arg_desc)

    parser.add_argument("file", metavar="FILE", 
                        help = "Path to your main input RIS file")
    
    parser.add_argument("-u", "--update", metavar="UPDATE", 
                        help = "Path to your file that contains an updated search.")

    parser.add_argument("-tj", "--title-journal", action='store_true',
                        help = "Deduplicate using both the title and the journal")

    # store true will save True for constant if included.  Default is False
    parser.add_argument("-aty", "--author-title-year", 
                        help = "Deduplicate using both the AUTHOR, TITLE AND YEAR.", action='store_true')

    parser.add_argument("-i", "--initial", 
                    help = "Trim first author to initials only.",  action='store_true')

    parser.add_argument("-a", "--author-all", 
                    help = "Use all authors as part of dedup.",  action='store_true')

    args = vars(parser.parse_args())

    file_name = sys.argv[1]
    author_func = truncate_surname

    # file used if updating a search
    update_file_name = None

    # duplicate matching function
    # -1: (title)
    # -2: (title, journal article)
    # -3: (authors, title, year)
    # by default use title only...
    match_func = lambda x: x[-1:][0]

    if args['initial']:
        author_func = truncate_first_initial            
    if args['author_all']:
        author_func == None
    # match by title and journal name
    if args['title_journal']:
        match_func = lambda x: x[-2:][0]
    if args['author_title_year']:
        match_func = lambda x: x[-3:][0]
    if args['update']:
        # performing a merge return unique records from merge datafile.
        update_file_name = args['update']

    return file_name, author_func, match_func, update_file_name

if __name__ == '__main__':
    file_name, author_func, match_func, update_file_name \
            = adv_parse_arguments()

    print(f'\nPyDeDup v{__version__}')
    print('** Reading records...')
    all_records = read_records(file_name[:-4], author_func)

    print('** Excluding duplicate titles...')
    if update_file_name is None:     
        edited_records = unique_titles(all_records, match_func)

    else:
        print('** Reading records to MERGE...')
        to_merge = read_records(update_file_name[:-4], author_func)
        edited_records = merge_unique(all_records, to_merge, match_func)

    print('** Deduplication complete.')

    print('** Writing edited and duplicates to file.')
    # save edited ris and list of duplicates.
    output_records(file_name[:-4], "edit", edited_records.edit)
    output_records(file_name[:-4], "dups", edited_records.duplicates)
    print('** Complete.')

    # number o
    original_n = len(all_records)

    total_dups = len(edited_records.duplicates)
    remaining = len(edited_records.edit)
    per_dups = (total_dups / original_n) * 100
    per_remaining = (remaining / original_n) * 100

    print(f'\noriginal\t: {original_n}')
    # number of candidates to merge
    if update_file_name is not None:
        merge_n = len(to_merge)
        print(f'merge refs\t: {merge_n}')

        per_dups = (total_dups / merge_n) * 100
        per_remaining = (remaining / merge_n) * 100
    print(f'duplicates\t: {total_dups}({per_dups:.1f}%)')
    print(f'remaining\t: {remaining}({per_remaining:.1f}%)\n')


