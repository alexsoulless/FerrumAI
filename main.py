from fastapi import FastAPI, UploadFile, File, HTTPException
import aiofiles
import os
from pathlib import Path
import uuid

app = FastAPI()

UPLOAD_DIR = Path("./audios")


@app.post("/text")
async def text_req(str):
    pass


@app.post("/audio")
async def upload_audio(file: UploadFile = File(...)):
    UPLOAD_DIR.mkdir(exist_ok=True)

    if not file.filename is None:
        _, file_ext = os.path.splitext(file.filename)
    else:
        raise HTTPException(status_code=400, detail="bad file")
    safe_filename = f"{uuid.uuid4()}{file_ext}"

    file_path = UPLOAD_DIR / safe_filename

    async with aiofiles.open(file_path, "wb") as f:
        await f.write(await file.read())

    return {"path": str(file_path)}
