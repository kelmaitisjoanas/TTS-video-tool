# VisionVox: Real-Time Video Storyteller

VisionVox is a professional tool for creating synchronized video stories by performing image/video drops over a TTS-generated or pre-recorded audio script.

## Features
- **AI Voice Generation**: Integrated Gemini TTS for high-quality narration.
- **Local TTS Support**: Connect your own local TTS API.
- **Real-Time Performance**: Drag and drop visuals while audio plays to sync them to the timeline.
- **Cinematic Transitions**: Fade, Slide, Zoom, Blur, Rotate, Bounce, and Skew effects.
- **Bulk Import**: Upload your own audio files with JSON metadata for subtitles.
- **Video Export**: Record your performance and download it as a `.webm` file.

## Prerequisites
- [Node.js](https://nodejs.org/) (v18 or higher)
- [npm](https://www.npmjs.com/) (comes with Node.js)

## Installation

1. **Clone or Download the Project**
   Extract the project files to a folder on your computer.

2. **Install Dependencies**
   Open your terminal in the project directory and run:
   ```bash
   npm install
   ```

3. **Set Up Environment Variables**
   Create a `.env` file in the root directory (copy from `.env.example`):
   ```bash
   cp .env.example .env
   ```
   Add your `GEMINI_API_KEY` to the `.env` file. You can get one from [Google AI Studio](https://aistudio.google.com/).

## Running the App

1. **Start the Development Server**
   ```bash
   npm run dev
   ```

2. **Open in Browser**
   The app will be running at `http://localhost:3000`.

## Bulk Import Format
To import your own audio with subtitles, upload your audio files (`.mp3`, `.wav`) along with a `metadata.json` file structured like this:
```json
[
  { "filename": "story_part1.mp3", "text": "Once upon a time..." },
  { "filename": "story_part2.mp3", "text": "In a galaxy far, far away..." }
]
```

## Exporting Videos
Click the **"Finish & Export"** button. The app will play through your project and record the canvas. Once finished, a `.webm` file will be downloaded automatically.
