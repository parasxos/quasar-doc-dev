import os
import re
import requests
import pypandoc
from pathlib import Path

str_dict = {
  'WEB_URL': 'http://quasar.cern.ch',
  'REPO_URL': 'https://raw.githubusercontent.com/parasxos/quasar/master/Documentation',
}

raw_contents_types = {
  'ChangeLog.html': 'table'
}

HOME_PATH = str(Path.home())
VERSIONS_PATH = '/home/fmagalla/quasar/'
EXCEPTION_INDEX = [ 'quasar OPC UA servers.html' ] 

def download_list_known_server(url, output_path):
  print(f'Downloading {url}')
  r = requests.get(url)
  with open(f'{output_path}/quasar OPC UA servers.html', 'w') as f:
    f.write(r.text)

def get_files(in_path, external_extensions = []):
  html_files = []
  note_files = []
  external_files = []
  current_versions = []

  try:
    folder_versions = os.listdir(VERSIONS_PATH)
  except:
    folder_versions = []

  for folder_version in folder_versions:
    if os.path.exists(os.path.join(VERSIONS_PATH, folder_version)):
      current_versions.append(folder_version)

  for filename in os.listdir(in_path):
    extension = os.path.splitext(filename)[1]
  
    if filename.endswith('.html'):
      html_files.append(filename)
    elif extension in external_extensions:
      external_files.append(filename)

  for filename in os.listdir(f'{in_path}/Notes'):
    note_files.append(filename)

  current_versions.sort(key=lambda x: x.lower(), reverse=True)
  html_files.sort(key=lambda x: x.lower())
  note_files.sort(key=lambda x: x.lower())
  external_files.sort(key=lambda x: x.lower())

  print(
    f"""
    Found {len(current_versions)} versions: {current_versions}
    Found {len(html_files)} html files
    Found {len(note_files)} note files
    Found {len(external_files)} external files
    """
  )

  return html_files, external_files, note_files, current_versions

def copy_external(html_path, output_path, extensions = []):
  if not os.path.exists(output_path):
    os.makedirs(output_path, exist_ok=True)

  os.makedirs(f'{output_path}/images', exist_ok=True)

  for filename in os.listdir(html_path):
    extension = os.path.splitext(filename)[1]
    if extension in extensions:
      os.system(f'cp {html_path}/{filename} {output_path}/{filename}')

  for image in os.listdir(f'{html_path}/images'):
    os.system(f'cp {html_path}/images/{image} {output_path}/images/{image}')

def clean_filename(string, exceptions = []):
  if string in exceptions:
    return string

  string = re.sub('([a-z](?=[A-Z]))', r'\1 ', string)
  string = re.sub('(?<=[a-z0-9])_', r' ', string)
  return string.capitalize()


def parse_raw_html(filename, html_path, output_path, extract_content_type = None):
  print('\t\tParsing raw html')

  with open(html_path, 'r') as f:
    content = f.read()
  
  if extract_content_type == 'table':
    idx_start_body = content.find('<table')
    idx_end_body = content.find('</table>') + 8

    if idx_start_body == -1 or idx_end_body == -1:
      print('\t\tNo table found')
      return
    content = content[idx_start_body: idx_end_body]

  with open(output_path, 'w') as f:
    filename = os.path.splitext(filename)[0]
    f.write(f'{clean_filename(filename)}\n=========\n\n')
    f.write('.. raw:: html\n\n')
    for line in content.split('\n'):
      f.write(f'\t{line}\n')

def parse_html_files(files, html_path, output_path, raw_html=['ChangeLog.html', 'quasar_opcua_servers.html']):
  print('Starting conversion')

  files_processed = 0
  for file in files:
    print(f'\tProcessing {file}')

    in_path = os.path.join(html_path, file)
    out_name =  os.path.basename(file).replace('.html', '.rst')
    out_path = os.path.join(output_path, out_name)

    with open(in_path, 'r') as f:
      content = f.read()

    idx_first_h1 = content.find('</h1>')
    if idx_first_h1 != -1:
      content_after = content[idx_first_h1 + 5:].replace('h1>', 'h2>')

      with open(in_path, 'w') as f:
        lines = content[:idx_first_h1] + '</h1>' + content_after
        f.write(lines)
    if file in raw_html:
      parse_raw_html(file, in_path, out_path, raw_contents_types.get(file))
    else:  
      rst = pypandoc.convert_file(in_path, 'rst', outputfile=out_path)
    files_processed += 1

  print(f'Done, {files_processed} files converted')


