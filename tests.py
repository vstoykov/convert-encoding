# coding: utf8
from __future__ import unicode_literals
import os
import tempfile
import shutil
import subprocess
import sys
from unittest import TestCase


class ConvertEncodingTestCase(TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tempdir, ignore_errors=True)

    def assertEncodedTextEqual(self, input_text, input_encoding, output_text, output_encoding):
        tmp_file = tempfile.NamedTemporaryFile(dir=self.tempdir, suffix='.txt', delete=False)
        new_file_name = None
        try:
            with tmp_file:
                tmp_file.write(input_text)

            retcode = subprocess.call([
                sys.executable, 'convert-encoding.py',
                '-i', input_encoding,
                '-o', output_encoding,
                tmp_file.name])

            new_file_name = tmp_file.name[:-4] + '.' + output_encoding + '.txt'

            self.assertEqual(retcode, 0)
            self.assertTrue(os.path.isfile(new_file_name))

            with open(new_file_name, 'rb') as new_file:
                self.assertEqual(new_file.read(), output_text)

        finally:
            os.unlink(tmp_file.name)
            if new_file_name is not None:
                os.unlink(new_file_name)

    def test_convert_utf8_to_windows1251(self):
        test_text = '\u201cТест\u201d\u2122\u2026'
        self.assertEncodedTextEqual(
            test_text.encode('utf8'), 'utf8',
            test_text.encode('windows-1251'), 'windows-1251')

    def test_convert_windows_1251_to_iso_8859_5_with_fallback(self):
        input_text = '\u201cТест\u201d\u2122\u2026'.encode('windows-1251')
        # iso-8859-5 dows not have some special characters available in
        # windows 1251 and for that reason we use fallback
        expected_text = '"Тест"TM...'.encode('iso-8859-5')
        self.assertEncodedTextEqual(
            input_text, 'windows-1251',
            expected_text, 'iso-8859-5',
        )
