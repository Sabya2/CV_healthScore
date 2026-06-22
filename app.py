
import streamlit as st

from features_utils import (

    render_measurement_inputs,
    render_star_plot, 
    render_sleep_score,
    render_bp_score,
    render_bmi_score,
    render_vo2_score,
    render_cimt_score,
    render_wrPeak_score, 
    render_baPWV_score,
    render_KidScreen_score,
    render_momo_score,
    render_gripStrength_score,
    
)

REFERENCE_PATHS = {
    "BMI": "reference_values/bmi.csv",
    "sleep_json": "reference_values/sleep_score.json",
    "bp_json": "reference_values/bp.json",

    "grip_strength": "reference_values/gripStrength_long_reference.csv",
    "kidScreen": "reference_values/kidscreen_long_reference.csv",
    "momo": "reference_values/momo_long_reference.csv",
    "baPWV_peak": "reference_values/baPWV_LMS_reference.csv",

    "vo2": {
        "boys": {"age": "reference_values/vo2peak_kg_boys_lms.csv"},
        "girls": {"age": "reference_values/vo2peak_kg_girls_lms.csv"},
    },
    "cimt": {
        "boys": {
            "age": "reference_values/cimt_age_boys_LMS.csv",
            "height": "reference_values/cimt_height_boys_LMS.csv",
        },
        "girls": {
            "age": "reference_values/cimt_age_girls_LMS.csv",
            "height": "reference_values/cimt_height_girls_LMS.csv",
        },
    },

    "wr_peak": {
        "boys": {'age':"reference_values/WR_peak_kg_boys_lms.csv"},
        "girls":{'age':"reference_values/WR_peak_kg_girls_lms.csv"},
    },
}


def render_scores(refs: dict):
    row1_col1, row1_col2, row1_col3 = st.columns(3, gap = 'xsmall', border = True)
    with row1_col1:
        render_sleep_score(refs)
    with row1_col2:
        render_bp_score(refs)
    with row1_col3:
        render_bmi_score(refs)

    row2_col1, row2_col2, row2_col3 = st.columns(3, gap = 'xsmall', border = True)
    with row2_col1:
        render_cimt_score(refs)
    with row2_col2:
        render_vo2_score(refs)
    with row2_col3:
        render_wrPeak_score(refs)

    row3_col1, row3_col2, row3_col3, row3_col4  = st.columns(4, gap = 'xsmall', border = True)
    with row3_col1:
        render_baPWV_score(refs)
    with row3_col2:
        render_KidScreen_score(refs)
    with row3_col3:
        render_momo_score(refs)
    with row3_col4:
        render_gripStrength_score(refs)
   


def main():
    st.set_page_config(page_title="Health Score Demo", layout="wide")
    st.title("Cardiac Health Score")

    if "score" not in st.session_state:
        st.session_state.score = {}

    render_measurement_inputs()
    st.divider()
    render_scores(REFERENCE_PATHS)
    # st.session_state.score

    profile_summary = st.checkbox(
                "Show full summary",
                value=False,
                key="profile_summary"
            )
    if profile_summary:
        render_star_plot(st.session_state.score)


if __name__ == "__main__":
    main()








