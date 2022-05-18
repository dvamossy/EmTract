
<h1><img src="doc/emotions.png" width="80px" align="left" style="margin-right: 9px;"> EmTract: Extracting Emotions from Social Media Text Tailored for Financial Contexts</h1>

EmTract is a tool that extracts emotions from social media text. It incorporates key aspects of social media data (e.g., non-standard phrases, emojis and emoticons), and uses cutting edge natural language processing (NLP) techniques to learn latent representations, such as word order, word usage, and local context, to predict the emotions. 

Details on the model and text processing are in the appendix of [EmTract: Investor Emotions and Market Behavior](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3975884&fbclid=IwAR1gAgHGekkp_bO2QkT_YbtQaJmvM7O5JrfXNHCAYXF2D3-N_9PaXZC-Cig). 

## User Guide

### Installation
Before being able to use the package [python3](https://www.python.org/downloads/) must be installed.
We also recommend using a virtual environment so that the tool runs with the same dependencies with which it was developed.
Instruction on how to set up a virtual environment can be found [here](https://docs.python.org/3/tutorial/venv.html).

Once basic requirements are setup, follow these instructions:
1. Clone the repository: `git clone https://github.com/dvamossy/EmTract.git`
2. Navigate into repository: `cd EmTract`
2. (Optional) Create and activate virtual environment:
    ```
   python3 -m venv venv
   source venv/bin/activate
    ```
3. Run `./install.sh`. This will install python requirements and also download our model files

### Usage

Our package should be run with the following command:
```commandline
python3 -m emtract.inference [args]
```
Where args are the following:
* --model_type: can be twitter or stocktwits. Default is stocktwits
* --interactive: Run in interactive mode
* --input_file/-i: input to use for predictions (only for non interactive mode)
* --output_file/-o: output location for predictions(only for non interactive mode)

#### Output
For each input (i.e., text), EmTract outputs probabilities (they sum to 1!) corresponding to seven emotional states: neutral, happy, sad, anger, disgust, surprise, fear. It also labels the text by computing the argmax of the probabilities. 

#### Modes
Our tool can be run in 2 execution modes.

Interactive mode allows the user to input a tweet and evaluate it in real time. This is great for exploratory analysis.
```commandline
python3 -m emtract.inference --interactive
```

The other mode is intended for automating predictions. Here an input file must be specified that will be used as the prediction input.
This file must be a csv or text file with 1 column. This column should have the messages/text to predict with.
```commandline
python3 -m emtract.inference -i tweets_example.csv -o predictions.csv
```

#### Model Types
We implemented and fine-tuned [DistilBERT](https://huggingface.co/bhadresh-savani/distilbert-base-uncased-emotion) model for emotion classification. One of the key concerns using emotion packages is that it is unknown how well they transfer to financial text data. We alleviate this concern by hand-tagging 10,000 StockTwits messages, and making use of them via 5-fold cross-validation. These are available at data/tagged_sample.parquet.snappy. We also tested an alternative emotion package in (notebooks/Alternative Packages.ipynb). 

We trained our emotion models with 2 different data sources. One from Twitter, and another from StockTwits. The Twitter training data comes from [here](https://github.com/sarnthil/unify-emotion-datasets/tree/master/datasets); it is available at data/emotion_sources.csv. For the StockTwits based model, we transferred the Twitter based model to the StockTwits sample via 5-fold cross-validation. We found our StockTwits model to perform best on the hand-tagged sample via five-fold CV, and therefore it is used as the default for predictions. 

The model is also available [here](https://huggingface.co/vamossyd/bert-base-uncased-emotion), and can be tested for inference without any software.

## Citation
If you use EmTract in your research, please cite us as follows:

   Domonkos Vamossy and Rolf Skog. **EmTract: Investor Emotions and Market Behavior** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3975884, 2021. 
   
## Contributing and Feedback
This project welcomes contributions and suggestions. 

Our goal is to provide a unified framework for extracting emotions from financial social media text. Particularly useful for research on emotions in financial contexts would be labeling financial social media text. We plan to upload sample text upon request.
