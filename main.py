from fastapi import FastAPI, UploadFile, File, HTTPException
import aiofiles
import os
from pathlib import Path
import uuid
from stt import get_text_from_audio
from ai import get_ai_response

app = FastAPI()

UPLOAD_DIR = Path("./audios")


@app.post("/text")
async def text_req(req : str):
    response = get_ai_response(req)
    return response


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

    request = get_text_from_audio(file.filename)

    return 
