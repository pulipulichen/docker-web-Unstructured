import os

from unstructured.partition.auto import partition
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.ppt import partition_ppt
from unstructured.partition.pptx import partition_pptx
from unstructured.partition.rtf import partition_rtf
from unstructured.partition.doc import partition_doc
from unstructured.partition.docx import partition_docx
from unstructured.partition.image import partition_image

def file_path_to_elements(file_ext, file_path, chunk_config):

    ocr_languages = os.getenv('UNSTRUCTED_OCR_LANGUAGES', "chi_tra,eng,chi_sim")
    if 'ocr_languages' in chunk_config:
        ocr_languages = chunk_config['ocr_languages']
    # split languages by commas
    ocr_languages = ocr_languages.split(',')

    # =================================================================

    # 根據副檔名決定 partition 方法
    if file_ext in [".pdf"]:
        # print('會出錯嗎？')
        # print(file_path)
        # print(type(file_path))
        # print('================================================================')
        elements = partition_pdf(
            filename=file_path,
            infer_table_structure=True,
            strategy="auto",
            languages=ocr_languages,
            include_page_breaks=False,
        )
    elif file_ext in [".ppt"]:
        elements = partition_ppt(
            filename=file_path,
            include_page_breaks=False,
        )
    elif file_ext in [".pptx"]:
        elements = partition_pptx(
            filename=file_path,
            include_page_breaks=False,
        )
    elif file_ext in [".rtf"]:
        elements = partition_rtf(
            filename=file_path,
            include_page_breaks=False,
        )
    elif file_ext in [".doc"]:
        elements = partition_doc(
            filename=file_path,
            include_page_breaks=False,
        )
    elif file_ext in [".docx"]:
        elements = partition_docx(
            filename=file_path,
            include_page_breaks=False,
        )
    elif file_ext in [".png",".jpg",".jpeg",".tiff",".bmp",".heic"]:
        elements = partition_image(
            filename=file_path,
            strategy="auto",
            languages=ocr_languages,
            infer_table_structure=True,
        )
    else:
        elements = partition(filename=file_path)


    return elements