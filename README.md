# EmTract

Emtract is a tool used to evaluate emotions in text. 
It uses cutting edge machine learning techniques to learn latent representations of words that are later used by a GRU based model to predict the emotion present.

It is explained in more detail in the paper [EmTract: Investor Emotions and Market Behavior](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3975884&fbclid=IwAR1gAgHGekkp_bO2QkT_YbtQaJmvM7O5JrfXNHCAYXF2D3-N_9PaXZC-Cig).
Details on the model and text processing appear in the appendix.

## User guide

### Installation
Before being able to use the package [python3](https://www.python.org/downloads/) must be installed.
We also recommend using a virtual environment so that the tool runs with the same dependencies with which it was developed.
Instruction on how to set up a virtual environment can be found [here](https://docs.python.org/3/tutorial/venv.html).

Once basic requirements are setup follow the following instructions:
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

Interactive mode will allow the user to input a tweet and evaluate it in real time.
This is great for quick exploration of different messages.
```commandline
python3 -m emtract.inference --interactive
```

The other mode is intended for larger predictions.
Here an input file must be specified that will be used as the prediction input.
This file must be a csv or text file with 1 column. 
This column should have the messages to predict with.
```commandline
python3 -m emtract.inference -i tweets_example.csv -o predictions.csv
```

#### Model types
We trained our emotion models with 2 tweet datasets. 
One from twitter and another from stocktwits.
As discussed in the paper the stocktwits model has better performance and is used as the default for predictions.