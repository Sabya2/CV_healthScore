# import pandas as pd
# import numpy as np
# import json



# def get_sleep_score_json(json_file, age, sex, sleep_hours):
#     with open(json_file, "r", encoding="utf-8") as f:
#         data = json.load(f)

#     sex = sex.strip().lower()
#     if sex not in data:
#         raise ValueError("sex must be 'boys' or 'girls'")

#     for row in data[sex]:
#         age_min = float(row["age_min"])
#         age_max = float(row["age_max"])

#         # left-inclusive, right-exclusive; last boundary included if exact
#         if age_min <= age < age_max or age == age_max:
#             mean_h = float(row["mean_h"])
#             sd_h = float(row["sd_h"])
#             upper_cutoff = float(row["upper_cutoff"])
#             lower_cutoff = float(row["lower_cutoff"])

#             upper_1 = upper_cutoff + 1
#             lower_1 = lower_cutoff - 1
#             lower_2 = lower_cutoff - 2
#             lower_3 = lower_cutoff - 3

#             print(upper_1, upper_cutoff, lower_cutoff, lower_1, lower_2, lower_3)

#             print()

#             if lower_cutoff <= sleep_hours <= upper_cutoff:
#                 score = 100
#                 band = "mean±sd"
#             elif upper_cutoff < sleep_hours <= upper_1:
#                 score = 90
#                 band = "upper_cutoff to upper_cutoff+1h"
#             elif sleep_hours > upper_1:
#                 score = 40
#                 band = "> upper_cutoff+1h"
#             elif lower_1 <= sleep_hours < lower_cutoff:
#                 score = 70
#                 band = "lower_cutoff-1h to lower_cutoff"
#             elif lower_2 <= sleep_hours < lower_1:
#                 score = 40
#                 band = "lower_cutoff-2h to lower_cutoff-1h"
#             elif lower_3 <= sleep_hours < lower_2:
#                 score = 20
#                 band = "lower_cutoff-3h to lower_cutoff-2h"
#             else:
#                 score = 0
#                 band = "< lower_cutoff-3h"

#             return {
#                 "score": score,
#                 "band": band,
#                 "sex": sex,
#                 "age": age,
#                 "age_group": f"{age_min}-{age_max}",
#                 "sleep_hours": sleep_hours,
#                 "mean_h": mean_h,
#                 "sd_h": sd_h,
#                 "upper_cutoff": upper_cutoff,
#                 "lower_cutoff": lower_cutoff,
#             }

#     raise ValueError(f"No age group found for age={age}, sex={sex}")



# def load_json(json_file: str):
#     with open(json_file, "r", encoding="utf-8") as f:
#         return json.load(f)


# def __get_bp_reference_row(
#     bp_json: dict,
#     sex: str,
#     bp_type: str,
#     age_years: float,
#     height_cm: float,
# ):
#     """
#     Find the matching BP reference row for a given sex, bp_type, age, and height.

#     Logic:
#     - filter rows by exact age_years
#     - from those rows, choose the nearest height_cm
#     """
#     sex = str(sex).strip().lower()
#     bp_type = str(bp_type).strip().lower()

#     if sex not in bp_json:
#         raise ValueError("sex must be 'boys' or 'girls'")

#     if bp_type not in bp_json[sex]:
#         raise ValueError("bp_type must be 'systolic' or 'diastolic'")

#     rows = bp_json[sex][bp_type]

#     age_rows = [r for r in rows if float(r["age_years"]) == float(age_years)]

#     if not age_rows:
#         available_ages = sorted(set(float(r["age_years"]) for r in rows))
#         raise ValueError(
#             f"No BP reference rows found for age_years={age_years}. "
#             f"Available ages: {available_ages}"
#         )

#     best_row = min(age_rows, key=lambda r: abs(float(r["height_cm"]) - float(height_cm)))
#     return best_row


# def get_bp_reference_row(
#     bp_json: dict,
#     sex: str,
#     bp_type: str,
#     age_years: float,
#     height_cm: float,
# ):
#     """
#     Find the matching BP reference row for a given sex, bp_type, age, and height.

