import streamlit as st

st.set_page_config(
    page_title="Comprehensive Fitness & Lifestyle Planner",
    page_icon="🏋️‍♂️",
    layout="wide"
)

st.title("🏋️‍♂️ Comprehensive Fitness & Lifestyle Assessment")
st.write("Input your details, schedule, and goals to generate your personalized health blueprint.")

# --- SIDEBAR: User Parameters ---
st.sidebar.header(" Profile & Parameters")

gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
age = st.sidebar.number_input("Age (years)", min_value=10, max_value=100, value=25)
height_cm = st.sidebar.number_input("Height (cm)", min_value=100.0, max_value=230.0, value=170.0, step=0.5)
weight_kg = st.sidebar.number_input("Current Weight (kg)", min_value=30.0, max_value=250.0, value=75.0, step=0.5)
target_weight = st.sidebar.number_input("Target Weight (kg)", min_value=30.0, max_value=250.0, value=68.0, step=0.5)

st.sidebar.subheader("Availability & Routine")
workout_days = st.sidebar.slider("Days available for workout / week", min_value=1, max_value=7, value=4)
session_duration = st.sidebar.selectbox("Time available per session", ["30 mins", "45 mins", "60 mins", "90 mins"])

activity_level = st.sidebar.selectbox(
    "Daily Activity Level",
    [
        "Sedentary (Desk job, minimal movement)",
        "Lightly Active (1-3 days mild movement)",
        "Moderately Active (3-5 days active movement)",
        "Very Active (6-7 days intense activity)"
    ]
)

goal = st.sidebar.selectbox(
    "Primary Fitness Goal",
    ["Weight Loss", "Muscle Gain", "General Fitness & Endurance", "Maintain Weight"]
)

# --- CALCULATIONS ---
height_m = height_cm / 100.0
bmi = weight_kg / (height_m ** 2)

# Ideal Weight Range (BMI 18.5 - 24.9)
ideal_min_weight = 18.5 * (height_m ** 2)
ideal_max_weight = 24.9 * (height_m ** 2)

# BMR (Mifflin-St Jeor)
if gender == "Male":
    bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
else:
    bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

# Activity Multiplier
multipliers = {
    "Sedentary (Desk job, minimal movement)": 1.2,
    "Lightly Active (1-3 days mild movement)": 1.375,
    "Moderately Active (3-5 days active movement)": 1.55,
    "Very Active (6-7 days intense activity)": 1.725
}
tdee = bmr * multipliers[activity_level]

# Target Calories
if goal == "Weight Loss":
    target_calories = max(tdee - 500, 1200)
elif goal == "Muscle Gain":
    target_calories = tdee + 400
else:
    target_calories = tdee

# --- MAIN DISPLAY ---

# 1. Ground Truth Metrics
st.header(" 1. Ground Truth Metrics")
col1, col2, col3, col4 = st.columns(4)

if bmi < 18.5:
    bmi_category = "Underweight"
elif 18.5 <= bmi < 25:
    bmi_category = "Normal Weight"
elif 25 <= bmi < 30:
    bmi_category = "Overweight"
else:
    bmi_category = "Obese"

col1.metric("Current BMI", f"{bmi:.1f}", delta=bmi_category, delta_color="off")
col2.metric("Current Weight", f"{weight_kg:.1f} kg")
col3.metric("Ideal Weight Range", f"{ideal_min_weight:.1f} - {ideal_max_weight:.1f} kg")
col4.metric("Daily Calorie Target", f"{int(target_calories)} kcal")

st.markdown("---")

# 2. Availability Summary
st.header("🗓️ 2. Availability & Commitment")
st.info(
    f"*Schedule Summary:* You have committed *{workout_days} days per week* with *{session_duration}* per session. "
    f"Your plan is calibrated for a total weekly exercise capacity of approximately *{workout_days * int(session_duration.split()[0])} minutes*."
)

st.markdown("---")

# 3. Recommended Exercise Program
st.header(" 3. Physical Exercise Recommendation")

if goal == "Weight Loss":
    st.subheader(f"Recommended Routine ({workout_days} Days/Week - {goal})")
    st.write("Focus on high caloric expenditure combined with resistance training to preserve muscle mass.")
    
    if workout_days <= 3:
        st.markdown("""
        * *Day 1:* Full Body Strength Training (Compound Movements) + 15 mins HIIT
        * *Day 2:* Full Body Strength Training + 15 mins Incline Walking
        * *Day 3:* Full Body Circuit Training & Core Focus
        """)
    else:
        st.markdown("""
        * *Day 1:* Upper Body Resistance + 15 mins Cardio
        * *Day 2:* Lower Body Resistance + Core Focus
        * *Day 3:* Rest or Active Recovery (Light Walking)
        * *Day 4:* Push-Pull Strength Circuit + 20 mins Steady Cardio
        * *Day 5:* Full Body Functional Training
        """)

elif goal == "Muscle Gain":
    st.subheader(f"Recommended Routine ({workout_days} Days/Week - {goal})")
    st.write("Focus on progressive overload, compound lifts, and adequate rest between sets.")
    
    if workout_days <= 3:
        st.markdown("""
        * *Day 1:* Full Body Heavy Resistance (Squat, Bench, Rows)
        * *Day 2:* Full Body Heavy Resistance (Deadlift, Overhead Press, Pull-ups)
        * *Day 3:* Full Body Hypertrophy & Accessory Movements
        """)
    else:
        st.markdown("""
        * *Day 1:* Push Focus (Chest, Shoulders, Triceps)
        * *Day 2:* Pull Focus (Back, Biceps, Rear Delts)
        * *Day 3:* Legs & Core Focus
        * *Day 4:* Upper Body Hypertrophy
        * *Day 5:* Lower Body Hypertrophy
        """)

else:
    st.subheader(f"Recommended Routine ({workout_days} Days/Week - General Health)")
    st.markdown("""
    * *Resistance Work (2-3 days):* Full-body functional movements (lunges, push-ups, bodyweight rows).
    * *Cardiovascular Health (1-2 days):* Zone 2 cardio (cycling, jogging, brisk walking) for 30–45 mins.
    * *Mobility & Flexibility (Daily):* 10 minutes of dynamic stretching every morning.
    """)

st.markdown("---")

# 4. Lifestyle & Habit Recommendations
st.header(" 4. Essential Lifestyle Changes")

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Hydration & Nutrition Habits")
    water_target = weight_kg * 0.035
    st.markdown(f"""
    * *Daily Hydration Goal:* Aim for at least *{water_target:.1f} Liters* of water per day.
    * *Protein Priority:* Consume 1.6–2.0g of protein per kg of target weight ({int(target_weight * 1.8)}g/day) to support muscle retention and satiety.
    * *Whole Foods First:* Shift 80% of dietary intake to unprocessed, single-ingredient foods (lean meats, vegetables, complex carbs).
    * *Meal Timing:* Stop consuming large meals 2–3 hours before sleep.
    """)

with col_b:
    st.subheader(" Sleep & Recovery Optimization")
    st.markdown("""
    * *Sleep Hygiene:* Maintain 7–8 hours of consistent sleep nightly to optimize hormonal balance and cortisol levels.
    * *Daily Movement:* Aim for 8,000–10,000 steps daily outside of structured gym workouts.
    * *Stress Reduction:* Dedicate 10 minutes daily to breathwork, mindfulness, or walking outdoors without digital distractions.
    * *Alcohol & Sugar:* Limit refined sugar intake and reduce alcohol consumption to prevent recovery disruption.
    """)
