import bs4, os, sys


file_path = sys.argv[1]

def getdoc(file_path, sourcefilename):
    text_file_path = "/".join(file_path.split("/")[:-1]).replace("data/","source/")+"/"+ sourcefilename+'.txt'
    source = open(text_file_path).read()
    return source

def represent_instance(document, predicate, candidates, role):
    minsent = max(predicate[0]-10, 0)
    maxsent = min(predicate[0]+10, len(document))
    rep = []
    for line_id, its_sentence in enumerate(document):
        if line_id >= minsent and line_id <= maxsent:
            each_sentence =its_sentence[:]
            if line_id == predicate[0]:
                each_sentence[predicate[1]] = "<<<"+each_sentence[predicate[1]]
                each_sentence[predicate[2]] = each_sentence[predicate[2]]+' ('+role+')>>>'
            for c in candidates:
                if c[0] == line_id:
                    each_sentence[c[1]] = "{{{{"+each_sentence[c[1]]
                    each_sentence[c[2]] = each_sentence[c[2]]+"}}}}"
            rep.append(each_sentence)
    return "\n".join([" ".join(x) for x in rep])
def process_file(file_path):

    its_xml = bs4.BeautifulSoup(open(file_path),'xml')
    
    doc = getdoc(file_path , its_xml.find("ISRLSPANS")['sourcefile'])
    sents = [x.split(" ") for x in doc.split("\n")]
    #print(its_xml)
    for imp in its_xml.find_all("implicit"):
        sent, start, end = int(imp['sentence']), int(imp['predstart']), int(imp['predend'])
        #print(imp['role'], sents[int(imp['sentence'])][start:end+1])
        cans = []
        for cand in imp.find_all("candidate"):
            csent, cstart, cend = int(cand['sentence']), int(cand['start']), int(cand['end'])
            cans.append([csent, cstart, cend])
        
        ri = represent_instance(sents[:], [sent, start, end], cans, imp['role'])
        if "{{{{" in ri:
            print("\n\n\n")
            print(ri)
        #sents[csent][cstart:cend+1])
        
    #print(doc)
process_file(file_path)