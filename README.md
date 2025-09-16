# 🕵️ Voice Detective – Truth Whisper  
**Innov8 3.0 Hackathon – IIT Delhi (ARIES & Eightfold AI)**  

An AI Detective that listens to voices, transcribes them, detects contradictions, and weaves together the most likely truth.

---

## ⚡ Problem Statement  
From the *Whispering Shadows Mystery*:  
- Shadows give contradictory testimonies across multiple sessions.  
- Audio quality may be noisy, emotional, whispered, or exaggerated.  

### Our AI Detective must:  
✅ Transcribe audio accurately despite noise.  
✅ Analyze contradictions across sessions.  
✅ Extract the most likely truth in structured JSON.  
✅ Provide both raw transcripts (`.txt`) and truth reports (`.json`).  

---

## 🛠️ Tech Stack  
- **Frontend** → HTML, CSS, JavaScript  
- **Backend** → FastAPI (Python)  
- **AI Models** →  
  - OpenAI Whisper → Audio transcription  
  - Groq LLM → Truth extraction & contradiction detection  

---

## 🚀 Features  
- 🎤 **Audio Upload** → Supports multiple `.mp3` / `.wav` files  
- 📝 **Whisper Transcription** → Converts noisy speech to text  
- 🔍 **Groq Analysis** → Detects contradictions & exaggerations  
- 📊 **Truth Score (0–1)** → Rates credibility of testimony  
- 🎨 **Color-Coded Summaries**:  
  - 🟥 Low truth (<50%)  
  - 🟧 Medium (50–75%)  
  - 🟩 High (>75%)  
- 📂 **JSON Output** → Hackathon Submission Scroll format  

---

## 📂 Project Structure  
























