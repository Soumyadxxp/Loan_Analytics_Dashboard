import streamlit as st
import pandas as pd
import plotly.express as px
import warnings
import io

warnings.filterwarnings("ignore")

# ================================
# PAGE CONFIG
# ================================
st.set_page_config(
    page_title="Interactive Loan Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.markdown("<br>", unsafe_allow_html=True)
st.title("Interactive Loan Analytics Dashboard")

# ================================
# SIDEBAR DROPDOWN STYLING
# ================================
st.markdown(
    """
    <style>
    section[data-testid="stSidebar"] .stSelectbox,
    section[data-testid="stSidebar"] .stMultiSelect {
        margin-bottom: 14px;
    }

    div[data-baseweb="popover"] {
        background-color: #111827 !important;
        border: 2px solid #3b82f6 !important;
        border-radius: 10px !important;
        box-shadow: 0 10px 25px rgba(59,130,246,.45) !important;
        z-index: 9999 !important;
    }

    li[data-baseweb="menu-item"] {
        background-color: #111827 !important;
        color: #e5e7eb !important;
        font-weight: 500;
    }

    li[data-baseweb="menu-item"]:hover {
        background-color: #2563eb !important;
        color: white !important;
    }

    li[aria-selected="true"] {
        background-color: #1d4ed8 !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ================================
# SAFE CSV LOADER (FIX)
# ================================
@st.cache_data
def load_csv_safe(file):
    try:
        if hasattr(file, "seek"):
            file.seek(0)  # IMPORTANT FIX
        return pd.read_csv(file)
    except pd.errors.EmptyDataError:
        st.error("Uploaded CSV is empty or unreadable.")
        st.stop()
    except Exception as e:
        st.error(f"CSV loading error: {e}")
        st.stop()

# ================================
# DATASET SELECTION
# ================================
st.subheader("Dataset Selection")

use_default = st.checkbox(
    "Use default dataset (test_Y3wMUE5_7gLdaTN.csv)",
    value=True
)

uploaded_file = None
if not use_default:
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if not use_default and uploaded_file is None:
    st.info("Please upload a CSV file to continue")
    st.stop()
# ================================
# RESET STATE WHEN NEW FILE UPLOADED
# ================================
if uploaded_file is not None and not use_default:
    if st.session_state.get("current_file") != uploaded_file.name:
        
        st.session_state.pop("null_columns", None)
        st.session_state.null_applied = False

        
        st.session_state.current_file = uploaded_file.name

        st.session_state.raw_df = load_csv_safe(uploaded_file)
        st.session_state.clean_df = st.session_state.raw_df.copy()

        # Store missing values BEFORE cleaning (for issue 1 later)
        st.session_state.missing_before = st.session_state.raw_df.isnull().sum()
        
        st.session_state.null_columns = (
            st.session_state.raw_df
            .columns[st.session_state.raw_df.isnull().sum() > 0]
            .tolist()
        )

# ================================
# SESSION STATE INIT
# ================================
if "raw_df" not in st.session_state:
    if use_default:
        st.session_state.raw_df = pd.read_csv("test_Y3wMUE5_7gLdaTN.csv")
    else:
        st.session_state.raw_df = load_csv_safe(uploaded_file)

if "clean_df" not in st.session_state:
    st.session_state.clean_df = st.session_state.raw_df.copy()

raw_df = st.session_state.raw_df
clean_df = st.session_state.clean_df

if "null_applied" not in st.session_state:
    st.session_state.null_applied = False


# ================================
# SIDEBAR : DATA PROCESSING
# ================================
st.sidebar.header("Data Processing")

remove_dupes = st.sidebar.checkbox("Remove duplicate rows", value=True)
if remove_dupes:
    clean_df = clean_df.drop_duplicates()
    
# ================================
# STORE NULL COLUMNS (UPLOAD CSV ONLY)
# ================================
if not use_default:
    # Recompute only once per dataset load
    if "null_columns" not in st.session_state:
        st.session_state.null_columns = clean_df.columns[
            clean_df.isnull().sum() > 0
        ].tolist()


# ================================
# NULL HANDLING (CSV ONLY)
# ================================
cleaning_log = []

def can_apply(series, method):
    if method in ["Mean", "Median"]:
        converted = pd.to_numeric(series, errors="coerce")
        return converted.notna().sum() > 0 and series.isnull().sum() > 0
    return True



if not use_default:
    st.sidebar.subheader("Missing Value Handling")

    null_cols = st.session_state.get("null_columns", [])
    strategies = {}  

    if not null_cols:
        st.sidebar.info(
            "All missing values are already handled."
        )
    else:
        for col in null_cols:
            strategies[col] = st.sidebar.selectbox(
                col,
                ["Mean", "Median", "Mode", "Drop"],
                key=f"null_{col}"
            )


    
    apply_clicked = st.sidebar.button(
        "Apply Null Handling Strategy",
        disabled=not bool(strategies) or st.session_state.null_applied
    )

    if apply_clicked:
        temp_df = clean_df.copy()
        temp_log = []
        errors = []

        for col, method in strategies.items():
            before = temp_df[col].isnull().sum()

            if not can_apply(temp_df[col], method):
                errors.append(f"{col}: {method} not valid for this column type")
                continue

            try:
                if method == "Mean":
                    temp_df[col] = pd.to_numeric(temp_df[col], errors="coerce")
                    temp_df[col] = temp_df[col].fillna(temp_df[col].mean())

                elif method == "Median":
                    temp_df[col] = pd.to_numeric(temp_df[col], errors="coerce")
                    temp_df[col] = temp_df[col].fillna(temp_df[col].median())

                elif method == "Mode":
                    temp_df[col] = temp_df[col].fillna(temp_df[col].mode()[0])
                elif method == "Drop":
                    temp_df = temp_df[temp_df[col].notnull()]

                after = temp_df[col].isnull().sum()
                temp_log.append([col, before, method, after])

            except Exception as e:
                errors.append(f"{col}: {e}")

        if errors:
            for e in errors:
                st.warning(e)
            st.info("Fix the issues and re-apply.")
        else:
            st.session_state.clean_df = temp_df.copy()
            clean_df = st.session_state.clean_df
            cleaning_log = temp_log
            
            st.session_state.null_applied = True

            # RESET + RECOMPUTE NULL COLUMNS
            st.session_state.null_columns = (
            clean_df.columns[clean_df.isnull().sum() > 0].tolist()
            )

else:
    # Default dataset auto cleaning
    for col in clean_df.select_dtypes(include="object"):
        if clean_df[col].isnull().sum() > 0:
            cleaning_log.append([col, clean_df[col].isnull().sum(), "Mode", 0])
            clean_df[col] = clean_df[col].fillna(clean_df[col].mode()[0])

    for col in clean_df.select_dtypes(include=["int64", "float64"]):
        if clean_df[col].isnull().sum() > 0:
            cleaning_log.append([col, clean_df[col].isnull().sum(), "Median", 0])
            clean_df[col] = clean_df[col].fillna(clean_df[col].median())
            
# ================================
# MISSING VALUE COMPARISON (CSV ONLY)
# ================================
if not use_default:
    before_missing = raw_df.isnull().sum()
    after_missing = clean_df.isnull().sum()

    missing_compare_df = pd.DataFrame({
        "Missing Before": before_missing,
        "Missing After": after_missing
    }).reset_index().rename(columns={"index": "Column"})


# ================================
# DATA CLEANING EXPLANATION
# ================================
st.subheader("Data Cleaning Explanation")

if use_default:
    # KEEP EXISTING BEHAVIOR FOR DEFAULT DATASET
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**Missing Values Before Cleaning**")
        st.dataframe(
            raw_df.isnull().sum()
            .rename("Missing Count")
            .to_frame()
            .rename_axis("Columns")
        )

    with c2:
        st.markdown("**Missing Values After Cleaning**")
        st.dataframe(
            clean_df.isnull().sum()
            .rename("Missing Count")
            .to_frame()
            .rename_axis("Columns")
        )

else:
    # SINGLE COMPARISON TABLE FOR UPLOADED CSV
    st.markdown("**Missing Values: Before vs After Cleaning**")
    st.dataframe(missing_compare_df, use_container_width=True)

# ================================
# RAW VS CLEAN
# ================================
if st.checkbox("Show Raw vs Clean Dataset"):
    r1, r2 = st.columns(2)
    with r1:
        st.subheader("Raw Dataset")
        st.dataframe(raw_df)
    with r2:
        st.subheader("Cleaned Dataset")
        st.dataframe(clean_df)

    if use_default:
        st.download_button(
            "Download Raw Dataset",
            raw_df.to_csv(index=False),
            "raw_dataset.csv"
        )

    st.download_button(
        "Download Cleaned Dataset",
        clean_df.to_csv(index=False),
        "cleaned_dataset.csv"
    )

# ================================
# FILTERS
# ================================
st.sidebar.header("Filters")

filtered_df = clean_df.copy()
for col in filtered_df.select_dtypes(include="object"):
    vals = st.sidebar.multiselect(f"Filter {col}", filtered_df[col].unique())
    if vals:
        filtered_df = filtered_df[filtered_df[col].isin(vals)]

# ================================
# METRICS
# ================================
m1, m2, m3 = st.columns(3)

m1.metric("Total Records", len(filtered_df))

numeric_cols = filtered_df.select_dtypes(include=["int64", "float64"]).columns

if len(numeric_cols) >= 1:
    m2.metric(
        f"Average {numeric_cols[0]}",
        round(filtered_df[numeric_cols[0]].mean(), 2)
    )
else:
    m2.metric("Average", "N/A")

if len(numeric_cols) >= 2:
    m3.metric(
        f"Average {numeric_cols[1]}",
        round(filtered_df[numeric_cols[1]].mean(), 2)
    )
else:
    m3.metric("Average", "N/A")

st.divider()

# ================================
# CUSTOM VISUALIZATION BUILDER
# ================================
st.subheader("Custom Visualization Builder")

chart_type = st.selectbox(
    "Select Chart Type",
    ["Bar Chart", "Scatter Plot", "Histogram", "Box Plot", "Pie Chart"]
)

x_axis = st.selectbox("Select X-Axis", filtered_df.columns)
num_cols = filtered_df.select_dtypes(include=["int64", "float64"]).columns.tolist()

if chart_type in ["Bar Chart", "Scatter Plot", "Box Plot"] and not num_cols:
    st.warning("No numeric columns available for this chart type.")
    st.stop()

if chart_type == "Bar Chart":
    y_axis = st.selectbox("Select Y-Axis", num_cols)
    fig = px.bar(filtered_df, x=x_axis, y=y_axis)
elif chart_type == "Scatter Plot":
    y_axis = st.selectbox("Select Y-Axis", num_cols)
    fig = px.scatter(filtered_df, x=x_axis, y=y_axis)
elif chart_type == "Histogram":
    fig = px.histogram(filtered_df, x=x_axis)
elif chart_type == "Box Plot":
    y_axis = st.selectbox("Select Y-Axis", num_cols)
    fig = px.box(filtered_df, x=x_axis, y=y_axis)
else:
    fig = px.pie(filtered_df, names=x_axis)

st.plotly_chart(fig, use_container_width=True)

# ================================
# SUMMARY + CORRELATION
# ================================
st.divider()
s1, s2 = st.columns(2)

with s1:
    st.subheader("Summary Statistics")
    st.dataframe(filtered_df[num_cols].describe().rename_axis("Columns"))

with s2:
    st.subheader("Correlation Heatmap")
    corr = filtered_df[num_cols].corr()
    fig_corr = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="Plasma",
        labels=dict(x="Columns", y="Columns")
    )
    fig_corr.update_layout(
        margin=dict(l=100, r=40, t=40, b=100),
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig_corr, use_container_width=True)

# ================================
# EDA EXPORT
# ================================
st.divider()
st.subheader("EDA Report Export")

include_info = st.checkbox("Include Dataset Info (df.info())")

if st.button("Generate EDA Report (HTML)"):
    html = "<h1>EDA Report</h1>"

    html += "<h2>Summary Statistics</h2>"
    html += filtered_df[num_cols].describe().to_html()

    html += "<h2>Missing Value Summary</h2>"
    html += filtered_df.isnull().sum().rename("Missing Count").to_frame().to_html()

    if include_info:
        buffer = io.StringIO()
        filtered_df.info(buf=buffer)
        html += "<h2>Dataset Info</h2><pre>" + buffer.getvalue() + "</pre>"

    fig_corr.update_layout(width=600, height=600)
    html += "<h2>Correlation Heatmap</h2>"
    html += fig_corr.to_html(full_html=False, include_plotlyjs="cdn")

    st.download_button(
        "Download EDA HTML",
        html,
        file_name="EDA_Report.html",
        mime="text/html"
    )
