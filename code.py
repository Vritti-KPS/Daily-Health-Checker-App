import streamlit as st
import pandas as pd

# PAGE SETTINGS
st.set_page_config(
    page_title="Daily Health Checker",
    page_icon="🌿",
    layout="wide"
)

# STORE DATA
if "water" not in st.session_state:
    st.session_state.water = 0

if "goal" not in st.session_state:
    st.session_state.goal = 8

if "heart_history" not in st.session_state:
    st.session_state.heart_history = []

if "sugar_history" not in st.session_state:
    st.session_state.sugar_history = []

if "bmi" not in st.session_state:
    st.session_state.bmi = None

# WEBSITE TITLE
st.title("🌿 Daily Health Checker")
st.write("Your everyday health tracking companion!")

st.divider()

# SIDEBAR MENU
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choose a section:",
    [
        "Home",
        "BMI Calculator",
        "Water Tracker",
        "Heart Rate Checker",
        "Blood Sugar Tracker"
    ]
)

# HOME PAGE
if page == "Home":

    st.header("Welcome to Daily Health Checker!")

    st.write(
        "This application helps you keep track "
        "of some daily health measurements."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Your BMI",
            f"{st.session_state.bmi:.2f}"
            if st.session_state.bmi is not None else "Not calculated"
        )

        st.metric(
            "Water Intake",
            str(st.session_state.water) + " glasses"
        )

    with col2:
        latest_heart = (
            str(st.session_state.heart_history[-1]["BPM"]) + " BPM"
            if st.session_state.heart_history else "Not recorded"
        )

        latest_sugar = (
            str(st.session_state.sugar_history[-1]["Level"]) + " mg/dL"
            if st.session_state.sugar_history else "Not recorded"
        )

        st.metric("Latest Heart Rate", latest_heart)
        st.metric("Latest Blood Sugar", latest_sugar)

    st.divider()

    st.subheader("Health Tips")

    st.info("💧 Drink water regularly throughout the day.")
    st.info("😴 Maintain a regular sleep schedule.")
    st.info("🏃 Stay physically active.")
    st.info("🥗 Eat a balanced diet.")

# BMI CALCULATOR
elif page == "BMI Calculator":

    st.header("⚖️ BMI Calculator")

    st.write("Enter your height and weight.")

    weight = st.number_input(
        "Weight (kg)",
        min_value=1.0,
        max_value=500.0,
        value=40.0
    )

    height = st.number_input(
        "Height (cm)",
        min_value=30.0,
        max_value=250.0,
        value=150.0
    )

    age = st.number_input(
        "Age (years)",
        min_value=2,
        max_value=120,
        value=14
    )

    if st.button("Calculate BMI"):

        height_m = height / 100

        bmi = weight / (height_m * height_m)

        st.session_state.bmi = bmi

        st.success(f"Your BMI is {bmi:.2f}")

        if age < 20:
            st.info(
                "For children and teenagers, BMI must be "
                "interpreted using age- and sex-specific "
                "growth charts. Adult BMI categories and "
                "weight ranges are not suitable."
            )

        else:
            if bmi < 18.5:
                st.write("Category: Underweight")
            elif bmi < 25:
                st.write("Category: Healthy weight range")
            elif bmi < 30:
                st.write("Category: Overweight")
            else:
                st.write("Category: Obesity range")

            min_weight = 18.5 * height_m ** 2
            max_weight = 24.9 * height_m ** 2

            st.write(
                f"Estimated adult BMI-based weight range: "
                f"{min_weight:.1f} - {max_weight:.1f} kg"
            )

# WATER TRACKER
elif page == "Water Tracker":

    st.header("💧 Water Intake Tracker")

    st.session_state.goal = st.number_input(
        "Set Daily Water Goal (Glasses)",
        min_value=1,
        max_value=50,
        value=st.session_state.goal
    )

    st.subheader("Today's Water Intake")

    st.metric(
        "Water Consumed",
        f"{st.session_state.water} / {st.session_state.goal} glasses"
    )

    progress = min(
        st.session_state.water / st.session_state.goal,
        1.0
    )

    st.progress(progress)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("➕ Add 1 Glass"):
            st.session_state.water += 1
            st.rerun()

    with col2:
        if st.button("➖ Remove 1 Glass"):
            if st.session_state.water > 0:
                st.session_state.water -= 1
            st.rerun()

    if st.session_state.water >= st.session_state.goal:
        st.success("Your tracking goal has been reached!")

    else:
        st.info("Keep tracking your water intake!")

# HEART RATE CHECKER
elif page == "Heart Rate Checker":

    st.header("❤️ Heart Rate Checker")

    bpm = st.number_input(
        "Enter Heart Rate (BPM)",
        min_value=1,
        max_value=300,
        value=70
    )

    if st.button("Save Heart Rate"):

        st.session_state.heart_history.append({
            "BPM": bpm
        })

        st.success("Heart rate reading saved!")

        st.info(
            "Heart rate depends on age, activity and other "
            "factors. This app does not diagnose heart problems."
        )

    st.subheader("Heart Rate History")

    if st.session_state.heart_history:

        df = pd.DataFrame(st.session_state.heart_history)

        st.dataframe(df, use_container_width=True)

        st.line_chart(df["BPM"])

    else:
        st.write("No heart rate records yet.")

# BLOOD SUGAR TRACKER
elif page == "Blood Sugar Tracker":

    st.header("🩸 Blood Sugar Tracker")

    sugar = st.number_input(
        "Enter Blood Sugar Level (mg/dL)",
        min_value=1.0,
        max_value=2000.0,
        value=100.0
    )

    reading_type = st.selectbox(
        "Reading Type",
        ["Fasting", "After Meal", "Random"]
    )

    if st.button("Save Blood Sugar"):

        st.session_state.sugar_history.append({
            "Level": sugar,
            "Type": reading_type
        })

        st.success("Blood sugar reading saved!")

        st.info(
            "Blood sugar readings need medical interpretation. "
            "This app does not diagnose diabetes."
        )

    st.subheader("Blood Sugar History")

    if st.session_state.sugar_history:

        df = pd.DataFrame(st.session_state.sugar_history)

        st.dataframe(df, use_container_width=True)

        st.line_chart(df["Level"])

    else:
        st.write("No blood sugar records yet.")

# FOOTER
st.divider()
