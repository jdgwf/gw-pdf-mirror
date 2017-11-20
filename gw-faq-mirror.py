import requests
import re
import os
import json
import imp

gw_faq_data = {}
local_faq_data = {}

gw_faqs_url = "https://www.warhammer-community.com/faqs/"
save_path = "./downloads/"
current_version_cache = "current_versions.json"
print_debug = False

# Try a to find a local config file...
try:
    imp.find_module('config')
    import config

    if hasattr(config, "save_path"):
        save_path = config.save_path
    if hasattr(config, "print_debug"):
        print_debug = config.print_debug
    if hasattr(config, "current_version_cache"):
        current_version_cache = config.current_version_cache
    if print_debug:
        print("* Config file found, using those settings")
except ImportError:
    no_local_config_found = True

# Make sure save_path has trailing slash... it's important.
if save_path[-1] != "/":
    save_path = save_path + "/"

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def load_local_cache():
    global local_faq_data
    local_faq_data = {}
    if os.path.isfile( save_path + current_version_cache ):
        with open( save_path + current_version_cache ) as data_file:
            local_faq_data = json.load(data_file)

def save_local_cache():
    with open(save_path + current_version_cache, 'w') as outfile:
        json.dump(gw_faq_data, outfile)

def get_remote_faq_list( request_data ):
    global download_items
    current_category = ""
    for line in request_data.split("\n"):
        if line.lower().find('faqs__header-count') > -1:
            current_category = cleanhtml( line )
            current_category = re.sub(  r'\(.*\)', '', current_category )
            current_category = current_category.strip()
            current_category = current_category.replace( u'\u2122', ' -' )
            if current_category not in gw_faq_data:
                gw_faq_data[ current_category ] = []
        if line.lower().find('faqs__list-title') > -1:
            version = line.split( 'faqs__list-version">' )
            title = line.split( 'faqs__list-title"><span>' )
            pdf_url = line.split( '<a href="')
            pdf = ""

            version = version[1]
            title = title[1]
            pdf_url = pdf_url[1]

            version = version[0: version.find('<')]
            title = title[0: title.find('<')]
            pdf_url = pdf_url[0: pdf_url.find('"')]

            raw_version = version

            raw_version = raw_version.split("/")
            raw_version[0] = raw_version[0].lower().replace( "updated ", "")
            raw_version[0] = raw_version[0].zfill(2)
            raw_version = raw_version[1] + raw_version[0]

            raw_version = raw_version.replace(".", "")
            raw_version = int( raw_version )

            version = version.replace("/", "-")

            pdf = title + " - " + version + ".pdf"

            pdf = pdf.replace(":", " -")
            pdf = pdf.replace("\\", "-")
            pdf = pdf.replace("/", "-")

            gw_faq_data[ current_category ].append(
                {
                    "version": raw_version,
                    "title": title,
                    "pdf_url": pdf_url,
                    "pdf": pdf,
                }
            )


def download_file( file_url, save_path):
    dlresponse = requests.get(file_url, stream=True)
    with open(save_path, 'wb') as f:
        for chunk in dlresponse.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return save_path

def download_files():
    for category in gw_faq_data:
        for faq_item in gw_faq_data[category]:
            needs_download = True

            file_save_path = save_path + category + "/" + faq_item["pdf"]

            if not os.path.exists(save_path + category):
                os.makedirs(save_path + category)

            if os.path.exists(file_save_path):
                if category in local_faq_data:
                    for local_item in local_faq_data[category]:
                        if local_item["title"].lower().strip() == faq_item["title"].lower().strip():
                            if int( faq_item["version"] ) > int( local_item["version"] ):
                                # Remove the old FAQ file
                                os.unlink(  save_path + category + "/" + local_item["pdf"] )
                                if print_debug:
                                    print( "* Removing old FAQ file " + category + "/" + local_item["pdf"] )
                            else:
                                needs_download = False


            if needs_download:
                if print_debug:
                    print( "* Downloading FAQ file " + category + "/" + faq_item["pdf"] )
                download_file( faq_item["pdf_url"], file_save_path )
            else:
                if print_debug:
                    print("* Not downloading " +  file_save_path)


if not os.path.exists(save_path):
    os.makedirs(save_path)

response = requests.get( gw_faqs_url )
if response.status_code == 200:
    load_local_cache()
    get_remote_faq_list( response.text )
    download_files()
    save_local_cache()

else:
    print( "Couldn't connect to " + gw_faqs_url )
