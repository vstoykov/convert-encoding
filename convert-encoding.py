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
import codecs
import sys
import os
import logging

from io import open
from optparse import make_option, OptionParser

__version__ = (0, 7)

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


def encoding_error_handler(err):
    bad_text = err.object[err.start:err.end]
    return ''.join(FAILSAFE_CHARACTERS.get(c, '?') for c in bad_text), err.end


def read_file(file_name, ecoding):
    with open(file_name, 'rt', encoding=ecoding, newline='') as in_file:
        return in_file.read()


def convert_to(in_file_name, input_encoding=DEFAULT_INPUT_ENCODING,
               output_encoding=DEFAULT_OUTPUT_ENCODING):

    # Read the content of the file
    try:
        content = read_file(in_file_name, input_encoding)
    except Exception as ex:
        logging.error("Can't read '%s' because: %s" % (in_file_name, ex))
        return False

    name, ext = os.path.splitext(in_file_name)
    out_file_name = "%s.%s%s" % (name, output_encoding, ext)

    # Write the content in the new encoding with our custom fallback
    with open(out_file_name, 'wt',
              encoding=output_encoding,
              errors='convert_encoding_fallback_replace',
              newline='') as out_file:
        out_file.write(content)
    return True


def main(*args, **options):
    has_errors = False
    for in_file in args:
        has_errors = not convert_to(in_file, **options) or has_errors

    if has_errors:
        sys.exit(1)


codecs.register_error('convert_encoding_fallback_replace',
                      encoding_error_handler)

if __name__ == '__main__':
    prog_name = os.path.basename(sys.argv[0])
    opt_parser = OptionParser(
        prog=prog_name,
        version="%prog " + get_version(),
        usage='usage: %prog [options] file1 [[file2] ... [fileN]]',
        option_list=(
            make_option('-i', '--input-encoding', dest='input_encoding',
                        default=DEFAULT_INPUT_ENCODING,
                        help="Encoding on the input file (Default is: %s)." % DEFAULT_INPUT_ENCODING),
            make_option('-o', '--output-encoding', dest='output_encoding',
                        default=DEFAULT_OUTPUT_ENCODING,
                        help="Encoding on the output file (Default is: %s)." % DEFAULT_OUTPUT_ENCODING),
        )
    )
    options, args = opt_parser.parse_args(sys.argv[1:])
    if args:
        main(*args, **options.__dict__)
    else:
        opt_parser.print_help()
