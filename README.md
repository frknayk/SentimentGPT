# SentimentGPT
Zero-shot sentiment &amp; intent analysis with LLMs

## Gradio App
Modify `app.py` script's `data_file` variable with correct name of json file `(e.g.data/data.json)`. 

```bash
python app.py
```

App will be running at LOCAL URL: http://127.0.0.1:7860

`Note: Click **Generate** button to start the app`

## Prompt to create dataset
To create own dataset feel free to use following prompt:
```text
Create a dataset in json format for a customer representative chatbot and human interaction that lasts 25 steps. 

Human wants to buy Iphone 14 and the chatbot interacts with him  
```
## TODO: 
- DOCKER
- speech2text API
- gRPC