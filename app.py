
# python streamlit app.py

# import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PIL import Image

import streamlit as st
# from streamlit_drawable_canvas import st_canvas
import json

from utils import (
    sum_numbers,
    load_csv,
    get_basic_info,
    get_missing_values,
    get_numeric_summary,
    get_categorical_summary,
    filter_dataframe,
    get_correlation,
    get_sleep_score_json, 
    score_bp_from_json, 
    score_bmi_from_df
)


st.set_page_config(page_title="Demo app ", layout="wide")

st.title("Use the sidebar to choose a function.")
# st.write("Use the sidebar to choose a function.")

# menu = st.sidebar.selectbox(
#     "Choose function",
#     ["CSV Analysis", "Sum Calculator"]
# )

menu = st.sidebar.selectbox(
    "Choose function",
    [ 
        'BP Score', 
        'BMI Score',
        "sleep score",
        # "Image annotator", 
        # "CSV Analysis",
        # "Variable Explorer",
        # "Sum Calculator", 
        # "Image annotator"
    ]
)

# -------------------------------------------------
# SUM CALCULATOR
# -------------------------------------------------
if menu == "Sum Calculator":
    st.header("Sum Calculator")

    a = st.number_input("Enter first number", value=0.0)
    b = st.number_input("Enter second number", value=0.0)

    if st.button("Calculate Sum"):
        result = sum_numbers(a, b)
        st.success(f"Result: {a} + {b} = {result}")


# -------------------------------------------------
# CSV ANALYSIS
# -------------------------------------------------

# -------------------------------------------------
# SLEEP SCORE
# -------------------------------------------------
elif menu == "sleep score":
    st.header("Sleep Score")

    json_file = "sleep_score.json"

    st.write("Enter sex, age, and sleep duration to calculate the sleep score.")

    sex = st.selectbox("Sex", ["boys", "girls"])
    age = st.number_input("Age (years)", min_value=0.0, max_value=25.0, value=8.0, step=0.1)
    sleep_hours = st.number_input("Sleep hours", min_value=0.0, max_value=24.0, value=9.0, step=0.1)

    if st.button("Calculate Sleep Score"):
        try:
            result = get_sleep_score_json(
                json_file=json_file,
                age=age,
                sex=sex,
                sleep_hours=sleep_hours
            )

            st.success(f"Sleep score: {result['score']}")
            st.markdown(
                f"<h1 style='text-align:center; color:green;'>Sleep Score: {result['score']}</h1>",
                unsafe_allow_html=True
            )

            col1, col2 = st.columns(2)

            with col1:
                st.write("### Input")
                st.write(f"**Sex:** {result['sex']}")
                st.write(f"**Age:** {result['age']}")
                st.write(f"**Sleep hours:** {result['sleep_hours']}")

            with col2:
                st.write("### Reference")
                st.write(f"**Age group:** {result['age_group']}")
                st.write(f"**Mean (h):** {result['mean_h']}")
                st.write(f"**SD (h):** {result['sd_h']}")
                st.write(f"**Upper cut-off:** {result['upper_cutoff']}")
                st.write(f"**Lower cut-off:** {result['lower_cutoff']}")

            if "band" in result:
                st.write(f"**Matched band:** {result['band']}")

            st.json(result)

        except FileNotFoundError:
            st.error(f"JSON file not found: {json_file}")
        except Exception as e:
            st.error(f"Error calculating sleep score: {e}")


