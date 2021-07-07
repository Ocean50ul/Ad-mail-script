from random import randint
import re

g_cases = ["г", "город", "гор", ""]
m_cases = ["москва"]
address = "улица Пушкина, дом Колотушкина 10"


def case_randomizer(line):
    for character in line:
        boolean = randint(0, 1)
        if boolean == 1:
            line = line.replace(character, character.upper())
    return line


def address_constructor():
    gorod = g_cases[randint(0, len(g_cases) - 1)]
    moskva = m_cases[randint(0, len(m_cases) - 1)]

    bool_g = randint(0, 1)
    if bool_g == 1:
        gorod = case_randomizer(gorod)
    
    bool_m = randint(0, 1)
    if bool_m == 1:
        moskva = case_randomizer(moskva)
    
    dot = randint(0, 1)
    whitespace = randint(0, 1)
    without_moskva_and_gorod = randint(0, 100)

    if without_moskva_and_gorod > 98:
        gorod = ''
        moskva = ''

    if moskva == '' and gorod == '':
        return address

    if gorod == '':
        if whitespace == 1:
            return moskva + ' ' + ',' + ' ' + address


    if whitespace == 1 and dot == 1:
        return gorod + '.' + ' ' + moskva + ',' + ' ' + address

    if whitespace == 1:
        return gorod + ' ' + moskva + ' ' + ',' + ' ' + address

    if dot == 1:
        return gorod + '.' + ' ' +  moskva + '.' + ',' + ' ' + address


    return gorod + moskva + ',' + ' ' + address



def starts_with_gorod(line):
    '''Returns True if address starts with город in any form '''
    if line == '':
        return False
    line = line.strip().lower()
    pattern = re.compile(r'^г\w*[.]?')
    match = pattern.search(line)
    if match is None:
        return False
    if len(match.group(0)) <= 6:
        return True
    return False

def starts_with_moscow(line):
    '''Returns True if address starts with Москва in any form'''
    if line == '':
        return False
    line = line.strip().lower()
    pattern = re.compile('москва[.]?')
    match = match = pattern.search(line)
    if match is None:
        return False
    if len(match.group(0)) <= 7:
        return True
    return False


def moscow_check(strng):
    '''Check if address contains city. I dont need city, because it is Moscow by default'''
    if starts_with_gorod(strng) or starts_with_moscow(strng):
        return True
    return False


def completely_eradicate_moscow(line):
    '''Entirely deletes city from line and some other garbrage stuff that i dont need'''
    line = line.strip()
    if line.lower() == 'москва':
        return ''
    while moscow_check(line):
        pattern = re.compile('^.+?, ')
        match = pattern.search(line)
        line = line.replace(match.group(0), '')
    if line.startswith(','):
        line = line[1:].strip()
    return line




for i in range(100000):
    addresss = address_constructor()
    check = moscow_check(addresss)
    if check == False and addresss != "улица Пушкина, дом Колотушкина 10":
        print(addresss)
    addresss = completely_eradicate_moscow(addresss)
    if addresss != "улица Пушкина, дом Колотушкина 10":
        print(addresss)

print('Test is passed!')