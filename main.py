import os
import time
import json
import soundfile as sf
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from kokoro_onnx import Kokoro
from subtitle_aligner import align_audio_to_text, generate_srt_file
import pathlib

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

API_KEY = "super-secret-key-123"

async def verify_token(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

MODELS_DIR = pathlib.Path("models")
OUTPUT_DIR = pathlib.Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

print("Loading Kokoro Engine...")
try:
    kokoro = Kokoro("kokoro-v0_19.onnx", "voices.bin")
    print("Kokoro loaded successfully")
except Exception as e:
    print(f"Error loading Kokoro: {e}")
    exit(1)

class TTSRequest(BaseModel):
    text: str
    voice: str = "af_bella"
    speed: float = 1.0
    lang: str = "en-us"

@app.post("/tts")
async def generate_speech(req: TTSRequest):
    timestamp = int(time.time() * 1000)
    audio_filename = f"audio_{timestamp}.wav"
    audio_path = OUTPUT_DIR / audio_filename
    
    try:
        samples, rate = kokoro.create(req.text, voice=req.voice, speed=req.speed)
        sf.write(audio_path, samples, rate)

        duration = len(samples) / rate
        word_timings = []
        srt_filename = f"audio_{timestamp}.srt"
        srt_path = OUTPUT_DIR / srt_filename
        try:
            word_timings, segments = align_audio_to_text(audio_path, lang=req.lang)
            generate_srt_file(segments, srt_path)
        except Exception:
            words = req.text.split()
            if words:
                weights = [len("".join(ch for ch in word if ch.isalnum())) or 1 for word in words]
                total_weight = sum(weights)
                current_time = 0.0
                for word, weight in zip(words, weights):
                    word_duration = duration * (weight / total_weight)
                    end_time = current_time + word_duration
                    word_timings.append({"word": word, "start": round(current_time, 2), "end": round(end_time, 2)})
                    current_time = end_time
            srt_filename = ""

        meta_path = OUTPUT_DIR / f"audio_{timestamp}.json"
        meta = {
            "id": timestamp,
            "text": req.text,
            "voice": req.voice,
            "duration": duration,
            "filename": audio_filename,
            "word_timings": word_timings,
            "srt_filename": srt_filename,
        }
        with open(meta_path, 'w') as f:
            json.dump(meta, f)

        response = {"audio_url": f"/audio/{audio_filename}", "filename": audio_filename, "word_timings": word_timings}
        if srt_filename:
            response["srt_url"] = f"/audio/{srt_filename}"
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/audio/{filename}")
async def get_audio(filename: str):
    return FileResponse(OUTPUT_DIR / filename)

@app.get("/archive")
async def get_archive():
    files = list(OUTPUT_DIR.glob("*.json"))
    return [json.load(open(f)) for f in sorted(files, reverse=True)]

if __name__ == "__main__":
    print("Starting server...")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
