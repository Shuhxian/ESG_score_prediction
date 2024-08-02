import streamlit as st
from helper import defaults, update_value

import pandas as pd
from imblearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.feature_selection import RFE
import numpy as np
import pickle

st.set_page_config(page_title="Calculator", page_icon="🧮")

st.markdown("# ESG Score Calculator")
st.sidebar.header("Calculator")

with open('model_e.pkl', 'rb') as f:
  model_e = pickle.load(f)
with open('model_s.pkl', 'rb') as f:
  model_s = pickle.load(f)
with open('model_g.pkl', 'rb') as f:
  model_g = pickle.load(f)

if "saved_values" not in st.session_state:
    defaults()
else:
  for key in st.session_state.saved_values:
    st.session_state[key]=st.session_state.saved_values[key]

num_input=["GHG_sales","ESG_funds","Indirect_carbon_emissions","CSR_board_size","Scope3_carbon_emissions","Net_zero_targets", 'Amount_of_fines', 'Total_carbon_emissions', 'Direct_carbon_emissions', ]
for num in num_input:
  st.number_input(num.replace("-"," "),key=num, on_change=update_value, args=[num])

st.slider("Controversy level", 0, 5, key="Controversy_level", on_change=update_value, args=["Controversy_level"])

cat_input=["Water_treatment","Biodiversity","Global_reporting_initiative","Climate_change_policy","Govt_collaboration","Recycling","Disclosure_of_R&D","EPA_fines","Waste_management","Integrated_reporting_framework",\
           "Planning_zero_carbon","Green_innovation","S","Issue_green_bonds", 'Compliance_environmental_laws', 'Renewal_energy']

for cat in cat_input:
  st.checkbox(cat.replace("-"," "),key=cat, on_change=update_value, args=[cat])

submitted = st.button("Submit")

if submitted:
  test=pd.DataFrame(st.session_state.saved_values,index=[0])
  for col in ["GHG_sales","ESG_funds",'Amount_of_fines']:
    test[col+"_log"]=np.log(test[col]+1)
    test.drop(col,axis=1,inplace=True)
  for col in ["Indirect_carbon_emissions","Scope3_carbon_emissions",'Total_carbon_emissions', 'Direct_carbon_emissions']:
    test[col+"_sqrt"]=np.sqrt(test[col]+1)
    test.drop(col,axis=1,inplace=True)
  e_score=max(0,model_e.predict(test)[0])
  s_score=max(0,model_s.predict(test)[0])
  g_score=max(0,model_g.predict(test)[0])
  st.write(f"E Score: {round(e_score,2)}")
  st.write(f"S Score: {round(s_score,2)}")
  st.write(f"G Score: {round(g_score,2)}")
  st.write(f"ESG Score: {round(e_score+s_score+g_score,2)}")
