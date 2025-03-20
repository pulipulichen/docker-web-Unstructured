import os
import uuid

# 設定上傳資料夾
UPLOAD_FOLDER = "/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # 確保資料夾存在

def save_upload_file(file):
    file_ext = os.path.splitext(file.filename)[1].lower()  # 取得副檔名
    random_filename = f"{uuid.uuid4().hex}{file_ext}"  # 產生隨機檔名
    file_path = os.path.join(UPLOAD_FOLDER, random_filename)

    # 確保目標資料夾存在
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # 存檔
    with open(file_path, "wb") as buffer:
        while chunk := file.file.read(4096):
            buffer.write(chunk)
        # buffer.write(file.file.read())  # 直接讀取檔案內容步的檔案內容

    # print(file_path)
    # print(file.filename)
    # print(file.content_type)
    # print(os.path.getsize(file_path))

    return file_ext, file_path