#     Logic:
#     - find nearest available age_years
#     - within that age group, choose nearest height_cm
#     """
#     sex = str(sex).strip().lower()
#     bp_type = str(bp_type).strip().lower()

#     if sex not in bp_json:
#         raise ValueError("sex must be 'boys' or 'girls'")

#     if bp_type not in bp_json[sex]:
#         raise ValueError("bp_type must be 'systolic' or 'diastolic'")

#     rows = bp_json[sex][bp_type]

#     available_ages = sorted(set(float(r["age_years"]) for r in rows))
#     matched_age = min(available_ages, key=lambda a: abs(a - float(age_years)))

#     age_rows = [r for r in rows if float(r["age_years"]) == matched_age]

#     if not age_rows:
#         raise ValueError(
#             f"No BP reference rows found for matched age_years={matched_age}"
#         )

#     best_row = min(age_rows, key=lambda r: abs(float(r["height_cm"]) - float(height_cm)))
#     return best_row


# def classify_bp_value(
#     value: float,
#     p90: float,
#     p95: float,
#     p99: float,
#     p99_plus_5: float,
#     fixed_90: float,
#     fixed_95: float,
#     fixed_99: float,
#     fixed_0: float,
# ):
#     """
#     Classify one BP value according to the rule:

#     100: value < min(P90, fixed_90)
#      75: value >= min(P90, fixed_90) and < min(P95, fixed_95)
#      50: value >= min(P95, fixed_95) and < min(P99, fixed_99)
#      25: value >= min(P99, fixed_99) and < min(P99+5, fixed_0)
#       0: value >= min(P99+5, fixed_0)

#     Example fixed cutoffs:
#     - systolic: 120, 130, 140, 160
#     - diastolic: 80, 85, 90, 100
#     """
#     thr_75 = min(float(p90), float(fixed_90))
#     thr_50 = min(float(p95), float(fixed_95))
#     thr_25 = min(float(p99), float(fixed_99))
#     thr_0 = min(float(p99_plus_5), float(fixed_0))

#     if value >= thr_0:
#         return 0
#     elif value >= thr_25:
#         return 25
#     elif value >= thr_50:
#         return 50
#     elif value >= thr_75:
#         return 75
#     else:
#         return 100


# def score_bp_from_json(
#     json_file: str,
#     sex: str,
#     age_years: float,
#     height_cm: float,
#     systolic_bp: float,
#     diastolic_bp: float,
#     treated: bool = False,
# ):
#     """
#     Score blood pressure from a pre-built BP reference JSON.

#     Parameters
#     ----------
#     json_file : str
#         Path to BP reference JSON.
#     sex : str
#         'boys' or 'girls'
#     age_years : float
#         Age in years, e.g. 10.5
#     height_cm : float
#         Height in cm
#     systolic_bp : float
#         Measured systolic BP
#     diastolic_bp : float
#         Measured diastolic BP
#     treated : bool
#         If True, subtract 20 points from final score, minimum 0.

#     Returns
#     -------
#     dict
#         Detailed result with final score, component scores, and matched reference rows.
#     """
#     data = load_json(json_file)

#     sex = str(sex).strip().lower()

#     sys_row = get_bp_reference_row(
#         bp_json=data,
#         sex=sex,
#         bp_type="systolic",
#         age_years=age_years,
#         height_cm=height_cm,
#     )

#     dia_row = get_bp_reference_row(
#         bp_json=data,
#         sex=sex,
#         bp_type="diastolic",
#         age_years=age_years,
#         height_cm=height_cm,
#     )

#     sys_score = classify_bp_value(
#         value=float(systolic_bp),
#         p90=float(sys_row["p90"]),
#         p95=float(sys_row["p95"]),
#         p99=float(sys_row["p99"]),
#         p99_plus_5=float(sys_row["p99_plus_5"]),
#         fixed_90=120,
#         fixed_95=130,
#         fixed_99=140,
#         fixed_0=160,
#     )

