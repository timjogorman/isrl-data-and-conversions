#!/usr/bin/env python3
# -*- coding: utf-8; -*-
import nltk
import os
import sys
import json
import logging
import argparse

def treebank2txt(treebank_location):
    trees = open(treebank_location).read()
    all_trees = [x for x in trees.replace("\n( ","\n\n( ").replace("\n((","\n\n((").split("\n\n") if len(x.strip()) > 0]
    sentences = []
    for sid, each_sentence in enumerate(all_trees):
        sent = " ".join([x[0] for x in nltk.Tree.fromstring(each_sentence).pos() if not x[1] == "-NONE-"]) 
        sentences.append(sent)
    return sentences

def load_all_bnb_data(treebank_location):
    tbdict = {}
    for tranche in ['train','test','validation']:
        dir_path = 'source/'+tranche+"/nombank/"
        for metadata_file in os.listdir(dir_path):
            if metadata_file.endswith(".metadata.json"):
                its_file = []
                for line in json.load(open(dir_path+"/"+metadata_file)):
                    each_file = line['sentence_id']
                    wsj_partition = each_file[4:6]
                    
                    tb3file = treebank_location+"/"+wsj_partition+"/"+each_file.split(".")[0]+".mrg"
                    if os.path.exists(tb3file):
                        if not each_file.split(".")[0] in tbdict:
                            tbdict[each_file.split(".")[0]] = treebank2txt(tb3file)
                        its_file.append(tbdict[each_file.split(".")[0]][int(line['sentence'])])
                    else:
                        logging.error(f"can't find {tb3file}")
                        continue
                open(dir_path+"/"+metadata_file.replace(".metadata.json",".txt"),'w').write("\n".join(its_file))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script for getting the raw text for Gerber and Chai 2012 data')
    parser.add_argument('tb3', help='Location of the treebank 3 wsj data')
    args = parser.parse_args()
    if not 'treebank_3/parsed/mrg/wsj/' in args.tb3:
        logging.error(f"double check if this looks right -- {args.tb3} should probably point to parsed/mrg/wsj/ within treebank 3")
    load_all_bnb_data(args.tb3)
