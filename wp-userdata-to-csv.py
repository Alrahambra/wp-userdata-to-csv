#!/usr/bin/env python3

import requests
import argparse
import csv
import json
import sys
import re
from urllib.parse import urlparse

requests.packages.urllib3.disable_warnings()


def retrieve_json(users_api_url):
    r = requests.get(users_api_url)
    if r.status_code != 200:
        print("This does not appear to be a Wordpress website")
        sys.exit(0)
    return r.text


def get_available_keys(userdata):
    return userdata.keys()

def gravatar_url_extract(avatar_url_sample):
    #Why? Because sometimes JSON contains False-booleans
    avatar_url_sample = str(avatar_url_sample)
    #Special treatment for Gravatar URLs
    md5_sum = re.search(r'[a-f0-9]{32}', avatar_url_sample)
    if bool(md5_sum) == False:
        return 'N/A'
    return md5_sum.group(0)

def main(baseurl):
    users_api_url = baseurl + '/wp-json/wp/v2/users'
    userdata = json.loads(retrieve_json(users_api_url))
    filename = re.sub(r'http.*\/\/', '', baseurl) + '.csv'


    #Get available keys as these can vary per website
    try:
        #These will be the headers as well
        keylist = list(userdata[0].keys())
    except:
        print("No data available to be parsed!")
        sys.exit(0)
    
    keylist.append('gravatar_md5')

    with open(filename, 'w') as wpscv:
        writer = csv.writer(wpscv, delimiter='|', quotechar='"')
        #Headers first
        writer.writerow(keylist)

        #Then the entries

        for user in userdata:
            row = []
            for key in keylist:
                if key != 'gravatar_md5':
                    try:
                       row.append(user[key])
                    except:
                        row.append('N/A')
                if key == 'gravatar_md5':
                    avatar_url_dict = user['avatar_urls']
                    avatar_url_loc = next(iter(avatar_url_dict))
                    avatar_url_sample = user['avatar_urls'][avatar_url_loc]
                    extracted_gravatar_md5 = gravatar_url_extract(avatar_url_sample)
                    row.append(extracted_gravatar_md5)
            writer.writerow(row) 



    wpscv.close()
    print("Success! Results are saved in: {filename}".format(filename=filename))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--baseurl", type=str, required=True,
                        help="baseurl of the Wordpress installation, include protocol e.g. https://domain.com")
    args = parser.parse_args()
    main(args.baseurl)