import typing
import pathlib
import json
import argparse
import logging
import numpy as np


import xml.etree.ElementTree as ET

from collections import namedtuple
implicitrole = namedtuple("Implicit", "file sentence index arg")
from typing import List, Dict

class Candidate:
    def __init__(self, file, sentence, start, end, heads=None):
        self.file:str = file
        self.sentence:int = sentence
        self.start:int = start
        self.inclusive_end:int = end  
        self.headindices = heads
    def score(self, gold_other_candidate)-> float:
        if self.sentence == gold_other_candidate.sentence:

            pred_candidate_tokens = set(range(self.start, self.inclusive_end+1))
            gold_candidate_tokens = set(range(gold_other_candidate.start, gold_other_candidate.inclusive_end+1))
            intersection = list(pred_candidate_tokens.intersection(gold_candidate_tokens))
            if self.headindices is None or len(set(gold_other_candidate.headindices).intersection(pred_candidate_tokens)) > 0:
                return (2.0 * len(intersection))/float((len(list(gold_candidate_tokens))+len(list(pred_candidate_tokens))))
            else:
                return 0.0
        else:
            return 0.0



class ComparisonSet:
    def __init__(self, is_gold=False):
        self.implicit_role_candidates = {}
        self.gold = is_gold
    def process_arg(self, predicate, candidate):
        self.implicit_role_candidates[predicate] = self.implicit_role_candidates.get(predicate, []) + [candidate]
        if not self.gold and len(self.implicit_role_candidates[predicate]) > 1:
            logging.error("multiple candidates predicted for the same role -- we assume only the first!!")

    def size_of_recoverable_mentions(self):
        return len(self.implicit_role_candidates)
    def evaluate_candidate(self, implicit_role_id, candidate):
        if not self.gold:
            logging.error("wrong direction, treating predicted arguments as gold")
        best:float = 0.0
        for gold_candidate in self.implicit_role_candidates.get(implicit_role_id,[]):
            partial_overlap = candidate.score(gold_candidate)

            best = max(partial_overlap, best)
        return best
    def add_txt_file(self, some_gold_path, has_head=False):
        with some_gold_path.open() as gold_file:
            for line in gold_file:
                predloc = line.split(" ")[0]
                file, sentence, index, arg = predloc.split(":")[0], predloc.split(":")[1], predloc.split(":")[2], line.split(" ")[2]
                its_role = implicitrole(file, int(sentence), int(index), arg)
                if has_head:
                    token_ids = [int(cand.split(":")[2]) for cand in line.strip("\n").split(" ")[4:]]
                    head_index = [int(x.split(":")[2]) for x in line.strip("\n").split(" ")[3].split("#")]
                    candidate_file, candidate_sent = line.strip("\n").split(" ")[4].split(":")[0], line.strip("\n").split(" ")[4].split(":")[1]
                else:
                    token_ids = [int(cand.split(":")[2]) for cand in line.strip("\n").split(" ")[3:]]
                    head_index = None
                    candidate_file, candidate_sent = line.strip("\n").split(" ")[3].split(":")[0], line.strip("\n").split(" ")[3].split(":")[1]
                c = Candidate(candidate_file, int(candidate_sent), min(token_ids), max(token_ids), head_index)
                self.process_arg(its_role,c)
    
    def add_json_file(self, some_gold_path):
        with some_gold_path.open() as gold_file:
            for line in json.load(gold_file):
                file, sentence, index, arg = str(some_gold_path.name.split(".")[0]), line['predicate-sentence'], line['predicate-start-inclusive'], line['role']
                arg = "A"+arg.split("|")[0][-1]
                its_role = implicitrole(file, int(sentence), int(index), arg)
                candidates = line.get("candidates",[])
                if len(candidates) > 0:
                    for each_candidate in candidates:
                        c= Candidate(file, int(each_candidate['sentence']), int(each_candidate['start-inclusive']), int(each_candidate['end-inclusive']))
                        self.process_arg(its_role,c)

    def add_xml_file(self, some_gold_path):
        with some_gold_path.open() as gold_file:
            tree = ET.parse(gold_file)
            root = tree.getroot()
            for implicit in root:
                if implicit.attrib['recoverable'].lower() == 'true':
                    file, sentence, index, arg = str(some_gold_path.name.split(".")[0]), implicit.attrib['sentence'], implicit.attrib['predstart'], implicit.attrib['role']
                    arg = "A"+arg.split("|")[0][-1]    
                    its_role = implicitrole(file, int(sentence), int(index), arg)
                    for candidate in implicit:
                        c= Candidate(file, int(candidate.attrib['sentence']), int(candidate.attrib['start']), int(candidate.attrib['end']))
                        self.process_arg(its_role,c)

def score_predictions(golds, predictions) -> Dict:
    
    total_score:float = 0
    for role_candidate in sorted(predictions.implicit_role_candidates):
        option = predictions.implicit_role_candidates[role_candidate][0]
        ts = golds.evaluate_candidate(role_candidate, option)
        total_score +=ts
    prec, recall = total_score/predictions.size_of_recoverable_mentions(), total_score/golds.size_of_recoverable_mentions()
    logging.info(f"precision {prec}, recall {recall}, and f1 {calculate_f1(prec, recall)}")
    
def calculate_f1(precision, recall):
    if (precision+recall) == 0:
        return 0
    else:
        return (2.0 * precision*recall )/(precision+recall)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A nontrivial modular command')
    parser.add_argument('gold', help='Gold file (or folder)')
    parser.add_argument('predicted', help='predicted file (or folder)')
    parser.add_argument("--verbose", help="print information ", default=False)
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    gold_path, predicted_path = pathlib.Path(args.gold), pathlib.Path(args.predicted)
    scores:Dict = {"precision":[], "recall":[]}
    distance_histo = []
    golds= ComparisonSet(is_gold=True)
    if gold_path.is_dir():
        for each_gold_path in gold_path.iterdir():
            if each_gold_path.name.endswith(".json"):
                golds.add_json_file(each_gold_path)
            else:
                golds.add_xml_file(each_gold_path)
    else:
        golds.add_txt_file(gold_path, has_head=True)
    predictions= ComparisonSet(is_gold=False)    
    for each_predicted_path in predicted_path.iterdir():
        predictions.add_json_file(each_predicted_path)
    score_predictions(golds, predictions)
