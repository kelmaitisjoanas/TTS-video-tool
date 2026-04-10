from kokoro_onnx import Kokoro
import soundfile as sf
import time

# Užkrauname modelį
kokoro = Kokoro("kokoro-v0_19.onnx", "voices.bin")

text = "I remember the day the world changed. The rain was cold, but the silence... the silence was colder. I stood there, waiting for a sign, any sign, that we weren't alone in this vast, empty darkness. And then, I heard it. A whisper. A single note of hope in a symphony of despair. We are still here. We are still fighting."

# Generuojame audio su vyrišku balsu 'am_michael'
print("Generuojamas emocingas audio su 'am_michael' balsu...")
gen_start = time.time()
samples, sample_rate = kokoro.create(text, voice="am_michael", speed=1.0, lang="en-us")
print(f"Audio sugeneruotas per {time.time() - gen_start:.2f}s")

# Išsaugome į failą
sf.write("kokoro_emotional.wav", samples, sample_rate)
print("Failas išsaugotas: kokoro_emotional.wav")
