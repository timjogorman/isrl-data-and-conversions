#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, sys, os
import logging
import argparse
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


     
def get_token_dictionary(alignment_data_unsplit_location):
    """ 
    Takes a pointer to an AMR release location, and rips out a dictionary mapping AMR ids to their tokenized strings.
    Note that this assumes ::tok elements, which are ONLY present in the automatic alignments included in AMR releases
    """
    amrid2tokens = {}
    # A small set of files don't map to the currently available 2017 release, and have sentences hidden away in this file.
    # I'm hoping to remove this as soon as possible. 
    temp = json.load(open("bin/patch-for-a-few-amrs-only-released-in-2019-release.json"))
    for amrid in temp:
        amrid2tokens[amrid] = temp[amrid].replace("%*%"," ")
    for some_file in os.listdir(alignment_data_unsplit_location):
        for line in open(alignment_data_unsplit_location+"/"+some_file).read().split("\n\n# ::id "):
            amr_id =line.strip().split(" ")[0]
            t = [x for x in line.split("\n") if "::tok" in x]
            if len(t) > 0:
                its_tokenized_sentence = t[0].split("::tok")[1].replace("@-","-").replace("-@","-").strip()
                amrid2tokens[amr_id] = its_tokenized_sentence
    return amrid2tokens

def load_amr_text_file(metadata_file_path, amrid2tokens_dict):
    """ 
    Take a metadata file (just a json) and builds a txt file next to it with the raw source text.
    """
    list_of_sentences = []
    for sentence in json.load(open(metadata_file_path)):
        sid = sentence['sentence_id']
        if sid in amrid2tokens_dict:
            list_of_sentences.append(amrid2tokens_dict[sid].strip("\n"))
            logging.debug(f"mapping {sid} into:: {amrid2tokens_dict[sid]}")
        else:
            logging.error(f"mapping error mapping {sid} -- this will break the data for {metadata_file_path} if not fixed")
    open(metadata_file_path.replace(".metadata.json",'.txt'),'w').write("\n".join(list_of_sentences))




def load_all_amr_files_in_directory(directory_location, alignment_location):
    """ 
    Goes through a directory of metadata files (mostly just lists of amr IDs) and creates a text file for each one
    """

    amrid2tokens_dict = get_token_dictionary(alignment_location)
    for file in os.listdir(directory_location):
        if file.endswith(".metadata.json"):
            file_path = directory_location+"/"+file
            load_amr_text_file(file_path, amrid2tokens_dict)

def load_all_amr_data(alignment_location):    
    """ 
    Pull the source text for the MSAMR and WS-AMR datasets
    """

    for amr_metadata_location in ["source/train/msamr/", "source/validation/msamr/", "source/test/msamr/", "source/train/amrsamesent/"]:        
        logging.info(f"getting text files for {amr_metadata_location}")
        load_all_amr_files_in_directory(amr_metadata_location, alignment_location)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Simple script for pulling text files')
    parser.add_argument('amrloc', help='Location of the alignments/unsplit folder from the AMR release (2017T10 or later)')
    args = parser.parse_args()
    load_all_amr_data(args.amrloc)
