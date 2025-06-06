import streamlit as st
import pandas as pd
import os
import json
from streamlit_elements import elements, mui, dashboard, sync

DATA_FILE = "data/board.csv"
COLUMNS_FILE = "data/columns.json"
DEFAULT_COLUMNS = [
    "new project/feature",
    "being built",
    "in testing",
    "deployed",
]

if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.isfile(DATA_FILE):
    df = pd.DataFrame(columns=['Feature', 'Status', 'Votes', 'Comments'])
    df.to_csv(DATA_FILE, index=False)

if not os.path.isfile(COLUMNS_FILE):
    with open(COLUMNS_FILE, "w") as f:
        json.dump(DEFAULT_COLUMNS, f)

df = pd.read_csv(DATA_FILE)
with open(COLUMNS_FILE) as f:
    column_list = json.load(f)

st.set_page_config(layout="wide")
st.title("Trello-like Project Management")

columns_input = st.sidebar.text_input("Columns (comma separated)", ",".join(column_list))
if st.sidebar.button("Update Columns"):
    column_list = [c.strip() for c in columns_input.split(",") if c.strip()]
    if column_list:
        with open(COLUMNS_FILE, "w") as f:
            json.dump(column_list, f)
        df.loc[~df["Status"].isin(column_list), "Status"] = column_list[0]
        df.to_csv(DATA_FILE, index=False)

st.sidebar.header("Add New Feature")
new_feature = st.sidebar.text_input("Feature Name")
if st.sidebar.button("Add Feature") and new_feature:
    default_status = column_list[0] if column_list else ""
    df = pd.concat([
        df,
        pd.DataFrame(
            {
                'Feature': [new_feature],
                'Status': [default_status],
                'Votes': [0],
                'Comments': [""],
            }
        ),
    ])
    df.to_csv(DATA_FILE, index=False)

with elements("dashboard"):
    col_width = max(1, 12 // len(column_list)) if column_list else 12
    layout = [
        {"i": col, "x": idx * col_width, "y": 0, "w": col_width, "h": 10}
        for idx, col in enumerate(column_list)
    ]
    with dashboard.Grid(layout=layout, draggableHandle=".draggable"):
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
        sync()
