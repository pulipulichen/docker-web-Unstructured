
import requests
import os

def check_convert(file_path):
    """
    把 file_path 用 post 傳送到 converter-libreoffice ，然後取得回覆裡面的 file_path 並return
    20250320-233000
    """
    converter_url = os.getenv("CONVERTER_LIBREOFFICE_URL", "http://converter_libreoffice:8000") # 從環境變數取得 converter-libreoffice 的 URL，如果沒有設定，預設為 http://converter_libreoffice:8000
    try:
        response = requests.post(converter_url, data={"file_path": file_path}) # 發送 POST 請求，將 file_path 作為 data 傳送
        response.raise_for_status()  # 如果回覆狀態碼不是 200，就拋出異常
        convert_file_path = response.text # 回傳回覆的文字內容

        if file_path != convert_file_path:
            os.remove(file_path)

        return convert_file_path 
    except requests.exceptions.RequestException as e:
        print(f"Error sending file to converter: {e}") # 打印錯誤訊息
        return None # 發生錯誤時回傳 None
