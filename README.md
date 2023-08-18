# SentimentGPT
Zero-shot sentiment &amp; intent analysis with LLMs


## Installation

### Installing sentimentgpt as Python Package
```bash
pip install -e .
```

### Install requirements
```bash
pip install -r requirements.txt
```

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
- DOCKER
- speech2text API
- gRPC