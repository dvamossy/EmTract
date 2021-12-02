# EmTract

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
Our models leverage [GloVe](https://nlp.stanford.edu/projects/glove/) Embeddings with Bidirectional GRU architecture. 

We trained our emotion models with 2 different data sources. One from Twitter, and another from StockTwits. The Twitter training data comes from [here](https://github.com/sarnthil/unify-emotion-datasets/tree/master/datasets); it is available at data/twitter_emotion.csv. The StockTwits training data is explained in the paper. 

One of the key concerns using emotion packages is that it is unknown how well they transfer to financial text data. We alleviate this concern by hand-tagging 10,000 StockTwits messages. These are available at data/hand_tagged_sample.parquet.snappy; they were not included during training any of our models. We use this for testing model performance, and alternative emotion packages (notebooks/Alternative Packages.ipynb). 

We found our StockTwits model to perform best on the hand-tagged sample, and therefore it is used as the default for predictions. 

#### Alternative Models
We also have an implementation of [DistilBERT](https://huggingface.co/bhadresh-savani/distilbert-base-uncased-emotion) in notebooks/Alternative Models.ipynb on the Twitter data; which can be easily extended to any other state-of-the-art models. We find marginal performance gains on the hand-tagged sample, which comes at the cost of far slower inference.

## Citation
If you use EmTract in your research, please cite us as follows:

   Domonkos Vamossy and Rolf Skog. **EmTract: Investor Emotions and Market Behavior** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3975884, 2021. 
   
## Contributing and Feedback
This project welcomes contributions and suggestions. 

Our goal is to provide a unified framework for extracting emotions from financial social media text. Particularly useful for research on emotions in financial contexts would be labeling financial social media text. We plan to upload sample text upon request.
