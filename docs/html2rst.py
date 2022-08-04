import os
import re
import sys
import utils
import pypandoc

# Define constants
HTMLS_PATH = './Documentation'
PATH_INDEX = './docs/source/index.rst'
OUTPUT_PATH = './docs/source/converted'
EXCEPTIONS_CLEAN = ['ChangeLog', 'LogIt']
EXTERNAL_EXTENSIONS = ['.pdf', '.docx', '.xlsx', '.pptx', '.odg', '.png', '.jpg', '.jpeg', '.gif',  '.cmake']
URL_KNOWN_LIST = 'https://gitlab.cern.ch/atlas-dcs-opcua-servers/ListKnownQuasarOpcUaServers/-/raw/master/quasar_opcua_servers.html'

if __name__ == '__main__':
  version_name = sys.argv[1]
  print(f'Converting to version {version_name}')

  # Download pandoc binary
  pypandoc.pandoc_download.download_pandoc()

  # Download the known list server
  utils.download_list_known_server(URL_KNOWN_LIST, HTMLS_PATH)

  # Get list of HTML files
  files = utils.get_files(HTMLS_PATH, EXTERNAL_EXTENSIONS)
  html_files, external_files, note_files, current_versions = files

  # Copy current assets to output directory
  utils.copy_external(HTMLS_PATH, OUTPUT_PATH, EXTERNAL_EXTENSIONS)

  # Parse HTML files to RST
  utils.parse_html_files(html_files, HTMLS_PATH, OUTPUT_PATH)

  # Update index content (table of contents)
  utils.update_index(
    html_files,
    external_files,
    note_files,
    current_versions,
    version_name,
    PATH_INDEX,
    EXCEPTIONS_CLEAN
  )

  exit(0)
