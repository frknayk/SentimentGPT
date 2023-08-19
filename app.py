import streamlit as st
import json
from sentimentgpt.classifier import PipelineSIGPT


if 'count' not in st.session_state:
	st.session_state.count = 0

def increment_counter():
	st.session_state.count += 1
    
def main():
    global current_conv_index
    # Define candidate labels
    candidate_labels_sentiment = ['positive', 'neutral', 'negative']
    candidate_labels_intention = ['compatibility', 'durability', 'storage', 'battery', 'camera']
    config_zs = {
        "candidate_labels_sentiment":candidate_labels_sentiment,
        "candidate_labels_intention":candidate_labels_intention}
    pipe_sigpt = PipelineSIGPT(config_zs)
    ###########################################
    st.title("Zero-Shot Classifier App")
    # Section to add labels
    st.header("Candidate Labels")
    st.write("Sentiment Labels: ", candidate_labels_sentiment)
    st.write("Intention Labels: ", candidate_labels_intention)
    # Section to upload conversation data
    st.header("Upload Conversation Data")
    uploaded_file = st.file_uploader("Upload JSON File", type=["json"])
    if uploaded_file is not None:
        pipe_sigpt.set_pipe()
        ####### Read conversations
        conversations = load_conversations(uploaded_file)["conversation"]
        if st.session_state.count >= len(conversations) - 1:
            return
        print("len conv:",len(conversations))
        # Process and display conversation data
        st.header("Conversation Data")
        with st.container():
            print("st.session_state.count:",st.session_state.count)
            current_conv_index = st.session_state.count
            show_conversation(pipe_sigpt, conversations[current_conv_index])
            # Next Conversation button
            st.button("Next Conversation",on_click=increment_counter)


def show_conversation(pipe_sigpt, conv):
    conv = pipe_sigpt.analyze_interaction(conv)
    st.subheader(f"Interaction")
    st.write("Customer: ", conv['sentence']['customer'])
    st.write("Bot: ", conv['sentence']['bot'])
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        show_prob(conv['sentiment_bot'], title="Sentiment Prediction for ChatBot")
    with col2:
        show_prob(conv['sentiment_customer'], title="Sentiment Prediction for Human")
    with col3:
        show_prob(conv['intent_bot'], title="Intent Prediction for ChatBot")
    with col4:
        show_prob(conv['intent_customer'], title="Intent Prediction for Human")

def load_conversations(uploaded_file):
    data = json.load(uploaded_file)
    return data

def show_prob(conversation_dict, title):
    def dict_to_prob(conversation_dict):
        return zip(
            conversation_dict['labels'], 
            conversation_dict['scores'])
    conversation_zip = dict_to_prob(conversation_dict)
    st.write(title)
    for i, (label, prob) in enumerate(conversation_zip):
        st.write(f"{i+1}. {label} ({prob*100:.2f}%)")
        st.progress(prob)

if __name__ == "__main__":
    main()
