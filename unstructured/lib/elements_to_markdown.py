
import sys
from .split_html_table import split_html_table
from .html_table_to_markdown import html_table_to_markdown
from .get_elements_metadata import get_elements_metadata

from markdownify import markdownify as md

import hanzidentifier
import opencc

from .count_token import count_token
import os

converter_s2t = opencc.OpenCC('s2t')  # 簡體轉繁體
converter_t2s = opencc.OpenCC('t2s')  # 簡體轉繁體

def elements_to_markdown(file_ext, elements, chunk_config):
    """將 Unstructured 解析的元素轉換為 Markdown 格式"""
    # markdown_chunks = []

    # =================================================================

    chunk_token_length = int(os.getenv('UNSTRUCTED_CHUNK_TOKEN_LENGTH', 500))
    if 'chunk_token_length' in chunk_config:
        chunk_token_length = int(chunk_config['chunk_token_length'])

    chunk_rows_per_table = int(os.getenv('UNSTRUCTED_CHUNK_ROWS_PER_TABLE', 30))
    if 'chunk_rows_per_table' in chunk_config:
        chunk_rows_per_table = int(chunk_config['chunk_rows_per_table'])

    enable_chunk = (os.getenv('UNSTRUCTED_ENABLE_CHUNK', "false").lower() == "true")
    if 'ENABLE_CHUNK' in chunk_config:
        enable_chunk = chunk_config['ENABLE_CHUNK']

    # =================================================================

    sections = []
    metadatas = []

    chinese_type = None

    section_container = []
    listitem_container = []

    skip_title_detection = False
    if len(elements) > 1:
        if getattr(elements[0], "category", "").lower() == 'title' and \
           getattr(elements[1], "category", "").lower() == 'title' and \
           getattr(elements[-1], "category", "").lower() == 'title':
            skip_title_detection = True
            print('Skip title detection...')

    next_is_title = False

    element_first = None

    for element in elements:
        # print(element)  
        text = element.text.strip()
        # print(text)
        # print(text == '‹#›')

        if file_ext in ['.ppt', '.pptx'] and text == '‹#›':
            next_is_title = True
            continue

        if not text:
            continue
        
        if chinese_type is None or chinese_type is hanzidentifier.UNKNOWN:
            chinese_type = hanzidentifier.identify(text)
            # print(chinese_type)

        #text = safe_fix_encoding(text)
        #print(text)

        # https://docs.unstructured.io/open-source/concepts/document-elements

        # 檢查 ElementMetadata 物件中的 category 是否存在
        category = getattr(element.metadata, "category", "")
        if category == "":
            category = getattr(element, "category", "")
        # print(category)
               
        if skip_title_detection is True and (category == "Title" or category == "Heading"):
            category = "NarrativeText"

        if next_is_title is True:
            # print('NEXT IS TITLE' + ' ' + category + " " + text)
            category = 'Title'
            # print(category + " " + str(category == "title"))
            next_is_title = False
         
        if category in ["Title", "Table"]:
            if len(section_container) > 0 and count_token(section_container) > int(chunk_token_length / 2) and enable_chunk is True:
                # print('title 超過' + str(count_token(section_container)))
                sections.append("\n\n".join(section_container))
                section_container = []
                metadatas.append(get_elements_metadata(element_first, element))
                element_first = None

        # print(category + " " + getattr(element, "category", "").lower() + ' ' + text[0:50])

        # ======================================
                
        if category != 'ListItem' and len(listitem_container) > 0:
            section_container.append("\n".join(listitem_container))
            if count_token(section_container) > chunk_token_length and enable_chunk is True:
                sections.append("\n\n".join(section_container))
                section_container = []
                metadatas.append(get_elements_metadata(element_first, element))
                element_first = None

            listitem_container = []

        # ======================================
                

        if category == "Title":
            if element_first is None:
                element_first = element

            section_container.append(f"# {text}")
            # print("\n\n".join(section_container))
        # elif category == "Heading":
            # section_container.append(f"## {text}")
        elif category == "Table":
            if element_first is None:
                element_first = element

            table = element.metadata.text_as_html
            
            enable_convert = True
            # enable_convert = False

            if enable_convert:
                tables = split_html_table(table, chunk_rows_per_table)
            else:
                tables = [table]
            

            for table in tables:

                if enable_convert:
                    table_md = html_table_to_markdown(table)
                    if chinese_type is hanzidentifier.TRADITIONAL or chinese_type is hanzidentifier.BOTH or chinese_type is hanzidentifier.MIXED:
                        table_md = converter_s2t.convert(table_md)
                    elif chinese_type is hanzidentifier.SIMPLIFIED:
                        table_md = converter_t2s.convert(table_md)
                else:
                    table_md = table

                if table_md.strip() == "":
                    continue

                section_container.append(table_md)

                if enable_chunk is True:
                    sections.append("\n\n".join(section_container))
                    section_container = []
                    metadatas.append(get_elements_metadata(element_first, element))
                    element_first = None
        elif category == "ListItem":
            if element_first is None:
                element_first = element

            listitem_container.append("* " + text)

            if count_token(section_container + listitem_container) > chunk_token_length and enable_chunk is True:
                section_container.append("\n".join(listitem_container))
                sections.append("\n\n".join(section_container))
                section_container = []
                listitem_container = []

                metadatas.append(get_elements_metadata(element_first, element))
                element_first = None
        elif category in ["PageBreak", "Heading", "Footer", "PageNumber"]:
            print('Skip...')
        else:

            # print('else')
            if count_token(section_container) > chunk_token_length and enable_chunk is True:
                sections.append("\n\n".join(section_container))
                section_container = []
                metadatas.append(get_elements_metadata(element_first, element))
                element_first = None

            if category == "FigureCaption":
                text = '## ' + text 
            elif category in ["Address", "EmailAddress"]:
                text = '`' + text + '`'
            elif category in ["CodeSnippet"]:
                text = '````\n' + text + '\n````'
            
            if element_first is None:
                element_first = element

            section_container.append(text)

    if len(section_container) > 0:
        sections.append("\n\n".join(section_container))
        metadatas.append(get_elements_metadata(element_first, elements[-1]))

    return sections, metadatas



if __name__ == "__main__":
    elements_to_markdown(sys.argv[1])