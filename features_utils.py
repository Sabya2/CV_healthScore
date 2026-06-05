import streamlit as st
import pandas as pd

from utils import (
    get_sleep_score_json,
    score_bp_from_json,
    score_bmi_from_df,
    score_measurement,
)



def init_measurement_state():
    defaults = {
        "sex": "boys",
        "age": 10.0,
        "height_cm": 140.0,
        "weight_kg": 35.0,
        "sleep_hours": 9.0,
        "systolic_bp": 110.0,
        "diastolic_bp": 70.0,
        "treated": False,
        "vo2_value": 45.0,
        "wr_peak_value": 0.380,
        "cimt_value": 0.380,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_measurement_inputs():
    init_measurement_state()

    with st.form("shared_measurement_inputs"):
        st.header("Measurements")

        col1, col2, col3 = st.columns(3,)

        with col1:
            sex = st.selectbox(
                "Sex",
                ["boys", "girls"],
                index=0 if st.session_state.sex == "boys" else 1,
                key="input_sex"
            )
            age = st.number_input(
                "Age (years)",
                min_value=0.0,
                max_value=25.0,
                value=float(st.session_state.age),
                step=0.1,
                key="input_age"
            )
            height_cm = st.number_input(
                "Height (cm)",
                min_value=30.0,
                max_value=250.0,
                value=float(st.session_state.height_cm),
                step=0.1,
                key="input_height"
            )

        with col2:
            weight_kg = st.number_input(
                "Weight (kg)",
                min_value=1.0,
                max_value=300.0,
                value=float(st.session_state.weight_kg),
                step=0.1,
                key="input_weight"
            )
            sleep_hours = st.number_input(
                "Sleep hours",
                min_value=0.0,
                max_value=24.0,
                value=float(st.session_state.sleep_hours),
                step=0.1,
                key="input_sleep"
            )
        

        with col3:
            systolic_bp = st.number_input(
                "Systolic BP",
                min_value=40.0,
                max_value=250.0,
                value=float(st.session_state.systolic_bp),
                step=1.0,
                key="input_sys"
            )
            diastolic_bp = st.number_input(
                "Diastolic BP",
                min_value=20.0,
                max_value=150.0,
                value=float(st.session_state.diastolic_bp),
                step=1.0,
                key="input_dia"
            )

            treated = st.checkbox(
                "BP Treated",
                value=bool(st.session_state.treated),
                key="input_treated"
            )

            vo2_value = st.number_input(
                "Observed VO2peak",
                min_value=0.1,
                max_value=100.0,
                value=float(st.session_state.vo2_value),
                step=0.1,
                key="input_vo2"
            )
            wr_peak_value = st.number_input(
                "Observed wr peak (get it checked fro min and max)",
                min_value=0.001,
                max_value=2.0,
                value=float(st.session_state.wr_peak_value),
                step=0.001,
                format="%.3f",
                key="input_wr_peak"
            )

        c1, c2 = st.columns(2)
        with c1:
            cimt_value = st.number_input(
                "Observed cIMT",
                min_value=0.001,
                max_value=2.0,
                value=float(st.session_state.cimt_value),
                step=0.001,
                format="%.3f",
                key="input_cimt"
            )
            # wr_peak_value = st.number_input(
            #     "Observed wr peak (get it checked fro min and max)",
            #     min_value=0.001,
            #     max_value=2.0,
            #     value=float(st.session_state.wr_peak_value),
            #     step=0.001,
            #     format="%.3f",
            #     key="input_wr peak"
            # )

        

        submitted = st.form_submit_button("Save Measurements")

    if submitted:
        st.session_state.sex = sex
        st.session_state.age = age
        st.session_state.height_cm = height_cm
        st.session_state.weight_kg = weight_kg
        st.session_state.sleep_hours = sleep_hours
        st.session_state.treated = treated
        st.session_state.systolic_bp = systolic_bp
        st.session_state.diastolic_bp = diastolic_bp
        st.session_state.vo2_value = vo2_value
        st.session_state.cimt_value = cimt_value
        st.session_state.wr_peak_value = wr_peak_value

        st.success("Measurements saved to session state.")


def render_sleep_score(refs):
    # json_file = "sleep_score.json"

    json_file = refs['sleep_json']#"bp.json"

    st.header("Sleep Score")

    if st.button("Calculate Sleep Score", key="sleep_btn"):
        try:
            result = get_sleep_score_json(
                json_file=json_file,
                age=st.session_state.age,
                sex=st.session_state.sex,
                sleep_hours=st.session_state.sleep_hours
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

            # if "band" in result:
            #     st.write(f"**Matched band:** {result['band']}")

            # st.json(result)

        except FileNotFoundError:
            st.error(f"JSON file not found: {json_file}")
        except Exception as e:
            st.error(f"Error calculating sleep score: {e}")


def render_bp_score(refs):
    # path = refs['BMI']
    json_file = refs['bp_json']#"bp.json"

    st.header("BP Score")

    if st.button("Calculate BP Score", key="bp_btn"):
        try:
            result = score_bp_from_json(
                json_file=json_file,
                sex=st.session_state.sex,
                age_years=st.session_state.age,
                height_cm=st.session_state.height_cm,
                systolic_bp=st.session_state.systolic_bp,
                diastolic_bp=st.session_state.diastolic_bp,
                treated=st.session_state.treated,
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

            # st.subheader("Matched Reference Row - Systolic")
            # st.json(result["reference_rows"]["systolic"])

            # st.subheader("Matched Reference Row - Diastolic")
            # st.json(result["reference_rows"]["diastolic"])

        except FileNotFoundError:
            st.error(f"JSON file not found: {json_file}")
        except Exception as e:
            st.error(f"Error calculating BP score: {e}")


def render_bmi_score(refs):
    st.header("BMI Score")
    # bmi_df = pd.read_csv("bmi.csv")
    path = refs['BMI']
    bmi_df = pd.read_csv(path)

    if st.button("Calculate BMI Score", key="bmi_btn"):
        try:
            result = score_bmi_from_df(
                bmi_df=bmi_df,
                sex=st.session_state.sex,
                age_years=st.session_state.age,
                weight_kg=st.session_state.weight_kg,
                height_cm=st.session_state.height_cm,
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

            # st.subheader("Matched Reference Row")
            # st.json(result["reference_row"])

        except Exception as e:
            st.error(f"Error calculating BMI score: {e}")


def render_vo2_score(refs):
    st.header("VO2_Peak_kg Percentile")

    if st.button("Calculate VO2 Percentile", key="vo2_btn"):
        try:
            result = score_measurement(
                metric="vo2",
                sex=st.session_state.sex,
                observed_value=st.session_state.vo2_value,
                age=st.session_state.age,
                refs = refs
            )

            st.markdown(
                f"""
                <div style="text-align:center;">
                    <h3>VO2 Percentile</h3>
                    <h1 style="color:green; font-size:80px;">{result['percentile_label']}</h1>
                    <h4>Percentile: {result['percentile']:.2f}</h4>
                    <h4>Z-score: {result['z_score']:.3f}</h4>
                </div>
                """,
                unsafe_allow_html=True
            )

            c1, c2 = st.columns(2)

            with c1:
                st.subheader("Inputs")
                st.write(f"**Sex:** {result['sex']}")
                st.write(f"**Age (years):** {result['x_value']}")
                st.write(f"**Observed VO2peak:** {result['observed_value']}")

            with c2:
                st.subheader("LMS Reference")
                st.write(f"**L:** {result['L']}")
                st.write(f"**M:** {result['M']}")
                st.write(f"**S:** {result['S']}")
                st.write(f"**Reference type:** {result['reference_type']}")

            # st.subheader("Result")
            # st.json(result)

        except Exception as e:
            st.error(f"Error calculating VO2 percentile: {e}")


def render_cimt_score(refs):
    st.header("cIMT Percentile")

    if st.button("Calculate cIMT Percentile", key="cimt_btn"):
        try:
            result = score_measurement(
                metric="cimt",
                sex=st.session_state.sex,
                observed_value=st.session_state.cimt_value,
                age=st.session_state.age,
                height=st.session_state.height_cm,
                refs = refs,
            )

            age_based = result.get("age_based")
            height_based = result.get("height_based")

            col1, col2 = st.columns(2)
            with col1:
                if age_based:
                    st.markdown(
                        f"""
                        <div style="text-align:center;">
                            <h3>cIMT Percentile by Age</h3>
                            <h1 style="color:green; font-size:80px;">{age_based['percentile_label']}</h1>
                            <h4>Percentile: {age_based['percentile']:.2f}</h4>
                            <h4>Z-score: {age_based['z_score']:.3f}</h4>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            with col2:
                if height_based:
                    st.markdown(
                        f"""
                        <div style="text-align:center;">
                            <h3>cIMT Percentile by Height</h3>
                            <h1 style="color:green; font-size:80px;">{height_based['percentile_label']}</h1>
                            <h4>Percentile: {height_based['percentile']:.2f}</h4>
                            <h4>Z-score: {height_based['z_score']:.3f}</h4>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            c1, c2 = st.columns(2)

            with c1:
                st.subheader("Inputs")
                st.write(f"**Sex:** {result['sex']}")
                st.write(f"**Age (years):** {st.session_state.age}")
                st.write(f"**Height (cm):** {st.session_state.height_cm}")
                st.write(f"**Observed cIMT:** {result['observed_value']:.3f}")

            with c2:
                st.subheader("Summary")
                if age_based:
                    st.write(f"**Age-based percentile:** {age_based['percentile']:.2f}")
                    st.write(f"**Age-based label:** {age_based['percentile_label']}")
                    st.write(f"**Age-based z-score:** {age_based['z_score']:.3f}")
                if height_based:
                    st.write(f"**Height-based percentile:** {height_based['percentile']:.2f}")
                    st.write(f"**Height-based label:** {height_based['percentile_label']}")
                    st.write(f"**Height-based z-score:** {height_based['z_score']:.3f}")

            # if age_based:
            #     st.subheader("Age-based LMS Reference")
            #     st.write(f"**L:** {age_based['L']}")
            #     st.write(f"**M:** {age_based['M']}")
            #     st.write(f"**S:** {age_based['S']}")
            #     st.json(age_based)

            # if height_based:
            #     st.subheader("Height-based LMS Reference")
            #     st.write(f"**L:** {height_based['L']}")
            #     st.write(f"**M:** {height_based['M']}")
            #     st.write(f"**S:** {height_based['S']}")
            #     st.json(height_based)

        except Exception as e:
            st.error(f"Error calculating cIMT percentile: {e}")



def render_wrPeak_score(refs):
    st.header("WR Peak/kg Percentile")

    if st.button("Calculate WR Peak Percentile", key="wrpeak_btn"):
        try:
            result = score_measurement(
                metric="wr_peak",
                sex=st.session_state.sex,
                observed_value=st.session_state.wr_peak_value,
                age=st.session_state.age,
                refs=refs,
            )

            st.markdown(
                f"""
                <div style="text-align:center;">
                    <h3>WR Peak/kg Percentile</h3>
                    <h1 style="color:green; font-size:80px;">{result['percentile_label']}</h1>
                    <h4>Percentile: {result['percentile']:.2f}</h4>
                    <h4>Z-score: {result['z_score']:.3f}</h4>
                </div>
                """,
                unsafe_allow_html=True
            )

            c1, c2 = st.columns(2)

            with c1:
                st.subheader("Inputs")
                st.write(f"**Sex:** {result['sex']}")
                st.write(f"**Age (years):** {result['x_value']}")
                st.write(f"**Observed WR Peak/kg:** {result['observed_value']}")

            with c2:
                st.subheader("LMS Reference")
                st.write(f"**L:** {result['L']}")
                st.write(f"**M:** {result['M']}")
                st.write(f"**S:** {result['S']}")
                st.write(f"**Reference type:** {result['reference_type']}")

        except Exception as e:
            st.error(f"Error calculating WR Peak percentile: {e}")