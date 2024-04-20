import streamlit as st
import requests

# Set page title and favicon
st.set_page_config(page_title="Medicine Information", page_icon=":pill:")

# Define CSS styles for Material Design
material_css = """
<style>
    body {
        font-family: 'Roboto', sans-serif;
        background-color: #f5f5f5;
    }
    .title {
        color: #3f51b5;
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .input {
        width: 100%;
        padding: 12px 20px;
        margin: 8px 0;
        box-sizing: border-box;
        border: 2px solid #ccc;
        border-radius: 4px;
        font-size: 18px;
    }
    .button {
        background-color: #3f51b5;
        color: white;
        padding: 14px 20px;
        margin: 8px 0;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 18px;
    }
    .button:hover {
        background-color: #283593;
    }
    .info {
        background-color: white;
        padding: 20px;
        border-radius: 4px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
    }
    .info h2 {
        color: #3f51b5;
        font-size: 24px;
        margin-bottom: 10px;
    }
    .info p {
        font-size: 18px;
        line-height: 1.6;
    }
</style>
"""

# Apply Material Design styles
st.markdown(material_css, unsafe_allow_html=True)

# Display title
st.markdown("<div class='title'>Medicine Information</div>", unsafe_allow_html=True)

# User input for medicine name
medicine_name = st.text_input("Enter the active substance or brand name:", "", key="medicine_input")

if st.button("Search"):
    # API endpoint for FDA's drug database
    url = f"https://api.fda.gov/drug/label.json?search=openfda.brand_name:{medicine_name}+openfda.generic_name:{medicine_name}&limit=1"
    
    # Make API request
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        if data["results"]:
            # Extract relevant information
            medicine_info = data["results"][0]
            brand_name = medicine_info.get("openfda", {}).get("brand_name", ["N/A"])[0]
            generic_name = medicine_info.get("openfda", {}).get("generic_name", ["N/A"])[0]
            indications = medicine_info.get("indications_and_usage", ["N/A"])[0]
            dosage = medicine_info.get("dosage_and_administration", ["N/A"])[0]
            warnings = medicine_info.get("warnings", ["N/A"])[0]
            adverse_reactions = medicine_info.get("adverse_reactions", ["N/A"])[0]
            
            # Display medicine information
            st.markdown("<div class='info'>", unsafe_allow_html=True)
            st.markdown(f"<h2>{brand_name}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Generic Name:</strong> {generic_name}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Indications and Usage:</strong> {indications}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Dosage and Administration:</strong> {dosage}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Warnings:</strong> {warnings}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Adverse Reactions:</strong> {adverse_reactions}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("No information found for the specified medicine.")
    else:
        st.error("Failed to retrieve data from the FDA's database.")