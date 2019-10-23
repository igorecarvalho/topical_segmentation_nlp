import nltk
import unidecode
import string

nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = stopwords.words('portuguese')

class Preprocessing:

    def __init__(self):
        self.sent_tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')
        self.stemmer = nltk.stem.RSLPStemmer()

    def remove_accents(self, text):
        return unidecode.unidecode(text)
    
    def remove_stopwords(self, sentences):
        filtred_sentence = []
        for sentence in sentences:
            filtred_sentence.append([word for word in sentence if word not in stop_words])
        return filtred_sentence

    def remove_punctuation(self, sentences):
        return [text.translate(str.maketrans('','',string.punctuation)) for text in sentences]

    def tokenize_sentences(self, text):
        sentences = self.sent_tokenizer.tokenize(text)
        return sentences

    def tokenize_words(self, sentences):
        tokens = []
        for text in sentences:
            tokens.append(nltk.tokenize.word_tokenize(text))
        return tokens

    def lemmatize(self, text):
        return text

    def stemmize(self, tokens):
        return [self.stemmer.stem(word) for word in tokens]

    def lowercase(self, sentences):
        return [text.lower() for text in sentences]