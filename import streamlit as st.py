import streamlit as st
import time
import streamlit.components.v1 as components

# ---------------------------- CONFIG ------------------------------- #
PINK = "#e2979c"
BLUE = "#18abde"
WHITE = "#ffffff"

WORK_SEC = 60         # Stretch duration
SHORT_BREAK_SEC = 10  # Prepare duration

# ---------------------------- APP SETUP ---------------------------- #
st.set_page_config(page_title="Yoga Timer", page_icon="🧘", layout="centered")
st.title("🧘 Yoga Timer")
st.caption("Alternate between 'Prepare' and 'Stretch' phases. Click 'Start' to begin.")

# ---------------------------- SESSION STATE ------------------------ #
if "running" not in st.session_state:
    st.session_state.running = False
    st.session_state.phase = "Prepare"
    st.session_state.seconds_remaining = SHORT_BREAK_SEC
    st.session_state.reps = 0

# Placeholders for dynamic updates
header_placeholder = st.empty()
timer_placeholder = st.empty()

# ---------------------------- SOUND PLAYER ------------------------ #
# Function to play sound via HTML audio (must be triggered by user click)
def play_sound(file):
    components.html(f"""
        <audio autoplay>
            <source src="{file}" type="audio/mp3">
        </audio>
    """, height=0)

# ---------------------------- TIMER LOGIC -------------------------- #
def update_timer():
    # Display phase
    color = PINK if st.session_state.phase == "Prepare" else BLUE
    header_placeholder.markdown(f"<h2 style='color:{color}'>{st.session_state.phase}</h2>", unsafe_allow_html=True)

    # Display countdown
    minutes = st.session_state.seconds_remaining // 60
    seconds = st.session_state.seconds_remaining % 60
    timer_placeholder.markdown(f"<h1 style='color:{color};'>{minutes:02d}:{seconds:02d}</h1>", unsafe_allow_html=True)

    # Decrease seconds
    if st.session_state.seconds_remaining > 0:
        st.session_state.seconds_remaining -= 1
    else:
        # Phase finished: switch
        st.session_state.reps += 1
        if st.session_state.phase == "Prepare":
            st.session_state.phase = "Stretch"
            st.session_state.seconds_remaining = WORK_SEC
            play_sound("beep1.mp3")
        else:
            st.session_state.phase = "Prepare"
            st.session_state.seconds_remaining = SHORT_BREAK_SEC
            play_sound("beep2.mp3")

# ---------------------------- BUTTONS ------------------------------ #
col1, col2 = st.columns(2)
start_btn = col1.button("Start 🕒")
stop_btn = col2.button("Stop 🔴")

if start_btn:
    st.session_state.running = True
    # Play initial sound
    play_sound("beep1.mp3")

if stop_btn:
    st.session_state.running = False
    st.session_state.phase = "Prepare"
    st.session_state.seconds_remaining = SHORT_BREAK_SEC
    st.session_state.reps = 0
    header_placeholder.markdown("<h2>Timer Stopped 🧘‍♀️</h2>", unsafe_allow_html=True)
    timer_placeholder.markdown("<h1 style='color:#444;'>00:00</h1>", unsafe_allow_html=True)

# ---------------------------- RUN TIMER --------------------------- #
if st.session_state.running:
    # Use a "Next second" button to trigger each tick
    tick_btn = st.button("Next second ⏱️ (Click once per second)")
    if tick_btn:
        update_timer()
