from random import randint

ao_list = ["СЗАО", "САО", "СВАО", "ВАО", "ЮВАО", "ЮАО", "ЮЗАО", "ЗАО", "ЦАО", "ЗелАО"]
raion_list = open("raion.txt", encoding="utf-8").readlines()
metro_list = open("metro.txt", encoding="utf-8").readlines()
street_list = open("streets.txt").readlines()
abbr = open("names_abbr.txt", encoding="utf-8").readlines()


def dom_extractor(line):
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

    if not dom_extractor(line):
        return False

    try:
        return line.split(',')[-2].strip()
    except IndexError:
        return False



def equal(line1, line2):
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




def house_generator():
    house = str(randint(0, 150))
    letters = randint(0, 5)     #0-4: without letters, 5 - with letters
    corpus = randint(0, 3)      #0-2 - without corpus\stroenie, 3 - with
    drob = randint(0, 20)       #0-19: wtihout '\', 20 - with '\'
    lett_list = ["А", "Б", "В", "Г", "Д"]
    corpus_list = ["с", "к"]

    if letters == 5 and corpus == 3 and drob == 20:
        corpus_number = str(randint(1, 10))
        drob_number = str(randint(1, 50))
        answer = house + lett_list[randint(0, 4)] + '/' + drob_number + corpus_list[randint(0, 1)] + corpus_number
        return answer

    if letters == 5 and corpus == 3:
        corpus_number = str(randint(1, 10))
        answer = house + lett_list[randint(0, 4)] + corpus_list[randint(0, 1)] + corpus_number
        return answer

    if letters == 5 and drob == 20:
        drob_number = str(randint(1, 50))
        answer = house + lett_list[randint(0, 4)] + '/' + drob_number
        return answer

    if corpus == 3 and drob == 20:
        corpus_number = str(randint(1, 10))
        drob_number = str(randint(1, 50))
        answer = house + '/' + drob_number + corpus_list[randint(0, 1)] + corpus_number
        return answer

    if letters == 5:
        answer = house + lett_list[randint(0, 4)]
        return answer

    if corpus == 3:
        corpus_number = str(randint(1, 10))
        answer = house + corpus_list[randint(0, 1)] + corpus_number
        return answer

    if drob == 20:
        drob_number = str(randint(1, 50))
        answer = house + '/' + drob_number
        return answer

    return house



def equal_tester(number):
    for _ in range(number):
        house = house_generator() #house number
        #street_abbr = randint(0, 1) #determine's wether street name is full or abbreviated
        address_style = randint(0, 1) #determine's style of address, 0 = cian, 1 = avito
        

        if address_style == 0:
            ao = ao_list[randint(0, len(ao_list) - 1)]
            raion = raion_list[randint(0, len(raion_list) - 1)].strip()
            metro = metro_list[randint(0, len(metro_list) - 1)].strip()
            street = street_list[randint(0, len(street_list) - 1)].strip()

            address = 'Москва,' + ' ' + ao + ',' + ' ' + 'р-н' + ' ' + raion + ',' + ' ' + 'м.' + ' ' + metro + ',' + ' ' + street + ',' + ' ' + house
            

        if address_style == 1:
            street = street_list[randint(0, len(street_list) - 1)].strip()
            address = street + ',' + ' ' + house
            
        extr_street = street_extractor(address)
        extr_dom = dom_extractor(address)

        if extr_street != street or extr_dom != house:
            print(f'Address is: [{address}];\nHouse is: [{house}];\nStreet is: [{street}];\nExtracted house is [{extr_dom}, extracted street is [{extr_street}]')
            print('========================')

        if extr_dom == house and extr_street == street:
            print('OK')

    return 'Done!'


equal_tester(100000)
