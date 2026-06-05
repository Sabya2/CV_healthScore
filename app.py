
import streamlit as st

from features_utils import (
    render_measurement_inputs,
    render_sleep_score,
    render_bp_score,
    render_bmi_score,
    render_vo2_score,
    render_cimt_score,
    render_wrPeak_score, 
)

REFERENCE_PATHS = {
    "BMI": "reference_values/bmi.csv",
    "sleep_json": "reference_values/sleep_score.json",
    "bp_json": "reference_values/bp.json",
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

    "wrPeak": {
        "boys": {'age':"reference_values/WR_peak_kg_boys_lms.csv"},
        "girls":{'age': "reference_values/WR_peak_kg_girls_lms.csv"},
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


def main():
    st.set_page_config(page_title="Health Score Demo", layout="wide")
    st.title("Health Score Demo")

    render_measurement_inputs()
    st.divider()
    render_scores(REFERENCE_PATHS)


if __name__ == "__main__":
    main()





# wr_peak_value = st.number_input(
#                 "Observed wr peak (get it checked fro min and max)",
#                 min_value=0.001,
#                 max_value=2.0,
#                 value=float(st.session_state.wr_peak_value),
#                 step=0.001,
#                 format="%.3f",
#                 key="input_wr peak"
#             )



