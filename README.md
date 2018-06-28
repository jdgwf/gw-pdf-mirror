# Games Workshop PDF Mirror(er)

**gw-faq-mirror.py** This script checks the Games Workshop Warhammer Community FAQ page for new or non-existent FAQs and attempts to download any newer versions or new files.

**gw-warscroll-downloader.py** This script finds and downloads all the publicly available Warscroll PDFs for Age of Sigmar. It uses the data from the public Warscroll Builder.

## Getting Started

You'll need Python installed on your system. Instructions to do so can be found here: https://www.python.org/downloads/

### Prerequisites

You'll need a fairly current version of python3 or python2, but the requirements are pretty minimal. Both versions should work with these scripts (no guarantees that it works on python2, for I don't use it anymore. I did test both with Python 2.7.12 on Ubuntu 16.04 in mid 2018 and they worked fine enough).

### Installing

The default config will download the files into a directory the script is located. If you're wanting to change the "base path", just copy the config.sample.py to config.py and change the settings there. The config.py will not be overwritten with subsequent git pulls, and the config.sample.py will have a list of all the options you can change in subsequent versions.

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Python](http://www.python.org) - Pure Python all the way

## License

This project is licensed under the GPL License - see the [LICENSE.md](LICENSE.md) file for details

