#!/usr/bin/env python3


def bool_input(input_str):
    input_str = input_str + ' [Y|n] '
    result = None
    while result is None:
        response = input(input_str)
        if response in ('', 'y', 'Y'):
            result = True
        elif response in ('n', 'N'):
            result = False
        else:
            print('Wrong option')

    return result
