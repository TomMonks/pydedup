import string
import sys
from dedupFuncs import *

duplicates = []
if len(sys.argv) == 1:
    print "Please enter a filename to deduplicate"
    sys.exit()

fileName = sys.argv[1]
authorFunc = truncate_surname
titleOnly = 0


for item in range(2, len(sys.argv)):
    if sys.argv[item] == '-initial':
        authorFunc = truncate_first_initial
    elif sys.argv[item] == '-title':
        titleOnly = 1
    elif sys.argv[item] == '-authorall':
        authorFunc == None
    else:
        print "Option {0} not recognised".format(sys.argv[item])
        sys.exit()


print 'Reading records...'
all_records = read_records(fileName[:-4], authorFunc)

print str(len(all_records)) + ' records found'

total_dups = 0

if titleOnly == 1:
    print 'Excluding duplicate titles...'
    edited_records = unique_titles(all_records, lambda x: x[len(x)-1:][0])
    output_records(fileName[:-4], "edit", edited_records.edit)
    output_records(fileName[:-4], "dups", edited_records.duplicates)
    total_dups = len(edited_records.duplicates)
    
else:
    
    print 'Running...'
    results = uniquify(all_records)
    
    remaining = 0

    for i in range(1, len(results)):
        output_records(fileName[:-4], 'Iteration' + str(i), results[i].edit)
        print 'it {0} - duplicates: {1}\tremaining: {2}'.format(i, len(results[i].duplicates), len(results[i].edit))
        total_dups += len(results[i].duplicates)
        
print 'deduplication complete.'
print 'duplicates: {0}'.format(total_dups)


#print 'duplicates removed: ', len(edited_records.duplicates)
#print 'Possible duplicates: ', len(likely_dups)
