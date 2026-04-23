import streamlit as st
import pandas as pd 
import numpy as np
import os 

from utils import (

    load_csv, 
    get_basic_info, 
    filter_dataframe, 
    describe_dataframe,
    get_column_info,
)


st.set_page_config(page_title="Simple Streamlit Demo for CSV analysis", layout="wide")
st.title("Simple Streamlit Demo App")
st.write("Choose a function from the sidebar.")

# Sidebar menu
menu = st.sidebar.selectbox(
    "Select function",
    [
        "CSV Analysis",
        "Sum or Multiply",  
    ]
)

####### funciton for each menu itme ##############

if menu == 'CSV Analysis':
     st.header("CSV Upload and Analysis")

    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        try:
            df = load_csv(uploaded_file)
            st.success("CSV loaded successfully.")

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