import spacy
from spacy import displacy

nlp = spacy.load('en_core_web_sm')


def pocess_spacy(text):
    doc = nlp(text)
    return displacy.render(doc, style='ent')
