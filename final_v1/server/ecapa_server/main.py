import os 
import shutil
import sys
import uuid
import traceback

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from agent import verify

app = FastAPI(
    title="ECAPA-TDNN Speaker Verification API",
    description="An API for speaker verification using the ECAPA-TDNN model.",
    version="1.0.0",
)

def temp_save_uploaded_file(upload_file: UploadFile, save_dir: str) -> str:
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, f"{uuid.uuid4()}.wav")
    with open(file_path, "wb") as f:
        shutil.copyfileobj(upload_file.file, f)
    return file_path

@app.post("/verify", response_class=JSONResponse)
async def verify_speakers(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    raw_paths = []
    optimised_paths = []
    try:
        path1 = temp_save_uploaded_file(file1, "temp")
        path2 = temp_save_uploaded_file(file2, "temp")
        raw_paths = [path1, path2]
        return verify(path1, path2)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Run with auto-reload during development
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True     # watches for file changes
    )