#     dia_score = classify_bp_value(
#         value=float(diastolic_bp),
#         p90=float(dia_row["p90"]),
#         p95=float(dia_row["p95"]),
#         p99=float(dia_row["p99"]),
#         p99_plus_5=float(dia_row["p99_plus_5"]),
#         fixed_90=80,
#         fixed_95=85,
#         fixed_99=90,
#         fixed_0=100,
#     )

#     # overall score is the worse of systolic/diastolic
#     final_score = min(sys_score, dia_score)

#     if treated:
#         final_score = max(final_score - 20, 0)

#     return {
#         "score": final_score,
#         "treated": treated,
#         "inputs": {
#             "sex": sex,
#             "age_years": float(age_years),
#             "height_cm": float(height_cm),
#             "systolic_bp": float(systolic_bp),
#             "diastolic_bp": float(diastolic_bp),
#         },
#         "component_scores": {
#             "systolic_score": sys_score,
#             "diastolic_score": dia_score,
#         },
#         "reference_rows": {
#             "systolic": sys_row,
#             "diastolic": dia_row,
#         },
#     }








# def age_to_months(age_years: float) -> int:
#     return int(round(age_years * 12))


# def calculate_bmi(weight_kg: float, height_cm: float) -> float:
#     height_m = height_cm / 100.0
#     if height_m <= 0:
#         raise ValueError("Height must be greater than 0")
#     return weight_kg / (height_m ** 2)


# def get_bmi_reference_row(df: pd.DataFrame, sex: str, age_years: float) -> pd.Series:
#     df2 = df.copy()
#     df2.columns = [str(c).strip() for c in df2.columns]
#     df2["sex"] = df2["sex"].astype(str).str.strip().str.lower()

#     sex = sex.strip().lower()
#     months = age_to_months(age_years)

#     df_sex = df2[df2["sex"] == sex].copy()
#     if df_sex.empty:
#         raise ValueError(f"No BMI reference rows found for sex='{sex}'")

#     if "Month" not in df_sex.columns:
#         raise ValueError("Column 'Month' not found in BMI dataframe")

#     for col in ["-3SD", "-2SD", "-1SD", "Median", "1SD", "2SD", "3SD"]:
#         if col not in df_sex.columns:
#             raise ValueError(f"Required column '{col}' not found in BMI dataframe")

#     if months in df_sex["Month"].values:
#         row = df_sex.loc[df_sex["Month"] == months].iloc[0]
#     else:
#         idx = (df_sex["Month"] - months).abs().idxmin()
#         row = df_sex.loc[idx]

#     return row


# def score_bmi_value(bmi_value: float, row: pd.Series) -> int:
#     minus_3 = float(row["-3SD"])
#     minus_2 = float(row["-2SD"])
#     plus_1 = float(row["1SD"])
#     plus_2 = float(row["2SD"])
#     plus_3 = float(row["3SD"])

#     # If value > -2SD and < +1SD = 100
#     if minus_2 < bmi_value < plus_1:
#         return 100

#     # If < -2SD and > -3SD or > +1SD and < +2SD = 70
#     if (minus_3 < bmi_value < minus_2) or (plus_1 < bmi_value < plus_2):
#         return 70

#     # If < -3SD or > +2SD and < +3SD = 30
#     if (bmi_value < minus_3) or (plus_2 < bmi_value < plus_3):
#         return 30

#     # If > +3SD = 0
#     if bmi_value > plus_3:
#         return 0

#     # exact boundary handling
#     if bmi_value == minus_2 or bmi_value == plus_1:
#         return 100
#     if bmi_value == minus_3 or bmi_value == plus_2:
#         return 30
#     if bmi_value == plus_3:
#         return 0

#     return np.nan


