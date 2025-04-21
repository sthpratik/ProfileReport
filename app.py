import streamlit as st 
import pandas as pd 
from ydata_profiling import ProfileReport
# from streamlit_pandas_profiling import st_profile_report
import sys
import os
import streamlit.components.v1 as components
from bs4 import BeautifulSoup

st.set_page_config(page_title='Data Profiler',layout='wide')


def get_filesize(file):
    size_bytes = sys.getsizeof(file)
    size_mb = size_bytes / (1024**2)
    return size_mb

def validate_file(file):
    filename = file.name
    name, ext = os.path.splitext(filename)
    if ext in ('.csv','.xlsx'):
        return ext
    else:
        return False

@st.cache_resource    
def save_file(file_name, data):
    with open(file_name, 'w') as f:
        f.write(data)
    return file_name

def remove_navbar_from_html(html_content):
    """
    Reads the HTML data, removes the content of the element with id 'navbar',
    and returns the modified HTML as a string.
    """
    # Parse the HTML content
    soup = BeautifulSoup(html_content, "html.parser")

    # Find the element with id 'navbar' and remove it
    navbar = soup.find(id="navbar")
    if navbar:
        navbar.decompose()

    # Return the modified HTML as a string
    return str(soup)

def get_dataframe(uploaded_file):
    df = None
    if uploaded_file is not None:
        ext = validate_file(uploaded_file)
        if ext:
            filesize = get_filesize(uploaded_file)
            if filesize <= 10:
                if ext == '.csv':
                    # time being let load csv
                    df = pd.read_csv(uploaded_file)
                else:
                    xl_file = pd.ExcelFile(uploaded_file)
                    sheet_tuple = tuple(xl_file.sheet_names)
                    sheet_name = st.sidebar.selectbox('Select the sheet',sheet_tuple)
                    df = xl_file.parse(sheet_name)
            else:
                st.error(f'Maximum allowed filesize is 10 MB. But received {filesize} MB')    
        else:
            st.error('Kindly upload only .csv or .xlsx file')     
    else:
        st.title('Data Profiler')
        st.info('Upload your data in the left sidebar to generate profiling')

    return df

@st.cache_resource
def get_profile_report(df,minimal):
    profile = ProfileReport(df, title="Profiling Report",minimal=minimal, explorative=True)
    return profile



def main():
    # sidebar
    minimal = False
    with st.sidebar:
        uploaded_file = st.file_uploader("Upload .csv, .xlsx files not exceeding 10 MB")
        if uploaded_file is not None:
            st.write('Modes of Operation')
            minimal = st.checkbox('Do you want minimal report ?')     

    df = get_dataframe(uploaded_file)    
    if df is not None:
        # generate report
        with st.spinner('Generating Report'):
            profile = get_profile_report(df,minimal)
            
        tab1, tab2 = st.tabs(["DataFrame", "Report"])
        with tab1:
            st.header("DataFrame")
            st.write(df, use_container_width=True)
        with tab2:
            profile_file = "report.html"
            # Save the profile report to an HTML file
            # save_file(profile_file, profile.html)
            # Remove the navbar from the HTML
            modified_html = remove_navbar_from_html(profile.html)
            components.html(modified_html, height=2000, scrolling=True)


if __name__ == "__main__":
    main()