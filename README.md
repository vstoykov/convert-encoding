convert-encoding
================

Simple script used to convert text files from one encoding to another. It's main
purpose is to convert subtitle files to match the cyrilic encoding of TVs.


Installing
----------

For installing the script just run:

    pip install git+https://github.com/vstoykov/convert-encoding.git

And you will have `convert-encoding.py` in your `bin` directory


Usage
-----

    Usage: convert-encoding.py [options] file1 [[file2] ... [fileN]]

    Options:
      -i INPUT_ENCODING, --input-encoding=INPUT_ENCODING
                            Encoding on the input file (Default is: windows-1251).
      -o OUTPUT_ENCODING, --output-encoding=OUTPUT_ENCODING
                            Encoding on the output file (Default is: iso-8859-5).
      --version             show program's version number and exit
      -h, --help            show this help message and exit