def update_ref(line):
  #check reduce complexity

  if 'image::' in line:
    img_path = line.split(' ')[-1]
    idx_start = line.index(img_path)
    return line[:idx_start] + f'./converted/{img_path}'

  elif '.html' in line:
    idx_start = line.find('<')
    idx_mid = line.find('.html')
    idx_end = line.find('>')

    if idx_start == -1 or idx_end == -1 or idx_mid == -1:
      return line

    return line[:idx_start] + '<converted/' + line[idx_start + 1:idx_end] + line[idx_end:]
  
  return line

def find_line(target, gap = 1, start = 0, lines = []):
  idx_target = -1
  
  for idx, line in enumerate(lines[start:]):
    if target in line:
      idx_target = idx + start + gap
      break
  return idx_target

def insert_files(idx = 0, format_str = '', files = [], lines = [], exceptions = [], str_kwargs = {}, is_rst=False):
  for idx_cur, filename in enumerate(files):
    if filename in EXCEPTION_INDEX:
      continue
    if is_rst:
      filename = os.path.splitext(filename)[0]
      clean_name = clean_filename(os.path.splitext(filename)[0], exceptions)
    else:
      clean_name = clean_filename(filename, exceptions)
    line_parsed = format_str.format(clean_name=clean_name, filename=filename, **str_kwargs)
    lines.insert(idx + idx_cur, line_parsed)

  return idx, lines


def update_index(html_files, external_files, note_files, current_versions, version_name, path_index, exceptions_clean = []):
  print('Updating index.rst')

  with open(path_index.replace('index', '_init_index'), 'r') as f:
    lines = f.readlines()

  with open('./docs/source/converted/quasar.rst', 'r') as f:
    quasar_lines = f.readlines()
    for idx, line in enumerate(quasar_lines):
      if 'Quasar' in line and '=' in quasar_lines[idx + 1]:
        line = f'Quasar {version_name}\n'
      quasar_lines[idx] = update_ref(line)

  lines = quasar_lines + lines

  print(f'\tInserting html files')
  idx_html = find_line('HTML documentation', gap=3, lines=lines)
  format_str = '\t\t{clean_name} <./converted/{filename}>\n'
  idx_html, lines = insert_files(idx_html, format_str, html_files, lines, exceptions_clean, is_rst=True)


  rst_add_files = ['external_files.rst', 'notes_files.rst']

  print(f'\tInserting additional files')
  idx_ext = find_line('Additional files', gap=3, start=idx_html, lines=lines)
  format_str = '\t{clean_name} <./{filename}>\n'
  idx_ext, lines = insert_files(idx_ext, format_str, rst_add_files, lines, exceptions_clean, is_rst=True)

  print('\tInserting versions')
  idx_versions = find_line('Documentation versions', gap=3, start=idx_ext, lines=lines)
  format_str = '- `{clean_name} <{WEB_URL}/version/{filename}/>`_\n'
  idx_versions, lines = insert_files(idx_versions, format_str, current_versions, lines, exceptions_clean, str_dict)

  print('\n'.join(lines))

  with open(path_index, 'w') as f:
    f.writelines(lines)


  ext_path = path_index.replace('index', '_init_ext')
  with open(ext_path) as f:
    lines = f.readlines()

  print(f'\tInserting external files')
  idx_note = find_line('External files', gap=3, lines=lines)
  format_str = '- `{clean_name} <{REPO_URL}/{filename}>`_\n'
  idx_note, lines = insert_files(idx_note, format_str, external_files, lines, exceptions_clean, str_dict)

  with open(path_index.replace('index', 'external_files'), 'w') as f:
    f.writelines(lines)


  notes_path = path_index.replace('index', '_init_notes')
  with open(notes_path) as f:
    lines = f.readlines()
  
  print(f'\tInserting notes files')
  idx_note = find_line('Notes', gap=3, lines=lines)
  format_str = '- `{clean_name} <{REPO_URL}/Notes/{filename}>`_\n'
  idx_note, lines = insert_files(idx_note, format_str, note_files, lines, exceptions_clean, str_dict)

  with open(path_index.replace('index', 'notes_files'), 'w') as f:
    f.writelines(lines)

  print('Update done')
