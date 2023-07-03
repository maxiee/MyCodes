from transformers import pipeline
import pandas as pd

text = "In this chapter, we will first start with the background of NLP that led to the rise of the Transformer. We will briefly go from early NLP to RNNs and CNNs. Then we will see how the Transformer overthrew the reign of RNNs and CNNs, which had prevailed for decades for sequence analysis."

ner_tagger = pipeline("ner", aggregation_strategy="simple")

outputs = ner_tagger(text)

outputs = pd.DataFrame(outputs)

print(outputs.to_markdown())