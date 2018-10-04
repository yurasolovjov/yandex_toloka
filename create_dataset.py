import os
import sys
import argparse
from glob2 import glob
import random
import re
import csv
import shutil
import pickle
import pprint



def converTime(strtime, time_labels):

    try:
        strtime = str(strtime)
        strtime = str(time_labels[strtime])
    except:
        raise Exception("Can not convert time")

    return strtime

def parse_header(data,input_tag = str("INPUT"),output_tag = str("OUTPUT")):

    input_index = list()
    output_index = list()

    for line in data:

        counter = int(0)

        for l in line:
            separate = str(l).split(":")

            info = {"tag":separate[1],"index":counter}

            if str(l).find(input_tag) >= 0:
                input_index.append(info)
            elif str(l).find(output_tag) >= 0:
                output_index.append(info)

            counter+=1

        return input_index,output_index

def parse_body_line(line, input_index, output_index, time_labels):

    info_inp = list()
    info_out = list()

    for inp in input_index:
        info_inp.append( {"tag":inp['tag'], "data":line[inp["index"]]} )

    for out in output_index:
        if str(out["tag"]).find("time") >= 0:
            data = converTime(line[out["index"]],time_labels=time_labels)
        else:
            data = line[out["index"]]

        info_out.append({"tag":out['tag'], "data":data})

    return {"input":info_inp,"output":info_out}

def write(outcatalog, data):

    if not os.path.exists(outcatalog):
        os.makedirs(outcatalog)

    meta_pickle_file = os.path.join(outcatalog,"meta_yandex_toloka.pickle")
    readme_file = os.path.join(outcatalog,"readme.txt")

    with open(meta_pickle_file,"wb") as f:
        pickle.dump(data,f)


    with open(readme_file,"w") as f:

        s = "Example struct of pickle file \n\n\n"

        f.write(s)
        f.write(pprint.pformat(data[0]))

    pass

def getListFiles(catalog, tokens = ["*.mp4","*.amr"]):

    tmpfiles = list()

    for token in tokens:
        ctlog = catalog +'/**/'+ token
        files = glob(ctlog, recursive=True);

    for vfile in files:
        tmpfiles.append(vfile);

    return tmpfiles


def main():

    parser = argparse.ArgumentParser(description="Options");
    parser.add_argument("-i", "--input", help="Input tsv-meta file from yandex toloka", default=None)
    parser.add_argument("-o", "--output", help="Output catalog", default="./dataset_toloka")
    parser.add_argument("-c", "--catalog", help="Catalog of files from yandex toloka", default=None)

    args = parser.parse_args()

    inputCatalog = os.path.abspath(args.input)
    outputCatalog = os.path.abspath(args.output)
    catalog = os.path.abspath(args.catalog)


    if os.path.exists(catalog):
        files = getListFiles(catalog)

        if not os.path.exists(outputCatalog):
            os.makedirs(outputCatalog)

        for file in files:
            t,h = os.path.split(file)

            outfile = os.path.join(outputCatalog,h)

            try:
                if not os.path.exists(outfile):
                    shutil.copyfile(file,outfile)
                    print("Copy file:", str(h))
            except:
                print("*** ERROR *** Can not copy file:", str(h))
                continue



    timelabels = {"time_1":"00:00 - 08:00",
                  "time_2":"08:00 - 12:00",
                  "time_3":"12:00 - 18:00",
                  "time_4":"18:00 - 24:00"
                  }

    if inputCatalog == None:
        inputCatalog = os.path.abspath(sys.modules["__main__"].__file__)

    findedFiles = os.path.join(inputCatalog,"*.tsv")

    inputFiles = glob(findedFiles)

    if len(inputFiles) == 0:
        raise Exception("*** ERROR *** : tsv-meta files is not found")


    for file in inputFiles:

        with open(file, "r", encoding="utf-8") as f:

            data = csv.reader(f, delimiter="\t")

            input_index, output_index = parse_header(data)

            meta_info = list()

            for line in data:
                if len(line[0]) == 0:
                    continue

                info = parse_body_line(line, input_index, output_index, time_labels=timelabels)

                meta_info.append(info)


    write(outputCatalog,meta_info)




if __name__ == '__main__':
    main()