# -------------------------------------------------
# BP SCORE
# -------------------------------------------------
elif menu == "BP Score":
    st.header("Blood Pressure Score")
    json_file = 'bp.json'

    st.write("Enter sex, age, height, systolic BP, diastolic BP, and treatment status.")

    col1, col2 = st.columns(2)

    with col1:
        sex = st.selectbox("Sex", ["boys", "girls"])
        age_years = st.number_input(
            "Age (years)",
            min_value=0.0,
            max_value=25.0,
            value=10.5,
            step=0.5
        )
        height_cm = st.number_input(
            "Height (cm)",
            min_value=50.0,
            max_value=250.0,
            value=140.0,
            step=1.0
        )

    with col2:
        systolic_bp = st.number_input(
            "Systolic BP",
            min_value=40.0,
            max_value=250.0,
            value=110.0,
            step=1.0
        )
        diastolic_bp = st.number_input(
            "Diastolic BP",
            min_value=20.0,
            max_value=150.0,
            value=70.0,
            step=1.0
        )
        treated = st.checkbox("Treated", value=False)

    if st.button("Calculate BP Score"):
        try:
            result = score_bp_from_json(
                json_file=json_file,
                sex=sex,
                age_years=age_years,
                height_cm=height_cm,
                systolic_bp=systolic_bp,
                diastolic_bp=diastolic_bp,
                treated=treated,
            )

            st.markdown(
                f"""
                <div style="text-align:center;">
                    <h3>Blood Pressure Score</h3>
                    <h1 style="color:green; font-size:80px;">{result['score']}</h1>
                </div>
                """,
                unsafe_allow_html=True
            )

            c1, c2 = st.columns(2)

            with c1:
                st.subheader("Inputs")
                st.write(f"**Sex:** {result['inputs']['sex']}")
                st.write(f"**Age (years):** {result['inputs']['age_years']}")
                st.write(f"**Height (cm):** {result['inputs']['height_cm']}")
                st.write(f"**Systolic BP:** {result['inputs']['systolic_bp']}")
                st.write(f"**Diastolic BP:** {result['inputs']['diastolic_bp']}")
                st.write(f"**Treated:** {result['treated']}")

            with c2:
                st.subheader("Component Scores")
                st.write(f"**Systolic score:** {result['component_scores']['systolic_score']}")
                st.write(f"**Diastolic score:** {result['component_scores']['diastolic_score']}")

            st.subheader("Matched Reference Row - Systolic")
            st.json(result["reference_rows"]["systolic"])

            st.subheader("Matched Reference Row - Diastolic")
            st.json(result["reference_rows"]["diastolic"])

        except FileNotFoundError:
            st.error(f"JSON file not found: {json_file}")
        except Exception as e:
            st.error(f"Error calculating BP score: {e}")


elif menu == "BMI Score":
    st.header("BMI Score")
    bmi_df = pd.read_csv('bmi.csv')

    st.write("Enter sex, age, weight, and height.")


    col1, col2 = st.columns(2)

    with col1:
        sex = st.selectbox("Sex", ["boys", "girls"], key="bmi_sex")
        age_years = st.number_input(
            "Age (years)",
            min_value=0.0,
            max_value=25.0,
            value=10.5,
            step=0.5,
            key="bmi_age"
        )

    with col2:
        weight_kg = st.number_input(
            "Weight (kg)",
            min_value=1.0,
            max_value=300.0,
            value=35.0,
            step=0.5,
            key="bmi_weight"
        )
        height_cm = st.number_input(
            "Height (cm)",
            min_value=30.0,
            max_value=250.0,
            value=140.0,
            step=0.5,
            key="bmi_height"
        )

    if st.button("Calculate BMI Score"):
        try:
            result = score_bmi_from_df(
                bmi_df=bmi_df,   # already loaded dataframe
                sex=sex,
                age_years=age_years,
                weight_kg=weight_kg,
                height_cm=height_cm,
            )

            score = result["score"]
            bmi_value = result["inputs"]["bmi"]

            color = "green"
            if score == 70:
                color = "orange"
            elif score in [30, 0]:
                color = "red"

            st.markdown(
                f"""
                <div style="text-align:center;">
                    <h3>BMI Score</h3>
                    <h1 style="color:{color}; font-size:80px;">{score}</h1>
                    <h4>BMI: {bmi_value}</h4>
                </div>
                """,
                unsafe_allow_html=True
            )

            c1, c2 = st.columns(2)

            with c1:
                st.subheader("Inputs")
                st.write(f"**Sex:** {result['inputs']['sex']}")
                st.write(f"**Age (years):** {result['inputs']['age_years']}")
                st.write(f"**Weight (kg):** {result['inputs']['weight_kg']}")
                st.write(f"**Height (cm):** {result['inputs']['height_cm']}")
                st.write(f"**BMI:** {result['inputs']['bmi']}")

            with c2:
                st.subheader("Matched Reference")
                st.write(f"**Month used:** {result['reference_row']['Month']}")
                st.write(f"**-3SD:** {result['reference_row']['-3SD']}")
                st.write(f"**-2SD:** {result['reference_row']['-2SD']}")
                st.write(f"**-1SD:** {result['reference_row']['-1SD']}")
                st.write(f"**Median:** {result['reference_row']['Median']}")
                st.write(f"**1SD:** {result['reference_row']['1SD']}")
                st.write(f"**2SD:** {result['reference_row']['2SD']}")
                st.write(f"**3SD:** {result['reference_row']['3SD']}")

            st.subheader("Matched Reference Row")
            st.json(result["reference_row"])

        except Exception as e:
            st.error(f"Error calculating BMI score: {e}")