import streamlit as st
import time
import streamlit.components.v1 as components

# ---------------------------- CONFIG ------------------------------- #
PINK = "#e2979c"
BLUE = "#18abde"
WHITE = "#ffffff"
WORK_SEC = 60
HALF_WORK = WORK_SEC / 2
SHORT_BREAK_SEC = 10

st.set_page_config(page_title="Yoga Timer", page_icon="🧘", layout="centered")

# ---------------------------- SOUND PLAYER -------------------------- #
# JavaScript for sound playback
def play_sound_js(file):
    components.html(f"""
        <audio id="sound" src="{file}" autoplay></audio>
    """, height=0)

# ---------------------------- TIMER LOGIC ---------------------------- #
def countdown(seconds, phase_name, color, sound_file):
    st.markdown(f"<h2 style='color:{color}'>{phase_name}</h2>", unsafe_allow_html=True)
    placeholder = st.empty()

    # Start sound (user click will already allow playback)
    play_sound_js(sound_file)

    for remaining in range(seconds, -1, -1):
        placeholder.markdown(f"<h1 style='color:{color};'>{remaining:02d}</h1>", unsafe_allow_html=True)
        time.sleep(1)
        if remaining == HALF_WORK:
            play_sound_js("beep2.mp3")

# ---------------------------- APP UI ------------------------------- #
st.title("🧘 Yoga Timer")
st.write("Alternate between **Stretch** and **Prepare** phases.")

if "running" not in st.session_state:
    st.session_state.running = False
    st.session_state.reps = 0

start = st.button("Start Timer 🕒")
stop = st.button("Stop 🔴")

if start:
    st.session_state.running = True
    st.session_state.reps = 0

if stop:
    st.session_state.running = False
    st.session_state.reps = 0
    st.write("Timer stopped.")

if st.session_state.running:
    while st.session_state.running:
        st.session_state.reps += 1
        if st.session_state.reps % 2 == 0:
            countdown(WORK_SEC, "Stretch", BLUE, "beep1.mp3")
        else:
            countdown(SHORT_BREAK_SEC, "Prepare", PINK, "beep3.mp3")
