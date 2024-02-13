---
title: 'EmTract: A Python Package for Extracting Emotions from Social Media for Finance Research'
tags:
  - Python
  - NLP
  - finance
  - emotions
authors:
  - name: Domonkos F. Vamossy
    affiliation: "1"
  - name: Rolf P. Skog
    affiliation: "2"
affiliations:
 - name: University of Pittsburgh
   index: 1
 - name: Pontifical Catholic University of Chile
   index: 2
bibliography: paper.bib
date: 13 February 2024

---

# Summary

EmTract introduces an open-source tool for analyzing emotions in financial social media texts, leveraging a dataset of 10,000 annotated messages from StockTwits and enhancing the DistilBERT NLP model with 4,861 emojis and emoticons. This tool aims to deepen the understanding of investor emotions and their impact on market trends, highlighting the significant correlation between social media sentiments and asset price movements.

# Statement of Need

In the complex interplay of financial markets, investor emotions play a pivotal role. EmTract is developed to address the need for accurate emotion extraction from financial social media, 
offering nuanced insights into investor sentiments and their implications for market dynamics. The tool's efficacy is rooted in a comprehensive dataset comprising 250,000 messages augmented
 by 10,000 annotated messages from StockTwits, enriched with a wide array of emojis and emoticons to capture the full spectrum of investor emotions. EmTract utilizes a modified version of the 
 DistilBERT NLP model, incorporating emojis and emoticons for a more context-aware emotion classification, setting a new standard in sentiment analysis within the financial domain.
EmTract's advanced emotion extraction capabilities demonstrate a marked improvement in the accuracy and depth of sentiment analysis, offering valuable insights into the emotional 
underpinnings of market movements. The tool's applications extend beyond academic research, providing practical insights for financial analysts and investors in deciphering market 
sentiments and predicting asset price trends.

# Performance Evaluation

The performance of EmTract and comparative models evaluted on StockTwits sample is summarized below, divided into two panels: Panel A for Ekman's Emotions (Happy, Sad, Anger, Disgust, Surprise, Fear, Neutral) and Panel B for Valence (Positive, Neutral, Happy).

BERT, as one of the comparative models, uses standard embeddings and does not augment them with emotional cues such as emojis or emoticons, which is a key distinction from the EmTract model. The performance of these models is evaluated based on both human-labeled data, on which they are trained via five-fold cross-validation, and on GPT 3.5 labeled data, which they are not trained on. This approach highlights the adaptability and generalization capabilities of the models to unseen data sources.


## Panel A: Ekman's Emotions

| Model             | Loss (Human Labeled) | Accuracy (Human Labeled) | F1-score (Macro, Human Labeled) | Loss (GPT 3.5 Labeled) | Accuracy (GPT 3.5 Labeled) | F1-score (Macro, GPT 3.5 Labeled) |
|-------------------|----------------------|--------------------------|---------------------------------|------------------------|----------------------------|-----------------------------------|
| EmTract           | 1.009 [0.059]        | 64.53% [1.98%]           | 0.4909 [0.0294]                 | 1.463 [0.032]          | 51.38% [1.65%]             | 0.3401 [0.0137]                   |
| BERT              | 1.112 [0.029]        | 61.12% [1.65%]           | 0.4051 [0.0481]                 | 1.453 [0.045]          | 48.50% [0.59%]             | 0.2802 [0.0234]                   |
| `@hartmann2022emotionenglish`   | 2.015 [0.047]        | 45.19% [0.94%]           | 0.3123 [0.0081]                 | 1.935 [0.029]          | 46.49% [0.43%]             | 0.2793 [0.0083]                   |
| RF                | 1.421 [0.017]        | 50.30% [1.3%]            | 0.2280 [0.0112]                 | 1.485 [0.021]          | 47.00% [0.9%]              | 0.1656 [0.0047]                   |
| XGB               | 1.367 [0.022]        | 52.40% [1.59%]           | 0.2842 [0.022]                  | 1.547 [0.03]           | 46.17% [1.35%]             | 0.1967 [0.011]                    |
| CART              | 18.148 [0.317]       | 45.23% [0.73%]           | 0.2939 [0.0097]                 | 21.32 [0.488]          | 38.54% [1.24%]             | 0.2052 [0.011]                    |

## Panel B: Valence (Positive, Neutral, Happy)

| Model           | Loss (Human Labeled) | Accuracy (Human Labeled) | F1-score (Macro, Human Labeled) | Loss (GPT 3.5 Labeled) | Accuracy (GPT 3.5 Labeled) | F1-score (Macro, GPT 3.5 Labeled) |
|-----------------|----------------------|--------------------------|---------------------------------|------------------------|----------------------------|-----------------------------------|
| EmTract         | 0.6636 [0.028]       | 72.34% [1.44%]           | 0.7084 [0.0141]                 | 0.932 [0.019]          | 62.54% [1.40%]             | 0.6127 [0.0153]                   |
| `@hartmann2022emotionenglish` | 1.327 [0.035]        | 56.70% [0.94%]           | 0.4852 [0.0068]                 | 1.311 [0.019]          | 56.48% [0.42%]             | 0.4734 [0.0055]                   |
| `@araci2019finbert`    | 1.373 [0.0233]       | 46.50% [0.89%]           | 0.4089 [0.010]                  | 1.259 [0.0228]         | 50.24% [0.70%]             | 0.4431 [0.016


_Note: The term "Test Fold" refers to a subset of 2,000 messages not seen by the model during training. Standard deviations are included in brackets. For a more comprehensive understanding and additional details, refer to `@vamossy2023emtract`._

# Conclusion

EmTract represents a significant advancement in financial sentiment analysis, offering a powerful tool for understanding and leveraging the emotional dynamics of financial markets.
For more details see `@vamossy2023emtract`.

# Acknowledgements

Special thanks to StockTwits for data and Huggingface for hosting the model(s).

# Research and Publications Using EmTract

EmTract is has been utilized in research projects and scholarly publications, demonstrating its value and effectiveness in the field of financial sentiment analysis. Below is a set of works that have leveraged EmTract:

- `@vamossy2023emtract`
- `@vamossy2021investor`
- `@vamossy2023emtract`

# References
