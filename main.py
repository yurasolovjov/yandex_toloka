import os
import sys
import argparse
from glob2 import glob
import random
import re
import csv


regular_expression = re.compile("[а-яА-Я]+")

header = ["INPUT:session1_text",
          "INPUT:session2_text",
          "INPUT:session3_text",
          "INPUT:session4_text",
          "INPUT:session1_number",
          "INPUT:session2_number",
          "INPUT:session3_number",
          "INPUT:session4_number"
          ]

common_phrase = int(0)
common_number = str("1 1 2 3 5")

def getRandomSample(len_sequence = 10):

    sequence = [x for x in range(len_sequence)]

    random.shuffle(sequence)
    sample = random.sample(sequence,k=5)

    str_sample = str("")

    for i in sample:
        str_sample += '{0} '.format(i)

    return converNumberStringToWordString(str_sample)

def getRandomPhrase(library,phrase = "", length = 5, id = None):

    if id is None:
        r = random.randint(0,len(library) - 10)
    else:
        r = int(id)

    if (len(library[r]) > 0):
        phrase += library[r]

    phrase_processed = phrase.split(" ")

    counter = int(0)

    for p in phrase_processed:

        if checkWord(p,3) == True:
            counter +=1

    try:
        if counter < length:
            phrase = getRandomPhrase(library = library, phrase = phrase, length = length, id = r + 1)
    except:
        raise  Exception("*** ERROR ***")

    return phrase.lower().replace('\n',' ')

def checkWord(word, length):

    if len(word) >= length :
        return True
    else:
        return False

def getListBooks(catalog):

    catalog = os.path.normpath(catalog+"//*.txt")

    listFiles = glob(catalog,recursive=True)

    return listFiles

def converNumberToWord(number):

    word = str("")

    number = int(number)

    if number == 0:
        word = "ноль"
    elif number == 1:
        word = str("один")
    elif number == 2:
        word = str("два")
    elif number == 3:
        word = str("три")
    elif number == 4:
        word = str("четыре")
    elif number == 5:
        word = str("пять")
    elif number == 6:
        word = str("шесть")
    elif number == 7:
        word = str("семь")
    elif number == 8:
        word = str("восемь")
    elif number == 9:
        word = str("девять")
    else:
        word = str("девять")

    return word

def converNumberStringToWordString(phrase):

    phrase = str(phrase).replace(" ","")

    new_phrase = str("")

    for number in phrase:

        word = converNumberToWord(number)

        new_phrase += word + str(", ")

    new_phrase = new_phrase[:-2]

    return new_phrase


def main():

    parser = argparse.ArgumentParser(description="Options");
    parser.add_argument("-i", "--input", help="Catalog of books. Catalog should include txt files", action="append", default=None, nargs="*")
    parser.add_argument("-o", "--output", help="Output catalog", default="./model_toloka")
    parser.add_argument("-l", "--len_dictionary", help="Length of dictionary", type=int, default=5)
    parser.add_argument("-s", "--shuffle", help="Shuffle of data", default=False)


    args = parser.parse_args()

    outputCatalog = os.path.abspath(args.output)
    input_list_catalogs = args.input
    inputCatalogs = list()
    len_dictionary = int(args.len_dictionary)
    shuffle_data = bool(args.shuffle)

    if input_list_catalogs is None:
        raise Exception("Input catalog is None")


    for inp in input_list_catalogs:
        for i in inp:
            inputCatalogs.append(i)


    books = list()

    for input in inputCatalogs:

        books += getListBooks(input)


    library = list()

    for book in books:
        with open(book,'r') as f:

            library += [w for w in filter(regular_expression.match,f.readlines())]

    pair_base = list()

    for line in library:

        if len(line) < 2:
            library.remove(line)

    if shuffle_data == True:
        random.shuffle(library)

    count_line = len(library)
    count = int(0)

    for line in library:

        line = getRandomPhrase(library=library, length=len_dictionary)

        try:
            line_data = {"number_1": getRandomSample(len_dictionary),
                         "phrase_1": line,
                         "number_2": getRandomSample(len_dictionary),
                         "phrase_2": line,
                         "number_3": getRandomSample(len_dictionary),
                         "phrase_3": getRandomPhrase(library=library, length=len_dictionary),
                         "number_4": converNumberStringToWordString(common_number),
                         "phrase_4": getRandomPhrase(library=library, length=len_dictionary, id = common_phrase)
                         }
        except:
            print("*** ERROR ***")
            continue

        pair_base.append(line_data)

        count +=1

        print(str(count) + "/" + str(count_line))


    outputFile = os.path.join(outputCatalog,"yandex_toloka_meta.tsv")

    if not os.path.exists(outputCatalog):
        os.makedirs(outputCatalog)
    elif os.path.exists(outputFile):
        os.remove(outputFile)

    with open(outputFile,'w+', encoding='utf-8') as tsvfile:
        writer = csv.writer(tsvfile,delimiter='\t')
        writer.writerow(header)

        for line in pair_base:
            data = list()
            data.append(line['phrase_1'])
            data.append(line['phrase_2'])
            data.append(line['phrase_3'])
            data.append(line['phrase_4'])
            data.append(line['number_1'])
            data.append(line['number_2'])
            data.append(line['number_3'])
            data.append(line['number_4'])
            writer.writerow(data)



if __name__ == '__main__':
    main()

