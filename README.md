# SentimentGPT
Zero-shot sentiment &amp; intent analysis with LLMs


## About
Perform sentiment and intent analysis with pre-trained LLMs. 
The repo is intentionally built to keep pre-trained LLMs model files in local file system.
 
Anyone who only want to develop applications without downloading pre-trained LLMs can use following: 
```Python
from transformers import pipeline

pipe = pipeline(model="facebook/bart-large-mnli")
pipe("Hello! I'm thinking of buying the iPhone 14, but I'm not sure which model to choose. Can you help me decide?",
    candidate_labels=["positive', 'neutral', 'negative"],
)
```

## Installation

### Installing sentimentgpt as Python Package
```bash
pip install -e .
```

### Install requirements
```bash
pip install -r requirements.txt
```
### Download facebook/bart-large-mnli model
Zero-shot classification uses 

1. Download model files from Huggingface model hub: https://huggingface.co/facebook/bart-large-mnli/tree/main
2. Copy model checkpoint'pytorch_model.bin' to resources/ folder.
3. Copy following config files to `config/` folder:
    - config.json
    - tokenizer.json
    - tokenizer_config.json
    - vocab.json

## Generating Data
Data is generated by the following Chatgpt prompt:
```text
Create a dataset in json format for a customer representative chatbot and human interaction that lasts 25 steps. 

Human wants to buy Iphone 14 and the chatbot interacts with him  
```

- Generate data with prompt: `data/data.json`

- Annotated Conversation with Intent&Sentiment Candidate Labels: `data/data_result.json`


## Gradio App
Modify `app.py` script's `data_file` variable with correct name of json file `(e.g.data/data.json)`. 

```bash
python app.py
```

App will be running at LOCAL URL: http://127.0.0.1:7860

`Note: Click **Generate** button to start the app`

<!-- ![Web App Overview](files/app_overview.png | width=50) -->
<img src="files/app_overview.png" alt="Web App Overview" width="400" height=400>

## Prompt to create dataset
To create own dataset feel free to use following prompt:
```text
Create a dataset in json format for a customer representative chatbot and human interaction that lasts 25 steps. 

Human wants to buy Iphone 14 and the chatbot interacts with him  
```
## TODO: 
- Make prompt deterministic, and produces json everytime in the same format
- speech2text API
- gRPC
- Make json file uploadable