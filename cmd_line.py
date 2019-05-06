#!/usr/bin/env python
"""
cmd_line.py
---

CMD Line parsing utilities.

"""
import argparse
import inspect
from types import GeneratorType

import src.utils.utility as _util

_logger = _util.get_logger(__file__)


def _str_to_bool(s):
    """Convert string to bool (in argparse context)."""
    if s.lower() not in ['true', 'false']:
        raise ValueError('Need bool; got %r' % s)
    return {'true': True, 'false': False}[s.lower()]


def add_boolean_argument(parser, name, default=False):
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--' + name,
        nargs='?',
        default=default,
        const=True,
        type=_str_to_bool)
    group.add_argument('--no' + name,
        dest=name,
        action='store_false')


def parseArgsForClassOrScript(fn):
    assert inspect.isfunction(fn) or inspect.ismethod(fn)

    sig = inspect.signature(fn)

    parser = argparse.ArgumentParser()
    for arg_name, arg in sig.parameters.items():
        if arg_name == 'self' or arg_name == 'logger':
            continue

        # Arguments are required or not required,
        # and have either an annotation or default value.
        # By default, args are parsed as strings if not otherwise specified.
        # REVIEW josephz: Is there a better way to determine if it is a positional/required argument?
        required = arg.default is inspect.Parameter.empty
        default = arg.default if arg.default is not inspect.Parameter.empty else None
        type_ = arg.annotation if arg.annotation is not inspect.Parameter.empty else type(default) if default is not None else str

        if type_ is bool:
            # REVIEW josephz: This currently has a serious flaw in that clients may only set positive boolean flags.
            #   The way to fix this would be to use the annotation to parse the input as a boolean.
            parser.add_argument("--" + arg_name, default=default, action='store_true')
        elif type_ in (tuple, list, GeneratorType):
            parser.add_argument("--" + arg_name, default=default, type=type_, nargs="+", help="Tuple of " + arg_name)
        else:
            parser.add_argument("--" + arg_name, default=default, type=type_, required=required)

    parser.add_argument("-v", "--verbosity",
        default=_util.DEFAULT_VERBOSITY,
        type=int,
        help="Verbosity mode. Default is 4. "
                 "Set as "
                 "0 for CRITICAL level logs only. "
                 "1 for ERROR and above level logs "
                 "2 for WARNING and above level logs "
                 "3 for INFO and above level logs "
                 "4 for DEBUG and above level logs")
    argv = parser.parse_args()
    argsToVals = vars(argv)

    if argv.verbosity >= 0 or hasattr(argv, 'help'):
        docstr = inspect.getdoc(fn)
        if docstr is None:
            "WARNING: Please write documentation :)"
        print()
        print(docstr.strip())
        print()
        print("Arguments and corresponding default or set values")
        for arg_name in sig.parameters:
            if arg_name == 'self' or arg_name == 'logger' or arg_name not in argsToVals:
                continue
            print("\t{}={}".format(arg_name, argsToVals[arg_name] if argsToVals[arg_name] is not None else ""))
        print()

    return argv

def test_cmdline(required,
        required_anno: int,
        required_anno_tuple: tuple,
        not_required="Test",
        not_required_bool=False,
        not_required_int=123,
        not_required_float=123.0,
        not_required_tuple=(1,2,3),
        not_required_str="123",
        not_required_None=None,
):
    """

    :param required: A required, unannotated parameter.
    :param required_anno: A required, annotated int parameter.
    :param required_anno_tuple: A required, annotated tuple parameter.
    :param not_required: A required, default-string parameter.
    :param not_required_bool: A not-required, default-string parameter.
    :param not_required_int: A not-required, default-int parameter.
    :param not_required_float: A not-required, default-float parameter.
    :param not_required_tuple: A not-required, default-tuple parameter.
    :param not_required_str: A not-required, default-string parameter.
    :param not_required_None: A not-required, default-string parameter.
    """
    print("required:", required)
    print("required_anno: ", required_anno)
    print("required_anno_tuple:", required_anno_tuple)
    print("not_required: ", not_required)
    print("not_required_bool:", not_required_bool)
    print("not_required_int:", not_required_int)
    print("not_required_float:", not_required_float)
    print("not_required_tuple:", not_required_tuple)
    print("not_required_str:", not_required_str)
    print("not_required_None:", not_required_None)

def main():
    global _logger
    args = parseArgsForClassOrScript(test_cmdline)
    varsArgs = vars(args)
    varsArgs.pop('verbosity', _util.DEFAULT_VERBOSITY)
    _logger.info("Passed arguments: '{}'".format(varsArgs))
    test_cmdline(**varsArgs)

if __name__ == '__main__':
    main()

