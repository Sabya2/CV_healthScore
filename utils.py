import pandas as pd
import json


def sum_numbers(a, b):
    return a + b


def load_csv(uploaded_file): 
    # df = pd.read_csv(uploaded_file)
    df = pd.read_csv('synAGE_klotho.csv')
    print(df.shape)
    return df

def load_excel():
    df = pd.read_excel('Sleep_Scoring.xlsx')

    for sheet in df.sheet_names:
        print(sheet)
        
def describe_dataframe(df):
    return df.describe()


def get_basic_info(df):
    info_df = pd.DataFrame({
        "column": df.columns,
        "dtype": df.dtypes.astype(str).values,
        "missing_values": df.isna().sum().values,
        "unique_values": df.nunique(dropna=True).values,
    })
    return info_df


def get_missing_values(df):
    missing_df = df.isna().sum().reset_index()
    missing_df.columns = ["column", "missing_count"]
    return missing_df


def get_numeric_summary(df):
    numeric_df = df.select_dtypes(include="number")
    if numeric_df.empty:
        return pd.DataFrame()
    return numeric_df.describe().T


def get_categorical_summary(df):
    categorical_df = df.select_dtypes(include=["object", "category", "bool"])
    if categorical_df.empty:
        return pd.DataFrame()
    return categorical_df.describe().T


def filter_dataframe(df, column, value):
    return df[df[column] == value]


def get_correlation(df):
    numeric_df = df.select_dtypes(include="number")
    if numeric_df.shape[1] < 2:
        return pd.DataFrame()
    return numeric_df.corr()

def get_sleep_score_json(json_file, age, sex, sleep_hours):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    sex = sex.strip().lower()
    if sex not in data:
        raise ValueError("sex must be 'boys' or 'girls'")

    for row in data[sex]:
        age_min = float(row["age_min"])
        age_max = float(row["age_max"])

        # left-inclusive, right-exclusive; last boundary included if exact
        if age_min <= age < age_max or age == age_max:
            mean_h = float(row["mean_h"])
            sd_h = float(row["sd_h"])
            upper_cutoff = float(row["upper_cutoff"])
            lower_cutoff = float(row["lower_cutoff"])

            upper_1 = upper_cutoff + 1
            lower_1 = lower_cutoff - 1
            lower_2 = lower_cutoff - 2
            lower_3 = lower_cutoff - 3

            print(upper_1, upper_cutoff, lower_cutoff, lower_1, lower_2, lower_3)

            print()

            if lower_cutoff <= sleep_hours <= upper_cutoff:
                score = 100
                band = "mean±sd"
            elif upper_cutoff < sleep_hours <= upper_1:
                score = 90
                band = "upper_cutoff to upper_cutoff+1h"
            elif sleep_hours > upper_1:
                score = 40
                band = "> upper_cutoff+1h"
            elif lower_1 <= sleep_hours < lower_cutoff:
                score = 70
                band = "lower_cutoff-1h to lower_cutoff"
            elif lower_2 <= sleep_hours < lower_1:
                score = 40
                band = "lower_cutoff-2h to lower_cutoff-1h"
            elif lower_3 <= sleep_hours < lower_2:
                score = 20
                band = "lower_cutoff-3h to lower_cutoff-2h"
            else:
                score = 0
                band = "< lower_cutoff-3h"

            return {
                "score": score,
                "band": band,
                "sex": sex,
                "age": age,
                "age_group": f"{age_min}-{age_max}",
                "sleep_hours": sleep_hours,
                "mean_h": mean_h,
                "sd_h": sd_h,
                "upper_cutoff": upper_cutoff,
                "lower_cutoff": lower_cutoff,
            }

    raise ValueError(f"No age group found for age={age}, sex={sex}")


import json


def load_json(json_file: str):
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)


def get_bp_reference_row(
    bp_json: dict,
    sex: str,
    bp_type: str,
    age_years: float,
    height_cm: float,
):
    """
    Find the matching BP reference row for a given sex, bp_type, age, and height.

    Logic:
    - filter rows by exact age_years
    - from those rows, choose the nearest height_cm
    """
    sex = str(sex).strip().lower()
    bp_type = str(bp_type).strip().lower()

    if sex not in bp_json:
        raise ValueError("sex must be 'boys' or 'girls'")

    if bp_type not in bp_json[sex]:
        raise ValueError("bp_type must be 'systolic' or 'diastolic'")

    rows = bp_json[sex][bp_type]

    age_rows = [r for r in rows if float(r["age_years"]) == float(age_years)]

    if not age_rows:
        available_ages = sorted(set(float(r["age_years"]) for r in rows))
        raise ValueError(
            f"No BP reference rows found for age_years={age_years}. "
            f"Available ages: {available_ages}"
        )

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
):
    """
    Classify one BP value according to the rule:

    100: value < min(P90, fixed_90)
     75: value >= min(P90, fixed_90) and < min(P95, fixed_95)
     50: value >= min(P95, fixed_95) and < min(P99, fixed_99)
     25: value >= min(P99, fixed_99) and < min(P99+5, fixed_0)
      0: value >= min(P99+5, fixed_0)

    Example fixed cutoffs:
    - systolic: 120, 130, 140, 160
    - diastolic: 80, 85, 90, 100
    """
    thr_75 = min(float(p90), float(fixed_90))
    thr_50 = min(float(p95), float(fixed_95))
    thr_25 = min(float(p99), float(fixed_99))
    thr_0 = min(float(p99_plus_5), float(fixed_0))

    if value >= thr_0:
        return 0
    elif value >= thr_25:
        return 25
    elif value >= thr_50:
        return 50
    elif value >= thr_75:
        return 75
    else:
        return 100


