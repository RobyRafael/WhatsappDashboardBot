from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import os
from utils.database import save_media_metadata

router = APIRouter()

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '../../../media/uploads')

@router.post("/upload", response_model=dict)
async def upload_media(files: List[UploadFile] = File(...)):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    media_files = []
    for file in files:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())
        media_files.append(file.filename)
        save_media_metadata(file.filename, file_location)

    return {"filenames": media_files}

@router.get("/media/{filename}", response_model=dict)
async def get_media(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return {"filename": filename, "file_path": file_path}