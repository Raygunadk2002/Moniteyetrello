
import streamlit as st
import pandas as pd
import os
from streamlit_sortables import sort_items

DATA_FILE = "data/board.csv"

# Initialize data
if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.isfile(DATA_FILE):
    df = pd.DataFrame(columns=['Feature', 'Status', 'Votes', 'Comments'])
    df.to_csv(DATA_FILE, index=False)

df = pd.read_csv(DATA_FILE)

st.title("Trello-like Project Management")

# Sidebar settings
columns = st.sidebar.text_input(
    "Set columns (comma separated)", 
    "new project/feature,being built,in testing,deployed"
)
column_list = [col.strip() for col in columns.split(",")]

# Add new feature
st.sidebar.header("Add New Feature")
new_feature = st.sidebar.text_input("Feature Name")
if st.sidebar.button("Add Feature") and new_feature:
    new_row = pd.DataFrame({
        'Feature': [new_feature],
        'Status': [column_list[0]],
        'Votes': [0],
        'Comments': [""]
    })
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# Prepare drag-and-drop interface
sorted_features = {}
for col in column_list:
    col_features = df[df['Status'] == col]['Feature'].tolist()
    sorted_features[col] = sort_items(col_features, header=col, direction='vertical')

# Update dataframe after sorting
for col, features in sorted_features.items():
    for feature in features:
        df.loc[df['Feature'] == feature, 'Status'] = col
df.to_csv(DATA_FILE, index=False)

# Feature details (votes/comments)
for col in column_list:
    st.subheader(col)
    col_features = df[df['Status'] == col]
    for idx, row in col_features.iterrows():
        with st.expander(row['Feature']):
            if st.button(f"Vote ({row['Votes']})", key=f"vote_{idx}"):
                df.at[idx, 'Votes'] += 1
                df.to_csv(DATA_FILE, index=False)
                st.experimental_rerun()
            new_comment = st.text_input("New comment", key=f"comment_{idx}")
            if st.button("Add Comment", key=f"add_comment_{idx}") and new_comment:
                df.at[idx, 'Comments'] += f"\n{new_comment}"
                df.to_csv(DATA_FILE, index=False)
                st.experimental_rerun()
            st.write("Comments:", (row['Comments'] if pd.notna(row['Comments']) else "").replace("\n", "\n- "))
