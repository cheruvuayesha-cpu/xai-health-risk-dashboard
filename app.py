import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

import matplotlib.pyplot as plt

st.set_page_config(page_title="Alzheimer's XAI Dashboard", layout="wide")
st.title("Alzheimer's Risk Prediction & Explainable AI Dashboard")
st.write("Analyze risk factors, evaluate model outputs against ground truth, and receive personalized lifestyle recommendations.")

# 1. Dataset & Model Setup
@st.cache_resource
def train_model():
    np.random.seed(42)
    n_samples = 100
    
    data = {
        'Age_Group': np.random.choice([1, 2, 3], n_samples),
        'Physical_Exercise_Days': np.random.choice([0, 1, 2, 3, 4, 5], n_samples),
        'Sleep_Hours': np.random.choice([4, 5, 6, 7, 8], n_samples),
        'Diet_Quality': np.random.choice([1, 2, 3], n_samples),
        'Cognitive_Activity': np.random.choice([1, 2, 3], n_samples),
        'Cardiovascular_Disease': np.random.choice([0, 1], n_samples),
        'Family_History': np.random.choice([0, 1], n_samples),
        'Memory_Repetition': np.random.choice([0, 1, 2], n_samples)
    }
    
    df = pd.DataFrame(data)
    risk_score = (
        df['Age_Group'] * 1.5 + 
        df['Family_History'] * 2.0 + 
        df['Memory_Repetition'] * 2.5 + 
        df['Cardiovascular_Disease'] * 1.2 - 
        df['Physical_Exercise_Days'] * 0.8 - 
        df['Sleep_Hours'] * 0.5
    )
    df['Ground_Truth'] = np.where(risk_score > 4.5, 1, 0)
    
    X = df.drop('Ground_Truth', axis=1)
    y = df['Ground_Truth']
    
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X, y)
    explainer = shap.TreeExplainer(model)
    return model, explainer

model, explainer = train_model()

# 2. Sidebar Inputs
st.sidebar.header("Patient Questionnaire Inputs")
age_group = st.sidebar.selectbox("1. Age Group", [1, 2, 3], format_func=lambda x: {1: "Young Age (18-35)", 2: "Middle Age (36-55)", 3: "Old Age (56+)"}[x])
exercise = st.sidebar.slider("2. Physical Exercise (Days/Week)", 0, 7, 2)
sleep = st.sidebar.slider("3. Average Sleep (Hours/Night)", 4, 10, 6)
diet = st.sidebar.selectbox("4. Diet Quality", [1, 2, 3], format_func=lambda x: {1: "Poor / Processed", 2: "Average", 3: "Brain-Healthy / MIND Diet"}[x])
cognitive = st.sidebar.selectbox("5. Cognitive Activity", [1, 2, 3], format_func=lambda x: {1: "Low", 2: "Moderate", 3: "High"}[x])
cardio = st.sidebar.radio("6. Cardiovascular Disease History?", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
family_hist = st.sidebar.radio("7. Family History of Alzheimer's?", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
memory_rep = st.sidebar.selectbox("8. Memory Repetition Frequency", [0, 1, 2], format_func=lambda x: {0: "Never", 1: "Sometimes", 2: "Frequently"}[x])
ground_truth_input = st.sidebar.radio("9. Actual Diagnosed Status (Ground Truth)", [0, 1], format_func=lambda x: "Disease Present / High Risk" if x == 1 else "Normal / Low Risk")

input_data = pd.DataFrame([{
    'Age_Group': age_group,
    'Physical_Exercise_Days': exercise,
    'Sleep_Hours': sleep,
    'Diet_Quality': diet,
    'Cognitive_Activity': cognitive,
    'Cardiovascular_Disease': cardio,
    'Family_History': family_hist,
    'Memory_Repetition': memory_rep
}])

# 3. Dashboard Outputs
col1, col2 = st.columns(2)
prediction = model.predict(input_data)[0]
prediction_prob = model.predict_proba(input_data)[0][1]

with col1:
    st.subheader(" 1. Availability of Disease (AI Prediction)")
    if prediction == 1:
        st.error(f"*High Risk of Cognitive Decline / Alzheimer's*\n\nProbability: {prediction_prob * 100:.1f}%")
    else:
        st.success(f"*Low Risk / Normal Profile*\n\nProbability of Disease: {prediction_prob * 100:.1f}%")

with col2:
    st.subheader("2. Ground Truth of the Disease")
    if ground_truth_input == 1:
        st.warning("*Status:* Confirmed High Risk / Clinical Diagnosis Recorded")
    else:
        st.info("*Status:* Confirmed Normal / No Clinical Diagnosis")

st.divider()

# 4. SHAP Plot
st.subheader(" 3. Explainable AI (Why did the AI make this prediction?)")
shap_values = explainer(input_data)

fig, ax = plt.subplots(figsize=(8, 3))
# Handle multi-class / binary SHAP output matrix
if len(shap_values.shape) == 3:
    shap.plots.waterfall(shap_values[0, :, 1], show=False)
else:
    shap.plots.waterfall(shap_values[0], show=False)

st.pyplot(fig)
# 5. Recommendations
st.subheader(" 4. Personalized Exercise & Lifestyle Recommendations")
recommendations = []
if exercise < 3:
    recommendations.append("• *Increase Physical Activity:* Engage in at least 30 minutes of moderate exercise 3–5 days per week.")
if sleep < 7:
    recommendations.append("• *Optimize Sleep Hygiene:* Aim for 7–8 hours of uninterrupted sleep per night.")
if diet < 3:
    recommendations.append("• *Dietary Adjustment:* Adopt a Mediterranean/MIND diet rich in green leafy vegetables and berries.")
if cognitive < 3:
    recommendations.append("• *Cognitive Stimulation:* Dedicate 15–30 minutes daily to puzzles, reading, or memory games.")

if recommendations:
    for rec in recommendations:
        st.write(rec)
else:
    st.success("Excellent! Your current lifestyle metrics fully align with healthy cognitive preservation guidelines.")
