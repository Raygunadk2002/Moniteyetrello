
import streamlit as st
import pandas as pd
import os

DATA_FILE = "data/board.csv"

if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.isfile(DATA_FILE):
    df = pd.DataFrame(columns=['Feature', 'Status', 'Votes', 'Comments'])
    df.to_csv(DATA_FILE, index=False)

df = pd.read_csv(DATA_FILE)

st.title("Trello-like Project Management")

# Column configuration
columns = st.sidebar.text_input("Set columns (comma separated)", "new project/feature,being built,in testing,deployed")
column_list = [col.strip() for col in columns.split(",")]

# Add new feature
st.sidebar.header("Add New Feature")
new_feature = st.sidebar.text_input("Feature Name")
if st.sidebar.button("Add Feature") and new_feature:
    df = df.append({'Feature': new_feature, 'Status': column_list[0], 'Votes': 0, 'Comments': ""}, ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# Display columns
col_objs = st.columns(len(column_list))

for idx, col_name in enumerate(column_list):
    with col_objs[idx]:
        st.subheader(col_name)
        col_df = df[df['Status'] == col_name]
        for i, row in col_df.iterrows():
            st.write(f"### {row['Feature']}")
            if st.button(f"Vote ({row['Votes']})", key=f"vote_{i}"):
                df.at[i, 'Votes'] += 1
                df.to_csv(DATA_FILE, index=False)
                st.experimental_rerun()

            comment = st.text_input("Comment", key=f"comment_{i}")
            if st.button("Add Comment", key=f"add_comment_{i}") and comment:
                df.at[i, 'Comments'] += f"\n{comment}"
                df.to_csv(DATA_FILE, index=False)
                st.experimental_rerun()
            comments = row['Comments'] if pd.notna(row['Comments']) else ""
            st.write("Comments:", comments.replace("\n", "\n- "))

        # Move features between columns
        move_feature = st.selectbox(f"Move Feature from {col_name}", ["-"] + list(col_df['Feature']), key=f"move_{idx}")
        if move_feature != "-":
            target_col = st.selectbox("Target Column", [col for col in column_list if col != col_name], key=f"target_{idx}")
            if st.button("Move", key=f"move_btn_{idx}"):
                df.loc[df['Feature'] == move_feature, 'Status'] = target_col
                df.to_csv(DATA_FILE, index=False)
                st.experimental_rerun()
