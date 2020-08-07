from argparse import ArgumentParser, FileType
from logging import error
from pathlib import Path
from sys import exit, stdout
from pandas import read_csv, DataFrame


def parse_command_line_arguments():
    parser = ArgumentParser(description='Process CSV.')

    parser.add_argument('file', metavar='INPUTFILE',
        type=FileType('r'), help='path to input csv file')
    parser.add_argument('-c', '--columns', metavar='NAME', nargs='+',
        type=str, default=[], help='name columns to be extracted')
    parser.add_argument('-o', '--output', metavar='OUTPUTFILE', default=stdout,
        type=FileType('w'), help='path to output csv file')

    return parser.parse_args()


def parse_csv(arguments):
    data = read_csv(arguments.file, sep=None, engine='python', dtype=str)

    column_names = [name for name in arguments.columns if name in data.columns.tolist()]

    output = DataFrame([list(data[name]) for name in column_names]).transpose()
    output.columns = column_names

    return output


def main():
    arguments = parse_command_line_arguments()
    parse_csv(arguments).to_csv(arguments.output, index=False)
    
    return 0


if __name__ == "__main__":
    try:
        exit(main())
    except Exception as exception:
        error(exception)
        exit(1)
