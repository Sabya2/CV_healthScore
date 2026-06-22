import streamlit as st
import pandas as pd
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
        "baPWV_peak_value":3.0,
        "cimt_value": 0.50,
        "momo": 10.0, 
        "kidscreen_value":10.0, 
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
    with col2:
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
        st.session_state.systolic_bp = systolic_bp
        st.session_state.diastolic_bp = diastolic_bp


        treated = st.checkbox(
            "BP Treated",
            value=bool(st.session_state.treated),
            key="input_treated"
        )
        st.session_state.treated = treated

    with col3:
        sleep_hours = st.number_input(
            "Sleep hours",
            min_value=0.0,
            max_value=24.0,
            value=float(st.session_state.sleep_hours),
            step=0.1,
            key="input_sleep"
        )
        st.session_state.sleep_hours = sleep_hours

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
            "Standing long jump momo",
            min_value=10.0,
            # max_value=100.0, 
            value=float(st.session_state.momo),
            step=0.1,
            key="input_momo"
        )
        st.session_state.momo_value = momo

        kid_screen = st.number_input(
            "kid screen",
            min_value=10.0,
            max_value=100.0, 
            value=float(st.session_state.kidscreen_value),
            step=0.1,
            key="input_kidScreen"
        )

        st.session_state.kidscreen_value = kid_screen

    with col4:
        vo2_value = st.number_input(
            "VO2 peak",
            min_value=0.1,
            max_value=100.0,
            value=float(st.session_state.vo2_value),
            step=0.1,
            key="input_vo2"
        )
        st.session_state.vo2_value = vo2_value


        cimt_value = st.number_input(
            "CIMT",
            min_value=0.001,
            max_value=2.0,
            value=float(st.session_state.cimt_value),
            step=0.001,
            format="%.3f",
            key="input_cimt"
        )
        st.session_state.cimt_value = cimt_value


        wr_peak_value = st.number_input(
            "WR peak",
            min_value=3.0,
            max_value=6.0,
            value=float(st.session_state.wr_peak_value),
            step=0.01,
            format="%.2f",
            key="input_wr_peak"
        )
        st.session_state.wr_peak_value = wr_peak_value

        if age >=12:
            baPWV_value = st.number_input(
                "baPWV",
                min_value=0.0,
                max_value=60.0,
                value=float(st.session_state.baPWV_peak_value),
                step=0.01,
                format="%.2f",
                key="input_baPWV"
            )
            st.session_state.baPWV_peak_value = baPWV_value

    # st.session_state.sex = sex
    # st.session_state.age = age
    # st.session_state.height_cm = height_cm
    # st.session_state.weight_kg = weight_kg
    # st.session_state.sleep_hours = sleep_hours
    # st.session_state.treated = treated
    # # st.session_state.grip_strength = grip_strength
    # # st.session_state.systolic_bp = systolic_bp
    # # st.session_state.diastolic_bp = diastolic_bp
    # # st.session_state.vo2_value = vo2_value
    # # st.session_state.cimt_value = cimt_value
    # # st.session_state.wr_peak_value = wr_peak_value
    # st.session_state.momo_value = momo
    # st.session_state.kidscreen_value = momo
    # st.session_state.bapwv_peak_value = momo
    

    st.success("Measurements saved to session state.")




