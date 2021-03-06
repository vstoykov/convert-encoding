from setuptools import setup

setup(
    name="convert-encoding",
    version='0.7',
    author="Venelin Stoykov",
    author_email="vkstoykov@gmail.com",
    description="Convert text files from one encoding to another.",
    long_description="""Program that convert text files from one encoding to another.
    By default it is used to convert windows-1251 encoded subtitles
    into ISO-8859-5 ecoded because this is encoding for cyrilic
    characters in Panasonic Viera TV""",
    url="https://github.com/vstoykov/convert-encoding",
    scripts=['convert-encoding.py'],
    test_suite='tests',
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ])
