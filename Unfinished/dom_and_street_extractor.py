#tested on avito and cian addresses 

def dom_extractor(line):
    '''Exctracting house number from an address line'''
    splt = line.split(',')
    
    if len(splt) < 2:
        return False
    
    ans = splt[-1].strip()

    check = 0
    for character in ans:
            if character.isdigit():
                check = 1
    if check == 1:
        return ans
    return False

def street_extractor(line):
    '''Exctracting street name from an address line'''
    if not dom_extractor(line):
        return False

    try:
        return line.split(',')[-2].strip()
    except IndexError:
        return False


def equal(line1, line2):
    '''Returns true if two addresses (line1, line2) are the same'''
    if dom_extractor(line1) == dom_extractor(line2):
        splt = street_extractor(line1).split()

        for item in splt:
            if not item[0].isupper():
                splt.remove(item)
        
        splt2 = street_extractor(line2).split()

        for item in splt2:
            if not item[0].isupper():
                splt2.remove(item)

        if splt == splt2:
            return True
        
        return False
    return False


