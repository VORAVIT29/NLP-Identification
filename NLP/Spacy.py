import spacy
from spacy import displacy

nlp = spacy.load('en_core_web_sm')

list = list(['PERSON', 'NORP', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'work_of_art',
            'LANGUAGE', 'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL'])
def pocess_spacy(text, list_check):
    doc = nlp(text)
    if 'all' in list_check:
        list_check = list
    options = {"ents": list_check}
    return displacy.render(doc, style='ent', options=options)
