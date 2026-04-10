# Local TTS API with Vision Composer

A complete local text-to-speech solution using Kokoro ONNX models with professional subtitle alignment and a React-based audio/video composition app.

## Features

- **Local TTS Engine**: FastAPI server using Kokoro ONNX models (no cloud dependencies)
- **Professional Subtitles**: Word-level timing using faster-whisper forced alignment
- **SRT Export**: Automatic subtitle file generation
- **Vision Composer**: React/Vite app for drag-and-drop audio/video composition
- **Multiple Voices**: Support for various Kokoro voices (American, British, etc.)
- **Real-time Playback**: Synchronized subtitle display during audio playback

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Vision App    │    │   FastAPI TTS    │    │  faster-whisper  │
│   (React/Vite)  │◄──►│     Server      │◄──►│   Alignment      │
│                 │    │                 │    │                 │
│ • Audio import  │    │ • /tts endpoint │    │ • Word timings   │
│ • Timeline      │    │ • WAV output    │    │ • SRT export     │
│ • Subtitle sync │    │ • JSON metadata │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Kokoro ONNX models (included)

### Backend Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Start TTS server
python main.py
```

### Frontend Setup
```bash
cd vision
npm install
npm run build
npm run preview
```

## API Usage

### Generate Speech
```bash
curl -X POST http://localhost:8002/tts \
  -H "x-api-key: super-secret-key-123" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello world",
    "voice": "af_bella",
    "lang": "en-us"
  }'
```

Response includes:
- `audio_url`: Path to generated WAV file
- `word_timings`: Array of word timestamps
- `srt_url`: Path to SRT subtitle file (if alignment succeeds)

### Get Archive
```bash
curl http://localhost:8002/archive
```

Returns list of all generated audio metadata.

## Voices

Available voices (defined in `voices.json`):
- `af_bella` - American Female
- `am_adam` - American Male
- `bf_alice` - British Female
- `bm_george` - British Male
- `Kore` - Korean


## Development

### Project Structure
```
tts-api/
├── main.py                 # FastAPI TTS server
├── subtitle_aligner.py     # Whisper alignment helper
├── voices.json            # Voice configurations
├── requirements.txt       # Python dependencies
├── vision/                # React frontend
│   ├── src/
│   │   ├── App.tsx       # Main composition app
│   │   ├── types.ts      # TypeScript types
│   │   └── ...
│   ├── package.json
│   └── vite.config.ts
├── outputs/               # Generated audio/metadata
└── models/                # ONNX models (not included)
```

### Adding New Voices
1. Update `voices.json` with new voice configuration
2. Ensure corresponding ONNX model files are available
3. Restart the TTS server

## License

This project is provided as-is for educational and research purposes.
