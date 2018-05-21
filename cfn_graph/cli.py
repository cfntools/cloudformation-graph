import argparse
import json
import sys

from . import capitalize_keys
from .changeset import ChangeSetGraph
from .exceptions import UnknownInputException, UnknownWrapTypeException


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--console',
        help='input copied from the AWS console',
        action='store_true'
    )
    parser.add_argument(
        '-w', '--wrap',
        help='Type to wrap input in, allowed values are "changeset',
    )
    args = parser.parse_args()

    input_dict = json.load(sys.stdin)

    if args.console:
        # Console changes keys:
        input_dict = capitalize_keys(input_dict)

    if args.wrap:
        if args.wrap == 'changeset':
            input_dict = {
                'ChangeSetName': 'cli-input',
                'Changes': input_dict,
            }
        else:
            raise UnknownWrapTypeException()

    if 'ChangeSetName' in input_dict:
        graph = ChangeSetGraph(input_dict)
    else:
        raise UnknownInputException()

    print(graph.graph())
    return
