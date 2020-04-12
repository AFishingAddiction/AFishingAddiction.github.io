#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2018, Christopher Stoll
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of this software nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import math
import numpy
import re

from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join

class PageObject(object):
  def __init__(self, arg):
    super(PageObject, self).__init__()
    self.arg = arg

  def objects_for_directory(self, path):
    return self._page_objects_from_files(self._list_files(path))
    
  def _list_files(self, path):
    return [join(path, file) for file in listdir(path) \
            if (isfile(join(path, file)) and ('.html' in file or '.md' in file))]

  def _page_objects_from_files(self, file_names):
    page_objects = []
    for file_name in file_names:
      page_objects.append(self._page_object_from_file(file_name))
    return page_objects

  def _page_object_from_file(self, file_name):
    file = open(file_name, 'r')
    file_contents = file.read()
    # TODO: check page_contents length and drop short pages
    page_url = self._extract_permalink(file_contents)
    page_date = self._extract_date(file_name, file_contents)
    page_title = self._extract_title(file_contents)
    if not page_url:
      page_url = self._generate_url(page_date, file_name)
    if not page_title:
      page_title = self._generate_page_title(file_name)
    page_object = {
      'file_name': file_name,
      'url': page_url,
      'date': page_date,
      'title': page_title,
      'image': self._extract_image(file_contents),
      'contents': self._extract_text(file_contents),
      'needs_related': self._extract_needs_related(file_contents)
    }
    file.close()
    return page_object

  def _extract_permalink(self, html):
    permalink = re.search('permalink: (.*)', html)
    if permalink:
      return permalink.group(1).strip()
    return None

  def _extract_date(self, file_name, html):
    date = re.search('date: (.*)', html)
    if date:
      return date.group(1).strip()
    date = re.search('.*(\d{4}-\d{2}-\d{2}).*', file_name)
    if date:
      return date.group(1).strip()
    return None

  def _generate_url(self, page_date, file_path):
    if not page_date or not file_path:
      return None
    date_parts = page_date.split('-')
    file_parts = file_path.split('/')
    file_name = file_parts[len(file_parts) - 1]
    title_part = file_name.split('.')
    title_no_date = re.sub('{}-'.format(page_date), '', \
                           title_part[0], flags=re.DOTALL)
    #return '/{}/{}/{}/{}.html'.format(date_parts[0], \
    #                                  date_parts[1], \
    #                                  date_parts[2], \
    #                                  title_no_date)
    return '/{}/'.format(title_no_date)

  def _extract_title(self, html):
    title = re.search('title: "(.*)"', html)
    if title:
      return title.group(1).strip()
    title = re.search('title: (.*)', html)
    if title:
      return title.group(1).strip()
    return None

  def _generate_page_title(self, file_name):
    title = re.search('.*(\d{4}-\d{2}-\d{2})-(.*)\.', file_name)
    if title:
      title_parts = title.group(2).split('-')
      return ' '.join(title_parts).title()
    return None

  def _extract_image(self, html):
    image = re.search('image: (.*)', html)
    if image:
      return image.group(1).strip()
    return None

  def _extract_text(self, html):
    remove_related = re.sub('<div id="related" class="clearfix">(.*?)</div>', \
                            '', html, flags=re.DOTALL)
    remove_br_tag = re.sub('<([brBR /]*?)>', ' ', remove_related, flags=re.DOTALL)
    remove_no_space = re.sub('\.<', ' <', remove_br_tag, flags=re.DOTALL)
    remove_html = BeautifulSoup(remove_no_space, "lxml").text
    remove_liquid = re.sub('{%.*?%}', '', remove_html, flags=re.DOTALL)
    remove_code = re.sub('```.*?```', '', remove_liquid, flags=re.DOTALL)
    remove_front_matter = re.sub('^---.*?---', '', remove_code, flags=re.DOTALL)
    remove_links = re.sub('\[(.*?)\]\((.*?)\)', r'\1 \2', \
                          remove_front_matter, flags=re.DOTALL)
    remove_urls = re.sub('http.*?://(.*?)/.*?[ \t\n]', r'\1 ', \
                         remove_links, flags=re.DOTALL)
    remove_hyphens = re.sub('([a-zA-Z])-([a-zA-Z])', r'\1\2', \
                            remove_urls, flags=re.DOTALL)
    remove_contractions = re.sub('([a-zA-Z])\'([a-zA-Z]) ', r'\1\2 ', \
                                 remove_hyphens, flags=re.DOTALL)
    remove_more_contractions = re.sub('([a-zA-Z])\'([a-zA-Z])', r'\1\2', \
                                      remove_contractions, flags=re.DOTALL)
    remove_periods = re.sub('\.[^a-zA-z0-9]', ' ', \
                            remove_more_contractions, flags=re.DOTALL)
    alpha_numeric = re.sub('[^ \.0-9a-zA-Z]+', ' ', \
                           remove_periods, flags=re.DOTALL)
    # TODO: stem all words
    return ' '.join(alpha_numeric.lower().split())

  def _extract_needs_related(self, html):
    related = re.search('related: \[(.*?)\]', html, re.DOTALL)
    return True if related else False

    date = re.search('<div id="related" class="clearfix">(.*?)</div>', \
                     html, re.DOTALL)
    if date:
      return True
    return False