def z_to_percentile(z):
    # st.write(z)
    return 100 * (0.5 * (1 + math.erf(z / math.sqrt(2))))



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

            st.markdown(
                f"<h3 style='text-align:center; color:green;'>Sleep Score: {result['score']}</h1>",
                unsafe_allow_html=True
            )
            st.session_state.score['sleep_score'] = result['score']

            with st.expander("Show matched reference rows", expanded=False):
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
            st.session_state.score['bp_score'] = result['score']
            st.markdown(
                f"<h3 style='text-align:center; color:green;'>BP Score: {result['score']}</h1>",
                unsafe_allow_html=True
            )

            

            with st.expander("Show matched reference rows", expanded=False):
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
            st.session_state.score['bmi_score'] = result['score']
            bmi_value = result["inputs"]["bmi"]

            color = "green"
            if score == 70:
                color = "orange"
            elif score in [30, 0]:
                color = "red"

            st.markdown(
                f"<h3 style='text-align:center; color:green;'>BMI Score: {score}</h1>",
                unsafe_allow_html=True
            )

            
            with st.expander("Show matched reference rows", expanded=False):
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
            st.session_state.score['vo2_score'] = result['z_score']
            st.markdown(
                f"<h3 style='text-align:center; color:green;'>VO2 Percentile: {result['percentile_label']}</h1>",
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


            with st.expander("Age based score", expanded=False):
                if age_based:
                    st.markdown(
                        f"""
                        <div style="text-align:center;">
                            <h3>CIMT Percentile by Age</h3>
                            <h3 style="color:green; font-size:50px;">{age_based['percentile_label']}</h3>
                            <h4>Percentile: {age_based['percentile']:.2f}</h4>
                            <h4>Z-score: {age_based['z_score']:.3f}</h4>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            with st.expander("height based score", expanded=False):
                if height_based:
                    st.markdown(
                        f"""
                        <div style="text-align:center;">
                            <h3>CIMT Percentile by Age</h3>
                            <h3 style="color:green; font-size:50px;">{height_based['percentile_label']}</h3>
                            <h4>Percentile: {height_based['percentile']:.2f}</h4>
                            <h4>Z-score: {height_based['z_score']:.3f}</h4>


                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            st.write("score or percentile to be sent for age or height?")
            st.session_state.score['cimt_score'] = age_based['z_score']

            # st.session_state.scores["cimt"] = {
            #                         "z_score": age_based["z_score"],
            #                         "percentile": age_based["percentile"],
            #                         "percentile_label": age_based["percentile_label"],
            #                         "observed_value": age_based["observed_value"],
            #                     }

            c1, c2 = st.columns([2,0.1])
            with c1:
                st.subheader("Summary")
                with st.expander("Age based", expanded=False):
                    st.write(f"**Age-based percentile:** {age_based['percentile']:.2f}")
                    st.write(f"**Age-based label:** {age_based['percentile_label']}")
                    st.write(f"**Age-based z-score:** {age_based['z_score']:.3f}")
                with st.expander("height based", expanded=False):
                    st.write(f"**Height-based percentile:** {height_based['percentile']:.2f}")
                    st.write(f"**Height-based label:** {height_based['percentile_label']}")
                    st.write(f"**Height-based z-score:** {height_based['z_score']:.3f}")

        

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
            st.write("score or percentile to be sent ?")
            # st.session_state.score['wr_score'] = result['z_score']

            # st.session_state.scores["wr_peak"] = {
            #     "z_score": result["z_score"],
            #     "percentile": result["percentile"],
            #     "percentile_label": result["percentile_label"],
            #     "observed_value": result["observed_value"],
            #     "age": result["x_value"],
            #     "sex": result["sex"],
            # }

            # st.markdown(
            #     f"""
            #     <div style="text-align:center;">
            #         <h3>WR Peak/kg Percentile</h3>
            #         <h1 style="color:green; font-size:80px;">{result['percentile_label']}</h1>
            #         <h4>Percentile: {result['percentile']:.2f}</h4>
            #         <h4>Z-score: {result['z_score']:.3f}</h4>
            #     </div>
            #     """,
            #     unsafe_allow_html=True
            # )
            st.markdown(
                f"<h3 style='text-align:center; color:green;'>WR Peak Percentile: {result['percentile_label']} {result['percentile']:.2f}</h1>",
                unsafe_allow_html=True
            )
            st.session_state.score['wr_score'] = result['z_score']


            with st.expander("Reference", expanded=False):
                st.write(f"Percentile: {result['percentile']:.2f}")
                st.write(f"Z-score: {result['z_score']:.3f}")
                st.write(f"**L:** {result['L']}")
                st.write(f"**M:** {result['M']}")
                st.write(f"**S:** {result['S']}")
                st.write(f"**Reference type:** {result['reference_type']}")

        except Exception as e:
            st.error(f"Error calculating WR Peak percentile: {e}")


def render_baPWV_score(refs):
    st.header("baPWV Peak Percentile")

    if st.button("Calculate baPWV Peak Percentile", key="bapwvpeak_btn"):
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
                f"<h3 style='text-align:center; color:green;'>baPWV Peak Percentile: {result['percentile_label']} {result['percentile']:.2f}</h3>",
                unsafe_allow_html=True
            )

            st.session_state.score['bapwv_score'] = result['z_score']

            with st.expander("Reference", expanded=False):
                st.write(f"Percentile: {result['percentile']:.2f}")
                st.write(f"Z-score: {result['z_score']:.3f}")
                st.write(f"**L:** {result['L']}")
                st.write(f"**M:** {result['M']}")
                st.write(f"**S:** {result['S']}")
                st.write(f"**Reference type:** {result['reference_type']}")

        except Exception as e:
            st.error(f"Error calculating baPWV Peak percentile: {e}")



def render_momo_score(refs):
    st.header("MOMO Percentile")

    if st.button("Calculate MOMO Percentile", key="momo_btn"):
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
                f"<h3 style='text-align:center; color:green;'>MOMO Percentile: {result['percentile_label']}</h3>",
                unsafe_allow_html=True
            )

            st.session_state.score["momo_score"] = result["z_score_label"]

            with st.expander("Reference", expanded=False):
                st.write(f"Observed value: {result['observed_value']:.2f}")
                st.write(f"Matched age: {result['age_used']}")
                st.write(f"Reference SW: {result['reference_value']:.2f}")
                st.write(f"Percentile rank: {result['percentile_label']}")
                st.write(f"Z-score: {result['z_score_label']}")
                st.write(f"Reference type: {result['reference_type']}")

        except Exception as e:
            st.error(f"Error calculating MOMO percentile: {e}")