# def score_bmi_from_df(
#     bmi_df: pd.DataFrame,
#     sex: str,
#     age_years: float,
#     weight_kg: float,
#     height_cm: float,
# ) -> dict:
#     bmi_value = calculate_bmi(weight_kg=weight_kg, height_cm=height_cm)
#     row = get_bmi_reference_row(df=bmi_df, sex=sex, age_years=age_years)
#     score = score_bmi_value(bmi_value=bmi_value, row=row)

#     return {
#         "score": score,
#         "inputs": {
#             "sex": sex,
#             "age_years": age_years,
#             "weight_kg": weight_kg,
#             "height_cm": height_cm,
#             "bmi": round(bmi_value, 2),
#         },
#         "reference_row": {
#             "Month": int(row["Month"]),
#             "-3SD": float(row["-3SD"]),
#             "-2SD": float(row["-2SD"]),
#             "-1SD": float(row["-1SD"]),
#             "Median": float(row["Median"]),
#             "1SD": float(row["1SD"]),
#             "2SD": float(row["2SD"]),
#             "3SD": float(row["3SD"]),
#         }
#     }






# import numpy as np
# import pandas as pd
# from scipy.stats import norm


# def percentile_label(percentile: float) -> str:
#     if percentile < 3:
#         return "<P3"
#     if percentile > 97:
#         return ">P97"
#     return f"P{round(percentile)}"


# def load_reference_csv(path: str) -> pd.DataFrame:
#     df = pd.read_csv(path)
#     df.columns = [col.strip() for col in df.columns]
#     return df


# def get_interp_lms(x: float, ref_df: pd.DataFrame, x_col: str) -> tuple[float, float, float]:
#     df = ref_df.sort_values(x_col).reset_index(drop=True)

#     x_vals = df[x_col].to_numpy(dtype=float)
#     l_vals = df["L"].to_numpy(dtype=float)
#     m_vals = df["M"].to_numpy(dtype=float)
#     s_vals = df["S"].to_numpy(dtype=float)

#     if x < x_vals.min() or x > x_vals.max():
#         raise ValueError(f"{x_col} must be between {x_vals.min()} and {x_vals.max()}")

#     l = np.interp(x, x_vals, l_vals)
#     m = np.interp(x, x_vals, m_vals)
#     s = np.interp(x, x_vals, s_vals)

#     return float(l), float(m), float(s)


# def lms_to_zscore(value: float, l: float, m: float, s: float) -> float:
#     if value <= 0:
#         raise ValueError("Observed value must be > 0")

#     if np.isclose(l, 0):
#         return float(np.log(value / m) / s)

#     return float((((value / m) ** l) - 1) / (l * s))


# def zscore_to_percentile(z: float) -> float:
#     return float(norm.cdf(z) * 100)


# def lms_score(value: float, x: float, ref_df: pd.DataFrame, x_col: str) -> dict:
#     l, m, s = get_interp_lms(x=x, ref_df=ref_df, x_col=x_col)
#     z = lms_to_zscore(value=value, l=l, m=m, s=s)
#     percentile = zscore_to_percentile(z)

#     return {
#         "x_col": x_col,
#         "x_value": float(x),
#         "observed_value": float(value),
#         "L": l,
#         "M": m,
#         "S": s,
#         "z_score": z,
#         "percentile": percentile,
#         "percentile_label": percentile_label(percentile),
#     }


# def get_reference_df(refs: dict, metric: str, sex: str, reference_type: str) -> pd.DataFrame:
#     try:
#         path = refs[metric][sex][reference_type]
#     except KeyError:
#         raise ValueError(
#             f"Missing reference for metric={metric}, sex={sex}, reference_type={reference_type}"
#         )
#     return load_reference_csv(path)


# def score_vo2(sex: str, observed_value: float, age: float, refs: dict) -> dict:
#     ref_df = get_reference_df(refs, metric="vo2", sex=sex, reference_type="age")
#     result = lms_score(
#         value=observed_value,
#         x=age,
#         ref_df=ref_df,
#         x_col="Age",
#     )
#     result.update({
#         "metric": "vo2",
#         "sex": sex,
#         "reference_type": "age",
#     })
#     return result


