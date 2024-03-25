import polars as pl
import os
import re
import spacy
from typing import List, Tuple
from gensim.models.ldamodel import LdaModel
from gensim.corpora.dictionary import Dictionary
from gensim import corpora


class TopicModeling:
    """
    Class for performing topic modeling on text data.
    """

    def __init__(self,
                 language_model: str = "en_core_web_sm",
                 path_to_serialize: str = "../my_benefits/models",

                 ):
        self.nlp = spacy.load(language_model)
        self.path_to_serialize = path_to_serialize
        self.lda_model_filename = 'pretrained_lda_model.model'
        self.dictionary_filename = 'pretrained_dictionary.dict'

    def preprocessing_text(self, text: str) -> List[str]:
        """
        Tokenizes and preprocesses the input text, removing stopwords and short tokens.

        Returns:
        list: A list of lemmatized preprocessed tokens.
        """

        def clean_data(text: str) -> str:
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            phone_pattern = r'(\d{3}[-.\s]??\d{3}[-.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-.\s]??\d{4}|\d{3}[-.\s]??\d{4})'
            url_pattern = r'\b(?:http[s]?://|www\.)[^\s()<>]+(?:\([\w\d]+\)|([^[:punct:]\s]|/))'
            # Removing Patterns
            text = re.sub(email_pattern, '', text)
            text = re.sub(phone_pattern, '', text)
            text = re.sub(url_pattern, '', text)
            text = re.sub(r'-\n', '', text)
            text = re.sub(r'\n', ' ', text)
            text = re.sub(r'[^a-zA-Z0-9.\s]', '', text)
            text = re.sub(r'\d+', '', text)
            text = re.sub(r'\s+', ' ', text).strip()
            return text

        doc = re.sub(r'\W', ' ', clean_data(text))
        # Convert text to lowercase
        doc = doc.lower()
        doc = self.nlp(doc)
        # Lemmatize and remove stop words
        tokens: List[str] = []
        for token in doc:
            if token.is_alpha and not token.is_stop and len(token) > 3:
                tokens.append(token.lemma_)
        return tokens
    # TODO: Test if this function can be reafactored to use lamda function apply over the column text

    def train_model(self, preprocessed_docs: pl.DataFrame, number_of_topics: int = 20, passes: int = 10):
        """
        Create a bag of words (BoW) and serialize it representation for each document using Gensim.
        Args:
            preprocessed_docs (pl.DataFrame): pages extracted from pdfs clennead and tokenized 
            path_to_serialize (str): path for bag_of_words file
            num_topics (int): number of topics
            passes (int): lda algorithm
        """
        documents_to_process = preprocessed_docs['tokenized_text'].to_list()
        dictionary = corpora.Dictionary(documents_to_process)
        dictionary.filter_extremes(no_below=2, no_above=0.5)
        bow_corpus = [dictionary.doc2bow(doc, allow_update=True)
                      for doc in documents_to_process]
        lda_model = LdaModel(corpus=bow_corpus, id2word=dictionary,
                             num_topics=number_of_topics, passes=passes)
        lda_model.save(os.path.join(
            self.path_to_serialize, self.lda_model_filename))
        dictionary.save(os.path.join(
            self.path_to_serialize, self.dictionary_filename))

    def get_path_to_serialize(self):
        return self.path_to_serialize

    def get_lda_model_filename(self):
        return self.lda_model_filename

    def get_dictionary_filename(self):
        return self.dictionary_filename

    def get_list_of_topics_from_document(self, preprocessed_docs: List[str], path_pretrained_model: str) -> List[str]:

        def load_pretrained_model(path_to_serialize: str, model_filename: str, dictionary_filename: str) -> Tuple[LdaModel, Dictionary]:
            pretrained_lda_model = LdaModel.load(
                os.path.join(path_to_serialize, model_filename))
            pretrained_dictionary = corpora.Dictionary.load(
                os.path.join(path_to_serialize, dictionary_filename))
            return pretrained_lda_model, pretrained_dictionary

        pretrained_lda_model, pretrained_dictionary = load_pretrained_model(
            self.path_to_serialize, self.lda_model_filename, self.dictionary_filename)
        new_corpus = [pretrained_dictionary.doc2bow(
            doc) for doc in preprocessed_docs]
        # Classify the new documents using the pre-trained LDA model
        for i, doc_bow in enumerate(new_corpus):
            print(f"Document {i+1}:")
            topic_distribution = pretrained_lda_model[doc_bow]
            sorted_topics = sorted(
                topic_distribution, key=lambda x: x[1], reverse=True)
        topics_words = []
        for topic_id, _ in sorted_topics:
            topic_words = pretrained_lda_model.show_topic(topic_id)
            for word, prob in topic_words:
                topics_words.append(f"\t{word} (Probability: {prob:.3f})")
        return topic_words
