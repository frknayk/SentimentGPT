from transformers import pipeline
from sentimentgpt.utils import (
    get_model_path,
    read_data_file,
    remove_configs_from_model,
    copy_configs_to_model)


### Class is better than creating function, for not needing init classifier everytime
# with different data files. 
class PipelineSIGPT(object):
    """SI-GPT: Sentiment-Intent GPT"""

    def __init__(self, config_zs: dict):
        ###### Copy config files
        self.set_pipe()
        self.zs_classifer = ZeroShotClassifer(
            candidate_labels_intention=config_zs['candidate_labels_intention'],
            candidate_labels_sentiment=config_zs['candidate_labels_sentiment'])

    def set_pipe(self):
        """Remove existing confis,copy updated ones"""
        copy_configs_to_model()

    def del_pipe(self):
        """Remove copied config files"""
        remove_configs_from_model()

    def read_analyze_data(self, data_file: str):
        """Read conversation data, analyze and return the analysis.

        Parameters
        ----------
        data_file : str
            file name of json file

        Returns
        -------
        dict
            Dict of every content's analyze with scores
        """
        ###### Read data
        conversation = read_data_file(data_file)
        if conversation is None:
            raise FileNotFoundError
        ###### Analyze
        conversation_with_labels = {}
        num_samples = len(conversation["conversation"])
        for idx, interaction in enumerate(conversation["conversation"]):
            print(f"Analyzing the conversation, progress: {idx}/{num_samples}")
            conversation_with_labels[idx] = self.analyze_interaction(interaction)
        return conversation_with_labels

    def analyze_interaction(self, interaction: dict):
        """Analyze provided interaction(1 piece of chatbot-human interaction).

        Parameters
        ----------
        interaction : str
            Read interaction data.

        Returns
        -------
        dict
            Dict of every content's analyze with scores
        """    
        return self.zs_classifer.classify(interaction)


class ZeroShotClassifer(object):
    def __init__(self,
                 candidate_labels_sentiment: list,
                 candidate_labels_intention: list):
        """_summary_

        Parameters
        ----------
        candidate_labels_sentiment : list
            List of candidate sentiment labels
        candidate_labels_intention : list
            List of candidate intention labels
        """
        self.candidate_labels_sentiment = candidate_labels_sentiment
        self.candidate_labels_intention = candidate_labels_intention
        model = get_model_path()
        self.classifier = pipeline("zero-shot-classification",
                                   model=model)

    def classify(self, interaction: str):
        """Classify given sentence by given sentiment labels

        Parameters
        ----------
        interaction : str
            _description_

        Returns
        -------
        dict
            {
                'sequence': sentence,
                'labels': self.candidate_labels,
                'scores': [prob_label_1,prob_label_2,...]
            }
        """
        customer = interaction["customer"]
        bot = interaction["bot"]
        # For simplicity, assuming intent and sentiment are None for now
        intent_customer = self.classifier(customer, self.candidate_labels_intention)
        intent_bot = self.classifier(bot, self.candidate_labels_intention)
        sentiment_customer = self.classifier(customer, self.candidate_labels_sentiment)
        sentiment_bot = self.classifier(bot, self.candidate_labels_sentiment)
        conversation_label = {
            "sentence": interaction,
            "intent_bot": {
                "labels": intent_bot['labels'],
                'scores': intent_bot['scores']},
            "intent_customer": {
                "labels": intent_customer['labels'],
                'scores': intent_customer['scores']},
            "sentiment_customer": {
                "labels": sentiment_customer['labels'],
                'scores': sentiment_customer['scores']},
            "sentiment_bot": {
                "labels": sentiment_bot['labels'],
                'scores': sentiment_bot['scores']}
        }
        return conversation_label
