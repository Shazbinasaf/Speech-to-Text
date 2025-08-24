import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
import tempfile, os
from st_audiorec import st_audiorec   # mic recording component

st.set_page_config(page_title="Speech to Text", page_icon="🎙️")
st.title("🎙️ Speech-to-Text Transcription")

# Language selector
lang = st.text_input("Language code (e.g., en-IN, en-US, hi-IN)", value="en-IN")

# --- OPTION 1: File Upload ---
st.subheader("📂 Upload Audio File")
file = st.file_uploader("Upload audio", type=["wav","mp3","flac","aiff"])

if file is not None:
    with tempfile.TemporaryDirectory() as td:
        in_path = os.path.join(td, file.name)
        with open(in_path, "wb") as f:
            f.write(file.getbuffer())

        wav_path = in_path
        if not in_path.lower().endswith(".wav"):
            wav_path = os.path.join(td, "converted.wav")
            AudioSegment.from_file(in_path).export(wav_path, format="wav")

        r = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio = r.record(source)

        try:
            text = r.recognize_google(audio, language=lang)
            st.success("✅ Transcription complete!")
            st.text_area("Result", value=text, height=200)
        except sr.UnknownValueError:
            st.warning("❔ Could not understand the audio.")
        except sr.RequestError as e:
            st.error(f"⚠️ API request error: {e}")

# --- OPTION 2: Live Mic Recording ---
st.subheader("🎤 Record from Microphone")
wav_audio_data = st_audiorec()   # returns raw audio data in WAV format

if wav_audio_data is not None:
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        f.write(wav_audio_data)
        temp_wav = f.name

    r = sr.Recognizer()
    with sr.AudioFile(temp_wav) as source:
        audio = r.record(source)

    try:
        text = r.recognize_google(audio, language=lang)
        st.success("✅ Live transcription complete!")
        st.text_area("Result (Live)", value=text, height=200)
    except sr.UnknownValueError:
        st.warning("❔ Could not understand the recording.")
    except sr.RequestError as e:
        st.error(f"⚠️ API request error: {e}")
