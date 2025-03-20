import os
import subprocess

def convert_file(file_path):
  need_convert = False
  file_ext = os.path.splitext(file_path)[1].lower()  # 取得副檔名
  base_file_path = file_path[0:(len(file_ext) * -1)]

  output_file_path = file_path
  dir_name = os.path.dirname(file_path)
  command = None
  if file_ext == '.odt':
    command = ["libreoffice", "--headless", "--convert-to", "docx", file_path, "--outdir", dir_name]
    output_file_path = base_file_path + '.docx'
  elif file_ext == '.ods':
    command = ["libreoffice", "--headless", "--convert-to", "xlsx", file_path, "--outdir", dir_name]
    output_file_path = base_file_path + '.xlsx'
  elif file_ext == '.odp':
    command = ["libreoffice", "--headless", "--convert-to", "pptx", file_path, "--outdir", dir_name]
    output_file_path = base_file_path + '.pptx'
  elif file_ext == '.odg':
    command = ["libreoffice", "--headless", "--convert-to", "pdf", file_path, "--outdir", dir_name]
    output_file_path = base_file_path + '.pdf'
  elif file_ext in ['.emf', ".wmf"]:
    command = ["libreoffice", "--headless", "--convert-to", "png", file_path, "--outdir", dir_name]
    output_file_path = base_file_path + '.png'

  if command is not None:
    print('converting file:', command)
    need_convert = True
    subprocess.run(command, check=True)

  return output_file_path
  