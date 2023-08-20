# Discussions About Zero-Shot Learning

## Zero-Shot Learning Advantages&Disadvantages in Classification

### What is Zero-Shot Learning ?
Zero-shot learning is a machine learning paradigm where a model is trained to recognize and generalize to classes it has never seen during training. 

This is achieved by providing the model with information about relationships between classes, attributes, or other forms of auxiliary data. 

### Zero-Shot Learning Advantages
    1. **Generalization to Unseen Classes**: The primary advantage of zero-shot learning is its ability to recognize and classify classes that were not present in the training data. This is particularly useful in scenarios where obtaining labeled data for all possible classes is impractical or expensive.

    2. **Reduced Data Annotation**: Zero-shot learning can significantly reduce the need for labeled training data. Since the model is learning to generalize from existing classes, you don't have to gather large amounts of labeled data for each individual class.

    3. **Flexibility and Scalability**: Zero-shot learning allows for greater flexibility in adapting to new tasks or domains. It makes it easier to incorporate new classes without the need to retrain the entire model, making it scalable for applications with evolving class sets.

    4. **Saves Time and Resources**: By not requiring data collection and annotation for every single class, zero-shot learning can save time, resources, and effort, making it a practical choice in situations where acquiring data is challenging.


### Zero-Shot Learning Disadvantages
    1. **Dependency on Auxiliary Information**: Zero-shot learning often relies on auxiliary information such as class relationships, attributes, or embeddings. If this auxiliary data is noisy or inaccurate, it can negatively impact the model's performance.

    2. **Limited Performance**: While zero-shot learning can generalize to unseen classes, the performance might not be as high as traditional supervised learning methods that have been trained on the specific classes. The model's accuracy could be compromised, especially when dealing with highly dissimilar or nuanced classes.

    3. **Difficulty in Capturing Complex Relationships**: Capturing complex relationships between classes using auxiliary data might be challenging. Some relationships could be subtle, context-dependent, or difficult to define, leading to reduced performance in such cases.

    4. **Lack of Fine-Grained Discrimination**: Zero-shot learning might struggle to discriminate between closely related classes that share similar attributes or characteristics. Fine-grained classification can be more challenging using this approach.

    5. **Overfitting to Auxiliary Information**: If the model over-relies on the provided auxiliary information, it might struggle to adapt to cases where the real-world distribution of data deviates from the assumptions made by the auxiliary data.

    6. **Limited Exploration of Class Space**: Zero-shot learning assumes that all relevant classes are known a priori, which might limit the model's ability to discover novel or emerging classes.

In summary, zero-shot learning offers a unique approach to dealing with new classes or domains without the need for extensive labeled training data. However, it comes with trade-offs in terms of performance and dependence on auxiliary information. The decision to use zero-shot learning should be based on the specific application requirements, available data, and the trade-offs you're willing to accept.

## Adapting Zero-Shot Model (Facebook/Bart) to Understand Turkish Language (Or any language)

The model I used for Zero-Shot task is facebook/bart-large-mnli model which is trained on MultiNLI(MNLI) dataset. 
The MLNI corpus is a crowd-soruced collection of 433k sentence pairs annotated with textual entailment information. 
The corpus is used to train the model to predict whether the sentence pairs are entailment or not. 
**However it contains samples from English only.**

The model is for understanding the Turkish language we may follow different directions:

### mBart-50 One-to-Many for Turkish NLU

Again, mBart-50 one-to-many multilingual machine translation model (facebook/mbart-large-50-one-to-many-mmt) is fined-tuned
for multilingual machine translation that is fined-tuned from mBart-50 model checkpoint.

The model can translate English to other 49 languages which also includes Turkish language. 

#### Option-1: Directly Use mBart-50 for Translation Task

It is possible to use mBart-50 model directly for translation task.

```python
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
article_en = "The head of the United Nations says there is no military solution in Syria"
model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-one-to-many-mmt")
tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-one-to-many-mmt", src_lang="en_XX")
model_inputs = tokenizer(article_en, return_tensors="pt")
# translate from English to Turkish
generated_tokens = model.generate(
    **model_inputs,
    forced_bos_token_id=tokenizer.lang_code_to_id["tr_TR"]
)
# => Birleşmiş Milletler başkanı Suriye'de bir askeri çözümün olmadığını belirtiyor.
```

#### Option-2: Fine-Tune mBart-50 for Translation Task
It is possible to fine-tune mBart-50 model for English-to-Turkish translation task.

Here is an example of one epoch training of fine-tune:
```python
from transformers import MBartForConditionalGeneration
model = MBartForConditionalGeneration.from_pretrained('facebook/mbart-large-50-one-to-many-mmt')
tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50", src_lang="en_XX", tgt_lang="tr_TR")

# Load dataset and gather src_text/target_text couples then feed into training loop
# Take this into the loop and do many times
src_text = " Let's translate english to turkish"
target_text =  "Haydi ingilizceden türkçeye çeviri yapalım."
model_inputs = tokenizer(src_text, return_tensors="pt")
with tokenizer.as_target_tokenizer():
    labels = tokenizer(target_text, return_tensors="pt").input_ids
# Set up the optimizer and training settings
optimizer = AdamW(model.parameters(), lr=1e-5)
model.train()
print('Fine-tuning started')
for i in range(100):
    optimizer.zero_grad()
    output = model(**model_inputs, labels=labels) # forward pass
    loss = output.loss
    loss.backward()
    optimizer.step()
print(f'Loss:{loss}')
```


Datasets may be used for training:
```Text
- [Bilkent Turkish Writings Dataset](https://github.com/selimfirat/bilkent-turkish-writings-dataset)
- [Translated Books in Turkish](https://www.kaggle.com/datasets/redrussianarmy/translated-books-in-turkish)
- Turkish wikipedia
```

## Acknowledgements:
- https://huggingface.co/facebook/bart-large-mnli
- https://huggingface.co/docs/transformers/v4.31.0/en/model_doc/mbart
- https://huggingface.co/facebook/mbart-large-50-one-to-many-mmt
- https://www.kaggle.com/datasets/redrussianarmy/turkish-corpus
- https://huggingface.co/datasets/multi_nli
