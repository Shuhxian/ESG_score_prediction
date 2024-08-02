import streamlit as st
import pickle

st.set_page_config(page_title="Homepage", page_icon="📕")

st.markdown("# ESG Score Calculator Homepage")
st.sidebar.header("Homepage")

with open('fw_model_e.pkl', 'rb') as f:
  feature_weights_e = pickle.load(f)
with open('fw_model_s.pkl', 'rb') as f:
  feature_weights_s = pickle.load(f)
with open('fw_model_g.pkl', 'rb') as f:
  feature_weights_g = pickle.load(f)
st.write('Welcome to ESG Score Calculator. The calculator is used to calculate the Sustainalytics ESG Risk Score using equations discovered using our machine learning algorithms. '+ \
         'The formula of the equations are documented as follow: ')
st.markdown("## E Score Equation")
e_equation="E Score = "
for i, (f,c) in enumerate(feature_weights_e):
  if c>0 and i>0:
    e_equation+=f"+ {round(c,2)}*{f}"
  else:
    e_equation+=f" {round(c,2)}*{f}"
  if (i-2)%3==0:
    st.latex(e_equation)
    e_equation=""
st.latex(e_equation[:-2])

st.markdown("## S Score Equation")
s_equation="S Score = "
for i, (f,c) in enumerate(feature_weights_s):
  if c>0 and i>0:
    s_equation+=f"+ {round(c,2)}*{f}"
  else:
    s_equation+=f" {round(c,2)}*{f}"
  if (i-2)%3==0:
    st.latex(s_equation)
    s_equation=""
st.latex(s_equation[:-2])

st.markdown("## G Score Equation")
g_equation="G Score = "
for i, (f,c) in enumerate(feature_weights_g):
  if c>0 and i>0:
    g_equation+=f"+ {round(c,2)}*{f}"
  else:
    g_equation+=f" {round(c,2)}*{f}"
  if (i-2)%3==0:
    st.latex(g_equation)
    g_equation=""
st.latex(g_equation[:-2])

st.markdown("## ESG Score Equation")
st.latex(r'''ESG Risk Score = E Score + S Score + G Score''')
