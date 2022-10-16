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

query = sys.argv[1]

json_path = "data/"
usage_path = "result/usages.json"

verbose = False
target_pos = ["NOUN", "PROPN"]

doc_cnt = 0
sent_cnt = 0

# Import tokenized fiction corpus
fiction_list = [_ for _ in os.listdir("data") if _.endswith(".txt")]
coca_dict = defaultdict(list)

print('Query:', query)

for fiction in fiction_list:
    with open(json_path + fiction, "rb") as f:
        tokenized_json = json.load(f)

    for doc in tqdm(tokenized_json, leave=False):
        doc = Document(doc)
        doc_cnt += 1
        for i_sent, sent in enumerate(doc.sentences):
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


# Write a separate result file for a query
with open("result/" + query + ".txt", "w") as f:
    for doc in coca_dict[query]:
        line = ' | '.join([doc['sent_before'], doc['sent_curr'], doc['sent_next']])
        f.writelines(line + '\n')