# def score_cimt(sex: str, observed_value: float, refs: dict, age: float = None, height: float = None) -> dict:
#     results = {
#         "metric": "cimt",
#         "sex": sex,
#         "observed_value": float(observed_value),
#     }

#     if age is not None:
#         age_df = get_reference_df(refs, metric="cimt", sex=sex, reference_type="age")
#         results["age_based"] = lms_score(
#             value=observed_value,
#             x=age,
#             ref_df=age_df,
#             x_col="Age (years)",
#         )

#     if height is not None:
#         height_df = get_reference_df(refs, metric="cimt", sex=sex, reference_type="height")
#         results["height_based"] = lms_score(
#             value=observed_value,
#             x=height,
#             ref_df=height_df,
#             x_col="Height (cm)",
#         )

#     if "age_based" not in results and "height_based" not in results:
#         raise ValueError("cIMT scoring requires age and/or height")

#     return results


# def score_measurement(
#     metric: str,
#     sex: str,
#     observed_value: float,
#     refs: dict,
#     age: float = None,
#     height: float = None,
# ) -> dict:
#     metric = metric.strip().lower()
#     sex = sex.strip().lower()

#     if metric == "vo2":
#         if age is None:
#             raise ValueError("VO2 scoring requires age")
#         return score_vo2(
#             sex=sex,
#             observed_value=observed_value,
#             age=age,
#             refs=refs,
#         )

#     if metric == "cimt":
#         return score_cimt(
#             sex=sex,
#             observed_value=observed_value,
#             refs=refs,
#             age=age,
#             height=height,
#         )

#     raise ValueError(f"Unsupported metric: {metric}")







import json
from typing import Optional

import numpy as np
import pandas as pd
from scipy.stats import norm


# =========================================================
# Generic helpers
# =========================================================

def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_reference_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    return df


def normalize_sex(sex: str) -> str:
    sex = str(sex).strip().lower()
    if sex not in {"boys", "girls"}:
        raise ValueError("sex must be 'boys' or 'girls'")
    return sex


def percentile_label(percentile: float) -> str:
    if percentile < 3:
        return "<P3"
    if percentile > 97:
        return ">P97"
    return f"P{round(percentile)}"


# =========================================================
# Sleep score
# =========================================================

def get_sleep_score_json(
    json_file: str,
    age: float,
    sex: str,
    sleep_hours: float,
) -> dict:
    data = load_json(json_file)
    sex = normalize_sex(sex)

    for row in data[sex]:
        age_min = float(row["age_min"])
        age_max = float(row["age_max"])

        if age_min <= age < age_max or age == age_max:
            mean_h = float(row["mean_h"])
            sd_h = float(row["sd_h"])
            upper_cutoff = float(row["upper_cutoff"])
            lower_cutoff = float(row["lower_cutoff"])

            upper_1 = upper_cutoff + 1
            lower_1 = lower_cutoff - 1
            lower_2 = lower_cutoff - 2
            lower_3 = lower_cutoff - 3

            if lower_cutoff <= sleep_hours <= upper_cutoff:
                score, band = 100, "mean±sd"
            elif upper_cutoff < sleep_hours <= upper_1:
                score, band = 90, "upper_cutoff to upper_cutoff+1h"
            elif sleep_hours > upper_1:
                score, band = 40, "> upper_cutoff+1h"
            elif lower_1 <= sleep_hours < lower_cutoff:
                score, band = 70, "lower_cutoff-1h to lower_cutoff"
            elif lower_2 <= sleep_hours < lower_1:
                score, band = 40, "lower_cutoff-2h to lower_cutoff-1h"
            elif lower_3 <= sleep_hours < lower_2:
                score, band = 20, "lower_cutoff-3h to lower_cutoff-2h"
            else:
                score, band = 0, "< lower_cutoff-3h"

            return {
                "score": score,
                "band": band,
                "sex": sex,
                "age": float(age),
                "age_group": f"{age_min}-{age_max}",
                "sleep_hours": float(sleep_hours),
                "mean_h": mean_h,
                "sd_h": sd_h,
                "upper_cutoff": upper_cutoff,
                "lower_cutoff": lower_cutoff,
            }

    raise ValueError(f"No age group found for age={age}, sex={sex}")


