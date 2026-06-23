import streamlit as st
import pandas as pd
import numpy as np
import math
import plotly.graph_objects as go
import streamlit as st



from utils import (
    get_sleep_score_json,
    score_bp_from_json,
    score_bmi_from_df,
    score_measurement,
    # score_baPWV_peak,
    # score_grip_strength, 
)



def init_measurement_state():
    defaults = {
        "sex": "boys",
        "age": 10.0,
        "height_cm": 140.0,
        "weight_kg": 35.0,
        "sleep_hours": 9.0,
        "grip_strength": 4.0,
        "systolic_bp": 110.0,
        "diastolic_bp": 70.0,
        "treated": False,
        "vo2_value": 45.0,
        "wr_peak_value": 3.20,
        "baPWV_peak_value":842.0,
        "cimt_value": 0.50,
        "momo": 10.0, 
        "kidscreen_value":10.0, 
        "non_hdl":10.0,
        "hb1ac":10.0, 
        "paq_c":10.0, 
        "paq_a":10.0, 
        "pdq":10.0, 
        'smoking': 10.0, 
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def render_measurement_inputs():
    init_measurement_state()
    
    col1, col2, col3, col4 = st.columns(4, border = True, gap = 'xxsmall')
    with col1:
        age = st.number_input(
            "Age (years)",
            min_value=0.0,
            max_value=25.0,
            value=float(st.session_state.age),
            step=0.1,
            key="input_age"
        )
        st.session_state.age = age

        sex = st.selectbox(
            "Sex",
            ["boys", "girls"],
            index=0 if st.session_state.sex == "boys" else 1,
            key="input_sex"
        )
        st.session_state.sex = sex

        height_cm = st.number_input(
            "Height (cm)",
            min_value=30.0,
            max_value=250.0,
            value=float(st.session_state.height_cm),
            step=0.1,
            key="input_height"
        )
        st.session_state.height_cm = height_cm

        weight_kg = st.number_input(
            "Weight (kg)",
            min_value=1.0,
            max_value=300.0,
            value=float(st.session_state.weight_kg),
            step=0.1,
            key="input_weight"
        )
        st.session_state.weight_kg = weight_kg

        hb1ac = st.number_input(
                "Hb1Ac",
                min_value=0.0,
                max_value=150.0,
                value=float(st.session_state.hb1ac),
                step=1.0,
                key="input_hb1ac"
            )
        st.session_state.hb1ac = hb1ac
        st.session_state.score['Blutzucker'] = hb1ac

        non_hdl = st.number_input(
                "Non-HDL cholesterol",
                min_value=0.0,
                max_value=150.0,
                value=float(st.session_state.non_hdl),
                step=1.0,
                key="input_nonHDL"
            )
        st.session_state.non_hdl = non_hdl
        st.session_state.score['Blutfette'] = non_hdl
    
    
    with col2:
        systolic_bp = st.number_input(
            "Systolic BP",
            min_value=40.0,
            max_value=250.0,
            value=float(st.session_state.systolic_bp),
            step=1.0,
            key="input_sys"
        )
        st.session_state.systolic_bp = systolic_bp

        diastolic_bp = st.number_input(
            "Diastolic BP",
            min_value=20.0,
            max_value=150.0,
            value=float(st.session_state.diastolic_bp),
            step=1.0,
            key="input_dia"
        )
        st.session_state.diastolic_bp = diastolic_bp


        treated = st.checkbox(
            "BP Treated",
            value=bool(st.session_state.treated),
            key="input_treated"
        )
        st.session_state.treated = treated

        if age >=12:
            baPWV_value = st.number_input(
                "baPWV",
                min_value=800.0,
                max_value=1500.0,
                value=float(st.session_state.baPWV_peak_value),
                step=0.01,
                format="%.2f",
                key="input_baPWV"
            )
            st.session_state.baPWV_peak_value = baPWV_value

        if age >=14:
            cimt_value = st.number_input(
                "cIMT",
                min_value=0.49,
                max_value=2.0,
                value=float(st.session_state.cimt_value),
                step=0.001,
                format="%.3f",
                key="input_cimt"
            )
            st.session_state.cimt_value = cimt_value
            
    
    
    with col3:
        
        grip_strength = st.number_input(
            "Grip Strength",
            min_value=4.0,
            max_value=300.0,
            value=float(st.session_state.grip_strength),
            step=1.0,
            key="grip strength"
        )
        st.session_state.grip_strength_value = grip_strength
    
        momo = st.number_input(
            "Standing long jump",
            min_value=10.0,
            # max_value=100.0, 
            value=float(st.session_state.momo),
            step=0.1,
            key="input_momo"
        )
        st.session_state.momo_value = momo


        vo2_value = st.number_input(
            "VO2peak/kg",
            min_value=0.1,
            max_value=100.0,
            value=float(st.session_state.vo2_value),
            step=0.1,
            key="input_vo2"
        )
        st.session_state.vo2_value = vo2_value


        wr_peak_value = st.number_input(
            "WRpeak/kg",
            min_value=3.0,
            max_value=6.0,
            value=float(st.session_state.wr_peak_value),
            step=0.01,
            format="%.2f",
            key="input_wr_peak"
        )
        st.session_state.wr_peak_value = wr_peak_value


    
    with col4:
    
        if age <=13:
            paq_c = st.number_input(
                "PAQ_C score",
                min_value=0.0,
                max_value=100.0, 
                value=float(st.session_state.paq_c),
                step=0.1,
                key="input_paq_c"
            )
            st.session_state.paq_c = paq_c
            st.session_state.score['Körperliche Aktivität'] = paq_c

        if age >13:
            paq_a = st.number_input(
                "PAQ_A score",
                min_value=0.0,
                max_value=100.0, 
                value=float(st.session_state.paq_a),
                step=0.1,
                key="input_paq_a"
            )
            st.session_state.paq_a = paq_a
            st.session_state.score['Körperliche Aktivität'] = paq_a

        pdq = st.number_input(
                "PDQ score",
                min_value=0.0,
                max_value=100.0, 
                value=float(st.session_state.pdq),
                step=0.1,
                key="input_pdq"
            )
        st.session_state.pdq = pdq
        st.session_state.score['Ernährung'] = pdq

        smoking = st.number_input(
            "Smoking score",
            min_value=0.0,
            max_value=100.0, 
            value=float(st.session_state.smoking),
            step=0.1,
            key="input_smoking"
        )
        st.session_state.smoking = smoking
        st.session_state.score['Nikotin'] = smoking


        sleep_hours = st.number_input(
            "Sleep hours",
            min_value=0.0,
            max_value=24.0,
            value=float(st.session_state.sleep_hours),
            step=0.1,
            key="input_sleep"
        )
        st.session_state.sleep_hours = sleep_hours

        kid_screen = st.number_input(
            "KIDSCREEN",
            min_value=10.0,
            max_value=100.0, 
            value=float(st.session_state.kidscreen_value),
            step=0.1,
            key="input_kidScreen"
        )
        st.session_state.kidscreen_value = kid_screen


    st.success("Measurements saved to session state.")




def z_to_percentile(z):
    # st.write(z)
    return 100 * (0.5 * (1 + math.erf(z / math.sqrt(2))))



def render_sleep_score(refs):
    # json_file = "sleep_score.json"

    json_file = refs['sleep_json']#"bp.json"

    st.header("Sleep")

    if st.button("Calculate Score", key="sleep_btn"):
        try:
            result = get_sleep_score_json(
                json_file=json_file,
                age=st.session_state.age,
                sex=st.session_state.sex,
                sleep_hours=st.session_state.sleep_hours
            )

            st.markdown(
                f"<h3 style='text-align:center; color:green;'>{result['score']}</h1>",
                # f"<h3 style='text-align:center; color:green;'>Sleep Score: {result['score']}</h1>",

                unsafe_allow_html=True
            )
            st.session_state.score['sleep_score'] = result['score']

            with st.expander("Reference Row", expanded=False):
                st.write(f"**Age group:** {result['age_group']}")
                st.write(f"**Mean (h):** {result['mean_h']}")
                st.write(f"**SD (h):** {result['sd_h']}")
                st.write(f"**Upper cut-off:** {result['upper_cutoff']}")
                st.write(f"**Lower cut-off:** {result['lower_cutoff']}")

        except FileNotFoundError:
            st.error(f"JSON file not found: {json_file}")
        except Exception as e:
            st.error(f"Error calculating sleep score: {e}")





def render_bp_score(refs):
    # path = refs['BMI']
    json_file = refs['bp_json']#"bp.json"

    st.header("BP")

    if st.button("Calculate Score", key="bp_btn"):
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
            st.session_state.score['bp_score'] = result['score']
            st.markdown(
                f"<h3 style='text-align:center; color:green;'>{result['score']}</h1>",
                # f"<h3 style='text-align:center; color:green;'>BP Score: {result['score']}</h1>",
                unsafe_allow_html=True
            )

            

            with st.expander("Reference Row", expanded=False):
                st.subheader("Component Scores")
                st.write(f"**Systolic score:** {result['component_scores']['systolic_score']}")
                st.write(f"**Diastolic score:** {result['component_scores']['diastolic_score']}")
                st.write("Matched Reference Row - Systolic")
                st.json(result["reference_rows"]["systolic"])
                st.write("Matched Reference Row - Diastolic")
                st.json(result["reference_rows"]["diastolic"])


        except FileNotFoundError:
            st.error(f"JSON file not found: {json_file}")
        except Exception as e:
            st.error(f"Error calculating BP score: {e}")



def render_bmi_score(refs):
    st.header("BMI")
    path = refs['BMI']
    bmi_df = pd.read_csv(path)

    if st.button("Calculate Score", key="bmi_btn"):
        try:
            result = score_bmi_from_df(
                bmi_df=bmi_df,
                sex=st.session_state.sex,
                age_years=st.session_state.age,
                weight_kg=st.session_state.weight_kg,
                height_cm=st.session_state.height_cm,
            )

            score = result["score"]
            st.session_state.score['bmi_score'] = result['score']
            bmi_value = result["inputs"]["bmi"]

            color = "green"
            if score == 70:
                color = "orange"
            elif score in [30, 0]:
                color = "red"

            st.markdown(
                f"<h3 style='text-align:center; color:green;'{score}</h1>",
                # f"<h3 style='text-align:center; color:green;'>BMI Score: {score}</h1>",
                unsafe_allow_html=True
            )

            
            with st.expander("Reference Row", expanded=False):
                st.write(f"**BMI:** {bmi_value}")
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



def render_vo2_Percentile(refs):
    st.header("VO2peak/kg")

    if st.button("Calculate Percentile", key="vo2_btn"):
        try:
            result = score_measurement(
                metric="vo2",
                sex=st.session_state.sex,
                observed_value=st.session_state.vo2_value,
                age=st.session_state.age,
                refs = refs
            )
            st.session_state.score['vo2_score'] = result['z_score']
            st.markdown(
                f"<h3 style='text-align:center; color:green;'>{result['percentile']:.2f} % </h1>",
                # f"<h3 style='text-align:center; color:green;'>VO2 Percentile: {result['percentile_label']}</h1>",
                unsafe_allow_html=True
            )


            with st.expander("LMS Reference", expanded=False):
                st.write(f"Percentile: {result['percentile']:.2f}")
                st.write(f"Z-score: {result['z_score']:.3f}")
                st.write(f"**L:** {result['L']}")
                st.write(f"**M:** {result['M']}")
                st.write(f"**S:** {result['S']}")
                st.write(f"**Reference type:** {result['reference_type']}")

        except Exception as e:
            st.error(f"Error calculating VO2 percentile: {e}")



def render_cimt_Percentile(refs):
    st.header("cIMT")

    if st.button("Calculate Percentile", key="cimt_btn"):
        try:
            result = score_measurement(
                metric="cimt",
                sex=st.session_state.sex,
                observed_value=st.session_state.cimt_value,
                age=st.session_state.age,
                height=st.session_state.height_cm,
                refs=refs,
            )

            if not result.get("possible", False):
                st.warning(result.get("message", "cIMT scoring not possible."))
                return

            percentile_label = result.get("percentile_label", "NA")
            percentile_numeric = result.get("percentile_numeric", "NA")
            # display = "NA" if percentile_numeric is None else f"{percentile_numeric:.1f}

            st.markdown(
                f"<h3 style='text-align:center; color:green;'>{percentile_numeric} % </h1>",
                # f"""
                # <div style="text-align:center;">

                #     <h3 style="color:green; font-size:50px;>{"NA" if percentile_numeric is None else f"{percentile_numeric:.1f}"}></h1>
                # </div>
                # """,
                unsafe_allow_html=True,
            )

            # st.markdown(
            #     f"""
            #     <div style="text-align:center;">
            #         <h3>cIMT Percentile</h3>
            #         <h2 style="color:green; font-size:50px;">{percentile_label}</h2>
            #         <h4>Percentile: {"NA" if percentile_numeric is None else f"{percentile_numeric:.1f}"}</h4>
            #     </div>
            #     """,
            #     unsafe_allow_html=True,
            # )

            with st.expander("Summary", expanded=False):
                st.write(f"**Observed cIMT:** {result['observed_value']}")
                st.write(f"**Sex:** {result['sex']}")
                st.write(f"**Age input:** {result['age_input']}")
                st.write(f"**Age used:** {result['age_used']}")
                st.write(f"**Height input:** {result['height_input']}")
                st.write(f"**Height reference mode:** {result['height_reference_mode']}")

                ref_cutpoints = result.get("reference_cutpoints", {})
                if ref_cutpoints:
                    st.write("**Reference cutpoints:**")
                    for k, v in ref_cutpoints.items():
                        st.write(f"- {k}: {v:.5f}")


        except Exception as e:
            st.error(f"Error calculating cIMT percentile: {e}")


def render_wrPeak_percentile(refs):
    st.header("WRpeak/kg")

    if st.button("Calculate Percentile", key="wrpeak_btn"):
        try:
            result = score_measurement(
                metric="wr_peak",
                sex=st.session_state.sex,
                observed_value=st.session_state.wr_peak_value,
                age=st.session_state.age,
                refs=refs,
            )
            st.markdown(
                f"<h3 style='text-align:center; color:green;'>{result['percentile']:.2f} % </h1>",
                unsafe_allow_html=True
            )
       
            # st.markdown(
            #     f"<h3 style='text-align:center; color:green;'>{result['percentile_label']} {result['percentile']:.2f}</h1>",
            #     unsafe_allow_html=True
            # )
            st.session_state.score['wr_score'] = result['z_score']

            with st.expander("Reference Row", expanded=False):
                st.write(f"Percentile: {result['percentile']:.2f}")
                st.write(f"Z-score: {result['z_score']:.3f}")
                st.write(f"**L:** {result['L']}")
                st.write(f"**M:** {result['M']}")
                st.write(f"**S:** {result['S']}")
                st.write(f"**Reference type:** {result['reference_type']}")

        except Exception as e:
            st.error(f"Error calculating WR Peak percentile: {e}")


def render_baPWV_percentile(refs):
    st.header("baPWV")

    if st.button("Calculate Percentile", key="bapwvpeak_btn"):
        try:
            result = score_measurement(
                metric="baPWV_peak",
                sex=st.session_state.sex,
                observed_value=st.session_state.baPWV_peak_value,
                age=st.session_state.age,
                refs=refs,
            )

            if not result.get("possible", True):
                st.warning(result.get("message", "Not possible for age <= 12"))
                return

            st.markdown(
                f"<h3 style='text-align:center; color:green;'>{result['percentile']:.2f} % </h3>",
                unsafe_allow_html=True
            )

            st.session_state.score['bapwv_score'] = result['z_score']

            with st.expander("Reference Row", expanded=False):
                st.write(f"Percentile: {result['percentile']:.2f}, {result['percentile_label']}")
                st.write(f"Z-score: {result['z_score']:.3f}")
                st.write(f"**L:** {result['L']}")
                st.write(f"**M:** {result['M']}")
                st.write(f"**S:** {result['S']}")
                st.write(f"**Reference type:** {result['reference_type']}")

        except Exception as e:
            st.error(f"Error calculating baPWV Peak percentile: {e}")



def render_momo_score(refs):
    st.header("Standing long jump")

    if st.button("Calculate Percentile", key="momo_btn"):
        try:
            result = score_measurement(
                metric="momo",
                sex=st.session_state.sex,
                observed_value=st.session_state.momo_value,
                age=st.session_state.age,
                refs=refs,
            )

            if not result.get("possible", True):
                st.warning(result.get("message", "MOMO percentile not possible"))
                return

            st.markdown(
                f"<h3 style='text-align:center; color:green;'>{result['percentile_label']} % </h3>",
                unsafe_allow_html=True
            )

            st.session_state.score["momo_score"] = result["z_score_label"]

            with st.expander("Reference row", expanded=False):
                st.write(f"Observed value: {result['observed_value']:.2f}")
                st.write(f"Matched age: {result['age_used']}")
                st.write(f"Reference SW: {result['reference_value']:.2f}")
                st.write(f"Percentile rank: {result['percentile_label']}")
                st.write(f"Z-score: {result['z_score_label']}")
                st.write(f"Reference type: {result['reference_type']}")

        except Exception as e:
            st.error(f"Error calculating MOMO percentile: {e}")

def render_gripStrength_score(refs):
    st.header("Grip Strength")

    if st.button("Calculate Percentile", key="gripstrength_btn"):
        try:
            
            result = score_measurement(
                metric="grip_strength",
                sex=st.session_state.sex,
                observed_value=st.session_state.grip_strength_value,
                age=st.session_state.age,
                refs=refs,
            )
            # st.write(result)

            if not result.get("possible", True):
                st.warning(result.get("message", "Grip strength percentile not possible"))
                return

            st.markdown(
                f"<h3 style='text-align:center; color:green;'>{result['percentile_label']} % </h3>",
                unsafe_allow_html=True
            )

            st.session_state.score["grip_score"] = result["percentile_label"]

            with st.expander("Reference Row", expanded=False):
                st.write(f"Observed grip strength: {result['observed_value']:.2f} kg")
                st.write(f"Matched age: {result['age_used']}")
                st.write(f"Reference grip strength: {result['reference_value']:.2f} kg")
                st.write(f"Percentile: {result['percentile_label']}")
                st.write(f"Reference type: {result['reference_type']}")

        except Exception as e:
            st.error(f"Error calculating Grip Strength percentile: {e}")



def render_KidScreen_percentile(refs):
    st.header("KIDSCREEN")

    if st.button("Calculate Percentile", key="kidscreen_btn"):
        try:
            result = score_measurement(
                metric="kidScreen",
                sex=st.session_state.sex,
                observed_value=st.session_state.kidscreen_value,
                age=st.session_state.age,
                refs=refs,
            )

            if not result.get("possible", True):
                st.warning(result.get("message", "KidScreen scoring not possible"))
                return

            st.markdown(
                f"<h3 style='text-align:center; color:green;'>{result['score_0_100']:.2f}</h3>",
                unsafe_allow_html=True
            )

            st.session_state.score["kidscreen_score"] = result["score_0_100"]
            

            with st.expander("Reference Row", expanded=False):
                st.write(f"Observed raw score: {result['observed_value']:.2f}")
                st.write(f"Raw score used: {result['raw_score']}")
                st.write(f"Age group: {result['age_group']}")
                st.write(f"0-100 Score: {result['score_0_100']:.2f}")
                st.write(f"Percentile rank: {result['percentile_label']}")
                st.write(f"T-score: {result['t_score']}")
                st.write(f"Reference type: {result['reference_type']}")

        except Exception as e:
            st.error(f"Error calculating KidScreen score: {e}")




def _render_star_plot(score_dict):
    plot_scores = {}

    if "Blutzucker" in score_dict:
        plot_scores["Blutzucker"] = float(score_dict["Blutzucker"])

    if "Blutfette" in score_dict:
        plot_scores["Blutfette"] = float(score_dict["Blutfette"])

    if "bmi_score" in score_dict:
        plot_scores["BMI"] = float(score_dict["bmi_score"])

    if "bp_score" in score_dict:
        plot_scores["Blutdruck"] = float(score_dict["bp_score"])

    if "Körperliche Aktivität" in score_dict:
        plot_scores["Körperliche Aktivität"] = float(score_dict["Körperliche Aktivität"])

    if "Ernährung" in score_dict:
        plot_scores["Ernährung"] = float(score_dict["Ernährung"])

    if "sleep_score" in score_dict:
        plot_scores["Schlaf"] = float(score_dict["sleep_score"])

    if "Nikotin" in score_dict:
        plot_scores["Nikotin"] = float(score_dict["Nikotin"])

    if not plot_scores:
        st.warning("No scores available for spider chart.")
        return

    categories = list(plot_scores.keys())
    values = [max(0, min(100, v)) for v in plot_scores.values()]
    mean_score = sum(values) / len(values)

    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]

    fig = go.Figure()

    # main spider / radar polygon only
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        mode="lines+markers",
        fill="toself",
        line=dict(color="rgb(0,82,20)", width=3),
        marker=dict(
            size=10,
            color=values,
            colorscale="RdYlGn",
            cmin=0,
            cmax=100,
            line=dict(color="black", width=1.2)
        ),
        fillcolor="rgba(70, 160, 90, 0.28)",
        hovertemplate="%{theta}: %{r:.1f}<extra></extra>",
        showlegend=False
    ))

    # optional outer frame
    fig.add_trace(go.Scatterpolar(
        r=[100] * len(categories_closed),
        theta=categories_closed,
        mode="lines",
        line=dict(color="rgba(0,0,0,0.18)", width=1.5, dash="dot"),
        hoverinfo="skip",
        showlegend=False
    ))

    # center white circle + average
    fig.add_shape(
        type="circle",
        xref="paper",
        yref="paper",
        x0=0.435,
        y0=0.435,
        x1=0.565,
        y1=0.565,
        line=dict(color="rgba(0,0,0,0.18)", width=1.5),
        fillcolor="white",
        layer="above"
    )

    fig.add_annotation(
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        text=f"<b>{mean_score:.0f}</b><br><span style='font-size:12px'>GESAMTSCORE</span>",
        showarrow=False,
        align="center",
        font=dict(color="rgb(0,51,102)", size=18),
        xanchor="center",
        yanchor="middle"
    )

    fig.update_layout(
        title=dict(
            text="SPIDERWEB CHART",
            x=0.5,
            xanchor="center",
            font=dict(size=20, color="rgb(10,30,50)")
        ),
        polar=dict(
            bgcolor="white",
            gridshape="linear",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickvals=[20, 40, 60, 80, 100],
                tickfont=dict(size=12, color="black"),
                gridcolor="rgba(0,0,0,0.10)",
                gridwidth=1,
                linecolor="rgba(0,0,0,0.15)",
                angle=90
            ),
            angularaxis=dict(
                tickfont=dict(size=15, color="black"),
                gridcolor="rgba(0,0,0,0.14)",
                linecolor="rgba(0,0,0,0.18)",
                rotation=90,
                direction="clockwise"
            )
        ),
        showlegend=False,
        paper_bgcolor="white",
        plot_bgcolor="white",
        height=800,
        margin=dict(l=80, r=80, t=100, b=80)
    )

    st.plotly_chart(fig, use_container_width=True)


