from audioop import reverse
from encodings import utf_8
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from collections import Counter
from gensim.corpora.dictionary import Dictionary
from gensim.models.tfidfmodel import TfidfModel
from collections import defaultdict
import itertools
import os

# patchHead = 'data\\'
# patch = os.listdir(patchHead)
# Read TXT file
# f = open(f".\data\ch3\wiki\wiki_article_{i}.txt", "r")


# def convertNLP(dir):
#     articles = []
#     text_list = ""
#     for i in dir:
#         article = open(i, "r").read()
#         text_list += f"\nชื่อไฟล์ {os.path.split(i)[-1]}\n{article}\n"
#         # Tokenize the article: tokens
#         tokens = word_tokenize(article)
#         # Convert the tokens into lowercase: lower_tokens
#         lower_tokens = [t.lower() for t in tokens]
#         # Retain alphabetic words: alpha_only
#         alpha_only = [t for t in lower_tokens if t.isalpha()]
#         # Remove all stop words: no_stops
#         no_stops = [
#             t for t in alpha_only if t not in stopwords.words('english')]
#         # Instantiate the WordNetLemmatizer
#         wordnet_lemmatizer = WordNetLemmatizer()
#         # Lemmatize all tokens into a new list: lemmatized
#         lemmatized = [wordnet_lemmatizer.lemmatize(t) for t in no_stops]
#         # list_article
#         articles.append(lemmatized)
#         # print(articles)
#         dictionary = Dictionary(articles)
#         computer_id = dictionary.token2id.get("premier")  # get id
#         # dictionary.get(computer_id)
#         text = "มีข้อมูล" if isinstance(computer_id, int) else"ไม่มีข้อมูล"

#     return [articles, text_list]

# create a corpus: corpus
# corpus = [dictionary.doc2bow(a) for a in articles]
# save the second document : doc
# doc = corpus[0]
# sort yhe doc for frequency: bow_doc
# bow_doc = sorted(doc, key=lambda w: w[1], reverse=True)
# print the top 5 words of the document alongside the count
# for word_id, word_count in bow_doc[:5]:
#     print(dictionary.get(word_id), word_count)

# create the defaultdict: total_word_count
# total_word_count = defaultdict(int)
# for word_id, word_count in itertools.chain.from_iterable(corpus):
#     total_word_count[word_id] += word_count

# sort a sort list from the defaultdict: sorted_word_count
# sorted_word_count = sorted(total_word_count.items(),
#                            key=lambda w: w[1], reverse=True)

# print the top 5 words across all doccuments alongside the count
# for word_id, word_count in sorted_word_count[:5]:
#     print(dictionary.get(word_id), word_count)


class NLP:

    def __init__(self, files_list):
        self.file = files_list
        self.articles = []
        self.corpus = []

    def createToken(self):
        self.reset()
        text_list = ""

        for i in self.file:
            article = open(i, "r").read()
            text_list += f"\nชื่อไฟล์ {os.path.split(i)[-1]}\n{article}\n"
            tokens = word_tokenize(article)
            lower_tokens = [t.lower() for t in tokens]
            alpha_only = [t for t in lower_tokens if t.isalpha()]
            no_stops = [
                t for t in alpha_only if t not in stopwords.words('english')]
            wordnet_lemmatizer = WordNetLemmatizer()
            lemmatized = [wordnet_lemmatizer.lemmatize(t) for t in no_stops]
            self.articles.append(lemmatized)

        return text_list

    def searchText(self, search):
        dictionary = Dictionary(self.articles)
        computer_id = dictionary.token2id.get(search)
        # text = "มีข้อมูล" if isinstance(computer_id, int) else"ไม่มีข้อมูล"
        if isinstance(computer_id, int):
            text = '<div class = "alert alert-success alert-dismissible fade show" role = "alert" ><strong >*</strong> มีข้อมูล <button type = "button" class = "btn-close" data-bs-dismiss = "alert"aria-label = "Close" ></button ></div>'
        else:
            text = '<div class = "alert alert-danger alert-dismissible fade show" role = "alert" ><strong >*</strong> ไม่มีข้อมูล <button type = "button" class = "btn-close" data-bs-dismiss = "alert"aria-label = "Close" ></button ></div>'

        return text

    def bag_of_words(self):
        dictionary = Dictionary(self.articles)
        self.corpus = [dictionary.doc2bow(a) for a in self.articles]
        bagOfWords = ""

        # total_word_count
        total_word_count = defaultdict(int)
        for word_id, word_count in itertools.chain.from_iterable(self.corpus):
            total_word_count[word_id] += word_count

        sorted_word_count = sorted(
            total_word_count.items(), key=lambda w: w[1], reverse=True)
        bagOfWords += "\nTop 5 Total bag of word\n"
        for word_id, word_count in sorted_word_count[:5]:
            bagOfWords += dictionary.get(
                word_id)+" " + str(word_count) + "\n"

        return bagOfWords

    def TfIdf(self):
        text = ""
        i = 0
        dictionary = Dictionary(self.articles)
        self.corpus = [dictionary.doc2bow(a) for a in self.articles]
        tfidf = TfidfModel(self.corpus)
        # print(self.corpus)
        if len(self.corpus) > 1:
            for cor in self.corpus:
                tfidf_weights = tfidf[cor]
                sorted_tfidf_weights =\
                    sorted(tfidf_weights, key=lambda w: w[1], reverse=True)
                text += f"\nไฟล์ {os.path.split(self.file[i])[-1]} \n"
                for term_id, weight in sorted_tfidf_weights[:5]:
                    text += "\t" + \
                        dictionary.get(term_id) + " " + str(weight) + "\n"
                text += "\n"
                i += 1

        return text

    def reset(self):
        self.articles = []
