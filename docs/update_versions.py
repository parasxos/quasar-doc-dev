import os
import sys
import json


JSON_FILE = './docs/source/_static/versions.json'
VERSIONS_FOLDER = '/usr/share/nginx/quasar/version'


if __name__ == '__main__':
  for folder_version in os.listdir(VERSIONS_FOLDER):
    print('Processing', folder_version)
    cp_command = f'cp {JSON_FILE} {VERSIONS_FOLDER}/{folder_version}'
    print(cp_command)
    #os.system(cp_command)
  exit(0)
