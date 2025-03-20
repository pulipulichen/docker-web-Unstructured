import plistlib
import json
import os

def plist_to_json(plist_file_path):
  """將 .plist 轉換成 .json，並將結果寫入同名 .json 檔案。
  Args:
    plist_file_path (str): plist 檔案的路徑。
  Returns:
    bool: 如果轉換成功則返回 True，如果發生錯誤則返回 False。
  """
  try:
    with open(plist_file_path, 'rb') as plist_file:
      plist_data = plistlib.load(plist_file) # 20250321-022020 從 plist 檔案讀取資料
      json_data = json.dumps(plist_data, indent=2) # 20250321-022020 將資料轉換為 JSON 格式

    # 20250321-022147 取得檔案名稱和目錄
    file_name, file_ext = os.path.splitext(plist_file_path)
    json_file_path = file_name + ".json"

    # 20250321-022147 寫入 JSON 檔案
    with open(json_file_path, 'w') as json_file:
      json_file.write(json_data)
    return json_file_path

  except FileNotFoundError:
    print(f"檔案未找到: {plist_file_path}") # 20250321-022020 檔案未找到的錯誤處理
    return False
  except plistlib.InvalidFileException:
    print(f"無效的 plist 檔案: {plist_file_path}") # 20250321-022020 plist 檔案格式錯誤的錯誤處理
    return False
  except Exception as e:
    print(f"發生錯誤: {e}") # 20250321-022020 其他錯誤處理
    return False