def render_gripStrength_score(refs):
    st.header("Grip Strength Percentile")

    if st.button("Calculate Grip Strength Percentile", key="gripstrength_btn"):
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
                f"<h3 style='text-align:center; color:green;'>Grip Strength Percentile: {result['percentile_label']}</h3>",
                unsafe_allow_html=True
            )

            st.session_state.score["grip_score"] = result["percentile_label"]

            with st.expander("Reference", expanded=False):
                st.write(f"Observed grip strength: {result['observed_value']:.2f} kg")
                st.write(f"Matched age: {result['age_used']}")
                st.write(f"Reference grip strength: {result['reference_value']:.2f} kg")
                st.write(f"Percentile rank: {result['percentile_label']}")
                st.write(f"Source table: {result['source_table']}")
                st.write(f"Reference type: {result['reference_type']}")

        except Exception as e:
            st.error(f"Error calculating Grip Strength percentile: {e}")



def render_KidScreen_score(refs):
    st.header("KidScreen Score")

    if st.button("Calculate KidScreen Score", key="kidscreen_btn"):
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
                f"<h3 style='text-align:center; color:green;'>KidScreen 0-100 Score: {result['score_0_100']:.2f}</h3>",
                unsafe_allow_html=True
            )

            st.session_state.score["kidscreen_score"] = result["score_0_100"]
            

            with st.expander("Reference", expanded=False):
                st.write(f"Observed raw score: {result['observed_value']:.2f}")
                st.write(f"Raw score used: {result['raw_score']}")
                st.write(f"Age group: {result['age_group']}")
                st.write(f"0-100 Score: {result['score_0_100']:.2f}")
                st.write(f"Percentile rank: {result['percentile_label']}")
                st.write(f"T-score: {result['t_score']}")
                st.write(f"Reference type: {result['reference_type']}")

        except Exception as e:
            st.error(f"Error calculating KidScreen score: {e}")



import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