# =========================================================
# Blood pressure score
# =========================================================

def get_bp_reference_row(
    bp_json: dict,
    sex: str,
    bp_type: str,
    age_years: float,
    height_cm: float,
) -> dict:
    sex = normalize_sex(sex)
    bp_type = str(bp_type).strip().lower()

    if bp_type not in {"systolic", "diastolic"}:
        raise ValueError("bp_type must be 'systolic' or 'diastolic'")

    rows = bp_json[sex][bp_type]
    available_ages = sorted({float(r["age_years"]) for r in rows})
    matched_age = min(available_ages, key=lambda x: abs(x - float(age_years)))

    age_rows = [r for r in rows if float(r["age_years"]) == matched_age]
    best_row = min(age_rows, key=lambda r: abs(float(r["height_cm"]) - float(height_cm)))

    return best_row


def classify_bp_value(
    value: float,
    p90: float,
    p95: float,
    p99: float,
    p99_plus_5: float,
    fixed_90: float,
    fixed_95: float,
    fixed_99: float,
    fixed_0: float,
) -> int:
    thr_75 = min(float(p90), float(fixed_90))
    thr_50 = min(float(p95), float(fixed_95))
    thr_25 = min(float(p99), float(fixed_99))
    thr_0 = min(float(p99_plus_5), float(fixed_0))

    if value >= thr_0:
        return 0
    if value >= thr_25:
        return 25
    if value >= thr_50:
        return 50
    if value >= thr_75:
        return 75
    return 100


def score_bp_from_json(
    json_file: str,
    sex: str,
    age_years: float,
    height_cm: float,
    systolic_bp: float,
    diastolic_bp: float,
    treated: bool = False,
) -> dict:
    bp_data = load_json(json_file)
    sex = normalize_sex(sex)

    systolic_row = get_bp_reference_row(
        bp_json=bp_data,
        sex=sex,
        bp_type="systolic",
        age_years=age_years,
        height_cm=height_cm,
    )
    diastolic_row = get_bp_reference_row(
        bp_json=bp_data,
        sex=sex,
        bp_type="diastolic",
        age_years=age_years,
        height_cm=height_cm,
    )

    systolic_score = classify_bp_value(
        value=systolic_bp,
        p90=systolic_row["p90"],
        p95=systolic_row["p95"],
        p99=systolic_row["p99"],
        p99_plus_5=systolic_row["p99_plus_5"],
        fixed_90=120,
        fixed_95=130,
        fixed_99=140,
        fixed_0=160,
    )
    diastolic_score = classify_bp_value(
        value=diastolic_bp,
        p90=diastolic_row["p90"],
        p95=diastolic_row["p95"],
        p99=diastolic_row["p99"],
        p99_plus_5=diastolic_row["p99_plus_5"],
        fixed_90=80,
        fixed_95=85,
        fixed_99=90,
        fixed_0=100,
    )

    final_score = min(systolic_score, diastolic_score)
    if treated:
        final_score = max(final_score - 20, 0)

    return {
        "score": final_score,
        "treated": treated,
        "inputs": {
            "sex": sex,
            "age_years": float(age_years),
            "height_cm": float(height_cm),
            "systolic_bp": float(systolic_bp),
            "diastolic_bp": float(diastolic_bp),
        },
        "component_scores": {
            "systolic_score": systolic_score,
            "diastolic_score": diastolic_score,
        },
        "reference_rows": {
            "systolic": systolic_row,
            "diastolic": diastolic_row,
        },
    }


# =========================================================
# BMI score
# =========================================================

def age_to_months(age_years: float) -> int:
    return int(round(age_years * 12))


def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    height_m = height_cm / 100.0
    if height_m <= 0:
        raise ValueError("Height must be greater than 0")
    return weight_kg / (height_m ** 2)


