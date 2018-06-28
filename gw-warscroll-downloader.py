import requests
# from bs4 import BeautifulSoup
# import re
import os
# import json
import imp
import csv

gw_faq_data = {}
local_faq_data = {}

gw_points_csv = "https://www.warhammer-community.com/wp-content/themes/gw-community/library/warscrollbuilder/data/gwPoints.csv"

warscroll_save_path = "./downloads/"
print_debug = False

warscroll_uris = []

# Try a to find a local config file...
try:
    imp.find_module('config')
    import config

    if hasattr(config, "warscroll_save_path"):
        warscroll_save_path = config.warscroll_save_path
    if hasattr(config, "print_debug"):
        print_debug = config.print_debug
    if print_debug:
        print("* Config file found, using those settings")
except ImportError:
    no_local_config_found = True

# Make sure warscroll_save_path has trailing slash... it's important.
if warscroll_save_path[-1] != "/":
    warscroll_save_path = warscroll_save_path + "/"


def download_file( file_url, warscroll_save_path):
    dlresponse = requests.get(file_url, stream=True)
    if print_debug:
        print("* Downloading " + file_url)
    with open(warscroll_save_path, 'wb') as f:
        for chunk in dlresponse.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return warscroll_save_path

def download_files():
    for fileuri in warscroll_uris:
        file_warscroll_save_path = warscroll_save_path + fileuri[fileuri.rfind("/")+1:].replace('%20', ' ')
        download_file( fileuri, file_warscroll_save_path )

def get_warscroll_list( csv_text ):
    global warscroll_uris
    reader = csv.reader(csv_text.split('\n'), delimiter=',')
    for row in reader:
        if row[1].strip() != '':
            fixed_uri = row[1].strip().replace('//', '/').replace('https:/www', 'https://www' )
            if fixed_uri not in warscroll_uris:
                warscroll_uris.append(fixed_uri)

if not os.path.exists(warscroll_save_path):
    if print_debug:
         print("* creating save directory " + warscroll_save_path)
    os.makedirs(warscroll_save_path)


response = requests.get( gw_points_csv )
if response.status_code == 200:
    get_warscroll_list( response.text )
    download_files()

