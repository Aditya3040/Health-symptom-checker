import streamlit as st
import pandas as pd

# -----------------------------
# Load Rules Safely
# -----------------------------
@st.cache_data
def load_rules(file_path="symptom_rules.csv"):
    # Load only required columns
    df = pd.read_csv(file_path, usecols=["symptom", "cause", "advice"])
    df = df.dropna(subset=["symptom"])  # remove rows with empty symptom
    df["symptom"] = df["symptom"].str.strip().str.lower()  # clean symptoms
    return df

rules = load_rules("symptom_rules.csv")

# -----------------------------
# Prepare Clean Symptom List
# -----------------------------
symptom_list = rules["symptom"].unique()
symptom_list.sort()

# -----------------------------
# Risk Score Calculator
# -----------------------------
def calculate_risk(severity, age):
    risk = severity * 10
    if age > 50:
        risk += 15
    if severity >= 7:
        risk += 20
    return min(risk, 100)

# -----------------------------
# Symptom Checker Function
# -----------------------------
def check_symptom(symptom):
    match = rules[rules["symptom"] == symptom.lower()]
    if not match.empty:
        row = match.iloc[0]
        return row["cause"], row["advice"]
    return "Unknown cause", "Rest, drink water, and monitor the symptom."

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Health Symptom Checker", layout="wide")

st.title("🩺 Health Symptom Checker (Professional)")
st.write("A smart rule-based tool to understand your symptoms quickly.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Enter Your Details")
    age = st.number_input("Age", 1, 100, 25)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    symptom = st.selectbox("Select Symptom", symptom_list)
    severity = st.slider("Symptom Severity (1 = low, 10 = high)", 1, 10)

with col2:
    st.subheader("Symptom Description")
    st.info("Select a symptom and adjust severity to estimate risk level.")

# Process Button
if st.button("Check Result"):
    cause, advice = check_symptom(symptom)
    risk = calculate_risk(severity, age)

    st.subheader("📌 Result Summary")
    st.write(f"### Symptom: **{symptom.capitalize()}**")
    st.write(f"#### Cause: {cause}")
    st.write(f"#### Advice: {advice}")

    st.write("### 🔥 Risk Level")
    if risk < 30:
        st.success(f"Low Risk ({risk}%)")
    elif risk < 70:
        st.warning(f"Moderate Risk ({risk}%)")
    else:
        st.error(f"High Risk ({risk}%)")

    st.write("---")
    st.write("### 🧾 Additional Notes")
    st.write(f"- Gender Considered: **{gender}**")
    st.write(f"- Age Considered: **{age}** years")
    st.write(f"- Severity Score: **{severity}/10**")
