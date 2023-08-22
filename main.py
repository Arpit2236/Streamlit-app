import streamlit as st
import pandas as pd 
import numpy as np 
import plotly.express as px 
import seaborn as sns 

@st.cache_data()
def load_data():
    return pd.read_csv('datasets/data.csv')

with st.spinner("Loading dataset..."):
    df = load_data()

st.title('My DataScience App')
st.dataframe(df)

st.header('Data Visualization')
st.subheader('Top 10 Job titles of the employees')
job_count=df['job_title'].value_counts().head(10)

fig1 = px.bar(job_count,job_count.index,job_count.values,title='Job titles of the employees')
st.plotly_chart(fig1, use_container_width=True)
st.subheader("These are the popular jobs")
st.info(",".join(job_count.index.tolist()))

# main question from the data set
st.markdown(''' 
## What can we find out?
- basic categorical analysis
- salary trend on the basis of
    - year
    - experience
    - employment type
    - job title
    - location
    - company size
    - currency
- statistical analysis of different category vs salary
''')

categories = df.select_dtypes(exclude=np.number).columns.tolist()
st.success(f'There are following categories:{",".join(categories)}')
for col in categories:
    counts = df[col].value_counts()
    if df[col].nunique() > 10:
        fig=px.bar(counts,counts.index,counts.values,log_y=True,text=counts.values,title=f'Distribution of {col}')
        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    else:
        fig = px.pie(counts,counts.index,counts.values,title=f'Distribution of {col}')
    st.plotly_chart(fig, use_container_width=True)
st.subheader("Trend of Salary over the years ")
year_wise_df_sum = df.groupby('work_year')[['salary','salary_in_usd']].sum().reset_index()
year_wise_df_mean = df.groupby('work_year')[['salary','salary_in_usd']].mean().reset_index()
st.dataframe(year_wise_df_sum, use_container_width=True)

fig = px.bar(year_wise_df_sum,'work_year', 'salary_in_usd',title='Salary trend over the years')
fig2 = px.area(year_wise_df_mean,'work_year', 'salary_in_usd',title='Mean Salary trend over the years')
c1, c2 = st.columns(2)
c1.plotly_chart(fig, use_container_width=True)
c2.plotly_chart(fig2, use_container_width=True)

c1, c2 =st.columns(2)
cats = c1.multiselect('Select Categories', categories)
graphs = ['box','violin', 'swarp', 'sunburst', 'treemap']
graph = c2.selectbox('Select graph',graphs)

for col in cats:
    if graph==graphs[0]:
        fig = px.box(df, x=col, y='salary_in_usd',title=f'Salary distribution of {col}')
    elif graph==graphs[1]:
        fig = px.box(df, x=col, y='salary_in_usd',title=f'Salary distribution of {col}')
    elif graph==graphs[2]:
        fig = px.bar_polar(df, r='salary_in_usd',theta=col,title=f'')    
    st.plotly_chart(fig, use_container_width=True)
if graph == graphs[3]:    
    fig = px.sunburst(df, path=cats, values='salary_in_usd', title=f'Salary distribution of {col}')
if graph == graphs[4]:
    fig = px.treemap(df, path=cats, values='salary_in_usd', title=f'Salary distribution of {col}')
st.plotly_chart(fig, use_container_width=True)    


