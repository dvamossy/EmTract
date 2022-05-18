import argparse
import sys


def cmd_inference(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--model_type",
        type=str,
        default="stocktwits",
        choices=["twitter", "stocktwits"],
        help="Use model trained with StockTwits data or Twitter data. Valida choices are twitter/stocktwits",
    )
    parser.add_argument(
        "--interactive",
        default=False,
        action="store_true",
        help="Specify to run in interactive mode instead of providing file",
    )
    parser.add_argument(
        "-i",
        "--input_file",
        type=str,
        required="--interactive" not in sys.argv,
        help="Input csv file were the first column will be evaluated",
    )
    parser.add_argument(
        "-o",
        "--output_file",
        type=str,
        required="--interactive" not in sys.argv,
        help="Output location",
    )
    parsed_args = parser.parse_args(args)

    from .model_inference import ModelInference

    model = ModelInference(parsed_args.model_type)

    if parsed_args.interactive:
        while True:
            tweet = input("Input tweet: ")
            print(model.inference(tweet))

    else:
        model.file_inference(parsed_args.input_file, parsed_args.output_file)


if __name__ == "__main__":
    cmd_inference()