def render_star_plot(score_dict):
    plot_scores = {}

    
    if "Blutzucker" in score_dict:
        plot_scores["Blutzucker"] = float(score_dict["Blutzucker"]) #float(100 - z_to_percentile(score_dict["Blutzucker"]))
        
    if "Blutfette" in score_dict:
        plot_scores["Blutfette"] = float(score_dict["Blutfette"]) #float(z_to_percentile(score_dict["wr_score"]))

    if "bmi_score" in score_dict:
        plot_scores["BMI"] = float(score_dict["bmi_score"])

    if "bp_score" in score_dict:
        plot_scores["Blutdruck"] = float(score_dict["bp_score"])

    if "Körperliche Aktivität" in score_dict:
        plot_scores["Körperliche Aktivität"] = float(score_dict["Körperliche Aktivität"])

    if "Ernährung" in score_dict:
        plot_scores["Ernährung"] = float(score_dict["Ernährung"])
    
    if "sleep_score" in score_dict:
        plot_scores["Schlaf"] = float(score_dict["sleep_score"])

    if "Nikotin" in score_dict:
        plot_scores["Nikotin"] = float(score_dict["Nikotin"])

    if not plot_scores:
        st.warning("No scores available for spider chart.")
        return

    st.write(plot_scores)
    categories = list(plot_scores.keys())
    values = [max(0, min(100, v)) for v in plot_scores.values()]
    mean_score = sum(values) / len(values)

    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]

    fig = go.Figure()

    def interp_color(v):
        v = max(0.0, min(100.0, float(v)))

        if v <= 50:
            t = v / 50.0
            r = 220 + (255 - 220) * t
            g = 20 + (140 - 20) * t
            b = 60 + (0 - 60) * t
        else:
            t = (v - 50) / 50.0
            r = 255 + (46 - 255) * t
            g = 140 + (204 - 140) * t
            b = 0 + (113 - 0) * t

        return f"rgba({int(r)}, {int(g)}, {int(b)}, 0.95)"

    # many thin rings for smooth gradient
    gradient_levels = np.linspace(1000, 10, 800)

    for level in gradient_levels:
        fig.add_trace(go.Scatterpolar(
            r=[level] * len(categories_closed),
            theta=categories_closed,
            fill="toself",
            fillcolor=interp_color(level),
            line=dict(color="rgba(0,0,0,0)"),
            hoverinfo="skip",
            showlegend=False
        ))

    # faded outer/background overlay
    fig.add_trace(go.Scatterpolar(
        r=[100] * len(categories_closed),
        theta=categories_closed,
        # fill="toself",
        fill="none",
        fillcolor="rgba(255,255,255,0.90)",
        line=dict(color="rgba(0,0,0,0)"),
        hoverinfo="skip",
        showlegend=False
    ))

    # vivid spider area
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        mode="lines+markers",
        fill="toself",
        line=dict(color="white", width=2),
        marker=dict(size=5, color="rgb(0,82,20)"),
        fillcolor="rgba(102,178,255,0.22)",
        hovertemplate="%{theta}: %{r:.1f}<extra></extra>",
        showlegend=False, 
        # layer = 'above'
    ))

    # central total average score
    fig.add_shape(
        type="circle",
        xref="paper",
        yref="paper",
        x0=0.45,
        y0=0.45,
        x1=0.55,
        y1=0.55,
        line=dict(color="white", width=0.5),
        # fillcolor="white",
        # layer="above", 
        layer="below"
    )

    fig.add_annotation(
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        text=f"<b style='font-size:20px'>{mean_score:.0f}</b><br><span style='font-size:12px'>GESAMTSCORE</span>",
        showarrow=False,
        align="center",
        font=dict(color="rgb(255,255,255)"),
        xanchor="center",
        yanchor="middle"
    )

    fig.update_layout(
        title=dict(
            text="CVH CHART",
            x=0.5,
            xanchor="center",
            font=dict(size=20, color="rgb(10,30,50)")
        ),
        polar=dict(
            bgcolor="white",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickvals=[20, 40, 60, 80, 100],
                tickfont=dict(size=12, color="black"),
                gridcolor="rgba(255,255,255,0.92)",
                gridwidth=1,
                # showline=False,
                angle=90
            ),
            angularaxis=dict(
                tickfont=dict(size=16, color="black"),
                gridcolor="rgba(0,0,0,0.35)",
                linecolor="rgba(0,0,0,0.35)",
                rotation=90,
                direction="clockwise",
                showline=False,
            )
        ),
        showlegend=False,
        paper_bgcolor="white",
        plot_bgcolor="white",
        height=900,
        # margin=dict(l=80, r=80, t=120, b=80)
    )

    st.plotly_chart(fig, use_container_width=True)

 

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
   



