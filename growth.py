import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout="wide")

# Custom CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# TITLE AND DESCRIPTION
st.title("Data Sweeper by Sahrish Rahman")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualizations.")

# UPLOAD FILE
upload_files = st.file_uploader("Upload your files (accepts CSV, Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if upload_files:
    for file in upload_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file format. Please upload CSV or Excel files only: {file_ext}")
            continue

        # File details
        st.write(f"### Preview of {file.name}")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.header(f"Data Cleaning Options for {file.name}")

        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")

            with col2:
                if st.button(f"Handle Missing Values in {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values Handled!")

        # Column selection
        st.subheader(f"Select Columns to Keep for {file.name}")
        columns = st.multiselect(f"Select columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data Visualization
        st.subheader(f"Data Visualization for {file.name}")
        if st.checkbox(f"Visualize Data for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # File Conversion
        st.subheader(f"Conversion Options for {file.name}")
        conversion_type = st.radio(f"Convert {file.name} to:", ["csv", "excel"], key=f"conversion_{file.name}")

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()

            if conversion_type == "csv":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            st.download_button(
                label=f"Download {file_name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime_type=mime_type,
            )

st.success("All files processed successfully!")
