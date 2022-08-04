'use strict';

function getGhPagesCurrentFolder() {
  // Extract version folder under the assumpgion that the URL is of the form
  // https://<username>.github.io/<project>/<version>/...
  const {
    location: { pathname = '' },
  } = window;
  if (pathname.includes('versions/')) {
    const [, version, ..._] = pathname.split('/');
    return version;
  }
  return 'latest';
}

function getRootUrl() {
  var root_url = window.location.origin;
  return root_url;
}

function getGithubProjectUrl() {
  return 'https://github.com/quasar-team/quasar';
}

function _addVersionsMenu(version_data) {
  console.log('version_data', version_data);
  // The menu was reverse-engineered from the RTD websites, so it's very
  // specific to the sphinx_rtd_theme
  var folders = version_data['versions'];
  var root_url = getRootUrl();
  var current_url = document.URL;
  var current_folder = getGhPagesCurrentFolder();
  var current_version = version_data['labels'][current_folder];
  var menu = document.createElement('div');
  menu.setAttribute('class', 'rst-versions');
  menu.setAttribute('data-toggle', 'rst-versions');
  menu.setAttribute('role', 'note');
  menu.setAttribute('aria-label', 'versions');
  var inner_html =
    "<span class='rst-current-version' data-toggle='rst-current-version'>" +
    "<span class='fa fa-book'> Doctr </span>" +
    '<span>' +
    current_version +
    ' </span>' +
    "<span class='fa fa-caret-down'></span>" +
    '</span>' +
    "<div class='rst-other-versions'>" +
    "<div class='injected'>" +
    '<dl>' +
    '<dt>Versions</dt>';
  var i;
  for (i in folders) {
    var folder = folders[i];
    console.log('folder', folder);
    if (folder == current_folder) {
      var inner_html =
        inner_html +
        "<strong><dd><a href='" +
        current_url +
        "'>" +
        current_version +
        '</a></dd></strong>';
    } else {
      var folder_url = folder == 'latest' ? folder : 'versions/' + folder;
      console.log('Current folder', current_folder);
      console.log('Folder URL', folder_url);
      var url_version = '';
      if (!current_url.includes('versions')) {
        url_version = current_url + 'versions/' + folder;
      } else {
        url_version = current_url.replace(current_folder, folder);
      }
      var inner_html =
        inner_html +
        "<dd><a href='" +
        url_version +
        "'>" +
        version_data['labels'][folder] +
        '</a></dd>';
    }
  }

  var github_project_url = getGithubProjectUrl();
  if (github_project_url !== null && github_project_url.length > 0) {
    var inner_html =
      inner_html +
      '<dt>On Github</dt>' +
      "<dd><a href='" +
      github_project_url +
      "'>Project Home</a></dd>" +
      "<dd><a href='" +
      github_project_url +
      "/issues'>Issues</a></dd>";
  }
  var inner_html =
    inner_html +
    '</dl>' +
    '<hr>' +
    "<small>Generated by <a href='https://goerz.github.io/doctr_versions_menu'>Doctr Versions Menu</a>" +
    '</small>' +
    '</div>' +
    '</div>';

  menu.innerHTML = inner_html;
  var parent = document.body;
  parent.insertBefore(menu, parent.lastChild);

  // Add a warning banner for dev/outdated versions
  var warning;
  var msg;
  if (
    version_data['warnings'] &&
    version_data['warnings'][current_folder] &&
    version_data['warnings'][current_folder].indexOf('outdated') >= 0
  ) {
    warning = document.createElement('div');
    warning.setAttribute('class', 'admonition danger');
    msg = 'This document is for an <strong>outdated version</strong>.';
  } else if (
    version_data['warnings'] &&
    version_data['warnings'][current_folder] &&
    version_data['warnings'][current_folder].indexOf('unreleased') >= 0
  ) {
    warning = document.createElement('div');
    warning.setAttribute('class', 'admonition danger');
    msg =
      'This document is for an <strong>unreleased development version</strong>.';
  } else if (
    version_data['warnings'] &&
    version_data['warnings'][current_folder] &&
    version_data['warnings'][current_folder].indexOf('prereleased') >= 0
  ) {
    warning = document.createElement('div');
    warning.setAttribute('class', 'admonition danger');
    msg =
      'This document is for a <strong>pre-release development version</strong>.';
  }
  if (warning !== undefined) {
    if (version_data['latest'] !== null) {
      msg =
        msg +
        ' Documentation is available for the ' +
        "<a href='" +
        current_url.replace(current_folder, version_data['latest']) +
        "'>latest public release</a>.";
    }
    warning.innerHTML =
      "<p class='first admonition-title'>Note</p> " +
      "<p class='last'> " +
      msg +
      '</p>';
    var parent =
      document.querySelector('div.body') ||
      document.querySelector('div.document') ||
      document.body;
    parent.insertBefore(warning, parent.firstChild);
  }
}

function addVersionsMenu() {
  var json_file = window.location.href + '/_static/versions.json';
  $.getJSON(json_file, _addVersionsMenu);
}

document.addEventListener('DOMContentLoaded', addVersionsMenu);
