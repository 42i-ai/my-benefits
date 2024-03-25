import polars as pl
import re
import spacy
from typing import List


class TopicModeling:
    """
    Class for performing topic modeling on text data.
    """

    def __init__(self,
                 language_model: str = "en_core_web_sm"
                 ):
        self.nlp = spacy.load(language_model)

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

    def train_model(self):
        """
        Train the topic modeling model.
        """
        # Train model
        pass

    def predict(self):
        """
        Use the trained model to predict topics.
        """
        # Predict
        pass

    def evaluate(self):
        """
        Evaluate the performance of the topic modeling model.
        """
        # Evaluate
        pass

    def save_model(self):
        """
        Save the trained model to a file.
        """
        # Save model
        pass

    def load_model(self):
        """
        Load a trained model from a file.
        """
        # Load model
        pass
