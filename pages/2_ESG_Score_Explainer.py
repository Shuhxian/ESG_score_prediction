import streamlit as st
from helper import defaults, update_value
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title="Explainer", page_icon="⚖️")

st.markdown("# ESG Score Explainer")
st.sidebar.header("Explainer")

with open('fw_model_e.pkl', 'rb') as f:
  feature_weights_e = pickle.load(f)
  feature_weights_e.pop()
with open('fw_model_s.pkl', 'rb') as f:
  feature_weights_s = pickle.load(f)
  feature_weights_s.pop()
with open('fw_model_g.pkl', 'rb') as f:
  feature_weights_g = pickle.load(f)
  feature_weights_g.pop()

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

#Button to select E, S, G, or total
st.selectbox(
    "Pillar to be Analyzed",
    ("E", "S", "G", "ESG"), key="component")

#slider to choose n
st.slider("Number of Key Factors", 1, 5, key="n_features")

submitted = st.button("Submit")

if submitted:
  #save the sum of contribution of each relevant feature to a dict
  contribution={}
  df=pd.DataFrame(st.session_state.saved_values,index=[0])
  for col in ["GHG_sales","ESG_funds",'Amount_of_fines']:
    df[col+"_log"]=np.log(df[col]+1)
    df.drop(col,axis=1,inplace=True)
  for col in ["Indirect_carbon_emissions","Scope3_carbon_emissions",'Total_carbon_emissions', 'Direct_carbon_emissions']:
    df[col+"_sqrt"]=np.sqrt(df[col]+1)
    df.drop(col,axis=1,inplace=True)
  if "E" in st.session_state['component']:
    transformed=model_e[:-1].transform(df)[0]
    col_names=[]
    for i in range(len(model_e[:-1].get_feature_names_out())):
      col_names.append(model_e[:-1].get_feature_names_out()[i].split("__")[1])
    transformed=pd.DataFrame(transformed.reshape(1,-1),columns=col_names)
    for f,w in feature_weights_e:
      f=f.replace("\\","")
      if f not in contribution: contribution[f]=0
      contribution[f]+=w*transformed[f][0]
  if "S" in st.session_state['component']:
    transformed=model_s[:-1].transform(df)[0]
    col_names=[]
    for i in range(len(model_s[:-1].get_feature_names_out())):
      col_names.append(model_s[:-1].get_feature_names_out()[i].split("__")[1])
    transformed=pd.DataFrame(transformed.reshape(1,-1),columns=col_names)
    for f,w in feature_weights_s:
      f=f.replace("\\","")
      if f not in contribution: contribution[f]=0
      contribution[f]+=w*transformed[f][0]
  if "G" in st.session_state['component']:
    transformed=model_g[:-1].transform(df)[0]
    col_names=[]
    for i in range(len(model_g[:-1].get_feature_names_out())):
      col_names.append(model_g[:-1].get_feature_names_out()[i].split("__")[1])
    transformed=pd.DataFrame(transformed.reshape(1,-1),columns=col_names)
    for f,w in feature_weights_g:
      f=f.replace("\\","")
      if f not in contribution: contribution[f]=0
      contribution[f]+=w*transformed[f][0]

  #sort the dict by value and select the top n and bottom n
  contribution_sorted=sorted(contribution.items(), key=lambda x: x[1]) #lower is better
  top_n=contribution_sorted[:st.session_state.n_features]
  bottom_n=contribution_sorted[-st.session_state.n_features-1:-1][::-1]

  #output
  st.markdown("## Top Positive Factors")
  for i in range(len(top_n)):
    if top_n[i][1]>=0: break
    feature=top_n[i][0].split("_")
    if feature[-1] in ["log","sqrt"]: feature.pop()
    st.write(f"{' '.join(feature)} : {top_n[i][1]}")
  st.markdown("## Top Negative Factors")
  for i in range(len(bottom_n)):
    if bottom_n[i][1]<=0: break
    feature=bottom_n[i][0].split("_")
    if feature[-1] in ["log","sqrt"]: feature.pop()
    st.write(f"{' '.join(feature)} : {bottom_n[i][1]}")
