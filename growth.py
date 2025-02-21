import streamlit as st
import pandas as pd
import os
from io import BytesIO 

st.set_page_config(page_title == "Data sweeper",layout="wide")


# custom css
st.markdown(
"""
<style>
.stApp{
     background-color:black;
     color:white;
}
</style>

""",
unsafe_allow_html=True
)
# TITLE AND DESCRIPTION

st.title("Data Sweeper by Sahrish Rahman")
st.write("Transform your files between  CSV and excel formats with built-in  data cleaning and visualizations.")

# UPLOAD FILE
upload_files =st.file_uploader("Upload your files ( accepts csv, excel):",type=["cvs","xlsx"], accept_multiple_files=(True))

if upload_files:
    for file in upload_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        if file_ext == '.csv':
            df = pd.read_csv(file)
        elif file_ext == "xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file format. Please upload CSV or Excel files only:{file_ext}")
            continue
        # file details
        st.write("preview the head of the dataframe")
        st.dataframe(df.head())


# data cleaning options

    
        st.header("Data Cleaning options")
        if st.checkbox(f"clean data for{file.name}"):
            col1, col2 =st.columns(2)
            with col1:
                if st.button(f"Remove Duplicates from the file :{file.name}" ):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicats Removed!")
            with col2:
                if st.button(f"Handle Missing Values in the file :{file.name}"):
                   numeric_cols = df.select_dtypes(include=['number']).columns
                   df[numeric_cols]= df[numeric_cols].fillna(df[numeric_cols].mean())
                   st.write("Missing Values Handled!")

        st.subheader("select columns to keep")
        columns =st.multiselect(f"select columns for{file.name}", df.columns, default=df.columns)
        df= df[columns]


        # data visualization options
        st.subheader("Data Visualization options")
        if st.checkbox(f"visualize data for{file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])

        # conversion options

        st.subheader("Conversion options")
        conversion_type =st.radio(f"Convert {file.name} to:",["csv","excel"],key=file.name)
        if st.button (f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type =="CSV":
                df.to.csv(buffer,index=False)
                file_name =file.name.replace(file_ext, ".csv")
                mime_type ="text/csv"

            elif conversion_type =="excel":
                df.to_excel(buffer,index=False)
                file_name =file.name.replace(file_ext, ".xlsx")
                mime_type ="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                buffer.seek(0)

                st.download_button(
                    label=f"Download {file_name} as {conversion_type}",
                    data=buffer,
                    file_name=file_name,
                    mimetype=mime_type,
                )
st.success("All files processed successfully")