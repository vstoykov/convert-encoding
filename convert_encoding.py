#!/usr/bin/env python
# coding: utf-8
"""
Program that convert text files from one encoding to another.
By default it is used to convert windows-1251 encoded subtitles
into ISO-8859-5 ecoded because this is encoding for cyrilic
characters in Panasonic Viera TV

Tested on Python 2.7+ and Python 3.2+

created by Venelin Stoykov <vkstoykov@gmail.com>
"""
from __future__ import unicode_literals
import sys
import os
import logging

from io import BytesIO
from optparse import make_option, OptionParser

__version__ = (0, 5)

DEFAULT_INPUT_ENCODING = 'windows-1251'
DEFAULT_OUTPUT_ENCODING = 'iso-8859-5'

FAILSAFE_CHARACTERS = {
    '\u2122': 'TM',
    '\u201c': '"',
    '\u201d': '"',
    '\u2026': '...',
}


def get_version():
    return '.'.join(str(x) for x in __version__)


def get_failsafe_char(char, output_encoding):
    return FAILSAFE_CHARACTERS.get(char, '?').encode(output_encoding)


def convert_to(in_file_name, input_encoding=DEFAULT_INPUT_ENCODING,
               output_encoding=DEFAULT_OUTPUT_ENCODING):
    out_file_name = "%s.%s%s" % (in_file_name[:-4],
                                 output_encoding, in_file_name[-4:])

    with open(in_file_name, 'rb') as in_file:
        try:
            content = in_file.read().decode(input_encoding)
        except Exception as ex:
            logging.error("Can't read '%s' because: %s" % (in_file_name, ex))
            return False

    new_content = BytesIO()
    for char in content:
        try:
            new_content.write(char.encode(output_encoding))
        except Exception as ex:
            new_content.write(get_failsafe_char(char, output_encoding))

    with open(out_file_name, 'wb') as out_file:
        out_file.write(new_content.getvalue())
    return True


def main(*args, **options):
    has_errors = False
    for in_file in args:
        has_errors = not convert_to(in_file, **options) or has_errors

    if has_errors:
        sys.exit(1)


if __name__ == '__main__':
    prog_name = os.path.basename(sys.argv[0])
    opt_parser = OptionParser(
        prog=prog_name,
        version="%prog " + get_version(),
        usage='usage: %prog [options] file1 [[file2] ... [fileN]]',
        option_list=(
            make_option('-i', '--input-encoding', dest='input_encoding',
                        default=DEFAULT_INPUT_ENCODING,
                        help="Encoding on the input file"),
            make_option('-o', '--output-encoding', dest='output_encoding',
                        default=DEFAULT_OUTPUT_ENCODING,
                        help="Encoding on the output file"),
        )
    )
    options, args = opt_parser.parse_args(sys.argv[1:])
    main(*args, **options.__dict__)
