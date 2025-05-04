import streamlit as st 
import pandas as pd 
from ydata_profiling import ProfileReport
# from streamlit_pandas_profiling import st_profile_report
import sys
import os
import streamlit.components.v1 as components
from bs4 import BeautifulSoup
import seaborn as sns
import matplotlib.pyplot as plt

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
async def save_file(file_name, data):
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

@st.cache_resource
def get_dataframe(uploaded_file):
    df = None
    if uploaded_file is not None:
        ext = validate_file(uploaded_file)
        if ext:
            filesize = get_filesize(uploaded_file)
            if filesize <= 100:
                if ext == '.csv':
                    # time being let load csv
                    df = pd.read_csv(uploaded_file)
                else:
                    xl_file = pd.ExcelFile(uploaded_file)
                    sheet_tuple = tuple(xl_file.sheet_names)
                    sheet_name = st.sidebar.selectbox('Select the sheet',sheet_tuple)
                    df = xl_file.parse(sheet_name)
            else:
                st.error(f'Maximum allowed filesize is 100 MB. But received {filesize} MB')    
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

@st.cache_resource  
def sns_heatmap(df):
    try:
        fig, ax = plt.subplots(figsize=(20, 10))  # Adjust the size (width=5, height=3)
        # Create a Seaborn correlation plot
        plot = sns.heatmap(df.select_dtypes(include=['number']).corr(), annot=True,  cmap='coolwarm', fmt='.2f')
        # Display the plot in Streamlit
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Data not supported for the selected plot type: {e}")

@st.cache_resource  
def pair_plot(df):
    try:
        # Create a pair plot
        fig, ax = plt.subplots(figsize=(20, 10))  # Adjust the size (width=5, height=3)
        # Create a Seaborn pairplot
        plot = sns.pairplot(df)
        # Display the plot in Streamlit
        st.pyplot(plot.figure)
    except Exception as e:
        st.error(f"Data not supported for the selected plot type: {e}")


@st.cache_resource  
def df_stats(df):
    #write function to show the stats of the dataframe like mean, median, mode, std, var, skew, kurtosis
    st.subheader('Statistics')
    st.write(df.describe())


@st.cache_resource  
def value_count_plot(df):
    st.subheader('Value Count')
    st.write('Select the column and plot type for the value count')

        # create columns for the scatter plot
    col1, col2 = st.columns([0.25, 0.75])

    with col1:
        # Create a selectbox for selecting the column
        column = st.selectbox('Select Column', df.columns, key="value_count_selectbox")
            

        # Create a selectbox for selecting the plot type
        plot_type = st.selectbox(
            'Select Plot Type',
            ['line', 'bar', 'barh', 'hist', 'box', 'kde', 'density', 'area', 'pie', 'scatter', 'hexbin'],
            key="value_count_plot_type_selectbox"
        )

        st.write(df[column].describe())

    with col2:
        if column:
            try:
                # Generate the value counts for the selected column
                value_counts = df[column].value_counts()

                # Plot based on the selected plot type
                if plot_type == 'pie':
                    # Special handling for pie plot
                    fig, ax = plt.subplots(figsize=(10, 6))
                    value_counts.plot.pie(autopct='%1.1f%%', ax=ax)
                    ax.set_ylabel('')  # Remove y-axis label for pie chart
                    st.pyplot(fig)
                else:
                    # General plotting for other types
                    fig, ax = plt.subplots(figsize=(10, 6))
                    value_counts.plot(kind=plot_type, ax=ax)
                    st.pyplot(fig)
            except Exception as e:
                st.error(f"Error generating the plot: {e}")

@st.cache_resource  
def sns_scatter_plot(df):
    # create columns for the scatter plot
    col1, col2 = st.columns([0.25, 0.75])
    with col1:
        st.subheader('Seaborn Plot')
        st.write('Select the columns for the scatter plot')
        #create a selectbox for selecting the columns
        x_axis = st.selectbox('Select X-axis', df.columns, key="sns_x_axis_selectbox")
        y_axis = st.selectbox('Select Y-axis', df.columns, key="sns_y_axis_selectbox")
        #Create a selectbox for selecting the plot type
        plot_type = st.selectbox('Select Plot Type', ['scatterplot','kdeplot','histplot',
                                                      'displot','lmplot','barplot','pointplot','catplot'], key="sns_plot_type_selectbox")
                # Define a mapping of plot types to Seaborn functions
        plot_functions = {
            'scatterplot': sns.scatterplot,
            'displot': sns.displot,
            'lmplot': sns.lmplot,
            'barplot': sns.barplot,
            'kdeplot': sns.kdeplot,
            'histplot': sns.histplot,
            'barplot': sns.barplot,
            'pointplot': sns.pointplot,
            'catplot': sns.catplot
        }
    with col2:
        try:
            st.write('Select the columns for the plot')
            fig, ax = plt.subplots(figsize=(20, 10))  # Adjust the size (width=5, height=3)
            # Get the selected plot function
            plot_func = plot_functions.get(plot_type)
            plot_func(data=df, x=x_axis, y=y_axis)
            # Display the plot in Streamlit
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Data not supported for the selected plot type: {e}")

def main():
    # Sidebar
    minimal = False
    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None
    if "dataframe" not in st.session_state:
        st.session_state.dataframe = None

    if st.session_state.uploaded_file is None:
        with st.sidebar:
            # File uploader
            uploaded_file = st.file_uploader("Upload .csv, .xlsx files not exceeding 10 MB", key="file_uploader")
            if uploaded_file is not None:
                st.session_state.uploaded_file = uploaded_file  # Cache the uploaded file
                st.write('Modes of Operation')
                minimal = st.checkbox('Do you want minimal report ?', key="minimal_checkbox")

    # Use the cached file from session state
    if st.session_state.uploaded_file is not None:
        if st.session_state.dataframe is None:  # Load the DataFrame only if not already cached
            st.session_state.dataframe = get_dataframe(st.session_state.uploaded_file)

        df = st.session_state.dataframe
        if df is not None:
            # Generate report
            with st.spinner('Generating Report'):
                profile =  get_profile_report(df, minimal)
            tab1, tab2 = st.tabs(["DataFrame", "Report"])
            with tab1:
                st.header("DataFrame")
                df.height = 2000
                st.write(df)
                stats_tab, valuepoint_tab,heatmap_tab, pairplot_tab, seabornplot = st.tabs(["Statistics","Valuepoint","Heatmap", "Pairplot", "Column Distribution"])
                with heatmap_tab:
                    sns_heatmap(df)
                with pairplot_tab:
                    pair_plot(df)
                with stats_tab:
                    df_stats(df)
                with valuepoint_tab:
                    value_count_plot(df=df)
                with seabornplot:
                    sns_scatter_plot(df=df)
            with tab2:
                profile_file = "report.html"
                #save_file(profile_file, profile.html)
                # Remove the navbar from the HTML
                modified_html = remove_navbar_from_html(profile.html)
                components.html(modified_html, height=2000, scrolling=True)
    
    else:
        st.title('Data Profiler')
        st.info('Upload your data in the left sidebar to generate profiling')


if __name__ == "__main__":
    main()