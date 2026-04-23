import streamlit as st
import pandas as pd

from utils import (
    sum_numbers,
    multiply_numbers,
    describe_dataframe,
    get_column_info,
    filter_dataframe,
)


st.set_page_config(page_title="Simple Streamlit Demo", layout="wide")

st.title("Simple Streamlit Demo App")
st.write("Choose a function from the sidebar.")

# Sidebar menu
menu = st.sidebar.selectbox(
    "Select function",
    [
        "Sum",
        "Multiply",
        "CSV Analysis",
    ]
)

# -----------------------------
# 1. SUM
# -----------------------------
if menu == "Sum":
    st.header("Sum Two Numbers")

    a = st.number_input("Enter first number", value=0.0)
    b = st.number_input("Enter second number", value=0.0)

    if st.button("Calculate Sum"):
        result = sum_numbers(a, b)
        st.success(f"Result: {a} + {b} = {result}")


# -----------------------------
# 2. MULTIPLY
# -----------------------------
elif menu == "Multiply":
    st.header("Multiply Two Numbers")

    a = st.number_input("Enter first number", value=1.0, key="mul_a")
    b = st.number_input("Enter second number", value=1.0, key="mul_b")

    if st.button("Calculate Multiply"):
        result = multiply_numbers(a, b)
        st.success(f"Result: {a} × {b} = {result}")


# -----------------------------
# 3. CSV ANALYSIS
# -----------------------------
elif menu == "CSV Analysis":
    st.header("CSV Upload and Simple Analysis")

    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        st.subheader("Preview")
        st.dataframe(df.head())

        st.subheader("Basic Summary")
        summary, numeric_desc, categorical_desc = describe_dataframe(df)

        st.write(f"**Rows:** {summary['rows']}")
        st.write(f"**Columns:** {summary['columns']}")
        st.write(f"**Column names:** {summary['column_names']}")

        st.subheader("Column Info")
        col_info = get_column_info(df)
        st.dataframe(col_info)

        st.subheader("Missing Values")
        st.json(summary["missing_values"])

        if not numeric_desc.empty:
            st.subheader("Numeric Description")
            st.dataframe(numeric_desc)

        if not categorical_desc.empty:
            st.subheader("Categorical Description")
            st.dataframe(categorical_desc)

        # Optional filtering
        st.subheader("Filter Data")
        filterable_cols = df.columns.tolist()
        selected_col = st.selectbox("Choose column to filter", filterable_cols)

        unique_values = df[selected_col].dropna().unique().tolist()
        if len(unique_values) > 0:
            selected_val = st.selectbox("Choose value", unique_values)

            if st.button("Apply Filter"):
                filtered_df = filter_dataframe(df, selected_col, selected_val)
                st.write(f"Filtered rows: {len(filtered_df)}")
                st.dataframe(filtered_df)