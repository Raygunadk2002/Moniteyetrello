import streamlit as st
import pandas as pd
import os
import json
from streamlit_sortables import sort_items

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
    df = pd.DataFrame(columns=["Feature", "Status", "Votes", "Comments"])
    df.to_csv(DATA_FILE, index=False)

if not os.path.isfile(COLUMNS_FILE):
    with open(COLUMNS_FILE, "w") as f:
        json.dump(DEFAULT_COLUMNS, f)

df = pd.read_csv(DATA_FILE)
with open(COLUMNS_FILE) as f:
    column_list = json.load(f)

if "df" not in st.session_state:
    st.session_state.df = df

if "columns" not in st.session_state:
    st.session_state.columns = column_list

df = st.session_state.df
column_list = st.session_state.columns

st.set_page_config(layout="wide")
st.title("Trello-like Project Management")

columns_input = st.sidebar.text_input(
    "Columns (comma separated)", ",".join(column_list)
)
if st.sidebar.button("Update Columns"):
    column_list = [c.strip() for c in columns_input.split(",") if c.strip()]
    if column_list:
        st.session_state.columns = column_list
        with open(COLUMNS_FILE, "w") as f:
            json.dump(column_list, f)
        df.loc[~df["Status"].isin(column_list), "Status"] = column_list[0]
        st.session_state.df = df
        df.to_csv(DATA_FILE, index=False)

st.sidebar.header("Add New Feature")
new_feature = st.sidebar.text_input("Feature Name")
if st.sidebar.button("Add Feature") and new_feature:
    default_status = column_list[0] if column_list else ""
    df = pd.concat(
        [
            df,
            pd.DataFrame(
                {
                    "Feature": [new_feature],
                    "Status": [default_status],
                    "Votes": [0],
                    "Comments": [""],
                }
            ),
        ]
    )
    st.session_state.df = df
    df.to_csv(DATA_FILE, index=False)

edited_columns = []
for idx, col in enumerate(column_list):
    new_title = st.text_input(f"Column {idx+1}", col, key=f"col_name_{idx}")
    edited_columns.append(new_title)

if edited_columns != column_list:
    column_list = edited_columns
    st.session_state.columns = column_list
    with open(COLUMNS_FILE, "w") as f:
        json.dump(column_list, f)
    df.loc[~df["Status"].isin(column_list), "Status"] = column_list[0]
    st.session_state.df = df
    df.to_csv(DATA_FILE, index=False)

# Prepare board data for streamlit-sortables
board = {c: df[df["Status"] == c]["Feature"].tolist() for c in column_list}

containers = [{"id": col, "children": items} for col, items in board.items()]
sorted_containers = sort_items(containers, direction="horizontal", multi_containers=True)
new_board = {c["id"]: c.get("children", []) for c in sorted_containers}

for col in column_list:
    features = new_board.get(col, [])
    df.loc[df["Feature"].isin(features), "Status"] = col

st.session_state.df = df
df.to_csv(DATA_FILE, index=False)

