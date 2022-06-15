# WP Userdata to CSV
Creates a CSV file of Wordpress users based on the Wordpress API offering public information

## Usage

Simply run the utility as described under your own responsibility.

    wp-user-indexer.py [-h] -b BASEURL

    optional arguments:
    -h, --help            show this help message and exit
    -b BASEURL, --baseurl BASEURL
                            baseurl of the Wordpress installation, include protocol e.g. https://domain.com


## Results

The resulting CSV file will be e.g. domain.com.csv

Delimiter is the pipe in the CSV: |

Quote character in the CSV is: "

## Extra features

This utility extracts Gravatar user MD5 checksums and inserts those into the CSV file.