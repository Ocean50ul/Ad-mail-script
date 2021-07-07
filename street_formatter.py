lst = open("streets.txt", encoding="utf-8").readlines()

def without_number():

    street = splitter[1].strip()
    name = splitter[0]

    new_line = street + ' ' + name
    return new_line

def with_number_one_word_aia():
    splitter2 = splitter[0].split()
    new_line = splitter2[1] + ' ' + splitter2[0] + ' ' + splitter[1].strip()
    return new_line

def with_number_one_word_no_aia():
    splitter2 = splitter[0].split()
    new_line = splitter2[1] + ' ' + splitter[1].strip() + ' ' + splitter2[0]
    return new_line

def two_words_with_number():
    splitter2 = splitter[0].split()

    street = splitter[1].strip()
    number = splitter2[len(splitter2) - 1].strip()
    name = ' '.join(splitter2[:len(splitter2) - 1]).strip()

    new_line = number + ' ' + street + ' ' + name
    return new_line

def printer():
    print(item.strip())
    print(f'{new_line}')
    print('------------')

for index, item in enumerate(lst):
    splitter = item.split(',')                               #splitting line into two halfs, one contains street name, other contain type of a street (boulvar, etc)

    if len(splitter) == 1:                                   #guard to skip lines without comma, i dont need them
        continue

    if item.find(',') != -1 and item.find('улица') != -1:    #formatting everything that contains 'улица'
        if not any([x.isdigit() for x in splitter[0]]):      #without any numbers in it (OK)
            new_line = without_number()
            lst[index] = new_line
        else:                                                #with numbers in it
            if len(splitter[0].split()) <= 2:                #with only 1 word in streets name
                if splitter[0].split()[0].endswith('ая'):    #with 'ая' in the end of streets name (OK)
                    new_line = with_number_one_word_aia()
                    lst[index] = new_line
                else:
                    new_line = with_number_one_word_no_aia() #without 'ая' in the end of street name (OK)
                    lst[index] = new_line
            else:
                new_line = two_words_with_number()           #with two words in street name (OK)
                lst[index] = new_line

    if item.find(',') > 0 and item.find('площадь') > 0:      #formatting everything that contains 'площадь' (OK)
        new_line = without_number()
        lst[index] = new_line
    
    if item.find(',') > 0 and item.find('проезд') > 0:       #formatting everything that contains 'проезд'
        if any([x.isdigit() for x in splitter[0]]):          #with numbers in it
            if len(splitter[0].split()) <= 2:                #with only 1 word in streets name
                if splitter[0].split()[0].endswith('й'):     #with 'ий' or 'ый' or 'ой' in the end of streets name (OK)
                    new_line = with_number_one_word_aia()
                    lst[index] = new_line
                else:
                    new_line = with_number_one_word_no_aia() #without 'ий' or 'ый' or 'ой' in the end of street name (OK)
                    lst[index] = new_line
            else:
                new_line = two_words_with_number()           #with two words in street name (OK)
                lst[index] = new_line
        else:                                                #wtihout numbers in it (OK)
            new_line = without_number()
            lst[index] = new_line

    if item.find(',') > 0 and item.find('проспект') > 0:     #formatting everything that contains 'проспект' (OK)
        new_line = without_number()
        lst[index] = new_line

    if item.find(',') > 0 and item.find('бульвар') > 0:      #formatting everything that contains 'бульвар' (OK)
        new_line = without_number()
        lst[index] = new_line

    if item.find(',') > 0 and item.find('набережная') > 0:   #formatting everything that contains 'набережная' (OK)
        new_line = without_number()
        lst[index] = new_line
        
    if item.find(',') > 0 and item.find('переулок') > 0:
        if any([x.isdigit() for x in splitter[0]]):          #with numbers in it
            if len(splitter[0].split()) <= 2:                #with only 1 word in streets name
                if splitter[0].split()[0].endswith('й'):     #with 'ий' or 'ый' or 'ой' in the end of streets name (OK)
                    new_line = with_number_one_word_aia()
                    lst[index] = new_line
                else:
                    new_line = with_number_one_word_no_aia() #without 'ий' or 'ый' or 'ой' in the end of street name (OK)
                    lst[index] = new_line
            else:
                new_line = two_words_with_number()           #with two words in street name (OK)
                lst[index] = new_line
        else:                                                #wtihout numbers in it (OK)
            new_line = without_number()
            lst[index] = new_line

    if item.find(',') > 0 and item.find('квартал') > 0:      #formatting everything that contains 'квартал' (OK)
        if splitter[0].startswith('Капотня'):
            new_line = with_number_one_word_no_aia()
            lst[index] = new_line
        else:
            new_line = without_number()
            lst[index] = new_line

    if item.find(',') > 0 and item.find('аллея') > 0:        #formatting everything that contains 'аллея' (OK)
        if any([x.isdigit() for x in splitter[0]]):
            new_line = with_number_one_word_aia()
            lst[index] = new_line
        else:
            new_line = without_number()
            lst[index] = new_line

    if item.find(',') > 0 and item.find('посёлок') > 0:      #formatting everything that contains 'посёлок' (OK)
        new_line = without_number()
        lst[index] = new_line

    if item.find(',') > 0 and item.find('микрорайон') > 0:   #formatting everything that contains 'микрорайон' (OK)
        if any([x.isdigit() for x in splitter[0]]):
            new_line = with_number_one_word_aia().replace(' микрорайон', '')
            lst[index] = new_line
        else:
            new_line = without_number()
            lst[index] = new_line


with open('new_streets.txt', 'w') as new:
    for line in lst:
        new.write(line.strip())
        new.write('\n')

