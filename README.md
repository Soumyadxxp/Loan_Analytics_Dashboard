# Interactive Loan Analytics Dashboard

An interactive dashboard built with Streamlit and Plotly to explore, clean, and visualize loan data.    
Perfect for quick exploratory data analysis (EDA) on loan portfolios.
<img width="1600" height="1112" alt="image" src="https://github.com/user-attachments/assets/3ecfcf91-5c20-4325-a8a8-594d5dc6c7cd" />
<img width="1600" height="1112" alt="image" src="https://github.com/user-attachments/assets/b3ad3271-a34e-4ed5-bf8d-5e36b6d1f212" />
<img width="1600" height="1112" alt="image" src="https://github.com/user-attachments/assets/dfb1a5c3-9112-4397-959b-b1353580bc6d" />
<img width="1600" height="1112" alt="image" src="https://github.com/user-attachments/assets/e2e5c21a-2602-4d78-808a-f1a3276881f1" />
<img width="1600" height="1112" alt="image" src="https://github.com/user-attachments/assets/f37debe4-39b1-425b-8ec8-ac99fb3f61fb" />
<img width="1600" height="1112" alt="image" src="https://github.com/user-attachments/assets/c04432f9-2af5-4262-9952-833712326978" />
<img width="1600" height="1112" alt="image" src="https://github.com/user-attachments/assets/cdfafe9c-ece9-4248-9729-cc124aa93985" />
<img width="1600" height="1112" alt="image" src="https://github.com/user-attachments/assets/58ed1570-af55-4bbf-9270-3100dbdeeb0a" />
<img width="1600" height="1112" alt="image" src="https://github.com/user-attachments/assets/73af9ca3-5bc1-4828-b473-317a77cc142a" />
<img width="1600" height="1112" alt="image" src="https://github.com/user-attachments/assets/64c656fd-16e2-43b6-8188-8e337e608c0c" />
<img width="1600" height="1112" alt="image" src="https://github.com/user-attachments/assets/f642fcf1-9d3a-4dc1-82c5-1275d6d0fd36" />
<img width="1600" height="1112" alt="image" src="https://github.com/user-attachments/assets/4e185049-fe07-4d48-b822-af892d832c5f" />
<img width="1600" height="1112" alt="image" src="https://github.com/user-attachments/assets/a990f1a2-9a6d-40cc-a979-7f0379261412" />

---

## Features

- Data Upload & Selection – Use the default sample dataset or upload your own CSV.
- Automatic Data Cleaning – Handle missing values with mean, median, mode imputation or row dropping.
- Interactive Filters – Filter by any categorical column.
- Custom Visualization Builder – Create bar charts, scatter plots, histograms, box plots, and pie charts with a few clicks.
- Summary Statistics – View descriptive statistics and correlation heatmaps.
- EDA Report Export – Generate an HTML report containing statistics and the correlation heatmap.

---

## Tech Stack

- Python 3.8+
- Streamlit – App framework
- Pandas – Data manipulation
- Plotly – Interactive visualizations
- Faker – Sample data generation 

---

## Installation

Clone this repository or download the files.

1. Install dependencies (preferably in a virtual environment):

   ```
   pip install streamlit pandas plotly faker pandas
   ```

   Note: `faker` is only required if you want to generate the sample CSV.

2. Generate the default sample dataset (if you don't have your own CSV):

   ```
   python generate_loan_data.py
   ```

   This will create `test_Y3wMUE5_7gLdaTN.csv` in the current folder.

---

## How to Run

Navigate to the project folder and start the Streamlit app:

```
streamlit run Loan_Analytics_Dashboard.py
```

The dashboard will open in your default browser at `http://localhost:8501`.

---

## Project Structure

```
Loan_Analytics_Dashboard/
├── Loan_Analytics_Dashboard.py   # Main Streamlit app
├── generate_loan_data.py         # Sample data generator 
├── test_Y3wMUE5_7gLdaTN.csv      # Default sample dataset
└── README.md                     
```

---

## Usage Guide

### Data Selection
- Check "Use default dataset" to load the sample CSV.
- Uncheck and upload your own CSV file to analyse your own data.

### Data Cleaning
- For uploaded CSVs: Choose a strategy (Mean, Median, Mode, Drop) for each column with missing values.
- For the default dataset: Missing values are automatically imputed (object columns -> mode, numeric -> median).

### Visualizations
- Use the sidebar filters to subset your data.
- Build custom charts by selecting chart type, X‑axis, and Y‑axis (if applicable).
- View correlation heatmap and summary statistics at the bottom.

### Export
- Click "Generate EDA Report (HTML)" to download a self‑contained report.

---

## Sample Data

The generator script (`generate_loan_data.py`) creates 500 loan records with the following columns:

- Loan_ID – Unique identifier
- Borrower_Name – Fake name
- Loan_Amount – Amount borrowed
- Interest_Rate – Annual interest rate
- Term_Months – Loan term (36, 48, or 60 months)
- Grade – Risk grade (A–F)
- Employment_Length – Work experience
- Annual_Income – Annual income
- Debt_to_Income – DTI ratio
- Loan_Status – Fully Paid / Charged Off / Current

About 5% missing values are introduced in some columns to demonstrate the cleaning functionality.

---


