# === IMPORT LIBRARIES ===
import streamlit as st                 # Web app UI
import pandas as pd                   # Data analysis and handling
from io import BytesIO                # In-memory file objects
import seaborn as sns                 # Data visualization (statistical)
import matplotlib.pyplot as plt       # Plotting (matplotlib backend)
import os
from fpdf import FPDF                 # Create PDFs
import plotly.express as px   
import streamlit as st
from PIL import Image

# Load and display the logo from the 'assets' folder
# === WEBPAGE TITLE ===
import streamlit as st
import base64

# Logo image (base64)
st.markdown("""
    <div style='
        border: 2px solid #00ffcc;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        background-color: #111111;
        margin-top: 20px;
    '>
        <h1 style='font-size: 42px; margin-bottom: 0;'>
            Welcome to <span style='color: #00ffcc;'>VizBoard</span>
        </h1>
    </div>
""", unsafe_allow_html=True)





# === DISPLAY STATIC IMAGE GALLERY OF GRAPH TYPES ===
st.subheader("Types of the Graphplots")

# First row (3 graph examples)
col1, col2, col3 = st.columns(3)
with col1:
    st.image("https://media.geeksforgeeks.org/wp-content/uploads/20240519083913/1.png", caption="Scatter Plot", use_container_width=True)
with col2:
    st.image("https://media.geeksforgeeks.org/wp-content/uploads/20240519083914/2.png", caption="Line Plot", use_container_width=True)
with col3:
    st.image("https://media.geeksforgeeks.org/wp-content/uploads/20240519083915/4.png", caption="Bar Plot", use_container_width=True)

# Second row (3 more graph examples)
col4, col5, col6 = st.columns(3)
with col4:
    st.image("https://media.geeksforgeeks.org/wp-content/uploads/20240519083916/6.png", caption="Box Plot", use_container_width=True)
with col5:
    st.image("https://media.geeksforgeeks.org/wp-content/uploads/20240519084142/11.png", caption="KDE Plot", use_container_width=True)
with col6:
    st.image("https://media.geeksforgeeks.org/wp-content/uploads/20240519084143/13.png", caption="ECDF Plot", use_container_width=True)

# === FUNCTION TO SHOW WHOLE GRAPH ON FULL DATA ===
def graph_show():
    st.subheader("The Full Data Graph")
    fig1 = plt.figure()
    if slide == "Scatter Plot":
        sns.scatterplot(df)
    elif slide == "Box Plot":
        sns.boxplot(df)
    elif slide == "Line Plot":
        sns.lineplot(df)
    elif slide == "Kernel Density Estimate Plot (kdeplot):":
        sns.kdeplot(df)
    elif slide == "Bar Plot":
        sns.barplot(df)
    elif slide == "Pairplot":
        sns.pairplot(df)
    st.pyplot(fig1)

# === FUNCTION TO PROCESS DATA (TOP, BOTTOM, DESCRIBE, FILTER) ===
def data_process():
    st.header("The Described Data Summary")

    global top, tail
    st.subheader("Top 10 Rows")
    top = df.head(10)
    st.write(top)

    st.subheader("Bottom 10 Rows")
    tail = df.tail(10)
    st.write(tail)

    st.subheader("Statistical Summary")
    st.write(df.describe())

    # Filter by X-axis value (in sidebar)
    if x_axis:
        global fa, filter_data, fi
        st.subheader(f"Filter by Unique {x_axis} Values")
        fa = df[x_axis].unique()
        filter_data = st.sidebar.selectbox(f"Filter {x_axis}", fa,key="filter x_axis")
        fi = df[df[x_axis] == filter_data]
        st.dataframe(fi)


    # Filter by Y-axis value (in sidebar)
    if y_axis:
        st.subheader(f"Filter by Unique {y_axis} Values")
        global la, ds, sd
        la = df[y_axis].unique()
        ds = st.sidebar.selectbox(f"Filter {y_axis}", la,key="filter y_axis")
        sd = df[df[y_axis] == ds]
        st.dataframe(sd)

       

    st.success("Data Summary Displayed Successfully!")

