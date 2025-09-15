import os
import whisper
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Whisper model
whisper_model = whisper.load_model("base")

# Groq client
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("❌ GROQ_API_KEY not found in .env")
client = Groq(api_key=groq_api_key)

def transcribe_audio(file_path: str) -> str:
    """Transcribe audio using Whisper"""
    try:
        result = whisper_model.transcribe(file_path)
        return result["text"].strip()
    except Exception as e:
        return f"Transcription failed: {str(e)}"

def analyze_transcripts(transcripts: list[dict]) -> str:
    """Send transcripts to Groq LLM for analysis"""
    joined_texts = "\n\n".join(
        [f"{t['filename']}: {t['transcript']}" for t in transcripts]
    )

    prompt = f"""
You are Voice Detective 🕵️‍♂️.
Analyze the following transcripts and extract:
- Programming Experience
- Programming Language
- Skill Mastery
- Leadership Claims
- Team Experience
- Skills & Keywords
- Deception Patterns

Transcripts:
{joined_texts}
"""

    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Groq analysis failed: {str(e)}"
