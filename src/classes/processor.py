import nltk
import string

from gensim import corpora
from gensim import models
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag.perceptron import PerceptronTagger
from nltk.tokenize import TreebankWordTokenizer


class Processor(object):
    def __init__(self,
                 stop_words=None,
                 sent_detector=None,
                 documents=None):
        # Load a persisted list of stopwords
        # unless something else is specified
        if not stop_words:
            self._stop_words = stopwords.words('english')
            self._stop_words += ['minister', 'question', 'member', "member’s"]
        else:
            self._stop_words = stop_words
        # Load these to save time reading from
        # disk later
        if not sent_detector:
            self._sent_detector = nltk.data.load(
                'tokenizers/punkt/english.pickle')
        else:
            self._sent_detector = sent_detector
        self._tokenizor = TreebankWordTokenizer()
        self._lemmatizer = WordNetLemmatizer()
        self._tagger = PerceptronTagger()

        if documents:
            # Create a list of lists of tokens all lowercased
            # , lemmatized and filtered
            self.documents = self._make_tokens(documents)
            self.dictionary = corpora.Dictionary(self.documents)
            self.corpus = self._bag_o_words(self.documents)
            self._tf_idf_model = models.TfidfModel(self.corpus)
            self.transformed_corpus = self._tf_idf_model[self.corpus]
        else:
            self.documents = None

    def _bag_o_words(self, documents):
        return [self.dictionary.doc2bow(doc) for doc in documents]

    def _remove_punctuation(self, sentences):
        tokens = [token for sentence in sentences for token in sentence]
        return [token for token in tokens if token not in string.punctuation]

    def _lemmatize(self, tokens):
        return [self._lemmatizer.lemmatize(token) for token in tokens]

    def _make_tokens(self, documents):
        documents = [doc for doc in documents[0:10] if doc is not None]
        outer_tokens = []
        for doc in documents:
            inner_tokens = []
            doc = doc.lower()
            sentences = self._sent_detector.tokenize(doc)
            # Tokenize the sentences
            tokens = [self._tokenizor.tokenize(sentence) for
                      sentence in sentences]
            # Remove punctuations
            tokens = self._remove_punctuation(tokens)
            # Only keep the lemma
            tokens = self._lemmatize(tokens)
            # Label tokens
            token_labels = self._tagger.tag(tokens)
            for tok in token_labels:
                if tok[1] == "NN" and tok[0] not in self._stop_words:
                    inner_tokens.append(tok[0])
            outer_tokens.append(inner_tokens)
        return outer_tokens
