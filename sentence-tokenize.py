import stanza
import json
from tqdm import tqdm
import os

def save_as_json(objects):
    with open('data/fiction-tokenized.json', 'w') as output:
        json.dump(objects, output, indent=4)

# stanza.download('en', package='partut')
# ParTUT has the best performance for English tokenization among the four models in Stanza
# Treebank	Tokens	Sentences	Words	UPOS	XPOS	UFeats
# UD_English-GUM	99.25	88.98	99.42	96.15	96.15	95.39
# UD_English-EWT	99.36	89.09	99.11	95.64	95.40	96.23
# UD_English-LinES	99.96	90.05	99.96	96.92	96.17	96.71
# UD_English-ParTUT	99.66	100.00	99.57	96.11	95.79	95.26

# nlp = stanza.Pipeline(lang='en', package='partut', processors='tokenize,mwt,pos,lemma', logging_level='DEBUG')
nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma', logging_level='DEBUG')
fiction_list = [_ for _ in os.listdir("input") if _.endswith(".txt")]
list_for_json = []

for fiction in tqdm(fiction_list):
    with open("input/" + fiction, "r") as f:
        documents = f.readlines()

    in_docs = [stanza.Document([], text=d) for d in documents]  # Wrap each document with a stanza.Document object
    out_docs = nlp(in_docs)  # Call the neural pipeline on this list of documents

    for d in out_docs:
        list_for_json.append(d.to_dict())

save_as_json(list_for_json)

