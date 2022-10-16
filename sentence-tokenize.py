import stanza
import json
from tqdm import tqdm
import os

def save_as_json(objects, fname):
    with open('data/'+fname, 'w') as output:
        json.dump(objects, output, indent=4)

nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma', logging_level='DEBUG')
fiction_list = [_ for _ in os.listdir("input") if _.endswith(".txt")]

for fiction in tqdm(fiction_list):
    list_for_json = []

    with open("input/" + fiction, "r") as f:
        documents = f.readlines()

    in_docs = [stanza.Document([], text=d) for d in documents]  # Wrap each document with a stanza.Document object
    out_docs = nlp(in_docs)  # Call the neural pipeline on this list of documents

    for d in out_docs:
        list_for_json.append(d.to_dict())

    save_as_json(list_for_json, fiction)

