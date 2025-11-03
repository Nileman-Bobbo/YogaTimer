import streamlit as st
import time

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
BLUE = "#18abde"
WHITE = "#ffffff"

WORK_SEC = 60       # Change to 60 for full minute
HALF_WORK = WORK_SEC / 2
SHORT_BREAK_SEC = 10

# ---------------------------- SOUND FUNCTION ------------------------------- #
# Streamlit can't play real beeps, but we can play HTML audio elements
def play_sound(frequency="start"):
    if frequency == "start":
        sound_url = "https://actions.google.com/sounds/v1/alarms/beep_short.ogg"
    elif frequency == "half":
        sound_url = "https://actions.google.com/sounds/v1/alarms/beep_short.ogg"
    else:  # end
        sound_url = "https://actions.google.com/sounds/v1/alarms/beep_short.ogg"

    st.markdown(
        f"""
        <audio autoplay>
            <source src="{sound_url}" type="audio/ogg">
        </audio>
        """,
        unsafe_allow_html=True
    )

# ---------------------------- TIMER LOGIC ------------------------------- #
def yoga_timer():
    st.subheader("🕉️ Center yourself...")

    col1, col2 = st.columns(2)
    start = col1.button("Start")
    stop = col2.button("End")

    header_placeholder = st.empty()
    timer_placeholder = st.empty()

    if start:
        reps = 0
        running = True
        phase = "prepare"
        count = SHORT_BREAK_SEC
        header_placeholder.markdown(
            f"<h2 style='color:{PINK}'>Prepare</h2>", unsafe_allow_html=True
        )
        play_sound("start")

        while running:
            minutes = count // 60
            seconds = count % 60
            timer_placeholder.markdown(
                f"<h1 style='color:{BLUE};'>{int(minutes):02d}:{int(seconds):02d}</h1>",
                unsafe_allow_html=True,
            )
            time.sleep(1)
            count -= 1

            # Play half beep in the middle of stretch
            if phase == "stretch" and count == HALF_WORK:
                play_sound("half")

            # When timer hits zero, switch phases
            if count <= 0:
                reps += 1
                if phase == "prepare":
                    phase = "stretch"
                    header_placeholder.markdown(
                        f"<h2 style='color:{BLUE}'>Stretch</h2>", unsafe_allow_html=True
                    )
                    play_sound("start")
                    count = WORK_SEC
                else:
                    phase = "prepare"
                    header_placeholder.markdown(
                        f"<h2 style='color:{PINK}'>Prepare</h2>", unsafe_allow_html=True
                    )
                    play_sound("end")
                    count = SHORT_BREAK_SEC

            if stop:
                running = False
                header_placeholder.markdown(
                    "<h2>Session Ended 🧘‍♀️</h2>", unsafe_allow_html=True
                )
                timer_placeholder.markdown(
                    "<h1 style='color:#444;'>00:00</h1>", unsafe_allow_html=True
                )
                break

# ---------------------------- PAGE SETUP ------------------------------- #
st.set_page_config(page_title="Yoga Timer", page_icon="🧘‍♀️", layout="centered")
st.title("🧘‍♀️ Yoga Timer")
st.caption("Alternate between 'Prepare' and 'Stretch' phases with audio cues.")

yoga_timer()
