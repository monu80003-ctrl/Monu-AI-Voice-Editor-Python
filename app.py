import os, uuid, shutil
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException

DATA = Path(os.getenv("DATA_DIR", "./data"))
for name in ("uploads", "profiles", "outputs"): (DATA/name).mkdir(parents=True, exist_ok=True)
app = FastAPI(title="Monu AI Voice Editor API", version="0.1.0")

@app.get("/health")
def health():
    return {"ok": True, "voice_model_ready": False}

@app.post("/v1/voice-profiles")
async def profile(audio: UploadFile = File(...), consent: str = Form(...)):
    if consent.lower() != "true": raise HTTPException(400, "Voice-owner consent required")
    ext = Path(audio.filename or "sample.wav").suffix.lower()
    if ext not in {".wav", ".mp3", ".m4a", ".flac"}: raise HTTPException(400, "Unsupported audio")
    pid = str(uuid.uuid4())
    with (DATA/"profiles"/(pid+ext)).open("wb") as f: shutil.copyfileobj(audio.file, f)
    # TODO: enqueue GPU RVC training/preprocessing; sample upload alone is not cloning.
    return {"profile_id": pid, "status": "uploaded_model_not_trained"}

@app.post("/v1/conversions")
async def conversion(video: UploadFile = File(...), profile_id: str = Form(...),
                     mode: str = Form("voice_conversion"),
                     preserve_timing: str = Form("true"), consent: str = Form(...)):
    if consent.lower() != "true": raise HTTPException(400, "Voice-owner consent required")
    ext = Path(video.filename or "video.mp4").suffix.lower()
    if ext not in {".mp4", ".mov", ".mkv"}: raise HTTPException(400, "Unsupported video")
    jid = str(uuid.uuid4())
    with (DATA/"uploads"/(jid+ext)).open("wb") as f: shutil.copyfileobj(video.file, f)
    # TODO: job queue -> FFmpeg extract -> RVC inference -> FFmpeg mux -> MP4 result.
    return {"job_id": jid, "status": "queued_model_not_connected"}

@app.get("/v1/jobs/{job_id}")
def job(job_id: str):
    return {"job_id": job_id, "status": "model_worker_not_connected"}
