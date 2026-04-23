
# python streamlit app.py

import matplotlib.pyplot as plt
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
elif menu == "CSV Analysis":
    st.header("CSV Upload and Analysis")

    # uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    st.subheader('uploaded_file that needs to be fixed and aded, for now the csv is directly uploaded')
    uploaded_file = None

    if uploaded_file is None:
        try:
            df = load_csv(uploaded_file)
            # df = pd.read_csv('synAGE_klotho.csv')
            st.success("CSV loaded successfully.")

            st.checkbox("preview")

            # Preview
            st.subheader("Preview")
            st.dataframe(df.head())

            # Shape
            st.subheader("Dataset Shape")
            col1, col2 = st.columns(2)
            col1.metric("Rows", df.shape[0])
            col2.metric("Columns", df.shape[1])

            # Column info
            st.subheader("Column Information")
            info_df = get_basic_info(df)
            st.dataframe(info_df)

            # Missing values
            st.subheader("Missing Values")
            missing_df = get_missing_values(df)
            st.dataframe(missing_df)

            # Numeric summary
            st.subheader("Numeric Summary")
            numeric_summary = get_numeric_summary(df)
            if not numeric_summary.empty:
                st.dataframe(numeric_summary)
            else:
                st.info("No numeric columns found.")

            # Categorical summary
            st.subheader("Categorical Summary")
            categorical_summary = get_categorical_summary(df)
            if not categorical_summary.empty:
                st.dataframe(categorical_summary)
            else:
                st.info("No categorical columns found.")

            # Histogram
            st.subheader("Histogram")
            numeric_columns = df.select_dtypes(include="number").columns.tolist()
            if numeric_columns:
                selected_num_col = st.selectbox("Select numeric column", numeric_columns)
                fig, ax = plt.subplots()
                ax.hist(df[selected_num_col].dropna(), bins=30)
                ax.set_title(f"Histogram of {selected_num_col}")
                ax.set_xlabel(selected_num_col)
                ax.set_ylabel("Frequency")
                st.pyplot(fig)
            else:
                st.info("No numeric columns available for histogram.")

            # Correlation
            st.subheader("Correlation Matrix")
            corr_df = get_correlation(df)
            if not corr_df.empty:
                st.dataframe(corr_df)
            else:
                st.info("Need at least two numeric columns for correlation matrix.")

            # Filtering
            st.subheader("Filter Data")
            selected_col = st.selectbox("Select a column to filter", df.columns.tolist())

            unique_vals = df[selected_col].dropna().unique().tolist()
            if len(unique_vals) > 0:
                selected_val = st.selectbox("Select a value", unique_vals)
                if st.button("Apply Filter"):
                    filtered_df = filter_dataframe(df, selected_col, selected_val)
                    st.write(f"Filtered rows: {len(filtered_df)}")
                    st.dataframe(filtered_df)
            else:
                st.info("No non-null values available in this column for filtering.")

            # Download
            st.subheader("Download Current CSV")
            csv_bytes = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download CSV",
                data=csv_bytes,
                file_name="processed_data.csv",
                mime="text/csv",
            )

        except Exception as e:
            st.error(f"Error reading CSV: {e}")
    else:
        st.info("Please upload a CSV file.")

elif menu == 'Image annotator' :
    # st.header("Image Upload and Analysis")
    st.title("Image Annotation Tool")

    # uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg", "TIF"])
    uploaded_file = True

    drawing_mode = st.selectbox(
        "Annotation type",
        ["rect", "point", "freedraw", "line", "circle"]
    )

    stroke_width = st.slider("Stroke width", 1, 10, 2)

    if uploaded_file is not None:
        uploaded_path = '/home/sachakra/Documents/Sabyasachi/2-Data-labsexpsTrials/retina_cfp/ummd/VCI306_02.TIF'
        image = Image.open(uploaded_path).convert("RGB")
        image = np.array(image)
        st.write("Numpy shape:", image.shape)
        w, h, c = image.shape

        st.write(f"Image size: {w} x {h}")
        st.image(image)

        # canvas_result = st_canvas(
        #     # fill_color="rgba(255, 0, 0, 0.2)",
        #     stroke_width=stroke_width,
        #     stroke_color="#ff0000",
        #     background_image=image,
        #     update_streamlit=True,
        #     height=h,
        #     width=w,
        #     drawing_mode=drawing_mode,
        #     key="canvas",
        # )

        # if canvas_result.json_data is not None:
        #     st.subheader("Raw annotation data")
        #     st.json(canvas_result.json_data)

        #     objects = canvas_result.json_data.get("objects", [])
        #     parsed_annotations = []

        #     for obj in objects:
        #         parsed = {
        #             "type": obj.get("type"),
        #             "left": obj.get("left"),
        #             "top": obj.get("top"),
        #             "width": obj.get("width"),
        #             "height": obj.get("height"),
        #             "radius": obj.get("radius"),
        #             "x1": obj.get("x1"),
        #             "y1": obj.get("y1"),
        #             "x2": obj.get("x2"),
        #             "y2": obj.get("y2"),
        #         }
        #         parsed_annotations.append(parsed)

            # st.subheader("Parsed annotations")
            # st.write(parsed_annotations)

            # annotation_json = json.dumps(parsed_annotations, indent=2)

            # st.download_button(
            #     "Download annotations as JSON",
            #     data=annotation_json,
            #     file_name="annotations.json",
            #     mime="application/json",
            # )

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