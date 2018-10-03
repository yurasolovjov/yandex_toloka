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

def getRandomSample(len_dictionary, len_sequence = 10):

    sequence = [x for x in range(len_sequence)]

    random.shuffle(sequence)
    sample = random.sample(sequence,k=random.randint(len_dictionary, len_dictionary * 2))

    str_sample = str("")

    for i in sample:
        str_sample += '{0} '.format(i)

    return str_sample


def getRandomPhrase(library):
    phrase = str("")

    r = random.randint(0,len(library))

    if (len(library[r]) > 0):
        phrase = library[r]

    return phrase

def getListBooks(catalog):

    catalog = os.path.normpath(catalog+"//*.txt")

    listFiles = glob(catalog,recursive=True)

    return listFiles



def main():

    parser = argparse.ArgumentParser(description="Options");
    parser.add_argument("-i", "--input", help="Catalog of books. Catalog should include txt files", action="append", default=None, nargs="*")
    parser.add_argument("-o", "--output", help="Output catalog", default="./model_toloka")
    parser.add_argument("-l", "--len_dictionary", help="Length of dictionary", type=int, default=5)


    args = parser.parse_args()

    outputCatalog = os.path.abspath(args.output)
    input_list_catalogs = args.input
    inputCatalogs = list()
    len_dictionary = int(args.len_dictionary)

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

    random.shuffle(library)


    count_line = len(library)
    count = int(0)

    for line in library:


        try:
            line_data = {"number_1": getRandomSample(len_dictionary),
                         "phrase_1": line,
                         "number_2": getRandomSample(len_dictionary),
                         "phrase_2": line,
                         "number_3": getRandomSample(len_dictionary),
                         "phrase_3": getRandomPhrase(library),
                         "number_4": getRandomSample(len_dictionary),
                         "phrase_4": getRandomPhrase(library)
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

