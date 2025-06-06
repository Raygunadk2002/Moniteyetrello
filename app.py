
import streamlit as st
import pandas as pd
import os
from streamlit_elements import elements, mui, dashboard, sync

DATA_FILE = "data/board.csv"

if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.isfile(DATA_FILE):
    df = pd.DataFrame(columns=['Feature', 'Status', 'Votes', 'Comments'])
    df.to_csv(DATA_FILE, index=False)

df = pd.read_csv(DATA_FILE)

st.set_page_config(layout="wide")
st.title("Trello-like Project Management")

columns = st.sidebar.text_input("Columns", "new project/feature,being built,in testing,deployed")
column_list = [col.strip() for col in columns.split(",")]

st.sidebar.header("Add New Feature")
new_feature = st.sidebar.text_input("Feature Name")
if st.sidebar.button("Add Feature") and new_feature:
    df = pd.concat([df, pd.DataFrame({'Feature': [new_feature], 'Status': [column_list[0]], 'Votes': [0], 'Comments': [""]})])
    df.to_csv(DATA_FILE, index=False)

with elements("dashboard"):
    with dashboard.Grid(layout=[{"i": col, "x": idx, "y": 0, "w": 1, "h": 10} for idx, col in enumerate(column_list)], draggableHandle=".draggable"):
        for col in column_list:
            with mui.Paper(key=col, elevation=3, style={"padding": "1rem", "overflowY": "auto"}):
                mui.Typography(col, variant="h6", className="draggable")
                col_features = df[df['Status'] == col]
                for idx, row in col_features.iterrows():
                    with mui.Card(key=f"card_{idx}", style={"margin": "0.5rem"}):
                        mui.CardContent(
                            mui.Typography(row['Feature'], variant="body2"),
                            mui.Button(f"Votes: {row['Votes']}", variant="outlined", size="small")
                        )
