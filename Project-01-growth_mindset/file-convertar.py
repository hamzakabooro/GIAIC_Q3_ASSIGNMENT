import streamlit as st
import pandas as pd
from io import BytesIO



st.set_page_config(page_title="file-converter",layout="wide")
st.title("file Converter & cleaner")
st.write("Upload csv or excel file, clean and convert formats.")

files = st.file_uploader("Upload CSV or EXcel file.", type=["csv", "xlsx"], accept_multiple_files=True)

if files :
    for file in files :
        ext = file.name.split(".")[-1]
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

        st.subheader(f"{file.name}-perview")
        st.detaframe(df.head())

        if st.checkbox(f"Remove Duplicates - {file.name}"):  
            df = df.drop_duplicates()
            st.success("Duplicates removed")
            st.dataframe(df.head())

            if st.checkbox(f"file messing velues - {file.name}"):
                df.fillna(df.select_dtypes(include=['number']).mean(), inplace=True)
                st.success("missing velues filled with maen")
                st.detaframe(df.head())
                
                selected_columns = st.multiselect(f"select COlumns -{file.name}",df.columns, default=df.columns)
                df = df[selected_columns]
                st.detaframe(df.head()) 
                if st.checkbox(f"show chart - {file.name}") and not df.select_dtypes(include='number').empty:
                 st.bar_chart(df.select_dtypes(include="number").iolc[:,:2])
                format_choice = st.radio(f"convert {file.name} to",["csv","Excle"], key=file.name)
                
                if st.button(f"Download {file.name} as {format_choice}" ):
                   output= BytesIO()
                   if format_choice == "csv":
                      df.to_cvs(output, index=False)
                      mine = "text/csv"
                      new_name = file.name.replace(ext,"csv")

                   else:
                      df.to_excel(output, index=False,engine='openpyxl')
                      main = "applicatoin/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                      new_name = file.name.replace(ext,"xlsx")

                      output.seak(0)
                      st.download_button( "download file ", file_name=new_name, deta=output, mimetype=mine)
                      st.success("peossing Complete")

                