def get_bmi_reference_row(df: pd.DataFrame, sex: str, age_years: float) -> pd.Series:
    df = df.copy()
    df.columns = df.columns.str.strip()
    df["sex"] = df["sex"].astype(str).str.strip().str.lower()

    sex = normalize_sex(sex)
    months = age_to_months(age_years)

    df_sex = df[df["sex"] == sex].copy()
    if df_sex.empty:
        raise ValueError(f"No BMI reference rows found for sex='{sex}'")

    required_cols = ["Month", "-3SD", "-2SD", "-1SD", "Median", "1SD", "2SD", "3SD"]
    missing_cols = [col for col in required_cols if col not in df_sex.columns]
    if missing_cols:
        raise ValueError(f"Missing BMI reference columns: {missing_cols}")

    if months in df_sex["Month"].values:
        return df_sex.loc[df_sex["Month"] == months].iloc[0]

    idx = (df_sex["Month"] - months).abs().idxmin()
    return df_sex.loc[idx]


def score_bmi_value(bmi_value: float, row: pd.Series) -> int:
    minus_3 = float(row["-3SD"])
    minus_2 = float(row["-2SD"])
    plus_1 = float(row["1SD"])
    plus_2 = float(row["2SD"])
    plus_3 = float(row["3SD"])

    if minus_2 <= bmi_value <= plus_1:
        return 100
    if (minus_3 < bmi_value < minus_2) or (plus_1 < bmi_value < plus_2):
        return 70
    if bmi_value == minus_3 or bmi_value == plus_2:
        return 30
    if bmi_value < minus_3 or (plus_2 < bmi_value < plus_3):
        return 30
    if bmi_value >= plus_3:
        return 0

    return np.nan


def score_bmi_from_df(
    bmi_df: pd.DataFrame,
    sex: str,
    age_years: float,
    weight_kg: float,
    height_cm: float,
) -> dict:
    bmi_value = calculate_bmi(weight_kg=weight_kg, height_cm=height_cm)
    ref_row = get_bmi_reference_row(df=bmi_df, sex=sex, age_years=age_years)
    score = score_bmi_value(bmi_value=bmi_value, row=ref_row)

    return {
        "score": score,
        "inputs": {
            "sex": normalize_sex(sex),
            "age_years": float(age_years),
            "weight_kg": float(weight_kg),
            "height_cm": float(height_cm),
            "bmi": round(bmi_value, 2),
        },
        "reference_row": {
            "Month": int(ref_row["Month"]),
            "-3SD": float(ref_row["-3SD"]),
            "-2SD": float(ref_row["-2SD"]),
            "-1SD": float(ref_row["-1SD"]),
            "Median": float(ref_row["Median"]),
            "1SD": float(ref_row["1SD"]),
            "2SD": float(ref_row["2SD"]),
            "3SD": float(ref_row["3SD"]),
        },
    }


# =========================================================
# LMS scoring helpers
# =========================================================

def get_interp_lms(
    x: float,
    ref_df: pd.DataFrame,
    x_col: str,
) -> tuple[float, float, float]:
    df = ref_df.sort_values(x_col).reset_index(drop=True)

    x_vals = df[x_col].to_numpy(dtype=float)
    l_vals = df["L"].to_numpy(dtype=float)
    m_vals = df["M"].to_numpy(dtype=float)
    s_vals = df["S"].to_numpy(dtype=float)

    if x < x_vals.min() or x > x_vals.max():
        raise ValueError(f"{x_col} must be between {x_vals.min()} and {x_vals.max()}")

    l = np.interp(x, x_vals, l_vals)
    m = np.interp(x, x_vals, m_vals)
    s = np.interp(x, x_vals, s_vals)

    return float(l), float(m), float(s)


def lms_to_zscore(value: float, l: float, m: float, s: float) -> float:
    if value <= 0:
        raise ValueError("Observed value must be > 0")

    if np.isclose(l, 0):
        return float(np.log(value / m) / s)

    return float((((value / m) ** l) - 1) / (l * s))


