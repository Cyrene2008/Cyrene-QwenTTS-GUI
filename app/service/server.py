import sys
import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from pathlib import Path
import threading
import signal

# Add the project root to sys.path to allow importing app modules
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# DLL Directory fixing for Windows
if sys.platform == 'win32':
    # Add PATH entries to DLL search path for Python 3.8+
    for path in os.environ.get('PATH', '').split(os.pathsep):
        if os.path.isdir(path):
            try:
                os.add_dll_directory(path)
            except:
                pass

app = FastAPI()

# Placeholder for the backend instance
backend_instance = None

class LoadModelRequest(BaseModel):
    model_name: str

class GenerateRequest(BaseModel):
    text: str
    speaker: str
    language: Optional[str] = None

class GenerateDesignRequest(BaseModel):
    text: str
    instruct: str
    language: Optional[str] = None

class GenerateCloneRequest(BaseModel):
    text: str
    ref_audio: str
    ref_text: Optional[str] = None
    language: Optional[str] = None
    x_vector_only_mode: bool = False

@app.on_event("startup")
async def startup_event():
    # We will initialize the backend lazily or here
    # Importing here to avoid import errors if dependencies are missing during top-level scan
    # But this file runs IN the env, so it should be fine.
    global backend_instance
    from app.service.backend_impl import QwenTTSBackend
    backend_instance = QwenTTSBackend()

@app.post("/load_model")
def load_model(req: LoadModelRequest):
    try:
        backend_instance.load_model(req.model_name)
        return {"status": "success", "message": f"Model {req.model_name} loaded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/speakers")
def get_speakers():
    speakers = backend_instance.get_supported_speakers()
    return {"speakers": speakers if speakers else []}

@app.get("/device_info")
def get_device_info():
    return backend_instance.get_device_info()

@app.post("/generate")
def generate(req: GenerateRequest):
    try:
        path = backend_instance.generate_custom_voice(
            text=req.text,
            speaker=req.speaker,
            language=req.language
        )
        return {"status": "success", "path": str(path)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_design")
def generate_design(req: GenerateDesignRequest):
    try:
        path = backend_instance.generate_voice_design(
            text=req.text,
            instruct=req.instruct,
            language=req.language
        )
        return {"status": "success", "path": str(path)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_clone")
def generate_clone(req: GenerateCloneRequest):
    try:
        path = backend_instance.generate_voice_clone(
            text=req.text,
            ref_audio=req.ref_audio,
            ref_text=req.ref_text,
            language=req.language,
            x_vector_only_mode=req.x_vector_only_mode
        )
        return {"status": "success", "path": str(path)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/shutdown")
def shutdown():
    os.kill(os.getpid(), signal.SIGTERM)
    return {"status": "shutting down"}

if __name__ == "__main__":
    # Get port from args or default
    port = 7951
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    
    uvicorn.run(app, host="127.0.0.1", port=port)
