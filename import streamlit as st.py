import streamlit as st
import streamlit.components.v1 as components

# ---------------------------- CONFIG ------------------------------- #
PINK = "#e2979c"
BLUE = "#18abde"

WORK_SEC = 60         # Stretch duration
SHORT_BREAK_SEC = 10  # Prepare duration

st.set_page_config(page_title="Yoga Timer", page_icon="🧘", layout="centered")
st.title("🧘 Yoga Timer")
st.caption("Auto countdown timer with Prepare and Stretch phases + sounds.")

# ---------------------------- SESSION STATE ------------------------ #
if "running" not in st.session_state:
    st.session_state.running = False

# ---------------------------- BUTTONS ------------------------------ #
col1, col2 = st.columns(2)
start_btn = col1.button("Start 🕒")
stop_btn = col2.button("Stop 🔴")

# ---------------------------- TIMER HTML + JS ---------------------- #
# We embed a full HTML/JS timer to run in the browser
# JS handles countdown and plays sounds automatically

if start_btn:
    st.session_state.running = True

if stop_btn:
    st.session_state.running = False

if st.session_state.running:
    timer_html = f"""
    <div style="text-align:center;">
        <h2 id="phase" style="color:{PINK};">Prepare</h2>
        <h1 id="timer" style="color:{PINK};">00:00</h1>
        <audio id="beep_prepare" src="beep2.mp3"></audio>
        <audio id="beep_stretch" src="beep1.mp3"></audio>
    </div>
    <script>
        let work_sec = {WORK_SEC};
        let short_break_sec = {SHORT_BREAK_SEC};
        let seconds = short_break_sec;
        let phase = "Prepare";
        const timer_display = document.getElementById("timer");
        const phase_display = document.getElementById("phase");
        const beep_prepare = document.getElementById("beep_prepare");
        const beep_stretch = document.getElementById("beep_stretch");

        function updateTimer() {{
            let minutes = Math.floor(seconds / 60);
            let secs = seconds % 60;
            timer_display.innerText = ("0" + minutes).slice(-2) + ":" + ("0" + secs).slice(-2);

            if(seconds <= 0){{
                if(phase === "Prepare"){{
                    phase = "Stretch";
                    seconds = work_sec;
                    phase_display.innerText = phase;
                    phase_display.style.color = "{BLUE}";
                    beep_stretch.play();
                }} else {{
                    phase = "Prepare";
                    seconds = short_break_sec;
                    phase_display.innerText = phase;
                    phase_display.style.color = "{PINK}";
                    beep_prepare.play();
                }}
            }} else {{
                seconds -= 1;
            }}
        }}

        // Start countdown every 1 second
        setInterval(updateTimer, 1000);
    </script>
    """
    components.html(timer_html, height=200)
else:
    st.write("Click Start to begin the yoga timer.")
