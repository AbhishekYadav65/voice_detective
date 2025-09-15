import os
import whisper
from groq import Groq
from dotenv import load_dotenv
import json

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


def analyze_transcripts(transcripts: list[dict]) -> dict:
    """
    Send transcripts to Groq LLM for analysis.
    Always return a JSON array of objects (one per transcript).
    """
    joined_texts = "\n\n".join(
        [f"=== {t['filename']} ===\n{t['transcript']}" for t in transcripts]
    )

    prompt = f"""
You are Voice Detective 🕵️‍♂️.
Analyze the transcripts below and output ONLY valid JSON as a single array of objects.

Example format:

[
  {{
    "shadow_id": "string",
    "revealed_truth": {{
      "programming_experience": "string",
      "programming_language": "string",
      "skill_mastery": "string",
      "leadership_claims": "string",
      "team_experience": "string",
      "skills and other keywords": ["string", ...]
    }},
    "deception_patterns": [
      {{
        "lie_type": "string",
        "contradictory_claims": ["string", ...]
      }}
    ],
    "truth_score": 0.0-1.0
  }},
  ...
]

⚠️ Rules:
- Return ONLY the JSON array (no markdown, no ``` fences, no commentary).
- Each transcript must map to exactly one object in the array.
- "shadow_id" = filename without extension.
- If info missing, use "unknown" or [].
- "truth_score" is a float between 0 and 1.
- Do not output multiple root-level objects. Always wrap inside a single JSON array.

Transcripts:
{joined_texts}
"""

    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        raw_output = response.choices[0].message.content.strip()

        # 🔧 Sanitize accidental code fences
        if raw_output.startswith("```"):
            raw_output = raw_output.strip("`")
            raw_output = raw_output.replace("json", "", 1).strip()

        # Parse JSON safely
        try:
            result = json.loads(raw_output)
        except json.JSONDecodeError:
            result = {"error": "Invalid JSON returned", "raw_output": raw_output}

        return result

    except Exception as e:
        return {"error": "Groq analysis failed", "details": str(e)}
