from collections import defaultdict
from stanza.models.common.doc import Document
from tqdm import tqdm
import os
import sys
import json

def get_text(stanza_sentence):
    return ' '.join([w.text for w in stanza_sentence.words])

def get_text_from_dict(sentence_dict):
    return ' '.join([w['text'] for w in sentence_dict])

def sample_match(sent, query, target_pos):
    lemmas_in_sent = [w.lemma.lower() for w in sent.words]
    try:
        i = lemmas_in_sent.index(query)  # only consider the first match (and ignore the rest if any)
    except ValueError:
        return False

    try:
        word_pos = sent.words[i].pos
    except IndexError:
        return False

    if word_pos in target_pos:
        return True
    else:
        return False

json_path = "data/fiction-tokenized.json"
usage_path = "data/usages.json"

query = sys.argv[1]
verbose = True
target_pos = ["NOUN", "PROPN"]

# Import tokenized fiction corpus
with open(json_path, "rb") as f:
    tokenized_json = json.load(f)

doc_cnt = 0
sent_cnt = 0

coca_dict = defaultdict(list)
print('Query:', query)

for doc in tokenized_json:
    doc = Document(doc)
    doc_cnt += 1
    for i_sent, sent in enumerate(tqdm(doc.sentences)):
        sent_cnt += 1
        if sample_match(sent, query, target_pos):
            sent_curr = get_text(sent)
            if verbose:
                print('-------')
                print(sent_curr)
            if i_sent > 1:
                sent_before = get_text(doc.sentences[i_sent-1])
            else:
                sent_before = ''
            if i_sent < len(doc.sentences)-1:
                sent_next = get_text(doc.sentences[i_sent+1])
            else:
                sent_next = ''
            cdoc = {'sent_before': sent_before, 'sent_curr': sent_curr, 'sent_next': sent_next}
            coca_dict[query].append(cdoc)
        else:
            continue

print("# documents: {}".format(str(doc_cnt)))
print("# sentences: {}".format(str(sent_cnt)))

if os.path.exists(usage_path):  # update the existing json dict
    with open(usage_path, "r") as j:
        prev_dict = json.load(j)
    prev_dict[query] = coca_dict[query]
    new_dict = prev_dict
else:  # write a new json dict
    new_dict = coca_dict

with open(usage_path, "w") as j:
    json.dump(new_dict, j, indent=4)


# with open("results/" + query + ".txt", "w") as f:
#     for doc in coca_dict[query]:
#         line = ' | '.join([doc.sent_before, doc.sent_curr, doc.sent_next])
#         f.writelines(line + '\n')


