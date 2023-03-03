def standardise_delimiter(pages):
    """
    Converts all page delimiters to '-' return page string delimited by '-'
    """
    return pages.replace('/', '-')

def start_page(pages):
    """
    Returns start page from string 123-134 by finding '-' returns start page no. as string e.g. 123
    """
    return pages[:pages.find('-')]

def end_page(pages):
    """
    Returns end page from string 123-134 by finding '-' returns end page no. as string e.g. 134
    """
    return pages[pages.find('-')+1:]

def standardise_end_page(startPage, endPage):
    """
    Removes any end page truncation e.g. if start = 123 and end = 45 then end becomes 145
    """
    lenDiff = len(startPage) - len(endPage)

    if lenDiff > 0:
        return ''.join([startPage[:1], endPage])
    else:
        return endPage
    
def remove_truncation(startPage, endPage):
    """
    Removes any truncation from the end page e.g. 123-45 becomes 123-145 returns string
    """
    return ''.join([startPage, '-', standardise_end_page(startPage, endPage)])


def standardise_page_format(pages):
    """
    Converts all journal pages to standard format returns standardised string of page numbers e.g. 123-145 or 1003-1014
    """
    x = standardise_delimiter(pages)
    startX = start_page(x)
    endX = end_page(x)

    print startX
    print endX

    return remove_truncation(startX, endX)
    

x = '134/56'
y = '199-7'

print standardise_page_format(x)



