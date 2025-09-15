import os
import shutil
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.pipeline import transcribe_audio, analyze_transcripts

app = FastAPI(title="Voice Detective-Truth Whisper")

# Enable CORS (frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "Voice Detective API is running 🚀"}

@app.post("/upload-audio")
async def upload_audio(files: list[UploadFile] = File(...)):
    """
    Upload one or more audio files and transcribe with Whisper.
    """
    transcripts = []
    for file in files:
        try:
            file_id = str(uuid.uuid4())
            save_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")

            with open(save_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            transcript = transcribe_audio(save_path)
            transcripts.append({"filename": file.filename, "transcript": transcript})

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing {file.filename}: {str(e)}")

    return {"status": "success", "transcripts": transcripts}

@app.post("/analyze")
async def analyze(data: dict):
    """
    Analyze transcripts with Groq LLM and return a Truth Report.
    """
    transcripts = data.get("transcripts")
    if not transcripts:
        raise HTTPException(status_code=400, detail="No transcripts provided")

    try:
        analysis = analyze_transcripts(transcripts)
        return JSONResponse(content={"analysis": analysis})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
