import os
import re
import sys
import pypandoc

from utils import (
  parse_html_files, clean_filename,
  update_index, copy_external, get_files
)

version_name = sys.argv[1]
print(f'Converting to version {version_name}')

# Define constants
HTMLS_PATH = './Documentation'
PATH_INDEX = './docs/source/index.rst'
OUTPUT_PATH = './docs/source/converted'
EXCEPTIONS_CLEAN = ['ChangeLog', 'LogIt']
EXTERNAL_EXTENSIONS = ['.pdf', '.docx', '.xlsx', '.pptx', '.odg', '.png', '.jpg', '.jpeg', '.gif',  '.cmake']

# Download pandoc binary
pypandoc.pandoc_download.download_pandoc()

# Get list of HTML files
html_files, external_files, note_files, current_versions = get_files(HTMLS_PATH, EXTERNAL_EXTENSIONS)

# Copy current assets to output directory
copy_external(HTMLS_PATH, OUTPUT_PATH, EXTERNAL_EXTENSIONS)

# Parse HTML files to RST
parse_html_files(html_files, HTMLS_PATH, OUTPUT_PATH)

# Update index content
update_index(html_files, external_files, note_files, current_versions, version_name, PATH_INDEX, EXCEPTIONS_CLEAN)
