import streamlit as st

# ---------------------------
# BASIC APP SETTINGS
# ---------------------------
st.set_page_config(
    page_title="Focus Sprint Planner",
    page_icon="✅",
    layout="wide",
)

# ---------------------------
# ACCESS CONTROL
# ---------------------------

APP_PASSWORD = "rose-47-dollar"  # <-- CHANGE THIS before sharing

# We use session_state so user doesn't have to re-enter on every rerun
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login_screen():
    st.title("Private Access")
    st.write("This tool is only available to paying members.")

    pw_input = st.text_input("Enter your access code:", type="password")

    # nice touch: let user press Enter instead of button
    unlock_clicked = st.button("Unlock")

    if unlock_clicked:
        if pw_input == APP_PASSWORD:
            st.session_state.authenticated = True
            st.success("Access granted.")
        else:
            st.error("Invalid code. Please check the email you received after purchase.")

    # If not authenticated yet, stop the app here
    if not st.session_state.authenticated:
        st.stop()

# show login if not logged in yet
login_screen()


# ---------------------------
# YOUR REAL APP STARTS HERE
# ---------------------------

st.title("Focus Sprint Planner")
st.caption("Plan your next 25-minute push and get unstuck fast.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("What are you stuck on?")
    task = st.text_area(
        "Describe the task you're avoiding / overthinking",
        placeholder="Ex: Send client pricing update...\nEx: Clean inbox to <20 emails...",
        height=120
    )

    st.subheader("Why does it matter?")
    reason = st.text_area(
        "Write the consequence of NOT doing it",
        placeholder="Ex: If I don't do this today, I miss the approval window and delay the project...",
        height=100
    )

with col2:
    st.subheader("Your 25-minute sprint plan")
    step1 = st.text_input("First micro-step (0-5 mins):", placeholder="Open email draft + paste template")
    step2 = st.text_input("Second micro-step (5-15 mins):", placeholder="Write rough bullet points, not perfect")
    step3 = st.text_input("Final push (15-25 mins):", placeholder="Polish, send, close tab")

    st.subheader("Accountability mode")
    intensity = st.select_slider(
        "How serious are we?",
        options=["Chill", "Focused", "No excuses"],
        value="Focused"
    )

st.divider()

st.subheader("Your commitment")
colA, colB, colC = st.columns(3)

with colA:
    done_in = st.number_input("I will work for (minutes):", min_value=5, max_value=60, value=25, step=5)

with colB:
    start_in = st.selectbox("Starting:", ["Right now", "In 5 min", "In 10 min", "In 30 min"])

with colC:
    reward = st.text_input("Reward after you finish:", placeholder="Tea break, scroll IG guilt-free, etc.")

st.divider()

st.subheader("Summary for you")
st.write("Copy this into Notes / send it to yourself:")

summary = f"""
TASK: {task or '[not filled]'}
WHY IT MATTERS: {reason or '[not filled]'}

SPRINT PLAN:
1. {step1 or '[not filled]'}
2. {step2 or '[not filled]'}
3. {step3 or '[not filled]'}

MODE: {intensity}
TIME BLOCK: {done_in} min
STARTING: {start_in}
REWARD: {reward or '[not filled]'}
"""

st.code(summary.strip())

st.success("You’re locked in. Go do the first 5 minutes.")
