from fastapi import FastAPI, File, UploadFile, HTTPException, Form

import os
import uvicorn
from starlette.responses import JSONResponse

from lib.check_convert import check_convert
from lib.elements_to_markdown import elements_to_markdown

from lib.save_upload_file import save_upload_file

from typing import Optional
from lib.parse_json import parse_json
from lib.file_path_to_elements import file_path_to_elements

from lib.app_cors import app_cors

from lib.chunk_cache.cache_get import cache_get
from lib.chunk_cache.cache_set import cache_set

# 初始化 FastAPI
app = FastAPI()
app_cors(app)

@app.post("/")
async def process_md(
    file: UploadFile = File(...),
    chunk_config: Optional[str] = Form(None)
    ):

    file_ext, file_path = save_upload_file(file)
    original_file_path = file_path

    chunk_config = parse_json(chunk_config)
    chunk_config["ENABLE_CHUNK"] = False

    cache = cache_get(chunk_config, file_path)
    if cache is not None:
        os.remove(file_path)
        return JSONResponse(content=cache)


    file_path = check_convert(file_path)
    if file_path is False:
        return JSONResponse(content="")
    
    import json # 20240321-104500

    if file_ext == '.plist':
        # 開啟 file_path 檔案，然後回傳檔案內容
        with open(file_path, "rb") as f:
            content = f.read().decode('utf-8') # 20240321-104500
            return JSONResponse(content=content) # 20240321-104500

    file_ext = os.path.splitext(file_path)[1].lower()  # 取得副檔名
    if file_ext in ['.csv', '.xml', '.md', '.txt']:
        with open(file_path, "rb") as f: # 20240321-104500
            content = f.read().decode('utf-8') # 20240321-104500
            return JSONResponse(content=content) # 20240321-104500
    if file_ext == '.json': # 20240321-104500
        with open(file_path, "r") as f: # 20240321-104500
            try: # 20240321-104500
                content = f.read().decode('utf-8') # 20240321-104500
                return JSONResponse(content=content) # 20240321-104500
            except json.JSONDecodeError as e: # 20240321-104500
                raise HTTPException(status_code=400, detail=f"Invalid JSON file: {e}") # 20240321-104500

    # =================================================================

    # https://docs.unstructured.io/open-source/core-functionality/partitioning#partition
    # file_ext, file_path = save_upload_file(file)

    print('Unstructure receive file: ', file_path, file_ext)

    elements = file_path_to_elements(file_ext, file_path, chunk_config)
    markdown_result, metadatas = elements_to_markdown(file_ext, elements, chunk_config)

    # print('metadatas', metadatas)

    # 返回 JSON 資料
    # output = {"status": "success", "documents": markdown_result, "metadatas": metadatas}
    output = "\n\n".join(markdown_result)
    cache_set(chunk_config, original_file_path, output)

    os.remove(file_path)
    if original_file_path != file_path:
        os.remove(original_file_path)

    return JSONResponse(content=output)

@app.post("/process")
async def process_file(
    file: UploadFile = File(...),
    # file_path: str = Form(None),
    chunk_config: Optional[str] = Form(None),
    ):

    file_ext, file_path = save_upload_file(file)

    chunk_config = parse_json(chunk_config)

    cache = cache_get(chunk_config, file_path)
    if cache is not None:
        return JSONResponse(content=cache)


    
    # =================================================================

    # https://docs.unstructured.io/open-source/core-functionality/partitioning#partition
    # file_ext, file_path = save_upload_file(file)

    print('Unstructure receive file: ', file_path, file_ext)

    elements = file_path_to_elements(file_ext, file_path, chunk_config)
    markdown_result, metadatas = elements_to_markdown(file_ext, elements, chunk_config)

    # print('metadatas', metadatas)

    # 返回 JSON 資料
    output = {"status": "success", "documents": markdown_result, "metadatas": metadatas}
    cache_set(chunk_config, file_path, output)

    return JSONResponse(content=output)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)),)
