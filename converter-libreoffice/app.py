from fastapi import FastAPI, UploadFile, File, Form, Request, BackgroundTasks, Response
from typing import Optional

from lib.convert_file import convert_file

app = FastAPI()

# =======================================

@app.post("/")
async def index(
        file_path: Optional[str] = Form(None)
    ):

    return convert_file(file_path)
