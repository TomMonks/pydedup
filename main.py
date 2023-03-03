import sys

from pydedup.dedup_funcs import (truncate_first_initial, 
                                 truncate_surname,
                                 read_records,
                                 output_records,
                                 unique_titles,
                                 uniquify)

if __name__ == '__main__':
    duplicates = []
    if len(sys.argv) == 1:
        print("Please enter a filename to deduplicate")
        sys.exit()

    file_name = sys.argv[1]
    author_func = truncate_surname
    title_only = False

    for item in range(2, len(sys.argv)):
        if sys.argv[item] == '-initial':
            author_func = truncate_first_initial
        elif sys.argv[item] == '-title':
            title_only = True
        elif sys.argv[item] == '-authorall':
            author_func == None
        else:
            print("Option {0} not recognised".format(sys.argv[item]))
            sys.exit()


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
        
    else:
        
        print('Running...')
        results = uniquify(all_records)
        
        remaining = 0

        for i in range(1, len(results)):
            output_records(file_name[:-4], 'Iteration' + str(i), results[i].edit)
            print('it {0} - duplicates: {1}\tremaining: {2}'.format(i, len(results[i].duplicates), len(results[i].edit)))
            total_dups += len(results[i].duplicates)
            
    print('deduplication complete.')
    print('duplicates: {0}'.format(total_dups))


    #print 'duplicates removed: ', len(edited_records.duplicates)
    #print 'Possible duplicates: ', len(likely_dups)
