#!/usr/bin/env python
from pandocfilters import toJSONFilter
from pandocfilters import OrderedList, Plain, Str, Space

def raw_list(key, value, format, meta):
    if key == "CodeBlock":
        [[ident, classes, keyvals], code] = value
        if "raw_list" in classes:
            OrderedList_list = []
            for listitem in code.split("\n"):
                if listitem is not None:
                    listitem_list = listitem.split(" ")
                    typechar = listitem_list[0]
                    i = 0
                    # if the kind of the list is "(typechar)", it has to take the second char
                    if typechar[-1] == ")":
                        i = 1
                        if typechar[0] == "(":
                            formating = "TwoParens"
                            number_str = typechar[1:][:-1]
                        else:
                            formating = "OneParen"
                            number_str = typechar[:-1]
                    elif typechar[-1] == ".":
                        formating = "Period"
                        number_str = typechar[:-1]
                    else:
                        print(typechar)
                        print(typechar[-1])
                        raise ValueError("Wrong formatting")

                    type_of_list, number = gettype_and_num(number_str)

                    Str_list = []
                    for str_part in listitem_list[1:]:  # loops trough all except the first item,
                        Str_list.append(Str(str_part))        # which is the type char

                    Str_Spcae_list = []
                    Str_Spcae_list.append(Str_list[0])
                    for Str_item in Str_list[1:]:
                        # Str_Spcae_list.append(Space())
                        Str_Spcae_list.append({'t': "Space"})
                        Str_Spcae_list.append(Str_item)

                    OrderedList_list.append(OrderedList([number, {"t":type_of_list}, {"t":formating}], [[Plain(Str_Spcae_list)]]))

            return OrderedList_list


def gettype_and_num(list_style_type_character):
    """ Input typechar of OrderedList, outputs its type
    inputs:  [1-9],   i,          I,          [a-z],      [A-z]
    outputs: Decimal, LowerRoman, UpperRoman, LowerAlpha, UpperAlpha
    """
    if list_style_type_character.isnumeric():
        type = "Decimal"
        number = int(list_style_type_character, 10)
    elif list_style_type_character.islower():
        type = "Lower"
    elif list_style_type_character.isupper():
        type = "Upper"
    else:
        raise ValueError("Wrong list type")

    if checkIfRomanNumeral(list_style_type_character) is None:
        type += "Roman"
        number = roman_to_int(list_style_type_character.upper())
    elif not list_style_type_character.isnumeric():
        type += "Alpha"
        number = int(list_style_type_character, 36) - 9

    return type, number


def roman_to_int(s):
    rom_val = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    int_val = 0
    for i in range(len(s)):
        if i > 0 and rom_val[s[i]] > rom_val[s[i - 1]]:
            int_val += rom_val[s[i]] - 2 * rom_val[s[i - 1]]
        else:
            int_val += rom_val[s[i]]
    return int_val


def checkIfRomanNumeral(numeral):
    """Controls that the userinput only contains valid roman numerals"""
    numeral = numeral.upper()
    validRomanNumerals = ["M", "D", "C", "L", "X", "V", "I"]
    for letters in numeral:
        if letters not in validRomanNumerals:
            return False


if __name__ == "__main__":
    """

    key = "CodeBlock"
    value = [["", ["raw_list"], []], "1. Ordered List_1\n3. Ordered List_2\n2. Ordered List_3"]

    print(raw_list(key, value, False, False))
    """
    toJSONFilter(raw_list)