def zscore_to_percentile(z: float) -> float:
    return float(norm.cdf(z) * 100)


def lms_score(
    value: float,
    x: float,
    ref_df: pd.DataFrame,
    x_col: str,
) -> dict:
    l, m, s = get_interp_lms(x=x, ref_df=ref_df, x_col=x_col)
    z = lms_to_zscore(value=value, l=l, m=m, s=s)
    percentile = zscore_to_percentile(z)

    return {
        "x_col": x_col,
        "x_value": float(x),
        "observed_value": float(value),
        "L": l,
        "M": m,
        "S": s,
        "z_score": z,
        "percentile": percentile,
        "percentile_label": percentile_label(percentile),
    }


def get_reference_df(
    refs: dict,
    metric: str,
    sex: str,
    reference_type: str,
) -> pd.DataFrame:
    sex = normalize_sex(sex)

    try:
        path = refs[metric][sex][reference_type]
    except KeyError as e:
        raise ValueError(
            f"Missing reference for metric={metric}, sex={sex}, reference_type={reference_type}"
        ) from e

    return load_reference_csv(path)


# =========================================================
# VO2 and cIMT scoring
# =========================================================

def score_vo2(
    sex: str,
    observed_value: float,
    age: float,
    refs: dict,
) -> dict:
    ref_df = get_reference_df(refs=refs, metric="vo2", sex=sex, reference_type="age")
    result = lms_score(
        value=observed_value,
        x=age,
        ref_df=ref_df,
        x_col="Age",
    )
    result.update(
        {
            "metric": "vo2",
            "sex": normalize_sex(sex),
            "reference_type": "age",
        }
    )
    return result


def score_cimt(
    sex: str,
    observed_value: float,
    refs: dict,
    age: Optional[float] = None,
    height: Optional[float] = None,
) -> dict:
    sex = normalize_sex(sex)

    results = {
        "metric": "cimt",
        "sex": sex,
        "observed_value": float(observed_value),
    }

    if age is not None:
        age_df = get_reference_df(refs=refs, metric="cimt", sex=sex, reference_type="age")
        results["age_based"] = lms_score(
            value=observed_value,
            x=age,
            ref_df=age_df,
            x_col="Age (years)",
        )

    if height is not None:
        height_df = get_reference_df(refs=refs, metric="cimt", sex=sex, reference_type="height")
        results["height_based"] = lms_score(
            value=observed_value,
            x=height,
            ref_df=height_df,
            x_col="Height (cm)",
        )

    if "age_based" not in results and "height_based" not in results:
        raise ValueError("cIMT scoring requires age and/or height")

    return results


def score_wr_peak(sex: str, observed_value: float, age: float, refs: dict) -> dict:
    ref_df = get_reference_df(refs = refs, metric="wr_peak", sex=sex, reference_type="age")
    result = lms_score(
        value=observed_value,
        x=age,
        ref_df=ref_df,
        x_col="Age",
    )
    print('score wr')
    result.update({
        "metric": "wr_peak",
        "sex": sex,
        "reference_type": "age",
    })
    return result


def score_measurement(
    metric: str,
    sex: str,
    observed_value: float,
    refs: dict,
    age: Optional[float] = None,
    height: Optional[float] = None,
) -> dict:
    metric = str(metric).strip().lower()

    if metric == "vo2":
        if age is None:
            raise ValueError("VO2 scoring requires age")
        return score_vo2(
            sex=sex,
            observed_value=observed_value,
            age=age,
            refs=refs,
        )

    if metric == "cimt":
        return score_cimt(
            sex=sex,
            observed_value=observed_value,
            refs=refs,
            age=age,
            height=height,
        )
    
    if metric == "wr_peak":
        return score_wr_peak(
            sex=sex,
            observed_value=observed_value,
            refs=refs,
            age=age,
        )

    raise ValueError(f"Unsupported metric: {metric}")