class LatentSemanticAnalysis(object):
  def __init__(self, page_objects):
    super(LatentSemanticAnalysis, self).__init__()
    term_index, document_term_matrix = \
      self._generate_document_term_matrix(page_objects)
    self.page_objects = page_objects
    self.document_space = self._generate_document_space(document_term_matrix)

  def top_matches(self, count=3):
    search_ids = self._list_search_ids(self.page_objects)
    return search_ids, self._top_matches(search_ids, self.document_space, count)

  def _generate_document_term_matrix(self, page_objects):
    term_index = self._generate_term_dictionary(page_objects)
    document_term_matrix = []
    for page_object in page_objects:
      document_row = [0] * len(term_index)
      for word in page_object['contents'].split():
        if word in term_index:
          word_index = term_index[word]
          document_row[word_index] += 1
      document_term_matrix.append(document_row)
    # here is your
    # - term index
    # - massive sparse matrix
    #   - columns represent words (see term index)
    #   - rows represent documents
    return term_index, document_term_matrix

  def _generate_term_dictionary(self, page_objects):
    raw_word_dict = {}
    # get the vocabulary and document count
    for page_object in page_objects:
      raw_words = page_object['contents'].split()
      raw_words.sort()
      # each word only counts once per document
      words = list(set(raw_words))
      for word in words:
        if len(word) > 1:
          if word in raw_word_dict:
            raw_word_dict[word] += 1
          else:
            raw_word_dict[word] = 1
    word_dict = {}
    word_index = 0
    # create a dictionary of words and give them id numbers
    for key, value in raw_word_dict.iteritems():
      # the words must appear in more than 1 document
      if value > 1:
        word_dict[key] = word_index
        word_index += 1
    return word_dict

  def _generate_document_space(self, term_doc_matrix):
    M = numpy.asmatrix(term_doc_matrix)
    U, singular_values, Vt = numpy.linalg.svd(M, full_matrices=True)
    
    k = self._get_k_limit(singular_values)
    for x in xrange(k, len(singular_values)):
      singular_values[x] = 0

    s = numpy.diag(singular_values)
    return numpy.dot(U, s)

  def _get_k_limit(self, sigma, klimit_min=1, klimit_max=1024):
    """ Take a list of singular values (eigen values)
        and return the number of signifigant values
    :sigma:         list of singular values
    :klimit_min:    the minimum number of signifigant values
    :klimit_max:    the maximum number of signifigant values
    :returns:       the number of signifigant singular values
    """
    # if current value times this value is less than the last
    # value then we found the last signifigant value
    DROP_FACTOR = 1.99
    klimit = klimit_max
    last_eigenvalue = 0
    eigenvalues = numpy.nditer(sigma, flags=['f_index'])
    while not eigenvalues.finished:
      if eigenvalues.index > klimit_min:
        if last_eigenvalue:
          if (eigenvalues[0] * DROP_FACTOR) < last_eigenvalue:
            klimit = eigenvalues.index - 1
            break
      last_eigenvalue = eigenvalues[0]
      eigenvalues.iternext()
    return klimit

  def _list_search_ids(self, page_objects):
    search_ids = []
    for index, page_object in enumerate(page_objects):
      if page_object['needs_related']:
        search_ids.append(index)
    return search_ids

  def _top_matches(self, search_ids, document_space, limit):
    all_matches = []
    for search_id in search_ids:
      search_document = document_space[search_id].tolist()[0]
      matches = [{'value': -999999, 'index': -1}]
      for index, current_document in enumerate(document_space):
        if index != search_id:
          cosign_similarity = \
            self._cosign_similarity(search_document, current_document.tolist()[0])
          if cosign_similarity > matches[len(matches)-1]['value']:
            matches.append({'value': cosign_similarity, 'index': index})
            matches.sort(key=lambda x: x['value'], reverse=True)
            matches = matches[:limit]
      all_matches.append(matches)
    return all_matches

  def _cosign_similarity(self, search_document, current_document):
    numerator = 0
    denominatorA = 0
    denominatorB = 0
    for index in xrange(0, len(search_document)):
      numerator += search_document[index] * current_document[index]
      denominatorA += search_document[index] * search_document[index]
      denominatorB += current_document[index] * current_document[index]
    if denominatorA == 0 or denominatorB == 0:
      return 0
    return numerator / (math.sqrt(denominatorA) * math.sqrt(denominatorB))


