import re
from datetime import timedelta
from pathlib import Path
from faster_whisper import WhisperModel
import srt

MODEL_NAME = "small"
MODEL = WhisperModel(MODEL_NAME, device="cpu", compute_type="int8")

WORD_RE = re.compile(r"[\w']+|[\u00C0-\u017F\w]+")


def _srt_timestamp(seconds: float) -> timedelta:
    return timedelta(seconds=seconds)


def transcribe_audio_with_timestamps(audio_path: Path, lang: str = "en"):
    language = lang.split("-")[0] if lang else None
    multilingual = language != "en"
    segments, info = MODEL.transcribe(
        str(audio_path),
        language=language,
        task="transcribe",
        word_timestamps=True,
        multilingual=multilingual,
        beam_size=5,
        log_progress=False,
    )
    return list(segments)


def extract_word_timings(segments):
    timings = []
    for segment in segments:
        if hasattr(segment, "words"):
            for word in segment.words:
                timings.append({
                    "word": word.word.strip(),
                    "start": round(word.start, 2),
                    "end": round(word.end, 2),
                })
        else:
            text = getattr(segment, "text", "").strip()
            if text:
                words = WORD_RE.findall(text)
                if words:
                    duration = segment.end - segment.start
                    weight = sum(max(1, len(w)) for w in words)
                    current_time = segment.start
                    for w in words:
                        wdur = duration * max(1, len(w)) / weight
                        timings.append({
                            "word": w,
                            "start": round(current_time, 2),
                            "end": round(current_time + wdur, 2),
                        })
                        current_time += wdur
    return timings


def generate_srt_file(segments, srt_path: Path):
    subtitles = []
    for index, segment in enumerate(segments, start=1):
        content = getattr(segment, "text", "").strip()
        if not content:
            continue
        subtitle = srt.Subtitle(
            index=index,
            start=_srt_timestamp(segment.start),
            end=_srt_timestamp(segment.end),
            content=content,
        )
        subtitles.append(subtitle)
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt.compose(subtitles))


def align_audio_to_text(audio_path: Path, lang: str = "en"):
    segments = transcribe_audio_with_timestamps(audio_path, lang=lang)
    word_timings = extract_word_timings(segments)
    return word_timings, segments
