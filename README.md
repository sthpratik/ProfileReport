# ProfileReport

ProfileReport is a data analytics tool built using **Streamlit** that allows users to generate detailed profiling reports for their datasets. It supports `.csv` and `.xlsx` file formats and provides an interactive interface for exploring data insights.

![Home Page](./docs/home.png)
![Report Page](./docs/report.png)

---

## Features

- **File Upload**: Upload `.csv` or `.xlsx` files up to 10 MB.
- **DataFrame Display**: View the uploaded dataset in a tabular format.
- **Profiling Report**: Generate an interactive profiling report using the `ydata-profiling` library.
- **Minimal Report Option**: Choose between a full or minimal profiling report.
- **Excel Sheet Selection**: For `.xlsx` files, select the desired sheet to analyze.
- **Custom HTML Rendering**: Removes unnecessary navigation elements from the profiling report for a cleaner display.

---

## Libraries Used

- **Streamlit**: For building the web application interface.
- **Pandas**: For data manipulation and analysis.
- **ydata-profiling**: For generating detailed profiling reports.
- **BeautifulSoup**: For modifying the HTML content of the profiling report.
- **Streamlit Components**: For embedding custom HTML content in the app.

---

## Installation and Setup

### 1. Create a Python Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
streamlit run app.py
```

---

## How to Use

1. **Upload a File**: Use the sidebar to upload a `.csv` or `.xlsx` file.
2. **Select Options**: Choose the minimal report option if desired.
3. **View Data**: Explore the uploaded dataset in the "DataFrame" tab.
4. **Generate Report**: View the profiling report in the "Report" tab.

---

## Testing

- Upload a `.csv` file to generate a profiling report.
- For `.xlsx` files, select the desired sheet from the sidebar.

---

## Notes

- The maximum allowed file size is **10 MB**.
- Only `.csv` and `.xlsx` file formats are supported.
- The profiling report is displayed directly in the app, with unnecessary navigation elements removed for better usability.





