# Monu AI Voice Editor — Python Pro Starter

यह शुरुआती scaffold है, पूरा AI cloning engine नहीं।

## Stack
- Android UI: Python + Kivy
- Cloud API: FastAPI
- Main voice conversion: RVC (GPU worker अभी जोड़ना बाकी)
- Media processing: FFmpeg (pipeline अभी जोड़ना बाकी)
- Android build: Buildozer + GitHub Actions

## अभी उपलब्ध
- Kivy UI
- API URL save
- audio/video file selection
- cloud API upload endpoints
- GitHub Actions APK build workflow

## अभी बाकी
- वास्तविक RVC training/inference worker
- user login, secure profile storage, job queue
- FFmpeg extraction/muxing और MP4 download
- timeline, trim, split, overlays, subtitles
- Android device testing और signed release

## Cloud API चलाना
    cd server
    pip install -r requirements.txt
    uvicorn app:app --host 0.0.0.0 --port 8000

API अभी uploads लेती है; model worker न होने के कारण वास्तविक conversion नहीं करती।