# === FUNCTION TO LET USER SELECT GRAPH TYPE FROM SIDEBAR ===
def graph():
    st.write("Select the type of graph:")
    global slide
    st.sidebar.subheader(" filters")
    slide = st.sidebar.selectbox("Select the Graph Plot", [
        "Scatter Plot", "Line Plot", "Bar Plot", "Box Plot",
        "Kernel Density Estimate Plot (kdeplot):", "Pairplot"
    ])

# === FUNCTION TO READ FILE ===
def read_file():
    global df
    df = pd.read_csv(file)
    graph()

# === FILE UPLOADER ===
file = st.file_uploader("Upload your file", type=["csv"])
if file:
    read_file()

# === BUTTON STYLING ===
st.markdown("""
    <style>
    div.stButton > button {
        background-color: #ffcc00;
        color: black;
        border-radius: 10px;
        padding: 0.5em 2em;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# === STATE TO SWITCH BETWEEN PAGES ===
if "show_graphs" not in st.session_state:
    st.session_state.show_graphs = False

# === BUTTON TO PROCEED TO NEXT PAGE ===
col1, col2 = st.columns([1, 2])
with col2:
   if st.button("Show"):
       st.session_state.show_graphs = True

    

# === FUNCTION TO CREATE PDF FROM PLOT ONLY ===
from fpdf import FPDF
from PIL import Image
import tempfile
from io import BytesIO

def create_pdf_with_plot_only(plot_buf):
    plot_image = Image.open(plot_buf)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_plot:
        plot_image.save(tmp_plot.name)
        plot_path = tmp_plot.name

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Generated Plot", ln=True, align='C')
    pdf.image(plot_path, x=10, y=25, w=180)

    pdf_bytes = pdf.output(dest='S').encode('latin1')
    pdf_output = BytesIO(pdf_bytes)
    pdf_output.seek(0)

    return pdf_output

# === DISPLAY GRAPH + PROCESS DATA SECTION ===
if st.session_state.show_graphs:
    st.markdown("<h2 style='color:#00cc99;'>Graph Output Section</h2>", unsafe_allow_html=True)
    graph_show()

    # Select X and Y axis
    st.subheader("Compare the Graphs with X and Y")
    x_axis = st.sidebar.selectbox("Select X-axis column", df.columns)
    y_axis = st.sidebar.selectbox("Select Y-axis column", df.columns)

    fig = plt.figure()

    if slide == "Scatter Plot":
        sns.scatterplot(data=df, x=x_axis, y=y_axis)
    elif slide == "Line Plot":
        sns.lineplot(data=df, x=x_axis, y=y_axis)
    elif slide == "Bar Plot":
        sns.barplot(data=df, x=x_axis, y=y_axis)
    elif slide == "Box Plot":
        sns.boxplot(data=df, x=x_axis, y=y_axis)
    elif slide == "Kernel Density Estimate Plot (kdeplot):":
        sns.kdeplot(data=df, x=x_axis, y=y_axis)
    elif slide == "Pairplot":
        st.pyplot(sns.pairplot(df))
        data_process()
        st.stop()

    plt.title(f"{y_axis} vs {x_axis} — {slide}")
    st.pyplot(fig)

    # Process data summary and filters
    data_process()

# === DOWNLOAD SECTION ===
col1, col2 = st.columns([1, 2])
with col2:
    file_name = st.text_input("Input the file name to save the graph:")
    if st.button("Download"):
        if file_name.strip():
            # Save plot to memory
            plot_buf = BytesIO()
            fig.savefig(plot_buf, format="png")
            plot_buf.seek(0)

            # Generate PDF and allow download
            pdf_file = create_pdf_with_plot_only(plot_buf)
            st.download_button(
                label="Download Graph + Data PDF",
                data=pdf_file,
                file_name=file_name.strip() + ".pdf",
                mime="application/pdf"
            )
            st.success("Graph + Data PDF downloaded successfully!")

