import streamlit as st

def defaults():
    st.session_state.saved_values = {
        "Water_treatment": 0,
        "GHG_sales": 0,
        "Biodiversity": 0,
        "Global_reporting_initiative": 0,
        "Climate_change_policy": 0,
        "Govt_collaboration": 0,
        "Recycling": 0,
        "ESG_funds": 0,
        "Disclosure_of_R&D": 0,
        "EPA_fines": 0,
        "Waste_management": 0,
        "Controversy_level": 3,
        "Integrated_reporting_framework": 0,
        "Indirect_carbon_emissions": 0,
        "Planning_zero_carbon": 0,
        "Green_innovation": 0,
        "S": 0,
        "Waste_management": 0,
        "CSR_board_size": 0,
        "Net_zero_targets": 0,
        "Issue_green_bonds": 0,
        "Scope3_carbon_emissions": 0,
        'Compliance_environmental_laws': 0,
        'Amount_of_fines' : 0,
        'Total_carbon_emissions' : 0,
        'Direct_carbon_emissions' : 0,
        'Renewal_energy': 0
    }

def update_value(key):
    st.session_state.saved_values[key]=st.session_state[key]
