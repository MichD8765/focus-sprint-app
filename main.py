import streamlit as st

st.set_page_config(
    page_title="Focus Sprint Planner",
    page_icon="✅",
    layout="wide",
)

# ---------------------------------
# 1. LICENSE KEYS YOU'VE ISSUED
# ---------------------------------
# Format:
# "CODE": {"active": True, "note": "who this was sold to"}
#
# - active = False means you've revoked it
# - note is optional, it's just for you to remember who bought it
#
VALID_KEYS = {
    "GX7R-PL9F-23KQ": {"active": True,  "note": "Buyer #1 from Gumroad"},
    "M11A-B82C-Z5Q9": {"active": True,  "note": "VIP early supporter"},
    "TEST-TEST-TEST": {"active": False, "note": "Refunded"},
}


# ---------------------------------
# 2. AUTH STATE
# ---------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "license_code" not in st.session_state:
    st.session_state.license_code = None


# ---------------------------------
# 3. LOGIN / LICENSE CHECK
# ---------------------------------
def login_screen():
    st.title("Private Access")
    st.write("Enter your personal access code to continue.")

    code_input = st.text_input(
        "Your access code (check your purchase email):",
        placeholder="e.g. GX7R-PL9F-23KQ",
    )

    unlock_clicked = st.button("Unlock")

    if unlock_clicked:
        code_input_clean = code_input.strip()

        # Check if code exists
        if code_input_clean in VALID_KEYS:
            license_info = VALID_KEYS[code_input_clean]

            if license_info.get("active", False):
                # ✅ Access granted
                st.session_state.authenticated = True
                st.session_state.license_code = code_input_clean
                st.success("Access granted. Welcome!")
            else:
                # Code found but disabled
                st.error("This code is no longer active. Please contact support.")
        else:
            # Code not found at all
            st.error("Invalid code. Please check the email you received after purchase.")

    # If still not authenticated, stop the app here
    if not st.session_state.authenticated:
        st.stop()


login_screen()


# ---------------------------------
# 4. (OPTIONAL) TOP BAR INFO FOR YOU
# ---------------------------------
with st.sidebar:
    st.markdown("### Access Status")
    st.write("You are logged in with:")
    st.code(st.session_state.license_code or "Unknown")

    # You can show a tiny message to the user here:
    st.info("This tool is licensed for personal use only. Thank you for supporting early builds 💛")


# ---------------------------------
# 5. THE ACTUAL APP UI
# ---------------------------------

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