def create_page_element(page_object):
  page_element = '<div class="card">'
  if page_object['image']:
    page_element += '<img class="card-img-top" '
    page_element += 'src="{}"'.format(page_object['image'])
    page_element += 'alt="{}">'.format(page_object['title'])
  page_element += '<div class="card-body">'
  if page_object['url']:
    page_element += '<a href="{}">'.format(page_object['url'])
    page_element += '<h5 class="card-title">{}'.format(page_object['title'])
    page_element += '</h5></a>'
  else:
    page_element += '<h5 class="card-title">{}</h5>'.format(page_object['title'])
  page_element += '<p class="card-text">'
  page_element += '<small class="text-muted">{}'.format(page_object['date'])
  page_element += '</small></p>'
  page_element += '</div></div>'
  return page_element


def update_pages(page_objects, search_ids, top_matches):
  for index, match_row in enumerate(top_matches):
    #page_elements = '<div id="related" class="clearfix">'
    #page_elements = '<div class="card mt-3">'
    #page_elements = '<div class="card-header">Related Posts</div>'
    #page_elements = '<div class="card-body"><div class="card-group bg-faded">'
    page_elements = 'related: ['
    print "{}".format(page_objects[search_ids[index]]['title'])
    for match in match_row:
      match_index = match['index']
      #page_elements += create_page_element(page_objects[match_index])
      page_elements += "{},".format(page_objects[match_index]['url'])
      print " {:.5f} -- {}".format(match['value'], page_objects[match_index]['title'])
    #page_elements += '</div></div></div></div>'
    page_elements += ']'

    file_to_update = page_objects[search_ids[index]]['file_name']
    with open(file_to_update, 'r') as file:
      file_contents = file.read()
      file.close()
      #new_file_contents = re.sub('<div id="related" class="clearfix">.*</div>', \
      #                           page_elements, file_contents, flags=re.DOTALL)
      new_file_contents = re.sub('related: \[.*\]', page_elements, file_contents)
      with open(file_to_update, 'w') as file:
        file.write(new_file_contents)
        file.close()

if __name__ == "__main__":
  page_objects = PageObject(None).objects_for_directory('./_posts/')
  search_ids, top_matches = LatentSemanticAnalysis(page_objects).top_matches()
  update_pages(page_objects, search_ids, top_matches)
