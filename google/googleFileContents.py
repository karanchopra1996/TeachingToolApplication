# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Recursively extracts the text from a Google Doc.
"""
from __future__ import print_function

import os

import googleapiclient.discovery as discovery
from google.auth.transport.requests import Request
from core.google_services import google_services as googleCore

DISCOVERY_DOC = 'https://docs.googleapis.com/$discovery/rest?version=v1'

# # Sample code: https://developers.google.com/docs/api/samples/extract-text


def read_paragraph_element(element):
    """Returns the text in the given ParagraphElement.

        Args:
            element: a ParagraphElement from a Google Doc.
    """
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')

def read_strucutural_elements(elements):
    """Recurses through a list of Structural Elements to read a document's text where text may be
        in nested elements.

        Args:
            elements: a list of Structural Elements.
    """
    text = ''
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            for elem in elements:
                text += read_paragraph_element(elem)
        elif 'table' in value:
            # The text in table cells are in nested Structural Elements and tables may be
            # nested.
            table = value.get('table')
            for row in table.get('tableRows'):
                cells = row.get('tableCells')
                for cell in cells:
                    text += read_strucutural_elements(
                        cell.get('content'))
        elif 'tableOfContents' in value:
            # The text in the TOC is also in a Structural Element.
            toc = value.get('tableOfContents')
            text += read_strucutural_elements(
                toc.get('content'))
    return text

def getFileContents(fileID):
    """Uses the Docs API to print out the text of a document."""
    credentials = googleCore.get_credentials()
    credentials.refresh(Request())
    try: 
        # create docs api client
        docs_service = discovery.build(
            'docs', 'v1', credentials=credentials, discoveryServiceUrl=DISCOVERY_DOC)
        doc = docs_service.documents().get(documentId=fileID).execute()
        doc_content = doc.get('body').get('content')
        response = read_strucutural_elements(doc_content)
        return response
    except: 
        return "Error"
