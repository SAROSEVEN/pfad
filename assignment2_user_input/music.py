import streamlit as st
import io
from midiutil import MIDIFile
import pretty_midi
import base64

# Define note to letter mapping
note_to_letter = {
    'C': 'A', 'D': 'B', 'E': 'C', 'F': 'D', 'G': 'E', 'A': 'F', 'B': 'G'
}

# Define scales (simplified version, using only major scales)
scales = {
    'C Major': 0, 'G Major': 7, 'D Major': 2, 'A Major': 9, 'E Major': 4,
    'B Major': 11, 'F Major': 5, 'Bb Major': 10, 'Eb Major': 3, 'Ab Major': 8,
    'Db Major': 1, 'Gb Major': 6, 'Cb Major': 11
}

def letter_to_midi_note(letter, scale):
    base_notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    note = next((n for n, l in note_to_letter.items() if l == letter.upper()), None)
    if note:
        return 60 + base_notes.index(note) + scale  # 60 is middle C
    return None

def create_midi(letters, scale):
    midi = MIDIFile(1)
    midi.addTempo(0, 0, 120)

    for i, letter in enumerate(letters):
        note = letter_to_midi_note(letter, scale)
        if note:
            midi.addNote(0, 0, note, i, 1, 100)

    midi_data = io.BytesIO()
    midi.writeFile(midi_data)
    return midi_data.getvalue()

def play_midi(midi_data):
    midi = pretty_midi.PrettyMIDI(io.BytesIO(midi_data))
    audio_data = midi.synthesize()
    return audio_data

st.title("Music Letter Converter")

# Select scale
selected_scale = st.selectbox("Select Scale", list(scales.keys()))

# Input letters
letters = st.text_input("Enter letters (A-G)").upper()

if st.button("Generate Music"):
    if letters:
        midi_data = create_midi(letters, scales[selected_scale])
        audio_data = play_midi(midi_data)

        # Create download link
        b64_midi = base64.b64encode(midi_data).decode()
        href_midi = f'<a href="data:audio/midi;base64,{b64_midi}" download="music.mid">Download MIDI File</a>'
        st.markdown(href_midi, unsafe_allow_html=True)

        # Create audio player
        st.audio(audio_data, format='audio/wav', sample_rate=44100)
    else:
        st.warning("Please enter letters!")