def score_bp_from_json(
    json_file: str,
    sex: str,
    age_years: float,
    height_cm: float,
    systolic_bp: float,
    diastolic_bp: float,
    treated: bool = False,
):
    """
    Score blood pressure from a pre-built BP reference JSON.

    Parameters
    ----------
    json_file : str
        Path to BP reference JSON.
    sex : str
        'boys' or 'girls'
    age_years : float
        Age in years, e.g. 10.5
    height_cm : float
        Height in cm
    systolic_bp : float
        Measured systolic BP
    diastolic_bp : float
        Measured diastolic BP
    treated : bool
        If True, subtract 20 points from final score, minimum 0.

    Returns
    -------
    dict
        Detailed result with final score, component scores, and matched reference rows.
    """
    data = load_json(json_file)

    sex = str(sex).strip().lower()

    sys_row = get_bp_reference_row(
        bp_json=data,
        sex=sex,
        bp_type="systolic",
        age_years=age_years,
        height_cm=height_cm,
    )

    dia_row = get_bp_reference_row(
        bp_json=data,
        sex=sex,
        bp_type="diastolic",
        age_years=age_years,
        height_cm=height_cm,
    )

    sys_score = classify_bp_value(
        value=float(systolic_bp),
        p90=float(sys_row["p90"]),
        p95=float(sys_row["p95"]),
        p99=float(sys_row["p99"]),
        p99_plus_5=float(sys_row["p99_plus_5"]),
        fixed_90=120,
        fixed_95=130,
        fixed_99=140,
        fixed_0=160,
    )

    dia_score = classify_bp_value(
        value=float(diastolic_bp),
        p90=float(dia_row["p90"]),
        p95=float(dia_row["p95"]),
        p99=float(dia_row["p99"]),
        p99_plus_5=float(dia_row["p99_plus_5"]),
        fixed_90=80,
        fixed_95=85,
        fixed_99=90,
        fixed_0=100,
    )

    # overall score is the worse of systolic/diastolic
    final_score = min(sys_score, dia_score)

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
            "systolic_score": sys_score,
            "diastolic_score": dia_score,
        },
        "reference_rows": {
            "systolic": sys_row,
            "diastolic": dia_row,
        },
    }


import pandas as pd
import numpy as np

import numpy as np
import pandas as pd


def age_to_months(age_years: float) -> int:
    return int(round(age_years * 12))


def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    height_m = height_cm / 100.0
    if height_m <= 0:
        raise ValueError("Height must be greater than 0")
    return weight_kg / (height_m ** 2)


def get_bmi_reference_row(df: pd.DataFrame, sex: str, age_years: float) -> pd.Series:
    df2 = df.copy()
    df2.columns = [str(c).strip() for c in df2.columns]
    df2["sex"] = df2["sex"].astype(str).str.strip().str.lower()

    sex = sex.strip().lower()
    months = age_to_months(age_years)

    df_sex = df2[df2["sex"] == sex].copy()
    if df_sex.empty:
        raise ValueError(f"No BMI reference rows found for sex='{sex}'")

    if "Month" not in df_sex.columns:
        raise ValueError("Column 'Month' not found in BMI dataframe")

    for col in ["-3SD", "-2SD", "-1SD", "Median", "1SD", "2SD", "3SD"]:
        if col not in df_sex.columns:
            raise ValueError(f"Required column '{col}' not found in BMI dataframe")

    if months in df_sex["Month"].values:
        row = df_sex.loc[df_sex["Month"] == months].iloc[0]
    else:
        idx = (df_sex["Month"] - months).abs().idxmin()
        row = df_sex.loc[idx]

    return row


def score_bmi_value(bmi_value: float, row: pd.Series) -> int:
    minus_3 = float(row["-3SD"])
    minus_2 = float(row["-2SD"])
    plus_1 = float(row["1SD"])
    plus_2 = float(row["2SD"])
    plus_3 = float(row["3SD"])

    # If value > -2SD and < +1SD = 100
    if minus_2 < bmi_value < plus_1:
        return 100

    # If < -2SD and > -3SD or > +1SD and < +2SD = 70
    if (minus_3 < bmi_value < minus_2) or (plus_1 < bmi_value < plus_2):
        return 70

    # If < -3SD or > +2SD and < +3SD = 30
    if (bmi_value < minus_3) or (plus_2 < bmi_value < plus_3):
        return 30

    # If > +3SD = 0
    if bmi_value > plus_3:
        return 0

    # exact boundary handling
    if bmi_value == minus_2 or bmi_value == plus_1:
        return 100
    if bmi_value == minus_3 or bmi_value == plus_2:
        return 30
    if bmi_value == plus_3:
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
    row = get_bmi_reference_row(df=bmi_df, sex=sex, age_years=age_years)
    score = score_bmi_value(bmi_value=bmi_value, row=row)

    return {
        "score": score,
        "inputs": {
            "sex": sex,
            "age_years": age_years,
            "weight_kg": weight_kg,
            "height_cm": height_cm,
            "bmi": round(bmi_value, 2),
        },
        "reference_row": {
            "Month": int(row["Month"]),
            "-3SD": float(row["-3SD"]),
            "-2SD": float(row["-2SD"]),
            "-1SD": float(row["-1SD"]),
            "Median": float(row["Median"]),
            "1SD": float(row["1SD"]),
            "2SD": float(row["2SD"]),
            "3SD": float(row["3SD"]),
        }
    }