#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import sys
import requests
import zipfile

required_data = [
    'Blocks.txt', 'CaseFolding.txt', 'DerivedCoreProperties.txt',
    'PropList.txt', 'PropertyAliases.txt', 'PropertyValueAliases.txt',
    'Scripts.txt', 'UnicodeData.txt',
    'auxiliary/GraphemeBreakProperty.txt', 'auxiliary/WordBreakProperty.txt',
    'emoji/emoji-data.txt'
]

if len(sys.argv) < 2:
    print('Fetching the latest version name of Unicode')
    latest_url = requests.get('https://www.unicode.org/versions/latest', allow_redirects=False).headers.get('Location', '')
    https_leading_text = 'https://www.unicode.org/versions/Unicode'
    http_leading_text = 'http://www.unicode.org/versions/Unicode'
    if latest_url.startswith(https_leading_text):
        version = latest_url[len(https_leading_text):]
    elif latest_url.startswith(http_leading_text):
        version =  latest_url[len(http_leading_text):]
    else:
        print('Failed detect the latest version name of Unicode. Please try to specify a version.')
        exit(1)
else:
    version = sys.argv[1]

print(f'Fetching UCD for Unicode {version}')
zip_data = requests.get(f'https://www.unicode.org/Public/{version}/ucd/UCD.zip').content

print('Unzipping required UCD data')
with zipfile.ZipFile(io.BytesIO(zip_data)) as zip:
    for name in required_data:
        output_file = name[name.find('/') + 1:]
        with open(output_file, 'wb') as f:
            f.write(zip.read(name))

print('Done!')