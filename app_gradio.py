import sys
import json
import gradio as gr
import numpy as np
from sentimentgpt.classifier import PipelineSIGPT

# # Read from args/ui
candidate_labels_sentiment = ['positive', 'neutral', 'negative']
candidate_labels_intention = ['compatibility','durability','storage','battery','camera']

data_file = "data.json"
config_zs = {
    "candidate_labels_sentiment":candidate_labels_sentiment,
    "candidate_labels_intention":candidate_labels_intention}
pipeline = PipelineSIGPT(config_zs)
result = pipeline.read_analyze_data(data_file)

result = {}
with open("data\data_result.json") as json_file:
    result = json.load(json_file)
    json_file.close()

def dict_to_prob(conversation_dict):
    return dict(zip(
        conversation_dict['labels'], 
        conversation_dict['scores']))

idx = 0
def zeroShotClassification(uploaded_json):
    global idx
    # Read uploaded json
    print("uploaded_json:",uploaded_json)
    # If reached to end of the file(data.json)
    if idx >= len(result):
        sample_dict_sentiment = dict(
            zip(candidate_labels_sentiment, 
            list(np.ones((len(candidate_labels_sentiment),))*-1) )
            )
        sample_dict_intent = dict(
            zip(candidate_labels_intention, 
            list(np.ones((len(candidate_labels_sentiment),))*-1)))
        sentiment_bot = sample_dict_sentiment
        sentiment_customer = sample_dict_sentiment
        intent_bot = sample_dict_intent
        intent_customer = sample_dict_intent
        human_msg = "-----END OF ANALYZE----"
        bot_msg = "restart the application with different conversation history"
        return [
            human_msg,
            bot_msg,
            sentiment_bot,
            sentiment_customer,
            intent_bot, 
            intent_customer]
    # Get message with index
    conversation = result[str(idx)]
    # Get chatbot&customer messages
    bot_msg = conversation['sentence']['bot']
    human_msg = conversation['sentence']['customer']
    # Get intent scores
    intent_customer = dict_to_prob(conversation['intent_customer'])
    intent_bot = dict_to_prob(conversation['intent_bot'])
    sentiment_bot = dict_to_prob(conversation['sentiment_bot'])
    sentiment_customer = dict_to_prob(conversation['sentiment_customer'])
    # Index of conversation
    idx += 1
    return [
        human_msg,
        bot_msg,
        sentiment_bot,
        sentiment_customer,
        intent_bot, 
        intent_customer]


demo = gr.Interface(
    fn=zeroShotClassification, 
    inputs=[gr.UploadButton(file_types=[".json"])], 
    outputs=[
        gr.Textbox(label="Customer:"),
        gr.Textbox(label="ChatGPT:"),
        gr.Label(label="ChatGPT-Sentiment"),
        gr.Label(label="Customer-Sentiment"),
        gr.Label(label="ChatGPT-Intent"),
        gr.Label(label="Customer-Intent")])
demo.launch(share=True)