
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Attendance Analyzer", layout="centered")

st.title("📊 Attendance Analyzer Agent")

# Upload or use sample CSV
uploaded_file = st.file_uploader("Upload Attendance CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    st.info("Using sample data. Upload your own for custom results.")
    df = pd.read_csv("sample_attendance(2).csv")

if 'Overall %' not in df.columns:
    # Calculate attendance percentage
    subject_cols = df.columns[2:]
    df['Total Lectures'] = len(subject_cols)
    df['Present Count'] = df[subject_cols].sum(axis=1)
    df['Overall %'] = round((df['Present Count'] / df['Total Lectures']) * 100, 2)

# Show data
st.subheader("📋 Attendance Table")
st.dataframe(df)

# Identify defaulters
threshold = 75
defaulters = df[df['Overall %'] < threshold]

st.subheader("🚨 Defaulters (Below 75%)")
st.dataframe(defaulters)

# Plot
st.subheader("📈 Attendance Chart")
fig, ax = plt.subplots()
ax.bar(df['Name'], df['Overall %'], color='skyblue')
ax.axhline(threshold, color='red', linestyle='--', label='75% Threshold')
plt.xticks(rotation=45)
ax.set_ylabel('Attendance %')
plt.legend()
st.pyplot(fig)

# Download processed data
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("⬇️ Download Report", csv, file_name="processed_attendance.csv", mime="text/csv")