import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import streamlit as st




import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import streamlit as st


def render_score_bars_gradient(score_dict):
    plot_scores = {}

    if "Blutzucker" in score_dict:
        plot_scores["Blutzucker"] = float(score_dict["Blutzucker"])

    if "Blutfette" in score_dict:
        plot_scores["Blutfette"] = float(score_dict["Blutfette"])

    if "bmi_score" in score_dict:
        plot_scores["BMI"] = float(score_dict["bmi_score"])

    if "bp_score" in score_dict:
        plot_scores["Blutdruck"] = float(score_dict["bp_score"])

    if "Körperliche Aktivität" in score_dict:
        plot_scores["Körperliche Aktivität"] = float(score_dict["Körperliche Aktivität"])

    if "Ernährung" in score_dict:
        plot_scores["Ernährung"] = float(score_dict["Ernährung"])

    if "sleep_score" in score_dict:
        plot_scores["Schlaf"] = float(score_dict["sleep_score"])

    if "Nikotin" in score_dict:
        plot_scores["Nikotin"] = float(score_dict["Nikotin"])

    if not plot_scores:
        st.warning("No scores available for bar chart.")
        return

    categories = list(plot_scores.keys())
    values = [max(0, min(100, float(v))) for v in plot_scores.values()]

    sns.set_style("whitegrid")

    cmap = mpl.colors.LinearSegmentedColormap.from_list(
        "score_map",
        ["#d73027", "#fee08b", "#1a9850"]
    )

    fig, axes = plt.subplots(
        nrows=2,
        ncols=4,
        figsize=(18, 7),
        sharex=True
    )

    axes_flat = axes.flatten()

    for ax, cat, val in zip(axes_flat, categories, values):
        grad = np.linspace(0, 1, 600).reshape(1, -1)

        ax.imshow(
            grad,
            extent=[0, 100, -0.22, 0.22],
            aspect="auto",
            cmap=cmap,
            interpolation="bicubic",
            zorder=1
        )

        border = plt.Rectangle(
            (0, -0.22), 100, 0.44,
            fill=False,
            edgecolor="lightgray",
            linewidth=1.0,
            zorder=2
        )
        ax.add_patch(border)

        ax.axvline(
            val,
            ymin=0.32,
            ymax=0.68,
            color="black",
            linewidth=3,
            zorder=3
        )

        ax.scatter(
            val, 0,
            s=35,
            color="white",
            edgecolor="black",
            linewidth=1,
            zorder=4
        )

        # x_text = min(max(val, 6), 94)
        x_text = val
        ax.text(
            x_text,
            0.33,
            f"{val:.1f}",
            ha="center",
            va="bottom",
            fontsize=18,
            fontweight="bold",
            color="black",
            bbox=dict(
                boxstyle="round,pad=0.2",
                fc="white",
                ec="none",
                alpha=0.95
            ),
            zorder=10
        )

        ax.annotate(
            f"{val:.1f}",
            xy=(val, 0.22),
            xytext=(x_text, 0.40),
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
            color="black",
            bbox=dict(
                boxstyle="round,pad=0.2",
                fc="white",
                ec="none",
                alpha=0.95
            ),
            arrowprops=dict(
                arrowstyle="-",
                color="black",
                lw=1.0
            ),
            zorder=5
        )

        ax.set_title(cat, fontsize=12, fontweight="bold", pad=10)
        ax.set_xlim(0, 100)
        ax.set_ylim(-0.6, 0.6)
        ax.set_yticks([])
        ax.set_xticks([0, 25, 50, 75, 100])
        ax.tick_params(axis="x", labelsize=9)

        for spine in ["top", "right", "left"]:
            ax.spines[spine].set_visible(False)

    for ax in axes_flat[len(categories):]:
        ax.axis("off")

    fig.suptitle("CVH Score Overview", fontsize=18, fontweight="bold", y=1.02)
    fig.tight_layout()

    st.pyplot(fig)