def render_star_plot(score_dict):
    plot_scores = {}

    if "sleep_score" in score_dict:
        plot_scores["Sleep"] = score_dict["sleep_score"]

    if "bp_score" in score_dict:
        plot_scores["Blood Pressure"] = score_dict["bp_score"]

    if "bmi_score" in score_dict:
        plot_scores["BMI"] = score_dict["bmi_score"]

    if "vo2_score" in score_dict:
        # st.write('vo2', score_dict["vo2_score"])
        plot_scores["VO2 Peak"] = z_to_percentile(score_dict["vo2_score"])

    if "wr_score" in score_dict:
        plot_scores["WR Peak/kg"] = z_to_percentile(score_dict["wr_score"])

    if "cimt_score" in score_dict:
        plot_scores["cIMT"] = 100 - z_to_percentile(score_dict["cimt_score"])

    if "kidscreen_score" in score_dict:
        plot_scores["KIDSCREEN"] = score_dict["kidscreen_score"]

    # if "grip_score" in score_dict:
    #     plot_scores["Grip Strength"] = z_to_percentile(score_dict["grip_score"])

    if "momo_score" in score_dict:
        plot_scores["MoMo"] = score_dict["momo_score"]

    if "bapwv_score" in score_dict:
        plot_scores["baPWV"] = score_dict["bapwv_score"]

    if not plot_scores:
        st.warning("No scores available for star plot.")
        return

    categories = list(plot_scores.keys())
    values = list(plot_scores.values())

    col1, col2 = st.columns([1.5, 2], gap = 'xsmall', border = False)
    with col1:
        # ---------- Combined CVH mean bar ----------
        mean_score = sum(values) / len(values)

        # 0 = bad (red), 100 = good (green)
        bar_color = px.colors.sample_colorscale(
            "RdYlGn",
            [mean_score / 100.0]
        )[0]

        fig_bar = go.Figure()

        fig_bar.add_trace(go.Bar(
            x=[mean_score],
            y=["Combined CVH Score"],
            orientation="h",
            text=[f"{mean_score:.1f}"],
            textposition="inside",
            insidetextanchor="middle",
            marker=dict(
                color=[bar_color],
                line=dict(color="white", width=1.5)
            ),
            hovertemplate="Mean score: %{x:.1f}<extra></extra>"
        ))

        fig_bar.update_layout(
            title="Combined Cardiovascular Health Score",
            title_font=dict(color="white"),
            font=dict(color="orange"),
            xaxis=dict(
                title="Score",
                range=[0, 100],
                tickfont=dict(color="orange"),
                title_font=dict(color="orange")
            ),
            yaxis=dict(
                tickfont=dict(color="orange")
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=180,
            showlegend=False,
            margin=dict(l=40, r=40, t=60, b=40)
        )

        st.plotly_chart(fig_bar, use_container_width=True)
        st.caption(f"Combined CVH score = mean of {len(values)} "
                       f"available elements in score_dict: {mean_score:.1f}/100")

        with st.expander("CVH score", expanded=True):
            st.write(st.session_state.score)
        
    with col2: 

        # ---------- Star plot ----------
        radar_categories = categories + [categories[0]]
        radar_values = values + [values[0]]

        fig_star = go.Figure()

        fig_star.add_trace(go.Scatterpolar(
            r=radar_values,
            theta=radar_categories,
            fill="toself",
            name="Patient profile",
            line=dict(color="lightgreen", width=3),
            fillcolor="rgba(10, 107, 190, 0.25)"
        ))

        fig_star.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(color="orange")
                ),
                angularaxis=dict(
                    tickfont=dict(color="orange")
                )
            ),
            showlegend=False,
            title="Cardiovascular Health Star Plot",
            title_font=dict(color="white"),
            font=dict(color="orange"),
            height=600
        )

        st.plotly_chart(fig_star, use_container_width=True)





def ___render_star_plot(score_dict):
    plot_scores = {}

    if "sleep_score" in score_dict:
        plot_scores["Sleep"] = score_dict["sleep_score"]

    if "bp_score" in score_dict:
        plot_scores["Blood Pressure"] = score_dict["bp_score"]

    if "bmi_score" in score_dict:
        plot_scores["BMI"] = score_dict["bmi_score"]

    if "vo2_score" in score_dict:
        plot_scores["VO2 Peak"] = z_to_percentile(score_dict["vo2_score"])

    if "wr_score" in score_dict:
        plot_scores["WR Peak/kg"] = z_to_percentile(score_dict["wr_score"])

    if "cimt_score" in score_dict:
        plot_scores["cIMT"] = 100 - z_to_percentile(score_dict["cimt_score"])

    if "kidscreen_score" in score_dict:
        plot_scores["kidscreen_score"] = score_dict["kidscreen_score"]

    if "kidscreen_score" in score_dict:
        plot_scores["kidscreen_score"] = score_dict["kidscreen_score"]

    if "grip_score" in score_dict:
        plot_scores["grip_score"] = score_dict["grip_score"]

    if "momo_score" in score_dict:
        plot_scores["momo_score"] = score_dict["momo_score"]

    if 'bapwv_score' in score_dict:
        plot_scores['bapwv_score'] = score_dict['bapwv_score']



    categories = list(plot_scores.keys())
    values = list(plot_scores.values())

    if not categories:
        st.warning("No scores available for star plot.")
        return

    categories += [categories[0]]
    values += [values[0]]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill="toself",
        name="Patient profile",
        line=dict(color="lightgreen", width=3),
        fillcolor="rgba(10, 107, 190, 0.25)"
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color="orange")
            ),
            angularaxis=dict(
                tickfont=dict(color="orange")
            )
        ),
        showlegend=False,
        title="Cardiovascular Health Star Plot",
        title_font=dict(color="white"),
        font=dict(color="orange"),
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)